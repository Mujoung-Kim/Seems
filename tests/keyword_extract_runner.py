from _init import *

from models.keyword_extract_model import KeywordExtractModel

MAX_SEQ_LEN = 64
EPOCHS = 1
BATCH_SIZE = 64
LEARNING_RATE = 0.01
PATIENCE = 10

model = KeywordExtractModel(MAX_SEQ_LEN)

work_dir = "../../data/keyword_extract/"
in_path = work_dir + "inputs/sentences/"
in_keyword_path = work_dir + "inputs/keywords/"
out_file_path = work_dir + "train_keyword_extract.txt"

# model.make_train_data(in_path, in_keyword_path, out_file_path)
model.load_train_data(out_file_path, "\t", "UTF-8", 9, 1)

model_path = work_dir + "keyword_extract_model.h5"

# model.train(model_path, EPOCHS, BATCH_SIZE, LEARNING_RATE, PATIENCE)

model.load_model(model_path)
model.performance_measure()

# import pandas as pd

# df = pd.DataFrame(model.test_ys, columns=["labels"])
# print(df.labels.value_counts())