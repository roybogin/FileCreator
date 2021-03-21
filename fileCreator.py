import os
import textract
from tika import parser
import sys
from enum import Enum
import re


class Subject(Enum):
    Logics = {'file_name': 'logics', 'heb': 'לוגיקה למדעי המחשב', 'folder': 'Logics', 'hw_search': 'לוגיקה', 'question_sym': r'\.(\d+)'}
    Algebra_b1 = {'file_name': 'algebra_b1', 'heb': 'אלגברה ב1', 'folder': 'Algebra b1', 'hw_search': 'אלגברה ב', 'question_sym': r'\.(\d+)'}
    Calculus_2a = {'file_name': 'calculus_2a', 'heb': 'חדו"א 2א', 'folder': 'Calculus 2a', 'hw_search': 'חדו"א', 'question_sym': r'\.(\d+)'}
    Computational_models = {'file_name': 'computational_models', 'heb': 'מודלים חישוביים', 'folder': 'Computational Models', 'hw_search': 'Computational', 'question_sym': r'(\d+)\.'}
    Computer_structure = {'file_name': 'computer_structure', 'heb': 'מבנה מחשבים', 'folder': 'Computer Structure', 'hw_search': 'מבנה מחשבים', 'question_sym': r'\.(\d+)'}
    Data_structures = {'file_name': 'data_structures', 'heb': 'מבני נתונים', 'folder': 'Data Structures', 'hw_search': 'מבני נתונים', 'question_sym': r'\.(\d+)'}
    Linear_2a = {'file_name': 'linear_2a', 'heb': 'אלגברה ליניארית 2א', 'folder': 'Linear 2a', 'hw_search': 'לינארית', 'question_sym': r'\.(\d+)'}
    Number_theory = {'file_name': 'number_theory', 'heb': 'תורת המספרים', 'folder': 'Number Theory', 'hw_search': 'תורת המספרים', 'question_sym': r'\.(\d+)'}


def rep(s, **kwargs):
    for key in kwargs:
        s = s.replace('{'+key+'}', str(kwargs[key]))
    return s


def hw_num(folder_path, create_file_path, sub):
    lst = os.listdir(folder_path)
    lst.sort(reverse=True)
    idx = 0
    while idx < len(lst) and lst[idx][:2] != 'hw':
        idx += 1
    num1 = int(lst[idx][2:lst[idx].index('_')])+1 if idx != len(lst) else 1
    num2 = 0
    if dups_in_create:
        lst2 = os.listdir(create_file_path)
        lst2 = sorted([f for f in lst2 if sub in f], reverse=True)
        idx2 = 0
        while idx2 < len(lst2) and lst2[idx2][:2] != 'hw':
            idx2 += 1
        num2 = int(lst2[idx2][2:lst2[idx2].index('_')]) + 1 if idx2 != len(lst2) else 1
    return max(num1, num2)


def create_folder(subject_path, create_file_path, sub):
    num = hw_num(subject_path, create_file_path, sub) if hw_number is None else hw_number
    folder_name = f'hw{num}_{subject.value["file_name"]}'
    if os.path.exists(os.path.join(subject_path, folder_name)):
        raise Exception('Folder already exists in saved files')
    create_path = os.path.join(create_folder_path, folder_name)
    if os.path.exists(create_path):
        raise Exception('Folder already exists in created files')
    os.mkdir(create_path)
    return create_path, folder_name, num


def generate_questions():
    q_text = ''
    for i in range(1, number_quest+1):
        q_text += rep(quest_text, q_num=i)
    return q_text


def get_subject(text):
    begin = '\n'.join(text.split('\n')[:get_lines])
    for sub in Subject:
        s = sub.value['hw_search']
        if any("\u0590" <= c <= "\u05EA" for c in s):
            s = ' '.join(s.split()[::-1])
        if s in begin:
            return sub
    return None


def count_questions(text, sub):
    def l_lis(arr):
        n = len(arr)
        lis = [[1, [arr[i]]] for i in range(n)]
        for i in range(1, n):
            for j in range(0, i):
                if arr[i] > arr[j] and lis[i][0] < lis[j][0] + 1:
                    lis[i][0] = lis[j][0] + 1
                    lis[i][1] = lis[j][1] + [arr[i]]
        max_lst = []
        for i in range(n):
            max_lst = lis[i][1] if lis[i][0] > len(max_lst) else max_lst
        return max_lst

    possibles = [int(r.group(1)) for r in re.finditer(f"[\\W\\D]{sub.value['question_sym']}[\\W\\D]", text)]
    questions = l_lis(possibles)
    for i in reversed(questions):
        if i < 15:
            return i
    return None


