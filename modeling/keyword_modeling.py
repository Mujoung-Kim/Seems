from _init import *

from commons import file_util, string_util

import time
import torch
import numpy as np
import pandas as pd
import tensorflow as tf

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, BertConfig, AdamW
from transformers import get_linear_schedule_with_warmup

# tensorflow 2.10.0
from keras.utils.data_utils import pad_sequences
# tensorflow 최신 버전의 경우
# from keras_preprocessing.sequence import pad_sequences

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class BertModel() :
    '''
        Constructor
        1. model_name :
        2. device : 
        3. delim :
        4. raw_df : 
        5. train_df :
        6. test_df : 
        7. train_batch_size : 
        8. test_batch_size :
        9. max_seq_len : 
        10. learning_rate : 
        11. dropout_rate : 
        12. patience : 
        13. epochs : 
    '''
    def __init__(self, model_name, in_dir) : 
        self.MODEL_NAME = model_name
        self.device = ""
        self.delim = "\t"
        self.raw_df = ""
        self.train_df = ""
        self.test_df = ""
        self.sentences = ""
        self.labels = ""

        self.input_ids = ""

        # 여기는 밖으로 뺴도 될꺼 같음
        self.train_batch_size = 0
        self.test_batch_size = 0
        self.max_seq_len = 0
        self.learning_rate = 0
        self.dropout_rate = 0
        self.patience = 0
        self.epochs = 0

        self._set(in_dir)

    '''
        Methods
        1. _set
        2. check_gpu
        3. load
        4. divide_dataset
        5. _print
    '''
    def _set(self, in_dir: str) :
        self.check_gpu()
        self.load(in_dir)

    # gpu 사용 여부 체크
    def check_gpu(self) :
        device_name = tf.test.gpu_device_name()

        if device_name == "/device:GPU:0" :
            print(f"Found GPU at : {device_name}")
        else :
            print("GPU device not found")

        if torch.cuda.is_available() :
            self.device = torch.device("cuda")

            print(f"There are {torch.cuda.device_count()} GPU(s) available.")
            print(f"We will use the GPU : {torch.cuda.get_device_name(0)}")
        else :
            self.device = torch.device("cpu")

            print("No GPU available, using the GPU instead.")

    # dataframe 생성
    def load(self, in_file_path: str) :
        file_paths = file_util.get_file_paths(in_file_path, True)

        for file_path in file_paths :
            self.raw_df = pd.read_csv(file_path, sep=self.delim, names=["train", "label"])

    # train, test 셋 설정
    def divide_dataset(self, data_rate: int) :
        self.train_df = self.raw_df[:data_rate]
        self.test_df = self.raw_df[data_rate:]

    # 결과 출력
    def _print(self) :
        print(f"dataframe_shape : {self.raw_df.shape}")
        print(f"dataframe_head : {self.raw_df.head()}\n")

        print("여기서부터 문맥에 맞게 DATA_RATE 값 변경")
        print(f"train - test : {int(self.raw_df.shape[0] * 0.9)}\n")
        
        if type(self.train_df) == pd.core.frame.DataFrame and type(self.test_df) == pd.core.frame.DataFrame : 
            print("==================== train_df ====================")
            print(f"{self.train_df.tail()}")
            print("==================== test_df ====================")
            print(f"{self.test_df.head()}\n")

# main
if __name__ == "__main__" :
    work_dir = "../../"
    in_dir = work_dir + "resources/keyword_extract/"

    bert = BertModel("klue/bert-base", in_dir)
    bert._print()
    bert.divide_dataset(11277)
    bert._print()