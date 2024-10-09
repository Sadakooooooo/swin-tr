# read data from file
with open('train_gt.txt', 'r', encoding='utf-8') as f:
    train_data = [line.strip().split('\t') for line in f.readlines()]
with open('eval_gt.txt', 'r', encoding='utf-8') as f:
    eval_data = [line.strip().split('\t') for line in f.readlines()]
with open('test_gt.txt', 'r', encoding='utf-8') as f:
    test_data = [line.strip().split('\t') for line in f.readlines()]

# copy images to train eval and test folder
import shutil
for line in train_data:
    shutil.copy(line[0], 'train')
for line in eval_data:
    shutil.copy(line[0], 'eval')
for line in test_data:
    shutil.copy(line[0], 'test')

with open('rec_gt_train.txt','w',encoding='utf-8') as f:
    for line in train_data:
        f.write(line[0].split('/')[-1]+'\t'+line[1]+'\n')

with open('rec_gt_eval.txt','w',encoding='utf-8') as f:
    for line in eval_data:
        f.write(line[0].split('/')[-1]+'\t'+line[1]+'\n')

with open('rec_gt_test.txt','w',encoding='utf-8') as f:
    for line in test_data:
        f.write(line[0].split('/')[-1]+'\t'+line[1]+'\n')