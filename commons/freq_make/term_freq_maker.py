from _init import *

from commons.sentence import Sentence
from commons import file_util, container_util, typo_util

class TermFreqMaker :
    def __init__(self) :
        self.encoding = "UTF-8"
        self.work_dir = "commons/freq_make/data/"
        self.josa_in_dir = self.work_dir + "josa_set.pickle"
        self.eomi_in_dir = self.work_dir + "eomi_set.pickle"
        self.freq_dict_dir = self.work_dir + "term_freq_dict.pickle"

        self.term_freq_dict = {}
        self.term_jamo_dict = {}
        self.jamo_term_dict = {}
        self.josa_set = set()
        self.eomi_set = set()
        self._load_josaeomi_file(self.josa_in_dir, self.eomi_in_dir)


    def make_folder(self, in_file_dir: str, encoding: str):
        if file_util.exists(self.freq_dict_dir):
            self._load_saved_dict(self.freq_dict_dir)


        in_file_paths = file_util.get_file_paths(in_file_dir, True)
        for in_file_path in in_file_paths:
            self._make_file(in_file_path, encoding)

        self._save_dict()
        
    def _make_file(self, in_file_path: str, encoding: str):
        in_file = file_util.open_file(in_file_path, encoding, 'r')

        while True:
            line = in_file.readline()
            if not line:
                break

            line = file_util.preprocess(line)
            if len(line) == 0:
                continue

            sentence = Sentence()
            sentence.set(line)

            for eojeol_str in sentence.eojeol_list:
                result_list, eojeol_str_list, _ = typo_util.check_eojeol_hangeul(eojeol_str)
                if result_list:
                    for eojeol_str in eojeol_str_list:
                        result_str, word_str = self._remove_josaeomi(eojeol_str)
                        if result_str:
                            container_util.add_str_int(self.term_freq_dict, word_str, 1)
                        container_util.add_str_int(self.term_freq_dict, eojeol_str, 1)

        in_file.close()

    def _remove_josaeomi(self, eojeol_str:str):
        idx = len(eojeol_str)
        for i in reversed(range(len(eojeol_str))):
            if (eojeol_str[i:] in self.josa_set) or (eojeol_str[i:] in self.eomi_set):
                idx = i

        if len(eojeol_str[:idx]) <= 1:
            return False, None
        
        return True, eojeol_str[:idx]

    def _load_josaeomi_file(self, josa_in_dir: str, eomi_in_dir: str):
        with open(josa_in_dir, 'rb') as fr:
            self.josa_set = pickle.load(fr)
        
        with open(eomi_in_dir, 'rb') as fr:
            self.eomi_set = pickle.load(fr)
    
    def _load_saved_dict(self, freq_in_dir: str):
        with open(freq_in_dir, 'rb') as fr:
            self.term_freq_dict = pickle.load(fr)
    
    def _save_dict(self):
        term_jamo_dir = self.work_dir + "term_jamo_dict.pickle"
        jamo_term_dir = self.work_dir + "jamo_term_dict.pickle"

        self._convert_jamo_dict()

        with open(self.freq_dict_dir, 'wb') as fw:
            pickle.dump(self.term_freq_dict, fw)

        with open(term_jamo_dir, 'wb') as fw:
            pickle.dump(self.term_jamo_dict, fw)

        with open(jamo_term_dir, 'wb') as fw:
            pickle.dump(self.jamo_term_dict, fw)

    def _convert_jamo_dict(self):
        for term in self.term_freq_dict:
            term_jamo = typo_util.convert_eojeol_jamo(term)
            self.term_jamo_dict[term] = term_jamo
            self.jamo_term_dict[term_jamo] = term


###########################################################################################

if __name__ == "__main__" :
    work_dir = "../../"
    in_file_dir = work_dir + "data/inputs/"
    encoding = "UTF-8"

    freq_maker = TermFreqMaker()
    freq_maker.make_folder(in_file_dir, encoding)
