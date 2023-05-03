from _init import *

from commons import file_util, container_util
from commons.sentence import Sentence
from module import typo_util

class MakeTrainData:
    def __init__(self):
        self.typo_dict = {}

    def make_folder(self, in_dir: str, out_file_ox_path: str, out_file_typo_path:str, encoding: str, delim: str, window_size):
        # if file_util.exists(out_file_ox_path):
        #     os.remove(out_file_ox_path)
        # if file_util.exists(out_file_typo_path):
        #     os.remove(out_file_typo_path)

        in_file_paths = file_util.get_file_paths(in_dir, True)
        for in_file_path in in_file_paths:
            self._make_file(in_file_path, out_file_ox_path, out_file_typo_path, encoding, window_size)
        
        # self.write_typo_dataset(out_file_typo_path, encoding, delim)

    def _make_file(self, in_file_path: str, out_file_ox_path:str, out_file_typo_path:str, encoding: str, window_size):
        in_file = file_util.open_file(in_file_path, encoding, 'r')
        out_ox_file = file_util.open_file(out_file_ox_path, encoding, 'a')
        out_typo_file = file_util.open_file(out_file_typo_path, encoding, 'a')
        
        while 1:
            line = in_file.readline()
            if not line:
                break
            
            line = file_util.preprocess(line)
            if len(line) == 0:
                continue
            
            line = line.replace('\t', ' ')
            sentence = Sentence(line)

            eojeol_len = len(sentence.eojeol_list)

            self.write_spell_dataset(out_ox_file, sentence.eojeol_list, sentence.eojeol_label_list, window_size)

            for i in range(eojeol_len):
                result, divided_eojeol_list, divided_eojeol_label_list = typo_util.check_eojeol_hangeul(sentence.eojeol_list[i])

                if result :
                    typo_set = set()
                    for _ in range(1):
                        typo_eojeol = typo_util.make_eojeol_typo(divided_eojeol_list, divided_eojeol_label_list)
                        if typo_eojeol not in typo_set:
                            converted_ojeol_list = sentence.eojeol_list[:i] + [typo_eojeol] + sentence.eojeol_list[i+1:]
                            converted_ojeol_label_list = sentence.eojeol_label_list[:i] + [1] + sentence.eojeol_label_list[i+1:]
                            self.write_spell_dataset(out_ox_file, converted_ojeol_list, converted_ojeol_label_list, window_size)

                            converted_window = container_util.get_window(converted_ojeol_list, i, window_size, delim=' ')
                            self.write_typo_dataset(out_typo_file, sentence.eojeol_list[i], converted_window)
                            typo_set.add(typo_eojeol)

        in_file.close()
        out_ox_file.close()
        out_typo_file.close()

    def write_spell_dataset(self, out_file, eojeol_list:list, eojeol_label_list, window_size:int):

        for i in range(len(eojeol_list)):
            feature = container_util.get_window(eojeol_list, i, window_size, ' ')
            label = eojeol_label_list[i]
            
            out_file.write(f"{feature}{delim}{label}\n")
    
    def write_typo_dataset(self, out_file:str, eojeol_str:str, converted_window:str, delim = '\t'):
        
        out_file.write(f"{converted_window}{delim}{eojeol_str}\n")



if __name__ == "__main__":
    work_dir = ''
    in_dir = work_dir + 'data/input/'
    out_file_ox_path = work_dir + 'data/spell_correct/spell_ox/train_data_out.txt'
    out_file_typo_path = work_dir + 'data/spell_correct/spell_typo/train_data_out.txt'
    encoding = "utf-8"
    delim = '\t'
    
    train_data_maker = MakeTrainData()
    train_data_maker.make_folder(in_dir, out_file_ox_path, out_file_typo_path, encoding, delim, 3)