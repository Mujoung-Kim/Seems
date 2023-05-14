from _init import *

from models.space_correct_model import SpaceCorrectModel

MAX_SEQ_LEN = 128

model = SpaceCorrectModel(MAX_SEQ_LEN)

work_dir = '../../data/space_correct/'
in_path = work_dir + 'inputs/'
out_file_path = work_dir + 'train_space_correct.txt'

model.make_train_data(in_path, out_file_path)
