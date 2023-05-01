from _init import *

from commons import file_util, string_util, container_util
from commons.sentence import Sentence

class KeywordExtractor() :
    '''
        Constructor
        1. text : 들어온 문장
        2. keyword_set : keyword 사전
        3. keyword_label_list : eojeol에 keyword를 포함 여부 저장
    '''
    def __init__(self, text: str, in_dir: str, encoding="UTF-8") :
        self.text = text
        self.keyword_set = set()
        self.keyword_label_list = []

        self._set(in_dir, encoding)

    '''
        Methods
        1. _set 
        2. load
        3. _print 
    '''

    '''
    '''
    def _set(self, in_dir: str, encoding: str, label_default=0) :
        self.load(in_dir, encoding)

        sentence = Sentence(self.text)

        for eojeol in sentence.eojeol_list :
            emjeol_len = len(eojeol)

            for i in range(emjeol_len) :
                if eojeol[:i] in self.keyword_set :
                    self.keyword_label_list.append(label_default + 1)
                    label_default = 0
                    break

                if i == emjeol_len - 1 :
                    self.keyword_label_list.append(label_default)

    '''
    '''
    def load(self, in_file_path: str, encoding: str) :
        file_paths = file_util.get_file_paths(in_file_path, True)

        for file_path in file_paths :
            in_file = file_util.open_file(file_path, encoding, "r")

            while True :
                line = in_file.readline()

                if not line :
                    break

                line = file_util.preprocess(line)
                if string_util.is_empty(line, True) :
                    continue
                
                if len(line) == 1 or line.isdigit() :
                    continue

                self.keyword_set.add(line)

    '''
    '''
    def _print(self) :
        print(f"sentence : {self.text}\n")
        
        print(f"keyword_len : {len(self.keyword_set)}")

        print(f"all keyword_set : {self.keyword_set}\n")
        
        print(f"keyword_label_list : {self.keyword_label_list}\n")

# main
if __name__ == "__main__" :
    work_dir = "../../"
    in_dir = work_dir + "data/keyword_extract/"

    text = "가라루파는 터키의 온천에 사는 민물고기이다."

    keyword = KeywordExtractor(text, in_dir)
    keyword._print()