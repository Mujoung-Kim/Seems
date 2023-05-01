import os

###########################################################################################

def is_empty(input: str, trim_flag: bool) :
    if input == None :
        return True
    
    if trim_flag :
        input = input.strip()
    
    if len(input) == 0 :
        return True
    
    return False

###########################################################################################

def trim(input_list: list, rm_empty_flag: bool) :
    if not rm_empty_flag :
        for i in range(len(input_list)) :
            if input_list[i] == None :
                input_list[i] = ""
            else :
                input_list[i] = str(input_list[i]).strip()
    else :
        result = []

        for i in range(len(input_list)) :
            if not is_empty(input_list[i], True) :
                result.append(str(input_list[i]).strip())
        
        return result
