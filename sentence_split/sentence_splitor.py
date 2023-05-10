from _init import *

from commons import file_util, string_util, container_util
from commons.sentence import Sentence
from commons import typo_util

class SentenceSplitor:
    
    def __init__(self):
        self.texts = ''
        
    
    def make_folder(self, in_dir: str, out_file_path: str, encoding: str):
        if file_util.exists(out_file_path):
            os.remove(out_file_path)
            
        in_file_paths = file_util.get_file_paths(in_dir, False)
        for in_file_path in in_file_paths:
            self._make_file(in_file_path, out_file_path, encoding)
    
    def _make_file(self, in_file_path: str, out_file_path: str, encoding: str):
        file_name = file_util.get_file_name(in_file_path)
        out_file_path = os.path.join(out_file_path , file_name)
        
        in_file = file_util.open_file(in_file_path, encoding, 'r')
        out_file = file_util.open_file(out_file_path, encoding, 'w')
        
        while 1:
            line = in_file.readline()
            if not line:
                break
            
            line = file_util.preprocess(line)
            if len(line) == 0:
                continue
            
            if line.isascii():
                continue
            
            # 여기까지 내려온 line은 문자만이거나 문자와 특수기호 또는 숫자가 조합된 line
            sentences = self.sentence_split(line)
            
            for sentence in sentences:
                out_file.write(f"{sentence}\n")
            
                
        
        in_file.close()
        out_file.close()
        
    def sentence_split(self, line: str):
        #texts = '.' + line
        
        sentences = []
        correct = True
        if line.count('.') == 0:
            hangeul = False
            for emjeol_str in line:
                if typo_util.check_emjeol_hangeul(emjeol_str):
                    hangeul = True
            if hangeul:
                sentences.append(line)
        else:
            num = '0123456789'
            josa_list = ['라고', '는 ', '라 ', '이라고', '고 ', '와 ']
            forward_line = ''
            sentences = []

            while line:
                if line[:2] == '  ':
                    correct = False
                line = line.strip()
                
                try:
                    idx = line.index('.')
                except ValueError:
                    idx = len(line)
                    
                forward_line += line[:idx+1]
                line = line[idx+1:]
                
                result = True
                if (forward_line[-2] in num) and (line[0] in num):
                    result = False
                    
                elif line[:2] in josa_list:
                    result = False
                    
                elif '  ' in forward_line:
                    result = False
                
                # result가 True일때 (문장이 끝났을때)   
                # else가 없기때문에 result가 False이면 조건문이 적용되지 않음
                if result:
                    # 문장이 완전한 문장이면
                    if correct:
                        # sentence 리스트에 foward_line값을 추가함
                        sentences.append(forward_line)
                    # 문장이 완전한 문장이 아니면
                    else:
                        # sentence 리스트에 추가하지 않음
                        # correct를 초기화 시킴
                        correct = True
                    # forward_line을 초기화 시킴    
                    forward_line = ''
        
        return sentences
                                
        
        
    
            
if __name__ == "__main__":
    
    work_dir = '../../'
    in_dir = work_dir + 'data/input/raw_data/'
    out_file_path = work_dir + 'data/input/sentences/'
    encoding = 'utf-8'
    
    sentence_splitor = SentenceSplitor()
    sentence_splitor.make_folder(in_dir, out_file_path, encoding)         
    
    
    