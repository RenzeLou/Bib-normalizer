'''
capitalize the title in your .bib file
remove all url and doi
'''
import argparse
from multiprocessing.connection import wait

parser = argparse.ArgumentParser()

parser.add_argument('-i','--input',type=str,default="./anthology.bib")
parser.add_argument('-o','--output',type=str,default="./anthology_cap.bib")
parser.add_argument('-v','--verbose',action="store_true")
args = parser.parse_args()

no_cap = ["with","of","for","to","from","and","on","in","under","a","by","the"]  # preposition
# dele = ['url', 'doi', 'publisher', 'organization'] 
cus_remain = ['title','author', 'booktitle', 'journal', 'year', 'pages', 'volume', 'number'] # reserved attributes, can be customized
fix = ['@']
remain = cus_remain + fix
new_bib = ""

def upper_already_cap(token:str):
    new_token = ''
    for t in token:
        if t.isupper():
            new_token += '{' + t + '}'
        else:
            new_token += t

    return new_token

def upper_all_tokens(title:str):
    all_tokens = title.split(" ")
    new_tokens = []
    for i,tk in enumerate(all_tokens):
        if i == 0 or tk.lower() not in no_cap:  # or tk[0].isupper
            ## must capitalize
            tk = tk.replace("{","")
            tk = tk.replace("}","")
            new_tk = '{' + tk[0].upper() + '}' + upper_already_cap(tk[1:])
            new_tokens.append(new_tk)
        else:
            new_tokens.append(tk)
    
    return " ".join(new_tokens)

def in_line(strr,line):
    new_str = strr.lower()
    new_line = line.lower()
    return new_str in new_line

def find_index(line,substr):
    if substr in line:
        return line.index('=')
    else:
        return len(line)

with open(args.input,"r",encoding="utf-8") as f:
    ori_bib = f.readlines()
    
for line in ori_bib:
    new_line = None
    com_line = line[:find_index(line,'=')].strip()
    # print(com_line)
    if not any([in_line(t,com_line) for t in remain]) and line != '}\n' and line != '}':
        new_line = ""  ## remove
    elif in_line('title',com_line) and not in_line('booktitle',com_line):
        start = line.index('{')  ## the first position of '{'
        end = len(line) - line[::-1].index("}")  ## the last position of '}'
        title = line[start+1:end-1]
        left,right = line[:start+1],line[end-1:]
        new_title = upper_all_tokens(title)
        new_line = left + new_title + right
    else:
        new_line = line
    
    new_bib += '\n' + new_line if '@' in new_line else new_line

new_bib = '% Encoding: UTF-8\n' + new_bib[1:] # add UTF-Encoding

if not args.verbose:
    print(new_bib)

with open(args.output,"w",encoding="utf-8") as f:
    f.write(new_bib)

print("write capitalized bib file at",args.output)
