from _init import *

from commons import file_util, string_util
from commons.sentence import Sentence

class KeywordExtractor :
    '''
        Constructor
        1. text : 들어온 문장
        2. keyword_set : keyword 사전
        3. keyword_label_list : 어절에 keyword를 포함 여부 저장
    '''
    def __init__(self) :
        self.text = ""
        self.keyword_set = set()
        self.keyword_label_list = []

    '''
        Methods
        1. set_text
        2. _init_label_list
        3. load_folder
        4. load_file
        5. write_keyword_set
        6. _print
    '''

    '''
        1. set_text
        text 설정 및 keyword_label_list 초기화
    '''
    def set_text(self, text) :
        self.text = text
        self._init_label_list()

    '''
        2. _init_label_list
        keyword_label_list 초기화 기능
        들어온 문장의 길이 만큼 label_list 값을 0으로 초기화
    '''
    def _init_label_list(self, label_default=0) :
        sentence = Sentence(self.text)
        eojeol_len = len(sentence.eojeol_list)

        for _ in range(eojeol_len) :
            self.keyword_label_list.append(label_default)

    '''
        3. load_folder
        폴더 내의 keyword_set을 전부 불러오는 기능
    '''
    def load_folder(self, in_dir: str, encoding: str) :
        file_paths = file_util.get_file_paths(in_dir, True)

        for file_path in file_paths :
            self.load_file(file_path, encoding)

    '''
        4. load_file
        keyword_set이 저장된 파일을 불러오는 기능
    '''
    def load_file(self, in_file_path: str, encoding: str) :
        in_file = file_util.open_file(in_file_path, encoding, "r")

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

        in_file.close()

    '''
        5. write_keyword_set
        추가된 keyword_set 저장하는 기능
    '''
    def write_keyword_set(self, out_file_path: str, encoding: str) :
        out_file = file_util.open_file(out_file_path, encoding, "w")

        for keyword in sorted(list(self.keyword_set)) :
            out_file.write(f"{keyword}\n")

        out_file.close()

    '''
        6. _print
        세팅된 값을 확인하는 기능
    '''
    def _print(self) :
        print(f"text : {self.text}\n")

        print(f"keyword_len : {len(self.keyword_set)}")
        print(f"keyword_set : {self.keyword_set}\n")

        print(f"keyword_label : {self.keyword_label_list}\n")

# from josa_extractor import JosaExtractor

# main
# if __name__ == "__main__" :
#     root_path = "../../"
#     in_file_path = root_path + "data/input/keywords/keyword_data_test.txt"
#     encoding = "UTF-8"

#     text = "코로나는 중국에서 발병한 질병이다."

#     keyword = KeywordExtractor()
#     josa = JosaExtractor()

#     keyword.set_text(text)
#     josa.set_text(text)
#     josa.extract_josa()
#     keyword.load_file(in_file_path, encoding)
#     josa.add_keyword_set(keyword.keyword_set)
#     keyword.write_keyword_set(in_file_path, encoding)
#     keyword._print()