from _init import *

from models.space_correct_model import SpaceCorrectModel

MAX_SEQ_LEN = 32
EPOCHS = 1
BATCH_SIZE = 128
LEARNING_RATE = 1e-5
PATIENCE = 3

model = SpaceCorrectModel(MAX_SEQ_LEN)

work_dir = '../../data/space_correct/'
in_path = work_dir + 'inputs/'
out_file_path = work_dir + 'train_space_correct.txt'

model.make_train_data(in_path, out_file_path)
model.load_train_data(out_file_path, "\t", "UTF-8", 9, 1)

model_path = work_dir + "space_split_model.h5"

model.train(model_path, EPOCHS, BATCH_SIZE, LEARNING_RATE, PATIENCE)

# model.load_model(model_path)
# model.performance_measure()

# text = "가라루파는 터키의 온천에 사는 민물고기이다."

# sentences = model.predict(text)

# for sentence in sentences :
#     print(sentence)