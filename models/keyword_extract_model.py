from _init import *

from commons import file_util, string_util

from models.default_model import DefaultModel
from models.module.keyword_extractor import KeywordExtractor
from models.module.josa_extractor import JosaExtractor

class KeywordExtractModel(DefaultModel) :
    '''
        Constructor
        1. josa_extract : 조사 추출하는 객체
    '''
    def __init__(self, max_seq_len: int, dropout_rate=0.3, num_labels=2, model_name='klue/bert-base'):
        super().__init__(max_seq_len, dropout_rate, num_labels, model_name)
        self.josa_extract = JosaExtractor()

    '''
        Methods
        1. make_train_data
        2. _make_train_data
        3. predict
    '''
    def make_train_data(self, in_path: str, in_keyword_path: str, out_file_path: str, delim="\t", encoding="UTF-8") :
        if file_util.exists(out_file_path) :
            os.remove(out_file_path)

        in_file_paths = file_util.get_file_paths(in_path, True)

        for in_file_path in in_file_paths :
            self._make_train_data(in_file_path, in_keyword_path, out_file_path, delim, encoding)

    def _make_train_data(self, in_file_path: str, in_keyword_path: str, out_file_path: str, delim: str, encoding: str) :
        in_file = file_util.open_file(in_file_path, encoding, "r")
        out_file = file_util.open_file(out_file_path, encoding, "a")

        while True :
            line = in_file.readline()

            if not line :
                break

            line = file_util.preprocess(line)

            if string_util.is_empty(line, True) :
                continue

            keyword = KeywordExtractor()
            keyword.set(line, in_keyword_path, encoding)

            feature_label_datas = keyword.get_feature_label_datas()
            feature_label_datas_len = len(feature_label_datas[0])

            for i in range(feature_label_datas_len) :
                out_file.write(f"{feature_label_datas[0][i]}{delim}{feature_label_datas[1][i]}\n")

        in_file.close()
        out_file.close()

    def predict(self, text: str, in_dir: str) :
        keywords = []
        sentences = []

        keyword = KeywordExtractor()
        keyword.set(text, in_dir)

        feature_label_datas = keyword.get_feature_label_datas(is_train=False)
        predict_xs, _ = self.reformator.reformat_datas(feature_label_datas)

        predict_ys = super()._predict(predict_xs)
        print(f"predict_ys : {predict_ys}")

        eojeol_list = keyword.eojeol_list
        eojeol_len = len(eojeol_list)

        start = 0
        for i in range(eojeol_len) :
            if i == eojeol_len - 1 and predict_ys[i] == 1 :
                self.josa_extract.set_text("".join(eojeol_list[start:]))
                sentences.append(" ".join(eojeol_list[start:]))
                keywords.append("".join(self.josa_extract.extract_josa()[-1]))
                keyword.write_keyword_set(f"{in_dir}train_keyword_set.txt")
                break
            elif i == eojeol_len - 1 :
                sentences.append(" ".join(eojeol_list[start:]))
            elif predict_ys[i] == 1 :
                self.josa_extract.set_text("".join(eojeol_list[start:i+1]))
                sentences.append(" ".join(eojeol_list[start:i+1]))
                keywords.append("".join(self.josa_extract.extract_josa()[start:i+1]))
                keyword.write_keyword_set(f"{in_dir}train_keyword_set.txt")
                start = i + 1

            # if i == eojeol_len - 1 :
            #     self.josa_extract.set_text("".join(eojeol_list[start:]))
            #     keywords.append("".join(self.josa_extract.extract_josa()[start : i + 1]))
            #     self.josa_extract.add_keyword_set(keyword.keyword_set)
            #     sentences.extend(eojeol_list[start:])
            #     keywords.append("".join(self.josa_extract.extract_josa()[start:]))
            # elif predict_ys[i] == 1 :
            #     self.josa_extract.set_text("".join(eojeol_list[start:i+ 1]))
            #     keywords.append("".join(self.josa_extract.extract_josa()[start:i+1]))
            #     self.josa_extract.add_keyword_set(keyword.keyword_set)
            #     sentences.append(" ".join(eojeol_list[start : i + 1]))
            #     keyword.write_keyword_set(f"{in_dir}train_keyword_set.txt")
            #     start = i + 1
            
        return [sentences, keywords]