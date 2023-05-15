from _init import *

from commons import file_util, string_util, container_util

from models.module.josa_extractor import JosaExtractor

class KeywordExtractor :
    '''
        Constructor
        1. text : 들어온 문장
        2. keyword_set : keyword 사전
        3. eojeol_list : 어절 리스트
        4. keyword_label_list : 어절에 keyword를 포함 여부 저장
        5. josa_extract : 조사 추출하는 객체
    '''
    def __init__(self) :
        self.text = ""
        self.keyword_set = set()
        self.eojeol_list = []
        self.keyword_label_list = []
        self.josa_extract = JosaExtractor()

    '''
        Methods
        1. set
        2. load_folder
        3. load_file
        4. get_feature_label_datas
        5. write_keyword_set
        6. _print
    '''

    '''
        1. set
        text 설정 및 keyword_label_list 초기화
    '''
    def set(self, text, in_dir: str, encoding="UTF-8") :
        self.load_folder(in_dir, encoding)
        self.text = text

        eojeols = text.split()

        eojeols = string_util.trim(eojeols, True)
        eojeol_len = len(eojeols)

        for i in range(eojeol_len) :
            eojeol = eojeols[i]

            self.eojeol_list.append(eojeol)
            self.keyword_label_list.append(0)

            self.josa_extract.set_text(eojeol)
            self.josa_extract.extract_josa()
            self.josa_extract.add_keyword_set(self.keyword_set)

            # 어절을 음절 단위로 쪼갠 후 keyword 목록에 있는지 확인하고 있다면 1로 labeling
            for keyword in sorted(list(self.keyword_set), reverse=True) :
                if eojeol.startswith(keyword) :
                    self.keyword_label_list[i] = 1

    '''
        2. load_folder
        폴더 내의 keyword_set을 전부 불러오는 기능
    '''
    def load_folder(self, in_dir: str, encoding: str) :
        file_paths = file_util.get_file_paths(in_dir, True)

        for file_path in file_paths :
            self.load_file(file_path, encoding)

    '''
        3. load_file
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
        4. get_feature_label_datas

    '''
    def get_feature_label_datas(self, window_size=3, is_train=False) :
        result = []
        features, labels = [], []

        input_list = self.eojeol_list
        label_list = self.keyword_label_list
        delim = " "

        input_len = len(input_list)
        for i in range(input_len) :
            feature = container_util.get_window(input_list, i, window_size, delim)
            label = label_list[i]

            if is_train :
                result.append([features, label])
            else :
                features.append(feature)
                labels.append(label)

        if is_train :
            return result
        else :
            return [features, labels]

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