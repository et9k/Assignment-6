import numpy as np
import math
import pandas as pd
import openpyxl

pwm = np.loadtxt("rbpj_pwm.txt")
background_pwm = [0.28, 0.22, 0.22, 0.28]

sequence = "TCTTCCTTTATCCTCATAACCACAAGGCAAAACTCAACAGGATGTGGTTTTTCCGGTTGCTTTCTACTCCTGTAAAGGCCCACTGCTTCCATTCAAACACAAGCAATGGGGCCCTGATAAACACCAGCATCAAGAATAGGCAGATGTTCTGTGGAAATATTCTGTAACTTTCCCACGAAAGTGCAAGAATATCTGAGATGCACGAAGAAAACATTTTGCCTCCATGGCTGACTGATTTAGTTGGGCATTTAGGTGGCCTTGGGTTAAAAGAAAATAGACTGAGAAAAAAGAATATGCTGT"

#make function to calculate a window's score
def calc_score(letters):
    x=0
    n=0
    sub_scores = []
    while x<=7:
        if letters[x]=="A":
            val = pwm[n,0]
        elif letters[x]=="C":
            val = pwm[n,1]
        elif letters[x]=="G":
            val = pwm[n,2]
        else:
            val = pwm[n,3]
        sub_scores.append(val)
        x=x+1
        n=n+1
    score=np.prod(sub_scores[0:8])
    return score

#make function to calculate a window's background score
def calc_background_score(letters):
    x=0
    val=0
    background_sub_scores = []
    while x <= 7:
        if letters[x]=="A":
            val = background_pwm[0]
        elif letters[x]=="C":
            val = background_pwm[1]
        elif letters[x]=="G":
            val = background_pwm[2]
        else:
            val = background_pwm[3]
        background_sub_scores.append(val)
        x=x+1
    background_score=np.prod(background_sub_scores[0:8])
    return background_score

#define function for making letter list
def make_letter_list(string):
    letters=[]
    for letter in string:
        letters.append(letter)
    make_letter_list.letters = letters

#make function to find a window's reverse complement
def find_compl(letters):
    x=0
    rc_letters=[]
    while x<=7:
        if make_letter_list.letters[x]=="A":
            rc_letters.append("T")
        elif make_letter_list.letters[x]=="C":
            rc_letters.append("G")
        elif make_letter_list.letters[x]=="G":
            rc_letters.append("C")
        else:
            rc_letters.append("A") 
        x=x+1
    find_compl.rc_letters= rc_letters

#initialize variables and create nested dictionary
n=8
m=0
i=len(sequence)-7
dict={'window':{}, 'score':{}, 'background_score':{}, 'total_score':{},
      'rc_window': {}, 'rc_score': {}, 'rc_background_score':{}, 'rc_total_score':{}}
list1=[]
list2=[]
list3=[]
list4=[]

#fill in dictionary w/ 8-character window sequences & scores
while i > 0:
    dict['window']= (sequence[m:n])
    dict['rc_window']=dict['window'][::-1]
    background_score=0
    rc_background_score=0
    make_letter_list(dict['window'])
    score=calc_score(make_letter_list.letters)
    background_score=calc_background_score(make_letter_list.letters)
    dict['score'] = {score}
    dict['background_score']= {background_score}
    dict['total_score']=math.log2(score/background_score)
    make_letter_list(dict['rc_window'])
    find_compl(make_letter_list.letters)
    rc_score=calc_score(find_compl.rc_letters)
    rc_background_score=calc_background_score(find_compl.rc_letters)
    dict['rc_score'] = {rc_score}
    dict['rc_background_score'] = {rc_background_score}
    dict['rc_total_score'] = math.log2(rc_score/rc_background_score)
    i=i-1
    m=m+1
    n=n+1
    list1.append(dict['total_score'])
    list2.append(dict['window'])
    list3.append(dict['rc_total_score'])
    dict['rc_window']=''.join(find_compl.rc_letters)
    list4.append(dict['rc_window'])

#Normal list
combinedList = [[list1[x], list2[x]] for x in range(len(list2))]
print(combinedList)
keymax=max(combinedList)
print(keymax)

#Reverse complement list
combinedList2 = [[list3[x], list4[x]] for x in range(len(list4))]
print(combinedList2)
keymax2=max(combinedList2)
print(keymax2)

df = pd.DataFrame()  
df['score'] = list1[0::1] 
df['sequence'] = list2[0::1] 
df.to_excel('seq21.xlsx', index = False)

df = pd.DataFrame()  
df['score'] = list3[0::1] 
df['sequence'] = list4[0::1] 
df.to_excel('seq22.xlsx', index = False)