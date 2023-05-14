from _init import *

import random
import numpy as np

from commons import file_util
from transformers import BertTokenizer

class DataReformator:
    def __init__(self, max_len, bert_model_name='klue/bert-base'):
        self.tokenizer = BertTokenizer.from_pretrained(bert_model_name)
        self.max_len = max_len
        
        self.data_reformats = []
        self.delim = '\t'

    def load_folder(self, in_path: str, delim='\t', encoding='utf-8'):
        in_file_paths = file_util.get_file_paths(in_path, True)
        for in_file_path in in_file_paths:
            self.load_file(in_file_path, delim, encoding)
            

    def load_file(self, in_file_path, delim='\t', encoding='utf-8'):
        self.delim = delim
        in_file = file_util.open_file(in_file_path, encoding,'r')

        while 1:
            line = in_file.readline()
            if not line:
                break

            line = line.strip()
            if len(line) == 0:
                continue

            self.data_reformats.append(line)

        in_file.close()

    def div(self, train_rate: int, val_rate: int, test_rate: int, is_shuffle: bool):
        if is_shuffle:
            datas = []
            datas.extend(self.data_reformats)
            random.shuffle(datas)            
        else:
            datas = self.data_reformats
        
        text_list = []
        label_list = []
        for term in datas:
            temp = term.split(self.delim)

            if len(temp) != 2:
                continue

            text_list.append(temp[0])
            label_list.append(temp[1])
        
        text_datas = self._div(text_list, train_rate, val_rate, test_rate)
        label_datas = self._div(label_list, train_rate, val_rate, test_rate)

        [text_datas[0], label_datas[0]]
        [text_datas[1], label_datas[1]]
        [text_datas[2], label_datas[2]]

        return [[text_datas[0], label_datas[0]],
                [text_datas[1], label_datas[1]],
                [text_datas[2], label_datas[2]]]

    
    def _div(self, datas, train_rate: int, val_rate: int, test_rate: int):
        data_len = len(datas)

        train_size = int(data_len * (train_rate *0.1))
        train_data = datas[ : train_size]

        val_size = int(data_len * (val_rate * 0.1))
        val_data = datas[train_size : train_size+val_size]
        
        # test_rate 값은 굳이 사용하지 않아도 된다. (남은 항목을 다 가져오면 되므로)
        test_data = datas[train_size+val_size:]

        return [train_data, val_data, test_data]

    def reformat_datas(self, datas):
        encodeds, masks, segments, labels = [], [], [], []

        data_len = len(datas[0])
        for i in range(data_len):
            text = datas[0][i]
            label = int(datas[1][i])

            reformated = self.reformat_text(text, False)

            encodeds.append(reformated[0])
            masks.append(reformated[1])
            segments.append(reformated[2])
            labels.append(label)
        
        encodeds = np.array(encodeds)
        masks = np.array(masks)
        segments = np.array(segments)
        labels = np.array(labels)
        
        return [encodeds, masks, segments], labels

    def reformat_text(self, text, is_single=True):
         # token_ids
        encoded = self.tokenizer.encode(text, truncation=True, padding='max_length', max_length=self.max_len)
        # atteintion_mask
        cnt_zero = encoded.count(0)
        mask = [1] * (self.max_len - cnt_zero) + [0] * cnt_zero
        # token_type_ids (sentence_segmentation)
        segment = [0] * self.max_len
        
        if is_single:
            encoded = np.array(encoded)
            mask = np.array(mask)
            segment = np.array(segment)
        
        return [encoded, mask, segment]

    ## 우리가 입력으로 넣은 텍스트는 실제 버트 모델의 입력으로 사용되는 것이 아니라, 실제 버트 모델이 사용하는 입력의 형태로 변환해서 넘겨줘야 함
    ##  - 입력 텍스트 : 1###이건테스
    ##  - 변환된 입력 : [[2, 21, 7, 7, 7, 5370, 10814, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # token_ids
    #                    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],          # attention_mask
    #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]          # token_type_ids
    # 위 변환된 입력이 하나의 x이고, 대응되는 y는 '0' 또는 '1'

    # 실제로 우리가 넘겨주는 형식 -> text : label
    #   - Ex). 
    #           x : ###이건테스
    #           y : 0 

    # 하지만, 우리가 넘겨준 text('###이건테스')를 버트의 입력([token_ids, attention_mask, token_type_ids])으로 변환해야 함
    #   - Ex). [ [2, 21, 7, 7, 7, 5370, 10814, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]

    # 결국 버트에 들어가는 x, y 형식은 [token_ids, attention_mask, token_type_ids] : label 과 같다.
    #   - Ex). 
    #           x : [ [2, 21, 7, 7, 7, 5370, 10814, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]
    #           y : 0