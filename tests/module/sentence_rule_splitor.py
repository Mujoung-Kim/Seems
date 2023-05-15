from _init import *

import re

from commons import file_util, string_util

SPLIT_PAT = re.compile('[.!?]+')

def split_sentence_folder(in_path: str, out_path: str, encoding='utf-8'):
    in_file_paths = file_util.get_file_paths(in_path, False)

    for in_file_path in in_file_paths:
        file_name = file_util.get_file_name(in_file_path)
        out_file_path = os.path.join(out_path, file_name)
            
        split_sentence_file(in_file_path, out_file_path, encoding)

def split_sentence_file(in_file_path: str, out_file_path: str, encoding: str):
    in_file = file_util.open_file(in_file_path, encoding, 'r')
    out_file = file_util.open_file(out_file_path, encoding, 'w')
    
    while 1:
        line = in_file.readline()
        if not line:
            break
        
        line = file_util.preprocess(line)
        if len(line) == 0:
            continue
        
        sentences = split_sentence(line)
        
        for sentence in sentences:
            out_file.write(f"{sentence}\n")

    in_file.close()
    out_file.close()

def split_sentence(text: str):
    sentences = []
    
    while 1:
        text_len = len(text)
        searched = SPLIT_PAT.search(text)
        
        if searched is not None:
            # start = searched.start()
            end = searched.end()
            # print(f'start : {start}, end : {end}')
            
            if end == text_len-1:
                sentences.append(text[:end])
                break
            else:
                sentences.append(text[:end])
                text = text[end:].strip()
                continue
        
        sentences.append(text)
        break
    
    sentences = string_util.trim(sentences, True)
    return sentences

# if __name__ == "__main__":
#     text = '이건 테스트 문장1. 이건 테스트 문장2 이건 테스트 문장!?? 이건 테스트 문장4'
    
#     sentences = split_sentence(text)
#     for sentence in sentences:
#         print(sentence)