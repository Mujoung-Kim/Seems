from _init import *

from default_model.data_reformator import DataReformator
from default_model.trainer import Trainer

root_path = "../../"
in_file_path = root_path + "data/keyword_extract/train_data_out.txt"
out_model_path = root_path + "resources/keyword_extract_model/bert_model.h5"
out_best_model_path = root_path + "resources/keyword_extract/best_bert_model.h5"
encoding = "utf-8"
delim = "\t"

data_reformator = DataReformator()
data_reformator.load_file(in_file_path, encoding, delim)
div_datas = data_reformator.div_reformat(8,1,1, False)

train_xys = data_reformator.reformating(div_datas[0], 20)
val_xys = data_reformator.reformating(div_datas[1], 20)
test_xys = data_reformator.reformating(div_datas[2], 20)

trainer = Trainer()

train_xs = train_xys[0]
train_ys = train_xys[1]

val_xs = val_xys[0]
val_ys = val_xys[1]

test_xs = test_xys[0]
test_ys = test_xys[1]

trainer.train(train_xs, train_ys, val_xs, val_ys, out_model_path, out_best_model_path, 10, 30, 2e-5, 3, 20, 0.5)
trainer.performance_measure(test_xs, test_ys)
