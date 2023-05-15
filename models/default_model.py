from _init import *

import json
import torch
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa

from transformers import TFBertForSequenceClassification
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint

from commons.logger import *
from models.data_reformator import DataReformator

class DefaultModel:
    '''
        Constructor
        1. model_name : 사용할 Bert 모델 이름
        2. max_seq_len : 입력할 데이터의 길이
        3. device : cpu or gpu
        4. our_model : 학습된 모델
    '''
    def __init__(self, max_seq_len: int, dropout_rate=0.3, num_labels=2, model_name='klue/bert-base') :
        self.logger = get_logger(__name__)
        self.model_name = model_name
        self.max_seq_len = max_seq_len
        self.device = ""
        self._check_env()
        self.our_model = self._init_model(dropout_rate, num_labels)
        self.reformator = DataReformator(max_seq_len, model_name)
        
        self.train_xs, self.train_ys = [], []
        # self.val_xs, self.val_ys = [], []
        self.test_xs, self.test_ys = [], []

    '''
        Methods
        1. _check_env
        2. _init_model
        3. available_gpu
        4. train
        5. performance_measure
        6. load_model
    '''
    def _check_env(self) :
        self.available_gpu()
    
    # GPU 사용 여부
    def available_gpu(self) :
        device_name = tf.test.gpu_device_name()

        if device_name == "/device:GPU:0" :
            self.logger.info(f"Found GPU at : {device_name}")
            
        if torch.cuda.is_available() :
            self.device = torch.device("cuda")

            self.logger.info(f"There are {torch.cuda.device_count()} GPU(s) available.")
            self.logger.info(f"We will use the GPU : {torch.cuda.get_device_name(0)}")
        else :
            self.device = torch.device("cpu")

            self.logger.info("No GPU available, using the CPU instead.\n")

    # model initializer
    def _init_model(self, dropout_rate: float, num_labels: int) :
        pretrained_model = TFBertForSequenceClassification.from_pretrained(
            self.model_name,                # model_name
            num_labels=num_labels,          # 분류 갯수
            from_pt=True                    # model convert & load 여부
        )

        # input data shape define
        token_inputs = tf.keras.layers.Input((self.max_seq_len, ), dtype=tf.int32, name="input_word_ids")
        mask_inputs = tf.keras.layers.Input((self.max_seq_len), dtype=tf.int32, name="input_masks")
        segment_inputs = tf.keras.layers.Input((self.max_seq_len,), dtype=tf.int32, name="input_segment")
        bert_outputs = pretrained_model([token_inputs, mask_inputs, segment_inputs])

        # hidden_layer
        dropout = tf.keras.layers.Dropout(dropout_rate)(bert_outputs[0])
        layer = tf.keras.layers.Dense(512, activation="relu")(dropout)
        dropout = tf.keras.layers.Dropout(dropout_rate)(layer)
        layer = tf.keras.layers.Dense(256, activation="relu")(dropout)
        layer = tf.keras.layers.Dense(num_labels, activation="softmax", kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.02))(layer)

        # our model define
        model = tf.keras.Model([token_inputs, mask_inputs, segment_inputs], layer)
        self.logger.info(f'DefaultModel._init_model() success.\n')

        return model

    def load_train_data(self, train_file_path: str, delim: str, encoding: str, train_rate: int, test_rate: int, is_shuffle=False):
        self.reformator.load_file(train_file_path, delim, encoding)
        div_datas = self.reformator.div(train_rate, 0, test_rate, is_shuffle)
        
        self.train_xs, self.train_ys = self.reformator.reformat_datas(div_datas[0])
        # self.val_xs, self.val_ys = self.reformator.reformat_datas(div_datas[1])
        self.test_xs, self.test_ys = self.reformator.reformat_datas(div_datas[2])

    '''
        klue/bert-base train function
        parameter : 학습용 데이터(data_xs, data_ys), 검증용 데이터(val_xs, val_ys), 모델 저장 경로(out_model_path), 학습 최대 사이클(epochs), 한 번에 학습시킬 데이터의 수(batch_size), 학습 수치(learning_rate), 성능 개선이 이뤄지지 않을 때 최대 시행 횟수(patience), 입력 데이터의 최대 길이(max_seq_len), 라벨의 갯수(num_labels)
    '''
    def train(self, out_best_model_path: str, epochs: int, batch_size: int, learning_rate: float, patience: int,
              data_xs=None, data_ys=None) :
        
        if data_xs is None: data_xs = self.train_xs
        if data_ys is None: data_ys = self.train_ys
        
        # optimzer define
        _optimizer = tfa.optimizers.RectifiedAdam(learning_rate=learning_rate,
                                                 total_steps=10000 * epochs,
                                                 warmup_proportion=0.1, 
                                                 min_lr=1e-5, 
                                                 epsilon=1e-8,
                                                 clipnorm=1.0)

        # loss define
        _loss = tf.keras.losses.SparseCategoricalCrossentropy()

        # model compile
        self.our_model.compile(optimizer=_optimizer, loss=_loss, metrics = ['accuracy'])

        early_stopping = EarlyStopping(
            monitor="accuracy",
            mode="max",
            patience=patience)

        model_checkpoint = ModelCheckpoint(
            filepath=out_best_model_path,
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1
        )

        # model_training
        # 데이터를 넘겨줄 때, 이미 셔플 여부 결정
        self.our_model.fit(data_xs, data_ys, epochs=epochs, batch_size=batch_size, shuffle=False, validation_split=0.1, callbacks=[early_stopping, model_checkpoint])

        # training config save
        self.save_parameter(out_best_model_path, batch_size, epochs)
        
        # test data 성능 평가
        self.performance_measure()

    # hyperparameter variable save
    def save_parameter(self, out_param_path: str, batch_size: int, epochs: int) :
        trainning_config = {
            "batch_size" : batch_size,
            "max_len" : self.max_seq_len,
            "epochs" : epochs
        }

        with open(f"{out_param_path[:out_param_path.rfind('/')]}/training_config.json", "w") as fw :
            json.dump(trainning_config, fw)

    # model load function
    def load_model(self, model_path: str) :
        self.our_model = tf.keras.models.load_model(model_path, custom_objects={"TFBertForSequenceClassification":TFBertForSequenceClassification})
        self.logger.info(f'DefaultModel.load_model() complete.')

    def _predict(self, data_xs):
        temp = self.our_model.predict(data_xs)
        data_predicts = np.argmax(temp, axis=1)
        return data_predicts
    
    # model accuracy calculator
    def performance_measure(self, data_xs=None, data_ys=None) :
        if data_xs is None: data_xs = self.test_xs
        if data_ys is None: data_ys = self.test_ys
        
        data_predicts = self._predict(data_xs)
        data_len = len(data_ys)
        
        cnt_correct = 0
        cnt_y_true = data_ys.tolist().count(1)
        cnt_predict_true = data_predicts.tolist().count(1)

        for i in range(data_len) :
            data_y = data_ys[i] # gold label
            data_predict = data_predicts[i] # model predict

            if data_y == data_predict :
                cnt_correct += 1

        accuracy = round(cnt_correct / data_len, 4)
        
        print(f'data_len : {data_len}')
        print(f'cnt_y_true : {cnt_y_true}')
        print(f'cnt_predict_true : {cnt_predict_true}')
        print(f'cnt_correct : {cnt_correct}')
        print(f'accuracy : {accuracy}')

        # self.logger.info(f'DefaultModel.performance_measure() accuracy : {accuracy}\n')
