with open('rec_gt.txt',encoding='utf-8') as f:
    data = f.readlines()
    data = [line.strip() for line in data]
    data = [line.split('\t') for line in data]

import random
random.seed(2023)
# shuffle and split data into train eval and test

train_size = 2000
eval_size = 300
random.shuffle(data)
train_data = data[:train_size]
eval_data = data[train_size:train_size+eval_size]
test_data = data[train_size+eval_size:]


# calculate the char set
train_chars = set()
eval_chars = set()
test_chars = set()
for line in train_data:
    train_chars.update(line[1])
for line in eval_data:
    eval_chars.update(line[1])
for line in test_data:
    test_chars.update(line[1])

# save the char set
with open('train_chr.txt','w',encoding='utf-8') as f:
    f.write(''.join(train_chars))
with open('eval_chr.txt','w',encoding='utf-8') as f:
    f.write(''.join(eval_chars))
with open('test_chr.txt','w',encoding='utf-8') as f:
    f.write(''.join(test_chars))
    

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