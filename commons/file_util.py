import os

###########################################################################################

def get_file_name(file_path: str, rm_ext_flag=False):
    file_name = os.path.basename(file_path)
    
    if rm_ext_flag:
        idx = file_name.rfind('.')
        
        if idx != -1:
            file_name = file_name[:idx]
    
    return file_name

###########################################################################################

def get_file_paths(in_dir: str, inner_flag: bool) :
    file_paths = []

    if inner_flag :
        for (parent_path, dirs, file_names) in os.walk(in_dir) :
                for file_name in file_names :
                    file_path = os.path.join(parent_path, file_name)

                    if os.path.isfile(file_path) :
                        file_paths.append(file_path)
    else :
        file_names = os.listdir(in_dir)
        for file_name in file_names :
            file_path = os.path.join(in_dir, file_name)

            if os.path.isfile(file_path) :
                file_paths.append(file_path)

    return file_paths

###########################################################################################

def make_parent(file_path: str) :
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def open_file(file_path: str, encoding: str, mode: str) :
    if mode == 'w' :
        make_parent(file_path)

    if len(encoding) == 0 :
        return open(file_path, mode)
    else :
        return open(file_path, mode, encoding=encoding)

###########################################################################################

def preprocess(input: str) :
    return input.strip()

###########################################################################################

def write_set(out_file_path: str, encoding: str, out_set: set, is_reverse: bool) :
    file = open_file(out_file_path, encoding, 'w')

    out_list = list(out_set)
    out_list.sort(reverse = is_reverse)

    for i in range(len(out_list)) :
        file.write(f"{out_list[i]}\n")
    
    file.close()

def write_dict(out_file_path: str, encoding: str, out_dict: dict, delim: str) :
    file = open_file(out_file_path, encoding, 'w')

    items = out_dict.items()
    for item in items :
        file.write(f"{item[0]}{delim}{item[1]}\n")
    
    file.close()

###########################################################################################

def exists(file_path: str) :
    if file_path == None or len(file_path) == 0 :
        return False

    if os.path.exists(file_path) and os.path.isfile(file_path) :
        return True

    return False
