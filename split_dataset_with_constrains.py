with open('rec_gt.txt',encoding='utf-8') as f:
    data = f.readlines()
    data = [line.strip() for line in data]
    data = [line.split('\t') for line in data]

import random
random.seed(2020)
# shuffle and split data into train eval and test

random.shuffle(data)
train_data = []
eval_data = []
test_data = []

train_size = 2000
eval_size = 300
test_size = len(data)-train_size-eval_size

train_chars = set()
eval_chars = set()
test_chars = set()

def append_line(line):
    _,gt = line
    for char in gt:
        if char not in test_chars:
            test_data.append(line)
            test_chars.update(gt)
            return
    for char in gt:
        if char not in eval_chars:
            eval_data.append(line)
            eval_chars.update(gt)
            return
    for char in gt:
        if char not in train_chars:
            train_data.append(line)
            train_chars.update(gt)
            return
        
    # if gt not in test_chars:
    #     test_data.append(line)
    #     test_chars.add(gt)
    #     return
    # if gt not in eval_chars:
    #     eval_data.append(line)
    #     eval_chars.add(gt)
    #     return
    # if gt not in train_chars:
    #     train_data.append(line)
    #     train_chars.add(gt)
    #     return

    train_distance = train_size - len(train_data)
    eval_distance = eval_size - len(eval_data)
    test_distance = test_size - len(test_data)
    if train_distance == max(train_distance,eval_distance,test_distance):
        train_data.append(line)
        train_chars.add(gt)
    elif test_distance == max(train_distance,eval_distance,test_distance):
        test_data.append(line)
        test_chars.add(gt)
    else:
        eval_data.append(line)
        eval_chars.add(gt)

new_data = []
new_data_dict = {}
def split_test_and_newData(line):
    _,gt = line
    for char in gt:
        if char not in test_chars:
            test_data.append(line)
            test_chars.update(gt)
            return
    new_data.append(line)
    for char in gt:
        if char in new_data_dict:
            new_data_dict[char].append(len(new_data)-1)
        else:
            new_data_dict[char] = [len(new_data)-1]
    

for line in data:
    split_test_and_newData(line)
    
data_dict = {}
chr_to_words = {}
words = []

class word:
    def __init__(self,line,gt):
        self.line = line
        self.word = gt

for line in new_data:
    _,gt = line
    wd = word(line,gt)
    words.append(wd)
    for char in set(gt):
        if char in data_dict:
            data_dict[char] += 1
        else:
            data_dict[char] = 1
        if char in chr_to_words:
            chr_to_words[char].append(wd)
        else:
            chr_to_words[char] = [wd]

chrs = [v for k,v in data_dict.items()]

def check_word():
    while [v for k,v in data_dict.items()].count(1) > 0:
        for k,v in data_dict.items():
            if v == 1:
                for wd in chr_to_words[k]:                   
                        test_data.append(wd.line)
                        test_chars.update(wd.word)
                        for char in set(wd.word):
                            data_dict[char] -= 1
                            chr_to_words[char].remove(wd)

check_word()

# import IPython; IPython.embed()

chrs = [k for k,v in data_dict.items()]
sorted_chrs = sorted(chrs,key=lambda x:data_dict[x])

for k in sorted_chrs:
    if data_dict[k] >= 2:
        eval_word = chr_to_words[k][0]
        eval_data.append(eval_word.line)
        eval_chars.update(eval_word.word)
        for char in set(eval_word.word):
            data_dict[char] -= 1
            chr_to_words[char].remove(eval_word)
        
        train_words = chr_to_words[k][1:]
        for wd in train_words:
            train_data.append(wd.line)
            train_chars.update(wd.word)
            for char in set(wd.word):
                data_dict[char] -= 1
                chr_to_words[char].remove(wd)
            
            # check_word()

# import IPython; IPython.embed()

# solve the unbalanced problem
for char in eval_chars-train_chars:
    for line in eval_data:
        _,gt = line
        if char in gt:
            train_data.append(line)
            train_chars.update(gt)
            break

# sequence = [v for k,v in data_dict.items()]
# print(sequence.count(1))
# import matplotlib.pyplot as plt
# plt.hist(sequence,bins=50,log=True)
# plt.savefig('hist.png')
# exit()

print('train_samples:',len(train_data))
print('eval_samples:',len(eval_data))
print('test_samples:',len(test_data))

print('train_labels_count:',len(train_chars))
print('eval_labels_count:',len(eval_chars))
print('test_labels_count:',len(test_chars))

# save the char set
with open('train_chr.txt','w',encoding='utf-8') as f:
    f.write(''.join(sorted(train_chars)))
with open('eval_chr.txt','w',encoding='utf-8') as f:
    f.write(''.join(sorted(eval_chars)))
with open('test_chr.txt','w',encoding='utf-8') as f:
    f.write(''.join(sorted(test_chars)))

print('eval_chars-train_chars:',eval_chars-train_chars)
print('test_chars-eval_chars:',test_chars-eval_chars)

# # save the char that test set has but train and eval set don't have
# with open('test_chr_only.txt','w',encoding='utf-8') as f:
#     f.write(''.join(sorted(test_chars-train_chars-eval_chars)))
    
# calculate the venn diagram
from matplotlib_venn import venn3
import matplotlib.pyplot as plt
plt.figure(figsize=(4,4))
venn3([train_chars,eval_chars,test_chars],('train','eval','test'))
plt.show()
plt.savefig('venn.png')

# write data to file
with open('train_gt.txt','w',encoding='utf-8') as f:
    for line in train_data:
        f.write('\t'.join(line)+'\n')
with open('eval_gt.txt','w',encoding='utf-8') as f:
    for line in eval_data:
        f.write('\t'.join(line)+'\n')
with open('test_gt.txt','w',encoding='utf-8') as f:
    for line in test_data:
        f.write('\t'.join(line)+'\n')

# copy images to train eval and test folder
import shutil
for line in train_data:
    shutil.copy(line[0], 'train')
for line in eval_data:
    shutil.copy(line[0], 'eval')
for line in test_data:
    shutil.copy(line[0], 'test')

# write data for paddleocr
with open('rec_gt_train.txt','w',encoding='utf-8') as f:
    for line in train_data:
        f.write(line[0].split('/')[-1]+'\t'+line[1]+'\n')

with open('rec_gt_eval.txt','w',encoding='utf-8') as f:
    for line in eval_data:
        f.write(line[0].split('/')[-1]+'\t'+line[1]+'\n')

with open('rec_gt_test.txt','w',encoding='utf-8') as f:
    for line in test_data:
        f.write(line[0].split('/')[-1]+'\t'+line[1]+'\n')