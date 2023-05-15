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

# model.make_train_data(in_path, out_file_path)
# model.load_train_data(out_file_path, '\t', 'utf-8', 9, 1)

model_path = work_dir + 'resources/spell_correct/specll_correct_model.h5'

model.load_model(model_path)
# model.train(model_path, EPOCHS, BATCH_SIZE, LEARNING_RATE, PATIENCE)

# model.load_model(model_path)
# model.performance_measure()

# text = '이건 테스트를 위햔 문장'
# sentences = model.predict(text)

# for sentence in sentences:
#     print(sentence)

model.predict('개구리는 사람에게 여러 모로 이로운 동물이다.')
model.predict('개구리는 사람얘게 여러 모로 이로운 동물이다.')
    
model.predict('학교 가는 길에 있는 떡볶이는 맛있다.')
model.predict('학교 가는 길에 있는 떡볶이는 맛있디.')
model.predict('개구리는 사람얘게 여러 모로 이로운 동물이댜.')
model.predict('노는 게 제일 좋아.')
model.predict('친구들아 모여라.')