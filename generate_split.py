import numpy as np
import random
import json
import os

np.random.seed(2020) # to ensure you always get the same train/test split

data_path = '/Users/jarroyo/OneDrive - California Institute of Technology/Courses/2022Spring/CS148/RedLights2011_Medium'
gts_path = './data/ground_truth'
split_path = './data'
preds_path = './preds'
os.makedirs(preds_path, exist_ok=True) # create directory if needed

split_test = False # set to True and run when annotations are available

train_frac = 0.85

# get sorted list of files:
file_names = sorted(os.listdir(data_path))

# remove any non-JPEG files:
file_names = [f for f in file_names if '.jpg' in f]

# split file names into train and test
file_names_train = []
file_names_test = []
train_indices = random.sample(range(len(file_names)), k=int(train_frac * len(file_names)))
train_indices = set(train_indices)
for i in range(len(file_names)):
    if i in train_indices:
        file_names_train.append(file_names[i])
    else:
        file_names_test.append(file_names[i])

assert (len(file_names_train) + len(file_names_test)) == len(file_names)
assert len(np.intersect1d(file_names_train,file_names_test)) == 0

np.save(os.path.join(split_path,'file_names_train.npy'),file_names_train)
np.save(os.path.join(split_path,'file_names_test.npy'),file_names_test)

if split_test:
    ann_filename = 'formatted_annotations_students_2021.json'
    with open(os.path.join(gts_path, ann_filename),'r') as f:
        gts = json.load(f)
    
    gts_train = {}
    for im_name in file_names_train:
        gts_train[im_name] = gts[im_name]

    gts_test = {}
    for im_name in file_names_test:
        gts_test[im_name] = gts[im_name]

    with open(os.path.join(gts_path, 'annotations_train.json'),'w') as f:
        json.dump(gts_train,f)

    with open(os.path.join(gts_path, 'annotations_test.json'),'w') as f:
        json.dump(gts_test,f)
