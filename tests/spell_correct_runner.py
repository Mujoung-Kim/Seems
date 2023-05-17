from _init import *

from models.spell_correct_model import SpellCorrectModel

MAX_SEQ_LEN = 64
EPOCHS = 100
BATCH_SIZE = 64
LEARNING_RATE = 1e-5
PATIENCE = 3


model = SpellCorrectModel(MAX_SEQ_LEN)

work_dir = '../../'
in_path = work_dir + 'data/inputs/'
out_file_path = work_dir + 'data/spell_correct/train_spell_correct.txt'

model.make_train_data(in_path, out_file_path)
model.load_train_data(out_file_path, '\t', 'utf-8', 9, 1)

model_path = work_dir + 'data/spell_correct/spell_correct_model.h5'

model.train(model_path, EPOCHS, BATCH_SIZE, LEARNING_RATE, PATIENCE)

model.load_model(model_path)
model.performance_measure()

# text = '개구리능 겨울이 되면 땅속으로 들어가 겨울잠을 잔다.'
# correct_sen = model.predict(text)
# print(correct_sen)

# text = "주변 온도에 따라 체온이 변하는 변온동몰이기 때문이다."
# correct_sen = model.predict(text)
# print(correct_sen)

# text = "게다가 겨울이 되면 먹이가 되는 곤츙들도 사라지기 때문에 겨울잠을 잘 수 밖에 없다."
# correct_sen = model.predict(text)
# print(correct_sen)