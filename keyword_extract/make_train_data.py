from _init import *

from commons import file_util, string_util, container_util

from keyword_extractor import KeywordExtractor

class MakeTrainData() :
    '''
        Constructor
    '''
    def __init__(self) :
        pass
    '''
        Methods
        1. make_folder
        2. _make_file
    '''

    '''
        1. make_folder
        train_dataset을 저장하는 디렉토리 생성하는 기능
    '''
    def make_folder(self, in_dir: str, in_keyword_dir: str, out_file_path: str, encoding: str, delim: str, window_size) :
        if file_util.exists(out_file_path) :
            os.remove(out_file_path)

        in_file_paths = file_util.get_file_paths(in_dir, True)

        for in_file_path in in_file_paths :
            self._make_file(in_file_path, in_keyword_dir, out_file_path, encoding, delim, window_size)

    '''
        2. _make_file
        train_dataset 생성하는 기능
        들어온 텍스트에서 키워드가 있으면 라벨링 후 학습 데이터를 생성
    '''
    def _make_file(self, in_file_path: str, in_keyword_dir: str, out_file_path: str, encoding: str, delim: str, window_size) :
        in_file = file_util.open_file(in_file_path, encoding, "r")
        out_file = file_util.open_file(out_file_path, encoding, "a")

        while True :
            line = in_file.readline()

            if not line :
                break

            line = file_util.preprocess(line)
            if string_util.is_empty(line, True) :
                continue

            keyword = KeywordExtractor(line, in_keyword_dir)
            line = string_util.trim(keyword.text.split(), True)
            eojeol_len = len(line)

            # keyword_labeling
            idx = 0
            # 문장을 어절 단위로 쪼갠 후 keyword_labeling 진행
            for eojeol in line :
                emjeol_len = len(eojeol)

                # 어절을 음절 단위로 쪼갠 후 keyword 목록에 있는지 확인하고 있다면 1로 labeling
                for i in range(emjeol_len) :
                    if eojeol[:i] in keyword.keyword_set :
                        keyword.keyword_label_list[idx] = 1
                idx += 1
            
            # 어절 단위로 학습 데이터 생성
            for i in range(eojeol_len) :
                feature = container_util.get_window(line, i, window_size, " ")
                label = keyword.keyword_label_list[i]

                out_file.write(f"{feature}{delim}{label}\n")

        in_file.close()
        out_file.close()

# main
if __name__ == "__main__" :
    work_dir = "../../"
    in_dir = work_dir + "data/input/sentences/"
    in_keyword_dir = work_dir + "data/input/keywords/"
    out_dir = work_dir + "data/keyword_extract/train_data_out.txt"
    encoding = "UTF-8"

    train_data_maker = MakeTrainData()
    train_data_maker.make_folder(in_dir, in_keyword_dir, out_dir, encoding, "\t", 3)