from _init import *

import os
from commons import string_util

class Sentence:
    def __init__(self, text: str):
        self.text = text
        self.eojeol_list = []
        self.eojeol_label_list = []
        
        self.emjeol_list = []
        self.emjeol_label_list = []
        
        self._set()
    
    def _set(self, label_default=0):
        eojeols = self.text.split()
        
        # eojeol_strs : [' A B', 'CDE', '', ' DDD ']
        #   rm_empty_flag is False : ['A B', 'CDE', '', 'DDD']
        #   rm_empty_flag is True : ['A B', 'CDE', 'DDD']
        eojeols = string_util.trim(eojeols, True)
        
        for i in range(len(eojeols)):
            eojeol = eojeols[i]
            
            self.eojeol_list.append(eojeol)
            self.eojeol_label_list.append(label_default)
            
            self.emjeol_list.extend([emjeol for emjeol in eojeol])
            self.emjeol_label_list.extend([label_default for i in range(len(eojeol))])

    def _print(self):
        print(f"sentence : {self.text}")
        
        eojeol_len = len(self.eojeol_list)
        print(f"eojeol_len : {eojeol_len}\n")
        
        print(f"eojeol_list : {self.eojeol_list}")
        print(f"eojeol_label_list : {self.eojeol_label_list}\n")
        
        print(f"all emjeol_list : {self.emjeol_list}")
        print(f"all emjeol_label_list : {self.emjeol_label_list}")

# if __name__ == "__main__":
#     text = '안녕하세요 저는 이성희입니다'
#     sentence = Sentence(text)
#     sentence._print()