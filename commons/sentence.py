from _init import *

import os
from commons import string_util, container_util

class Sentence:
    def __init__(self):
        self.text = ''
        self.eojeol_list = []
        self.eojeol_label_list = []

        self.emjeol_list = []
        self.emjeol_label_list = []

    def _clear(self):
        self.text = ''
        self.eojeol_list.clear()
        self.eojeol_label_list.clear()

        self.emjeol_list.clear()
        self.emjeol_label_list.clear()

    def set(self, text: str, do_clear=True):
        if do_clear:
            self._clear()
            self.text = text
        else:
            self.text += text

        eojeols = text.split()

        # eojeol_strs : [' A B', 'CDE', '', ' DDD ']
        #   rm_empty_flag is False : ['A B', 'CDE', '', 'DDD']
        #   rm_empty_flag is True : ['A B', 'CDE', 'DDD']
        eojeols = string_util.trim(eojeols, True)
        eojeol_len = len(eojeols)

        for i in range(eojeol_len):
            eojeol = eojeols[i]

            self.eojeol_list.append(eojeol)
            self.eojeol_label_list.append(0)

            self.emjeol_list.extend([emjeol for emjeol in eojeol])

            emjeol_len = len(eojeol)
            for j in range(emjeol_len):
                if j == emjeol_len-1:
                    self.emjeol_label_list.append(1)
                else:
                    self.emjeol_label_list.append(0)

        self.eojeol_label_list[-1] = 1

    def get_feature_label_datas(self, window_size=3, is_train=False, is_emjeol=False):
        result = []
        features, labels = [], []

        if is_emjeol:
            input_list = self.emjeol_list
            label_list = self.emjeol_label_list
            delim = ''
        else:
            input_list = self.eojeol_list
            label_list = self.eojeol_label_list
            delim = ' '

        input_len = len(input_list)
        for i in range(input_len):
            feature = container_util.get_window(input_list, i, window_size, delim)
            label = label_list[i]
            
            if is_train:
                result.append([feature, label])
            else:
                features.append(feature)
                labels.append(label)
        
        if is_train:
            return result
        else:
            return [features, labels]


    def _print(self):
        print(f"sentence : {self.text}")

        eojeol_len = len(self.eojeol_list)
        print(f"eojeol_len : {eojeol_len}\n")

        print(f"eojeol_list : {self.eojeol_list}")
        print(f"eojeol_label_list : {self.eojeol_label_list}\n")

        print(f"all emjeol_list : {self.emjeol_list}")
        print(f"all emjeol_label_list : {self.emjeol_label_list}\n")



# def _print(train_datas):
#     for i in range(len(train_datas)):
#         train_data = train_datas[i]
#         print(f'[{i}] freature : {train_data[0]}, label : {train_data[1]}')
#     print()

# if __name__ == "__main__":
#     text = '가라루파는 터키의 온천에 사는 민물고기이다.'
#     sentence = Sentence(text)
#     sentence._print()

#     train_datas = sentence.convert_train_data()
#     _print(train_datas)

#     train_datas = sentence.convert_train_data(is_emjeol=True)
#     _print(train_datas)
