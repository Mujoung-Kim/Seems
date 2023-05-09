from _init import *

import torch
import tensorflow as tf
import tensorflow_addons as tfa

from transformers import TFBertForSequenceClassification

class Trainer:
    '''
        Constructor
        
    '''
    def __init__(self, model_name='klue/bert-base') :
        self.model_name = model_name
        self.device = ""

        self.our_model = None

        self._set()
    '''
        Methods
        1. train
        2. eval
        3. calculator_accuracy
        4. save_checkpoint
    '''
    def _set(self) :
        self.available_gpu()

    # ㅁ?ㄹ
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

    def train(self, data_xs, data_ys, val_xs, val_ys, epochs: int, batch_size: int, learning_rate: float, num_labels=2) :
        pretrained_model = TFBertForSequenceClassification.from_pretrained(
            self.model_name,					# model_name
            num_labels=num_labels,				# 분류 갯수
            from_pt=True						# model convert & load 여부
        )

        token_inputs = tf.keras.layers.Input((20,), dtype="int64", name='input_word_ids')
        mask_inputs = tf.keras.layers.Input((20), dtype="int64", name='input_masks')
        segment_inputs = tf.keras.layers.Input((20,), dtype="int64", name='input_segment')
        bert_outputs = pretrained_model([token_inputs, mask_inputs, segment_inputs])

        # hidden_layer
        dropout = tf.keras.layers.Dropout(0.5)(bert_outputs[0])
        layer = tf.keras.layers.Dense(128, activation="relu")(dropout)
        dropout = tf.keras.layers.Dropout(0.5)(layer)
        layer = tf.keras.layers.Dense(64, activation="relu")(dropout)
        layer = tf.keras.layers.Dense(2, activation='softmax', kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.02))(layer)

        # our model define
        self.our_model = tf.keras.Model([token_inputs, mask_inputs, segment_inputs], layer)

        # optimzer define
        optimizer_name = 'RAdam'
        _optimizer = tfa.optimizers.RectifiedAdam(learning_rate = 5e-5,
                                                 total_steps = 10000, 
                                                 warmup_proportion = 0.1, 
                                                 min_lr = 1e-5, 
                                                 epsilon = 1e-8,
                                                 clipnorm = 1.0)

        # loss define
        _loss = tf.keras.losses.SparseCategoricalCrossentropy()

        # model compile
        self.our_model.compile(optimizer=_optimizer, loss=_loss, metrics = ['accuracy'])

        max_acc = 0

        # 데이터를 넘겨줄 때, 이미 셔플 여부 결정
        for i in range(epochs):
            self.our_model.fit(data_xs, data_ys, epochs=1, batch_size=batch_size, shuffle=False)

            # performance measure
            acc = _performance_measure(self.our_model, val_xs, val_ys)

            if max_acc <= acc:
                self.our_model.save()


    
    def get_model(self):
        return self.out_model

    def performance_measure(self, data_xs, data_ys):
        _performance_measure(self.our_model, data_xs, data_ys)

def _performance_measure(model, data_xs, data_ys):
    data_ys_predict = model(data_xs)
    data_len = len(data_ys)

    correct_cnt = 0

    for i in range(data_len):
        label = data_ys[i]
        predict = data_ys_predict[i]

        if label == predict:
            correct_cnt += 1
    
    return correct_cnt / data_len





    