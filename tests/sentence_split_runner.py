from _init import *

from models.sentence_split_model import SentenceSplitModel

MAX_SEQ_LEN = 32
EPOCHS = 50
BATCH_SIZE = 128
LEARNING_RATE = 1e-5
PATIENCE = 3

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

# text = '가라루파는 터키의 온천에 사는 민물고기이다. 하지만 이 물고기가 실제로 피부병을 치료하는 데 효과가 있는지에 대해서는 논란이 있다. 가라루파는 주로 터키, 시리아, 이란, 그리고 이라크에 분포한다.'
# sentences = model.predict(text)

# for sentence in sentences:
#     print(sentence)