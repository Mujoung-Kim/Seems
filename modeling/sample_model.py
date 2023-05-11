from _init import *

from default_model.data_reformator import DataReformator
from default_model.trainer import Trainer

# load_data variable
root_path = "../../"
in_file_path = root_path + "data/keyword_extract/train_data_out.txt"
out_model_path = root_path + "resources/keyword_extract/bert_model.h5"
out_best_model_path = root_path + "resources/keyword_extract/best_bert_model.h5"
encoding = "UTF-8"
delim = "\t"

# hyperparameter variable
MAX_SEQ_LEN = 256
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
EPOCHS = 50
DROPOUT_RATE = 0.3
PATIENCE = 3

# data loading and split
data_reformator = DataReformator()

data_reformator.load_file(in_file_path, encoding, delim)
div_datas = data_reformator.div_reformat(9, 0, 1, True)

train_xys = data_reformator.reformating(div_datas[0], MAX_SEQ_LEN)
val_xys = data_reformator.reformating(div_datas[1], MAX_SEQ_LEN)
test_xys = data_reformator.reformating(div_datas[2], MAX_SEQ_LEN)

train_xs = train_xys[0]
train_ys = train_xys[1]

val_xs = val_xys[0]
val_ys = val_xys[1]

test_xs = test_xys[0]
test_ys = test_xys[1]

# train fine tuning
trainer = Trainer()

trainer.train(
    train_xs, train_ys,
    # val_xs, val_ys, out_model_path, 
    out_best_model_path,
    EPOCHS, BATCH_SIZE, LEARNING_RATE, PATIENCE, MAX_SEQ_LEN, dropout_rate=DROPOUT_RATE)
# trainer.performance_measure(test_xs, test_ys)
trainer._predict(test_xs, test_ys)