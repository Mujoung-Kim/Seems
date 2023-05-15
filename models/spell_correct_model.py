from _init import *

from commons import file_util, container_util, typo_util
from commons.sentence import Sentence

from models.default_model import DefaultModel

class SpellCorrectModel(DefaultModel):
    def __init__(self, max_seq_len: int, dropout_rate=0.3, num_labels=2, model_name='klue/bert-base'):
        super().__init__(max_seq_len, dropout_rate, num_labels, model_name)
    
    def make_train_data(self, in_path: str, out_file_path: str, delim='\t', encoding='utf-8'):
        if file_util.exists(out_file_path):
            os.remove(out_file_path)
        
        in_file_paths = file_util.get_file_paths(in_path, True)
        
        for in_file_path in in_file_paths:
            self._make_train_data(in_file_path, out_file_path, delim, encoding)

    def _make_train_data(self, in_file_path: str, out_file_path: str, delim='\t', encoding='utf-8'):
        in_file = file_util.open_file(in_file_path, encoding, 'r')
        out_file = file_util.open_file(out_file_path, encoding, 'a')
        
        while 1:
            line = in_file.readline()
            if not line:
                break
            
            line = file_util.preprocess(line)
            if len(line) == 0:
                continue
            
            line = line.replace('\t', ' ')
            sentence = Sentence()
            sentence.set(line)
            sentence.eojeol_label_list = self._set_eojeol_label_list(sentence.eojeol_label_list)
            
            feature_label_datas = sentence.get_feature_label_datas(is_train=True,is_emjeol=False)
            
            for feature_label_data in feature_label_datas:
                out_file.write(f'{feature_label_data[0]}{delim}{feature_label_data[1]}\n')
            
            len_eojeol = len(sentence.eojeol_list)
            for i in range(len_eojeol):
                result, div_eojeol_list, div_eojeol_label_list = typo_util.check_eojeol_hangeul(sentence.eojeol_list[i])
                if result and div_eojeol_label_list.count(1):
                    typo_set = set()
                    for _ in range(1):
                        typo_eojeol = typo_util.make_eojeol_typo(div_eojeol_list, div_eojeol_label_list)
                        if typo_eojeol not in typo_set:
                            eojeol_list = sentence.eojeol_list[:i] + [typo_eojeol] + sentence.eojeol_list[i+1:]
                            # eojeol_label_list = sentence.eojeol_label_list[:i] + [1] + sentence.eojeol_label_list[i+1:]
                            
                            train_sentence = container_util.get_window(eojeol_list, i, 3, ' ')
                            out_file.write(f'{train_sentence}{delim}1\n')

        in_file.close()
        out_file.close()

    def _set_eojeol_label_list(self, eojeol_label_list: list):
        eojeol_label_list = [0] * len(eojeol_label_list)
        
        return eojeol_label_list
    
    def predict(self, line):
        sentence = Sentence()
        sentence.set(line)
        
        feature_label_datas = sentence.get_feature_label_datas(is_train=False)
        predict_xs, _ = self.reformator.reformat_datas(feature_label_datas)
        
        predict_ys = super()._predict(predict_xs)
        print(f'predict_ys : {predict_ys}')
