from _init import *
import pickle
import numpy as np

from commons import typo_util

class SpellCorrector() :

    def __init__(self):
        self.work_dir = "commons/freq_maker/data/"
        self.josa_dir = self.work_dir + 'josa_set.pickle'
        self.eomi_dir = self.work_dir + 'eomi_set.pickle'
        self.freq_dir = self.work_dir + 'term_freq_dict.pickle'

        self.josa_set = set()
        self.eomi_set = set()
        self.term_freq_dict = {}
        self.term_jamo_dict = {}
        self._open_file(self.josa_dir, self.eomi_dir, self.freq_dir)
        self._make_jamo_dict()

    def _open_file(self, josa_dir, eomi_dir, freq_dir):
        with open(josa_dir, 'rb') as fr:
            self.josa_set = pickle.load(fr)

        with open(eomi_dir, 'rb') as fr:
            self.eomi_set = pickle.load(fr)

        with open(freq_dir, 'rb') as fr:
            self.term_freq_dict = pickle.load(fr)
    
    def _make_jamo_dict(self):
        for key in self.term_freq_dict:
            jamo = ''
            for emjeol_str in key:
                jamo += typo_util.divide_jamo(emjeol_str)
            self.term_jamo_dict[jamo] = key

    def discriminate_typo(self, eojeol_str):
        result, eojeol_list, eojeol_label_list = typo_util.check_eojeol_hangeul(eojeol_str)
        if result:
            for i in range(len(eojeol_label_list)):
                if eojeol_label_list[i]:
                    typo_eojeol = eojeol_list[i]
                    eojeol_list[i] = self.convert_typo_correct(typo_eojeol)
            
            return ''.join(eojeol_list)
        
        else:
            return eojeol_str

    def convert_typo_correct(self, typo_eojeol):
        typo_jamo = typo_util.convert_eojeol_jamo(typo_eojeol)
        len_typo = len(typo_jamo)
        correct = (10, '')

        for correct_jamo in self.term_jamo_dict:
            len_correct = len(correct_jamo)
            if abs(len_correct - len_typo) > 1:
                continue
            distance = self.minimum_edit_distance(typo_jamo, correct_jamo)

            if distance < correct[0]:
                correct = min(correct, (distance, correct_jamo))

            if distance == 1:
                break
        
        correct_str = self.term_jamo_dict[correct[1]]
        return correct_str

    def minimum_edit_distance(self, typo_jamo, correct_jamo):
        deletion_cost = lambda x: 1
        substitution_cost = lambda x, y: 0 if x==y else 2
        insertion_cost = lambda x: 1
        n = len(typo_jamo)
        m = len(correct_jamo)
        D = np.zeros((n+1, m+1))
        
        for i in range(1, n+1):
            D[i,0] = D[i-1,0] + deletion_cost(typo_jamo[i-1])
        for j in range(1, m+1):
            D[0,j] = D[0, j-1] + insertion_cost(correct_jamo[j-1])       
        for i in range(1, n+1):
            for j in range(1, m+1):
                D[i, j] = min(D[i-1, j] + deletion_cost(typo_jamo[i-1]),
                            D[i-1, j-1] + substitution_cost(typo_jamo[i-1], correct_jamo[j-1]),
                            D[i, j-1] + insertion_cost(correct_jamo[j-1]))
        return D[-1, -1]

# main
if __name__ == "__main__" :
    
    spellcorrect = SpellCorrector()
    eojeol_str = '병완에서'
    print(bool('병원에서' in spellcorrect.term_freq_dict))
    print(spellcorrect.discriminate_typo(eojeol_str))