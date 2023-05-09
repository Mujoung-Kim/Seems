from _init import *
import re, random

from commons.jamolist import *

def random_idx(something):
    if type(something) == int:
        return random.randrange(something)
   
    return random.randrange(len(something))

def add_typo_sen(in_dict: dict, key:str, value:str):
    if in_dict != None:
        if key in in_dict:
            in_dict[key].add(value)
        else:
            in_dict[key] = {value}


def check_emjeol_hangeul(emjeol_str):
    if re.match(r'[ㄱ-ㅣ|가-힣]', emjeol_str):
        return True
    return False

def divide_jamo(emjeol_str):
    if re.match(r'[가-힣]', emjeol_str):
        chosung_idx, junsung_idx, jongsung_idx = get_unicode_number(emjeol_str)
        return CHO[chosung_idx] + JUNG[junsung_idx] + JONG[jongsung_idx]

    else : 
        return emjeol_str
    
def convert_eojeol_jamo(eojeol_str):
    eojeol_jamo = ''
    for emjeol_str in eojeol_str:
        eojeol_jamo += divide_jamo(emjeol_str)
    return eojeol_jamo
    
def get_unicode_number(emjeol_str):
    emjeol_code = ord(emjeol_str)
    chosung_index = int((emjeol_code - 44032) / 588)
    jungsung_index = int((emjeol_code - 44032 - (chosung_index * 588)) / 28)
    jongsung_index = int((emjeol_code - 44032 - (chosung_index * 588) - (jungsung_index * 28)))
    return chosung_index, jungsung_index, jongsung_index


def get_hangeul_unicode(chosung_index, jungsung_index, jongsung_index):
    return((chosung_index * 588) + (jungsung_index * 28) + (jongsung_index)) + 44032

def convert_jamo_hangeul(emjeol_jamo_str):
    if check_emjeol_hangeul(emjeol_jamo_str):
        if len(emjeol_jamo_str) == 1:
            return emjeol_jamo_str
        else:
            try:
                global cho_idx; global jung_idx; global jong_idx
                cho_idx = CHO.index(emjeol_jamo_str[0])
                jung_idx = JUNG.index(emjeol_jamo_str[1])
                jong_idx = JONG.index(emjeol_jamo_str[2])
            except:
                jong_idx = 0
            emjeol_str = chr(get_hangeul_unicode(cho_idx, jung_idx, jong_idx))
    else:
        return emjeol_jamo_str
    
    return emjeol_str

def check_eojeol_hangeul(eojeol_str:str, default_label = 0):
    if eojeol_str.isascii(): # 숫자 + 특수문자
        return False, None, None
    
    else : # 한글 특수문자 영어가 섞인 어절
        result = False
        divided_eojeol_list = []
        eojeol_han_label_list = []
        hangeul_str = ''
        special_symbol = ''
        for emjeol_str in eojeol_str:
            if check_emjeol_hangeul(emjeol_str):
                result = True
                if special_symbol:
                    divided_eojeol_list.append(special_symbol)
                    eojeol_han_label_list.append(default_label)
                    special_symbol = ''
                hangeul_str += emjeol_str
            else :
                if hangeul_str :
                    divided_eojeol_list.append(hangeul_str)
                    eojeol_han_label_list.append(1)
                    hangeul_str = ''
                special_symbol += emjeol_str

        if hangeul_str:
            divided_eojeol_list.append(hangeul_str)
            eojeol_han_label_list.append(1)
        if special_symbol:
            divided_eojeol_list.append(special_symbol)
            eojeol_han_label_list.append(default_label)

        if result:
            return True, divided_eojeol_list, eojeol_han_label_list
        else:
            return False, None, None

def typo_change_jamo(jamo):
    i = random.randrange(len(jamo))
    idx = random.randrange(len(TYPO[jamo[i]]))
    jamo = jamo[:i] + TYPO[jamo[i]][idx] + jamo[i+1:]
    return jamo
        
def typo_position_convert(jamo):
    idx = random.randrange(0, len(jamo)-1)
    if jamo[idx+1] in ggub_jong:
        jamo = jamo[:idx] + ggub_jong[jamo[idx+1]][0] + jamo[idx] + ggub_jong[jamo[idx+1]][1]
    else :
        jamo = jamo[:idx] + jamo[idx+1] + jamo[idx]
    return jamo

def make_eojeol_typo(eojeol_list, eojeol_label_list):

    if len(eojeol_list) > 1:
        index_list = list(filter(lambda x: eojeol_label_list[x] == 1, range(len(eojeol_label_list))))
        eojeol_idx = random.choice(index_list)
        eojeol_str = eojeol_list[eojeol_idx]
    else:
        eojeol_str = eojeol_list[0]; eojeol_idx = 0

    emjeol_idx = random_idx(eojeol_str)
    emjeol_jamo = divide_jamo(eojeol_str[emjeol_idx])
    jamo_idx = random_idx(emjeol_jamo)
    typo_idx = random_idx(TYPO[emjeol_jamo[jamo_idx]])
    emjeol_jamo = emjeol_jamo[:jamo_idx] + TYPO[emjeol_jamo[jamo_idx]][typo_idx] + emjeol_jamo[jamo_idx +1:]
    emjeol_str = convert_jamo_hangeul(emjeol_jamo)
    eojeol_str = eojeol_str[:emjeol_idx] + emjeol_str + eojeol_str[emjeol_idx+1:]

    # eojeol_list[eojeol_idx] = eojeol_str
    converted_eojeol_list = eojeol_list[:eojeol_idx] + [eojeol_str] + eojeol_list[eojeol_idx+1:]
    return ''.join(converted_eojeol_list)





