import os
import shutil as sh
import json
import cv2 as cv

IMAGES_DIR = '/mnt/DATA/fharookshaik/Major Project/dataset/images/'
IMAGES_READ_DIR = '/mnt/DATA/fharookshaik/Major Project/dataset/ReadImages'
TRAIN_JSON = '/mnt/DATA/fharookshaik/Major Project/notebooks/train.json'

def show_img(impath):
    img = cv.imread(impath)
    img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    # print(img.shape)
    img = cv.resize(img,(700,500))
    cv.imshow(impath.split('/')[-1],img)
    cv.waitKey(0)
    cv.destroyAllWindows()

with open(TRAIN_JSON,'r') as f:
    data = json.load(f)

for idx in data.keys():
    impath = os.path.join(IMAGES_DIR,data.get(idx).get("image"))
    print(f"{idx} : {impath}")
    show_img(impath)
