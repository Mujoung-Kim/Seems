from _init import *

import json
import torch
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa

from transformers import TFBertForSequenceClassification
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint

class DefaultModel:
    '''
        Constructor
        1. model_name : 사용할 Bert 모델 이름
        2. max_seq_len : 입력할 데이터의 길이
        3. device : cpu or gpu
        4. our_model : 학습된 모델
    '''
    def __init__(self, max_seq_len: int, dropout_rate=0.3, num_labels=2, model_name='klue/bert-base') :
        self.model_name = model_name
        self.max_seq_len = max_seq_len
        self.device = ""
        self.our_model = self._init_model(dropout_rate, num_labels)

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
        layer = tf.keras.layers.Dense(128, activation="relu")(dropout)
        dropout = tf.keras.layers.Dropout(dropout_rate)(layer)
        layer = tf.keras.layers.Dense(64, activation="relu")(dropout)
        layer = tf.keras.layers.Dense(num_labels, activation="softmax", kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.02))(layer)

        # our model define
        model = tf.keras.Model([token_inputs, mask_inputs, segment_inputs], layer)
        self._check_env()

        return model

    # GPU 사용 여부
    def available_gpu(self) :
        device_name = tf.test.gpu_device_name()

        if device_name == "/device:GPU:0" :
            print(f"Found GPU at : {device_name}")
            
        if torch.cuda.is_available() :
            self.device = torch.device("cuda")

            print(f"There are {torch.cuda.device_count()} GPU(s) available.")
            print(f"We will use the GPU : {torch.cuda.get_device_name(0)}")
        else :
            self.device = torch.device("cpu")

            print("No GPU available, using the CPU instead.")

    '''
        klue/bert-base train function
        parameter : 학습용 데이터(data_xs, data_ys), 검증용 데이터(val_xs, val_ys), 모델 저장 경로(out_model_path), 학습 최대 사이클(epochs), 한 번에 학습시킬 데이터의 수(batch_size), 학습 수치(learning_rate), 성능 개선이 이뤄지지 않을 때 최대 시행 횟수(patience), 입력 데이터의 최대 길이(max_seq_len), 라벨의 갯수(num_labels)
    '''
    def train(self, data_xs, data_ys, out_best_model_path: str, epochs: int, batch_size: int, _learning_rate: float, patience: int) :
        # optimzer define
        _optimizer = tfa.optimizers.RectifiedAdam(learning_rate=_learning_rate,
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
            monitor="loss",
            mode="min",
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

        # best model 기록
        # best_acc, counter, best_loss = 0, 0, float("inf")

        # 데이터를 넘겨줄 때, 이미 셔플 여부 결정
        # for i in range(epochs) :
        #     print(f"{'=' * 40} Epoch {i + 1} / {epochs} {'=' * 40}")
        #     fit_out = self.our_model.fit(data_xs, data_ys, epochs=1, batch_size=batch_size, shuffle=False)

            # performance measure
            # acc = _performance_measure(self.our_model, val_xs, val_ys)

            # best model save
            # if best_acc < acc :
            #     best_acc = acc
            #     self.our_model.save(out_best_model_path)

            #     # weight load
            #     self.our_model = tf.keras.models.load_model(out_best_model_path, custom_objects={"TFBertForSequenceClassification" : TFBertForSequenceClassification})
            # else :
            #     self.our_model.save(out_model_path)

            #     # weight load
                # self.our_model = tf.keras.models.load_model(out_model_path, custom_objects={"TFBertForSequenceClassification" : TFBertForSequenceClassification})
            # print(f"val_accuracy : {acc}\t\tbest_accuracy : {best_acc}")

            # early stopping
            # if round(fit_out.history["loss"][0], 4) < best_loss :
            #     best_loss = round(fit_out.history["loss"][0], 4)
            #     counter = 0
            # else :
            #     counter += 1

            #     if counter >= patience :
            #         print("Early stopping")
            #         break

        # training config save
        self.save_parameter(out_best_model_path, batch_size, epochs)

        # best model load
        self.our_model = self.load_model(out_best_model_path)

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
        return tf.keras.models.load_model(model_path, custom_objects={"TFBertForSequenceClassification":TFBertForSequenceClassification})
    
    # model accuracy calculator
    def performance_measure(self, data_xs, data_ys) :
        predict_val = self.our_model.predict(data_xs)
        predict_label = np.argmax(predict_val, axis=1)
        label_len = len(data_ys)
        correct_cnt = 0

        for i in range(label_len) :
            label = data_ys[i]
            predict = predict_label[i]

            if label == predict :
                correct_cnt += 1

        print(round(correct_cnt / label_len, 4))

# 정확도 계산 메소드 -> 이건 돌려봐야 암
def _performance_measure(model, data_xs, data_ys) :
    predicts = []
    
    for data_x in data_xs :
        predict = model(data_x)
        predicts.append(predict)

    data_ys_predict = np.argmax(predicts, axis = 1)
    data_len = len(data_ys)
    correct_cnt = 0

    for i in range(data_len):
        label = data_ys[i]
        predict = data_ys_predict[i]

        if label == predict:
            correct_cnt += 1
    
    return round(correct_cnt / data_len, 4)
