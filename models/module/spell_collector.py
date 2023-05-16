from _init import *
import pickle
import numpy as np

from commons import typo_util

class SpellCorrector() :

    def __init__(self):
        self.work_dir = "commons/freq_make/data/"
        self.josa_dir = self.work_dir + 'josa_set.pickle'
        self.eomi_dir = self.work_dir + 'eomi_set.pickle'
        self.term_freq_dir = self.work_dir + 'term_freq_dict.pickle'
        self.term_jamo_dir = self.work_dir + 'term_jamo_dict.pickle'
        self.jamo_term_dir = self.work_dir + 'jamo_term_dict.pickle'

        self.josa_set = set()
        self.eomi_set = set()
        self.term_freq_dict = {}
        self.term_jamo_dict = {}
        self.jamo_term_dict = {}
        self._open_file(self.josa_dir, self.eomi_dir, self.term_freq_dir, self.term_jamo_dir, self.jamo_term_dir)

    def _open_file(self, josa_dir: str, eomi_dir: str, term_freq_dir: str, term_jamo_dir: str, jamo_term_dir: str):
        with open(josa_dir, 'rb') as fr:
            self.josa_set = pickle.load(fr)

        with open(eomi_dir, 'rb') as fr:
            self.eomi_set = pickle.load(fr)

        with open(term_freq_dir, 'rb') as fr:
            self.term_freq_dict = pickle.load(fr)
    
        with open(term_jamo_dir, 'rb') as fr:
            self.term_jamo_dict = pickle.load(fr)

        with open(jamo_term_dir, 'rb') as fr:
            self.jamo_term_dict = pickle.load(fr)

    def discriminate_typo(self, eojeol_str: str):
        result, eojeol_list, eojeol_label_list = typo_util.check_eojeol_hangeul(eojeol_str)
        if result:
            for i in range(len(eojeol_label_list)):
                if eojeol_label_list[i]:
                    typo_eojeol = eojeol_list[i]
                    eojeol_list[i] = self.convert_typo_correct(typo_eojeol)
            
            return ''.join(eojeol_list)
        
        else:
            return eojeol_str

    def convert_typo_correct(self, typo_eojeol: str):
        correct = (10, '')
        for correct_eojeol in self.term_freq_dict:
            if abs(len(correct_eojeol) - len(typo_eojeol)) > 1:
                continue
            correct_jamo = self.term_jamo_dict[correct_eojeol]
            typo_jamo = typo_util.convert_eojeol_jamo(typo_eojeol)
            if abs(len(correct_jamo) - len(typo_jamo)) > 1:
                continue
            distance = self.minimum_edit_distance(typo_jamo, correct_jamo)

            if distance < correct[0]:
                correct = min(correct, (distance, correct_jamo))
            
            if distance == 0:
                break

        correct_str = self.jamo_term_dict[correct[1]]
        return correct_str

    def minimum_edit_distance(self, typo_jamo: str, correct_jamo: str):
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