def main():
    new_path = os.path.join(get_path, subject.value['folder'])
    create_path, name, ex_num = create_folder(new_path, create_folder_path, subject.value['file_name'])
    questions = generate_questions()
    data = rep(default_file, subject=subject.value['heb'], ex_num=ex_num, questions=questions)
    with open(os.path.join(create_path, name+'.lyx'), 'w', encoding='UTF-8') as file:
        file.write(data)
    os.startfile(os.path.join(create_path, name+'.lyx'))


if __name__ == '__main__':
    default_file = r'''#LyX 2.3 created this file. For more info see http://www.lyx.org/
\lyxformat 544
\begin_document
\begin_header
\save_transient_properties true
\origin unavailable
\textclass article
\begin_preamble
\date{}
\relpenalty=10000
\binoppenalty=10000
\end_preamble
\use_default_options true
\maintain_unincluded_children false
\language hebrew
\language_package default
\inputencoding auto
\fontencoding global
\font_roman "default" "David"
\font_sans "default" "David"
\font_typewriter "default" "David"
\font_math "auto" "auto"
\font_default_family default
\use_non_tex_fonts true
\font_sc false
\font_osf false
\font_sf_scale 100 100
\font_tt_scale 100 100
\use_microtype false
\use_dash_ligatures true
\graphics default
\default_output_format default
\output_sync 0
\bibtex_command default
\index_command default
\float_placement H
\paperfontsize default
\spacing single
\use_hyperref false
\papersize default
\use_geometry true
\use_package amsmath 1
\use_package amssymb 1
\use_package cancel 1
\use_package esint 1
\use_package mathdots 1
\use_package mathtools 1
\use_package mhchem 1
\use_package stackrel 1
\use_package stmaryrd 1
\use_package undertilde 1
\cite_engine basic
\cite_engine_type default
\biblio_style plain
\use_bibtopic false
\use_indices false
\paperorientation portrait
\suppress_date false
\justification true
\use_refstyle 1
\use_minted 0
\index Index
\shortcut idx
\color #008000
\end_index
\leftmargin 3cm
\topmargin 3cm
\rightmargin 3cm
\bottommargin 3cm
\secnumdepth 3
\tocdepth 3
\paragraph_separation skip
\defskip medskip
\is_math_indent 0
\math_numbering_side default
\quotes_style english
\dynamic_quotes 0
\papercolumns 1
\papersides 1
\paperpagestyle default
\tracking_changes false
\output_changes false
\html_math_output 0
\html_css_as_file 0
\html_be_strict false
\end_header

\begin_body

\begin_layout Standard
\begin_inset CommandInset include
LatexCommand include
filename "C:/Users/roybo/Desktop/University/shortcuts/shortcuts.lyx"

\end_inset


\end_layout

\begin_layout Title
{subject} - תרגיל בית
\family roman
\series medium
\shape up
\size largest
\emph off
\bar no
\strikeout off
\xout off
\uuline off
\uwave off
\noun off
\color none
 
\family default
\series default
\shape default
\size default
\emph default
\numeric on
\bar default
\strikeout default
\xout default
\uuline default
\uwave default
\noun default
\color inherit
{ex_num}
\end_layout

\begin_layout Author
רועי בוגין -
\family roman
\series medium
\shape up
\size large
\emph off
\bar no
\strikeout off
\xout off
\uuline off
\uwave off
\noun off
\color none
 
\family default
\series default
\shape default
\size default
\emph default
\numeric on
\bar default
\strikeout default
\xout default
\uuline default
\uwave default
\noun default
\color inherit
209729524
\end_layout

{questions}

\end_body
\end_document
'''
    quest_text = r'''\begin_layout Section*

\bar under
שאלה
\family roman
\series bold
\shape up
\size larger
\emph off
\strikeout off
\xout off
\uuline off
\uwave off
\noun off
\color none
 
\family default
\series default
\shape default
\size default
\emph default
\numeric on
\strikeout default
\xout default
\uuline default
\uwave default
\noun default
\color inherit
{q_num}
\numeric off
:
\end_layout'''
    get_path = r'C:\Users\roybo\Desktop\University\semester 2'
    create_folder_path = r'C:\Users\roybo\OneDrive\University'
    dups_in_create = True
    subject = None
    hw_number = None
    number_quest = None
    get_lines = 3
    assignment_path = r"C:\Users\roybo\Desktop\temp\models.pdf"
    assignment_path = assignment_path if assignment_path is not None else sys.argv[1]
    assignment_text = parser.from_file(assignment_path)['content'].strip()
    # try:
    #     assignment_text = textract.process(assignment_path).decode('UTF-8')
    # except UnicodeDecodeError as e:
    #     print(parser.from_file(assignment_path))

    calculated_subject = get_subject(assignment_text)
    if subject is None:
        if calculated_subject is None:
            raise Exception("can't detect subject")
        else:
            subject = calculated_subject
    calculated_questions = count_questions(assignment_text, subject)
    if number_quest is None:
        if calculated_questions is None:
            raise Exception("can't detect question number")
        else:
            number_quest = calculated_questions
    main()
