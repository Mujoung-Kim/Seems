import os

###########################################################################################

def add_str_int(in_dict: dict, key: str, value: int) :
    if in_dict != None :
        if key in in_dict :
            value_prev = int(in_dict[key])
            in_dict[key] = value_prev + value
        else :
            in_dict[key] = value

###########################################################################################

def get_window(in_list: list, idx: int, window_size: int, delim=''):
    result = []
    in_len = len(in_list)
    
    # 앞 부분 저장
    start = idx - window_size
    if start < 0:
        result.append('$'*(start*-1))
        start = 0
    
    if start < idx:
        result.extend(in_list[start:idx])
    
    # 현재 부분 저장
    result.append(in_list[idx])
    
    # 뒷 부분 저장
    end = idx + window_size
    
    if end < in_len:
        result.extend(in_list[idx+1:end+1])
    else:
        if idx+1 < in_len:
            result.extend(in_list[idx+1:in_len])
        
        end = end - in_len + 1
        if end > 0:
            result.append('$$'*end)
    
    return delim.join(result)

###########################################################################################

'''
    key를 기준으로 정렬
        - is_reverse = False : 오름 차순
        - is_reverse = True : 내림 차순
'''
def sorted_dict_key(in_dict: dict, is_reverse: bool) :
    return dict(sorted(in_dict.items(), key=lambda item:item[0], reverse=is_reverse))

'''
    value를 기준으로 정렬
        - is_reverse = False : 오름 차순
        - is_reverse = True : 내림 차순
'''
def sorted_dict_value(in_dict: dict, is_reverse: bool) :
    return dict(sorted(in_dict.items(), key=lambda item:item[1], reverse=is_reverse))

'''
    key를 기준으로 오름 차순 정렬, value를 기준으로 내림 차순 정렬
'''
def sorted_dict(in_dict: dict) :
    return sorted_dict_value(sorted_dict_key(in_dict, False), True)
