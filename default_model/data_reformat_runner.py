from _init import *

from commons import file_util
import data_reformat

def _print_1(datas):
    print(f"train data size : {len(datas[0][0])} / {len(datas[0][1])}")
    print(f'train data text : {datas[0][0]}')
    print(f'train label text : {datas[0][1]}\n')

    print(f"val data size : {len(datas[1][0])} / {len(datas[1][1])}")
    print(f'val data text : {datas[1][0]}')
    print(f'val label text : {datas[1][1]}\n')

    print(f"test data size : {len(datas[2][0])} / {len(datas[2][1])}")
    print(f'test data text : {datas[2][0]}')
    print(f'test label text : {datas[2][1]}\n')

def _print_2(data_xys):
    data_xs = data_xys[0]
    data_ys = data_xys[1]

    for i in range(len(data_xs)):
        data_x = data_xs[i]
        data_y = data_ys[i]
        print(f"{data_x}\n{data_y}\n")


# in_path = 'C:\\Users\\user\\Desktop\\nlp_project\\data\\space_correct'
in_file_path = 'C:\\Users\\user\\Desktop\\nlp_project\\data\\space_correct\\train_data_out_test.txt'
encoding = 'utf-8'
delim = '\t'


data_reformator = data_reformat.DataReformator()

# # data_reformator.load_folder(in_path, encoding, delim)
data_reformator.load_file(in_file_path, encoding, delim)

div_datas = data_reformator.div_reformat(8,1,1, True)
# _print(div_datas)

div_datas = data_reformator.div_reformat(8,1,1, False)
# _print(div_datas)

train_xys = data_reformator.reformating(div_datas[0], 'klue/bert-base', 20)
val_xys = data_reformator.reformating(div_datas[1], 'klue/bert-base', 20)
test_xys = data_reformator.reformating(div_datas[2], 'klue/bert-base', 20)
# _print_2(train_xys)
# _print_2(val_xys)
# _print_2(test_xys)