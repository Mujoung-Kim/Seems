from _init import *

from models.sentence_split_model import SentenceSplitModel

MAX_SEQ_LEN = 32
EPOCHS = 1
BATCH_SIZE = 128
LEARNING_RATE = 0.01
PATIENCE = 10

model = SentenceSplitModel(MAX_SEQ_LEN)

work_dir = '../../data/sentence_split/'
in_path = work_dir + 'inputs/'
out_file_path = work_dir + 'train_sentence_split.txt'

model.make_train_data(in_path, out_file_path)
model.load_train_data(out_file_path, '\t', 'utf-8', 9, 1)

model_path = work_dir + 'sentence_split_model.h5'

model.train(model_path, EPOCHS, BATCH_SIZE, LEARNING_RATE, PATIENCE)

# model.load_model(model_path)
# model.performance_measure()

# text = '자연단음계 화성단음계 가락단음계는 다음과 같다. 그 이름은 필살의 상처를 입히는 창 또는 톱니 모양 새김눈이 있는 창 볼록한 창이라는 뜻이다.'
# sentences = model.predict(text)

# for sentence in sentences:
#     print(sentence)