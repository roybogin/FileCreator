import os


def rep(s, **kwargs):
    for key in kwargs:
        s = s.replace('{'+key+'}', str(kwargs[key]))
    return s


def capitalize(sub):
    sub = sub.lower()
    spl = sub.split()
    for idx, word in enumerate(spl):
        if len(word) > 2:
            spl[idx] = word.capitalize()
    return ' '.join(spl)


def hw_num(folder_path):
    lst = os.listdir(folder_path)
    lst.sort(reverse=True)
    idx = 0
    while idx < len(lst) and lst[idx][:2] != 'hw':
        idx += 1
    return int(lst[idx][2:lst[idx].index('_')])+1 if idx != len(lst) else 1


def create_folder(subject_path):
    num = hw_num(subject_path) if hw_number is None else hw_number
    subject_name = '_'.join(subject.lower().split())
    folder_name = f'hw{num}_{subject_name}'
    folder_path = os.path.join(subject_path, folder_name)
    if os.path.exists(folder_path):
        raise Exception('Folder already exists')
    os.mkdir(folder_path)
    return folder_path, folder_name


def main():
    global subject
    subject = capitalize(subject)
    new_path = os.path.join(path, subject)
    folder_path, name = create_folder(new_path)



if __name__ == '__main__':
    path = r'C:\Users\roybo\Desktop\University\semester 2'
    subject = r'logics'
    hw_number = None
    main()
