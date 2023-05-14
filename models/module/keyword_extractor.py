from _init import *

from commons import file_util, string_util
from commons.sentence import Sentence

from josa_extractor import JosaExtractor

class KeywordExtractor() :
    '''
        Constructor
        1. text : 들어온 문장
        2. keyword_set : keyword 사전
        3. keyword_label_list : 어절에 keyword를 포함 여부 저장
    '''
    def __init__(self, text:str, in_dir: str, encoding="UTF-8") :
        self.text = text
        self.keyword_set = set()
        self.keyword_label_list = []

        self._set(in_dir, encoding)

    '''
        Methods
        1. _set
        2. load
        3. add_keyword_set
        4. _print
    '''

    '''
        1. _set
        클래스의 초기값을 설정하는 기능
        keywordExtractor의 keyword_set, keyword_label_list의 초기 값을 설정
    '''
    def _set(self, in_dir: str, encoding: str, label_default=0) :
        self.load(in_dir, encoding)

        # 조사 앞에 단어가 있으면 키워드로 추가
        JosaExtractor(self.text, self.keyword_set)
        self.add_keyword_set(in_dir, encoding)

        # keyword_label_list 초기화
        sentence = Sentence(self.text)    
        eojeol_len = len(sentence.eojeol_list)

        for _ in range(eojeol_len) :
            self.keyword_label_list.append(label_default)

    '''
        2. load
        keyword목록을 불러오는 기능
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

        in_file.close()

    '''
        3. add_keyword_set
        조사 앞에 단어가 있으면 해당 단어들도 키워드로 추가하는 기능
    '''
    def add_keyword_set(self, out_file_path: str, encoding: str) :
        file_paths = file_util.get_file_paths(out_file_path, True)

        for file_path in file_paths :
            # 파일이 존재하면 제거하고 다시 저장
            if file_util.exists(file_path) :
                os.remove(file_path)

            out_file = file_util.open_file(file_path, encoding, "a")

            for keyword in sorted(list(self.keyword_set)) :
                out_file.write(f"{keyword}\n")

        out_file.close()

    '''
        4. _print
        세팅된 값을 확인하는 기능
    '''
    def _print(self) :
        print(f"sentence : {self.text}\n")
        
        print(f"keyword_len : {len(self.keyword_set)}")
        print(f"all keyword_set : {self.keyword_set}\n")
        
        print(f"keyword_label_list : {self.keyword_label_list}\n")