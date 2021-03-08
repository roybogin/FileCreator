import os


def rep(s, **kwargs):
    for key in kwargs:
        s = s.replace('{'+key+'}', str(kwargs[key]))
    return s


def capitalize(sub):
    sub = sub.lower()
    spl = sub.split()
    for idx, word in enumerate(spl):
        if len(word)>2:
            spl[idx] = word.capitalize()
    return ' '.join(spl)


def count_hw(pth):
    os.listdir(pth)


def create_folder(pth):
    cnt = count_hw(pth)


def main():
    global subject
    subject = capitalize(subject)
    print(subject)
    new_path = os.path.join(path, subject)


if __name__ == '__main__':
    path = r'C:\Users\roybo\Desktop\University\semester 2'
    subject = r'logics'
    hw_number = None
    main()
