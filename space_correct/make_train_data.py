from _init import *

from commons import file_util, container_util
from commons.sentence import Sentence

class MakeTrainData:
    def __init__(self):
        pass

    def make_folder(self, in_dir: str, out_file_path: str, encoding: str, delim: str, window_size):
        if file_util.exists(out_file_path):
            os.remove(out_file_path)

        in_file_paths = file_util.get_file_paths(in_dir, True)
        for in_file_path in in_file_paths:
            self._make_file(in_file_path, out_file_path, encoding, delim, window_size)

    def _make_file(self, in_file_path: str, out_file_path, encoding: str, delim: str, window_size):
        in_file = file_util.open_file(in_file_path, encoding, 'r')
        out_file = file_util.open_file(out_file_path, encoding, 'a')
        
        while 1:
            line = in_file.readline()
            if not line:
                break
            
            line = file_util.preprocess(line)
            if len(line) == 0:
                continue
        
            sentence = Sentence(line)
            
            # 어절을 확인하면서, 각 어절의 마지막 음절 부분만 '1'로 레이블 변경
            idx = -1
            for eojeol in sentence.eojeol_list:
                idx += len(eojeol)
                sentence.emjeol_label_list[idx] = 1
            
            # 음절 단위로 학습 데이터 생성
            emjeol_len = len(sentence.emjeol_list)
            for i in range(emjeol_len):
                feature = container_util.get_window(sentence.emjeol_list, i, window_size)
                label = sentence.emjeol_label_list[i]
                
                out_file.write(f"{feature}{delim}{label}\n")
        in_file.close()
        out_file.close()

if __name__ == "__main__":
    work_dir = '../../'
    # work_dir = "C:/Users/user/Desktop/nlp_project/data/input/sejong_sentence_sample.txt"
    in_dir = work_dir + 'data/input/sentences'
    out_file_path = work_dir + 'data/space_correct/train_data_out.txt'
    encoding = "utf-8"
    
    train_data_maker = MakeTrainData()
    train_data_maker.make_folder(in_dir, out_file_path, encoding, '\t', 3)
    