################################################################################################

# 
# typo_position_conver를 이용했을 때 사용

################################################################################################

def make_right_emjeol(emjeol_list):
    emjeol_jamo = ''.join(emjeol_list)

    converted_list = []

    while emjeol_jamo:
        
        remain_emjeol = ''
        moeum = False
        
        for i in reversed(range(len(emjeol_jamo))):


            if emjeol_jamo[i] not in JUNG:
                continue
            
            if (re.match(r'[ㄱ_ㅎ|가-힣]', emjeol_jamo[i]) == False):
                first_idx, last_idx = i, i
                remain_emjeol = emjeol_jamo[i+1:]
            
            moeum = True

            if (i == 0): # i가 첫 번째 음절일 경우
                first_idx, last_idx = i, i
                remain_emjeol = emjeol_jamo[i+1:]

            elif (emjeol_jamo[i-1] in JUNG) and ((emjeol_jamo[i-1], emjeol_jamo[i]) not in reversed_ggub_jung):
                first_idx, last_idx = i, i
                remain_emjeol = emjeol_jamo[i+1:]
            
            elif (emjeol_jamo[i-1] in JUNG) and ((emjeol_jamo[i-1], emjeol_jamo[i]) in reversed_ggub_jung):
                emjeol_jamo = emjeol_jamo[:i-1] + reversed_ggub_jung[(emjeol_jamo[i-1], emjeol_jamo[i])] + emjeol_jamo[i+1:]
                continue

            #########################################################################################3333

            else: # i가 첫 번째 음절이 아닐 경우

                '''
                    i 앞의 자모를 확인
                    i 는 중성 (ㅏ), i-1은 자음(ㄱ, ㄲ, ㄺ)
                '''
                
                if emjeol_jamo[i-1] in CHO: # i-1이 초성인 경우 (ㄱ, ㄲ)
                    first_idx = i-1

                else: # i-1이 겹받침인 경우(ㄺ)
                    cho1, cho2 = ggub_jong[emjeol_jamo[i-1]]
                    emjeol_jamo = emjeol_jamo[:i-1] + cho1 + cho2 + emjeol_jamo[i:]
                    i += 1; first_idx = i-1

                '''
                    i 뒤의 자모를 확인
                    i 는 중성, i+1은 자음(ㄱ, ㄲ, ㄺ)
                '''
                if len(emjeol_jamo)-1 == i: # i 가 마지막 음절일 경우
                    last_idx = i

                else: # i가 마지막 음절이 아닌 경우
                    if (emjeol_jamo[i+1] in ssang_jaeum) or (emjeol_jamo[i+1] in ggub_jong):
                        last_idx = i+1
                        remain_emjeol = emjeol_jamo[last_idx+1:]
                    
                    else: # i+1이 쌍자음, 겹받침이 아닌 자음인 경우
                        if i+2 < len(emjeol_jamo): # i 뒤의 자음이 두 개 이상인 경우
                            jong1, jong2 = emjeol_jamo[i+1:i+3]
                            if (jong1, jong2) in reversed_ggub_jong:
                                emjeol_jamo = emjeol_jamo[:i+1] + reversed_ggub_jong[(jong1, jong2)] + emjeol_jamo[i+3:]
                        last_idx = i+1
                        remain_emjeol = emjeol_jamo[i+2:]
            

            '''
                first_idx, last_idx, remain_emjeol
            '''
            emjeol_str = emjeol_jamo[first_idx: last_idx+1]
            jaeum_list = []
            jaeum_list.append(emjeol_str)
            
            if remain_emjeol:
                # 전체 자음인 경우
                x = 0
                for i in range(len(remain_emjeol)):
                    jaeum = remain_emjeol[i]
                    if (jaeum in ssang_jaeum) or (jaeum in ggub_jong):
                        jaeum_list.append(jaeum)
                    else : # 쌍자음이나 겹받침이 아닌 자음인 경우
                        if x == 0:
                            if i == len(remain_emjeol)-1:
                                jaeum_list.append(jaeum)
                            else:
                                x = jaeum; continue
                        else:
                            y = jaeum
                            if (x, y) in ggub_jong:
                                jaeum_list.append(ggub_jong[(x, y)])
                            else:
                                jaeum_list.append(x); jaeum_list.append(y)

            emjeol_jamo = emjeol_jamo[:first_idx]
            converted_list = jaeum_list + converted_list
            break

        if moeum == False:
            # 전체 자음인 경우
            jaeum_list = []

            if len(emjeol_jamo) == 1:
                converted_list.insert(0, emjeol_jamo)
            else:
                x = 0
                for i in range(len(emjeol_jamo)):
                    jaeum = emjeol_jamo[i]
                    if (emjeol_jamo[i] in ssang_jaeum) or (emjeol_jamo[i] in ggub_jong):
                        jaeum_list.append(jaeum)
                    elif x:
                        y = jaeum
                        if (x, y) in reversed_ggub_jong:
                            jaeum_list.append(ggub_jong[(x, y)])
                        else:
                            jaeum_list.append(x); jaeum_list.append(y)
                    elif i == len(emjeol_jamo)-1:
                        jaeum_list.append(jaeum)
                    else:
                        x = jaeum

            emjeol_jamo = ''
            converted_list = jaeum_list + converted_list

    return converted_list

