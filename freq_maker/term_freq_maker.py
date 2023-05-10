from _init import *

from commons import typo_util
from commons.sentence import Sentence
from commons import file_util
from commons import container_util

class TermFreqMaker :
    def __init__(self) :
        self.encoding = "UTF-8"

        self.term_freq_dict = {}
        self.josa_set = set()
        self.eomi_set = set()

    def make_folder(self, in_dir: str, josa_in_dir: str, eomi_in_dir: str, freq_in_dir: str, out_dir: str, encoding: str):
        self.load_file(josa_in_dir, eomi_in_dir)

        in_file_paths = file_util.get_file_paths(in_dir, True)
        for in_file_path in in_file_paths:
            self._make_file(in_file_path, encoding)
        
        total_freq_dict = self.load_saved_dict(freq_in_dir)
        print('1:', len(total_freq_dict))
        for key in self.term_freq_dict:
            container_util.add_str_int(total_freq_dict, key, self.term_freq_dict[key])
        print('2:', len(total_freq_dict))
        self.save_dict(total_freq_dict, out_dir)
    
    def _make_file(self, in_file_path: str, encoding: str, ):
        in_file = file_util.open_file(in_file_path, encoding, 'r')

        while True:
            line = in_file.readline()
            if not line:
                break

            line = file_util.preprocess(line)
            if len(line) == 0:
                continue

            sentence = Sentence(line)
            for eojeol_str in sentence.eojeol_list:
                result_list, eojeol_str_list, _ = typo_util.check_eojeol_hangeul(eojeol_str)
                if result_list:
                    for eojeol_str in eojeol_str_list:
                        result_str, word_str = self.remove_josaeomi(eojeol_str)
                        if result_str:
                            container_util.add_str_int(self.term_freq_dict, word_str,1)
                        container_util.add_str_int(self.term_freq_dict, eojeol_str, 1)


    def remove_josaeomi(self, eojeol_str:str):
        idx = len(eojeol_str)
        for i in reversed(range(len(eojeol_str))):
            if (eojeol_str[i:] in self.josa_set) or (eojeol_str[i:] in self.eomi_set):
                idx = i

        if len(eojeol_str[:idx]) <= 1:
            return False, None
        
        return True, eojeol_str[:idx]

    def load_file(self, josa_in_dir: str, eomi_in_dir: str):
        with open(josa_in_dir, 'rb') as fr:
            self.josa_set = pickle.load(fr)
        
        with open(eomi_in_dir, 'rb') as fr:
            self.eomi_set = pickle.load(fr)
    
    def load_saved_dict(self, freq_in_dir: str):
        with open(freq_in_dir, 'rb') as fr:
            total_freq_dict = pickle.load(fr)
        return total_freq_dict
    
    def save_dict(self, freq_dict: dict, out_dir: str):
        with open(out_dir, 'wb') as fw:
            pickle.dump(freq_dict, fw)


###########################################################################################

if __name__ == "__main__" :
    work_dir = "source/Seems/freq_maker/data/"

    josa_in_dir = work_dir + "josa_set.pickle"
    eomi_in_dir = work_dir + "eomi_set.pickle"
    freq_dict_dir = work_dir + "term_freq_dict.pickle"
    in_dir = "input/"
    out_dir = work_dir + "term_freq_dict.pickle"

    encoding = "UTF-8"
    delim_key = "\t"

    freq_maker = TermFreqMaker()
    freq_maker.make_folder(in_dir, josa_in_dir, eomi_in_dir, freq_dict_dir, out_dir, encoding)
    freq_maker.load_file(josa_in_dir, eomi_in_dir)