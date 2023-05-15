from _init import *

from commons import file_util
from commons.sentence import Sentence

from models.default_model import DefaultModel

class SpaceCorrectModel(DefaultModel):
    def __init__(self, max_seq_len: int, dropout_rate=0.3, num_labels=2, model_name='klue/bert-base'):
        super().__init__(max_seq_len, dropout_rate, num_labels, model_name)
    
    def make_train_data(self, in_path: str, out_file_path: str, delim='\t', encoding='utf-8'):
        if file_util.exists(out_file_path):
            os.remove(out_file_path)
        
        in_file_paths = file_util.get_file_paths(in_path, True)
        
        for in_file_path in in_file_paths:
            self._make_train_data(in_file_path, out_file_path, delim, encoding)

    def _make_train_data(self, in_file_path, out_file_path, delim, encoding):
        in_file = file_util.open_file(in_file_path, encoding, 'r')
        out_file = file_util.open_file(out_file_path, encoding, 'a')
        
        while 1:
            line = in_file.readline()
            if not line:
                break
            
            line = file_util.preprocess(line)
            if len(line) == 0:
                continue
            
            sentence = Sentence()
            sentence.set(line)
            
            feature_label_datas = sentence.get_feature_label_datas(is_train=True, is_emjeol=True)
            
            for feature_label_data in feature_label_datas:
                out_file.write(f'{feature_label_data[0]}{delim}{feature_label_data[1]}\n')
            
        in_file.close()
        out_file.close()

    def predict(self, text: str) :
        sentences = []

        sentence = Sentence()
        sentence.set(text)

        feature_label_datas = sentence.get_feature_label_datas(is_emjeol=True, is_train=False)
        predict_xs, _ = self.reformator.reformat_datas(feature_label_datas)
        
        predict_ys = super()._predict(predict_xs)
        print(f"predict_ys : {predict_ys}")

        emjeol_list = sentence.emjeol_list
        emjeol_len = len(emjeol_list)

        start = 0
        for i in range(emjeol_len) :
            if i == emjeol_len - 1 :
                sentences.append(" ".join(emjeol_list[start:]))
            elif predict_ys[i] == 1 :
                sentences.append(" ".join(emjeol_list[start:i+1]))
                start = i + 1

        return sentences