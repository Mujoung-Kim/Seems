from _init import *

import torch
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa

from transformers import TFBertForSequenceClassification

class Trainer:
    '''
        Constructor
        1. model_name : 
        2. device : 
        3. our_model : 
    '''
    def __init__(self, model_name='klue/bert-base') :
        self.model_name = model_name
        self.device = ""

        self.our_model = None

        self._set()
    '''
        Methods
        1. _set
        2. available_gpu
        3. train
        4. eval
        5. get_model
        6. performance_measure
    '''
    def _set(self) :
        self.available_gpu()

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
    def train(self, data_xs, data_ys, val_xs, val_ys, out_model_path: str, epochs: int, batch_size: int, _learning_rate: float, patience: int, max_seq_len: int, dropout_rate=0.3, num_labels=2) :
        pretrained_model = TFBertForSequenceClassification.from_pretrained(
            self.model_name,					# model_name
            num_labels=num_labels,				# 분류 갯수
            from_pt=True						# model convert & load 여부
        )

        # input data shape define
        token_inputs = tf.keras.layers.Input((max_seq_len,), dtype="int64", name='input_word_ids')
        mask_inputs = tf.keras.layers.Input((max_seq_len), dtype="int64", name='input_masks')
        segment_inputs = tf.keras.layers.Input((max_seq_len,), dtype="int64", name='input_segment')
        bert_outputs = pretrained_model([token_inputs, mask_inputs, segment_inputs])

        # hidden_layer
        dropout = tf.keras.layers.Dropout(dropout_rate)(bert_outputs[0])
        layer = tf.keras.layers.Dense(128, activation="relu")(dropout)
        dropout = tf.keras.layers.Dropout(dropout_rate)(layer)
        layer = tf.keras.layers.Dense(64, activation="relu")(dropout)
        layer = tf.keras.layers.Dense(2, activation='softmax', kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.02))(layer)

        # our model define
        self.our_model = tf.keras.Model([token_inputs, mask_inputs, segment_inputs], layer)

        # optimzer define
        _optimizer = tfa.optimizers.RectifiedAdam(learning_rate=_learning_rate,
                                                 total_steps=len(data_xs) * epochs,
                                                 warmup_proportion=0.1, 
                                                 min_lr=1e-5, 
                                                 epsilon=1e-8,
                                                 clipnorm=1.0)

        # loss define
        _loss = tf.keras.losses.SparseCategoricalCrossentropy()

        # model compile
        self.our_model.compile(optimizer=_optimizer, loss=_loss, metrics = ['accuracy'])

        # best model 기록
        best_acc, counter, best_loss = 0, 0, float("inf")

        # 데이터를 넘겨줄 때, 이미 셔플 여부 결정
        for i in range(epochs) :
            print(f"{'=' * 40} Epoch {i} / {epochs} {'=' * 40}")
            fit_out = self.our_model.fit(data_xs, data_ys, epochs=1, batch_size=batch_size, shuffle=False)

            # performance measure
            acc = _performance_measure(self.our_model, val_xs, val_ys)
            print(f"val_accuracy : {acc}\t\tbest_accuracy : {best_acc}")

            # best model save
            if best_acc <= acc :
                best_acc = acc
                self.our_model.save(out_model_path)

            # early stopping
            if round(fit_out.history["loss"][0], 4) < best_loss :
                best_loss = round(fit_out.history["loss"][0], 4)
                counter = 0
            else :
                counter += 1

                if counter >= patience :
                    print("Early stopping")
                    break
            
            # weight load
            self.our_model = tf.keras.models.load_model(out_model_path, custom_objects={"TFBertForSequenceClassification" : TFBertForSequenceClassification})

    # 삭제 예정
    def eval(self, model, data_xs, data_ys, batch_size: int, _learning_rate: float) :
        _optimizer = tfa.optimizers.RectifiedAdam(
                                        learning_rate=_learning_rate,
                                        total_steps=len(data_xs),
                                        warmup_proportion=0.1,
                                        min_lr=1e-5,
                                        epsilon=1e-8,
                                        clipnorm=1.0)
        
        # loss define
        _loss = tf.keras.losses.SparseCategoricalCrossentropy()

        # model compile
        model.compile(optimizer=_optimizer, loss=_loss, metrics=['accuracy'])

        # 모델 검증
        model.fit(data_xs, data_ys, epochs=1, batch_size=batch_size, shuffle=False)

    # 모델 가져오기
    def get_model(self) :
        return self.our_model

    # 모델의 정확도 계산
    def performance_measure(self, data_xs, data_ys) :
        print(_performance_measure(self.our_model, data_xs, data_ys))

# 정확도 계산 메소드
def _performance_measure(model, data_xs, data_ys) :
    data_ys_predict = np.argmax(model(data_xs), axis = 1)
    data_len = len(data_ys)

    correct_cnt = 0

    for i in range(data_len):
        label = data_ys[i]
        predict = data_ys_predict[i]

        if label == predict:
            correct_cnt += 1
    
    return round(correct_cnt / data_len, 4)
