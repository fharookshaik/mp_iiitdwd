# Imports
import pywebio as web
import json
import os
import pandas as pd

# Dataset Paths
IMAGES_DIR = '/mnt/DATA/fharookshaik/Major Project/dataset/images/'
IMAGES_READ_DIR = '/mnt/DATA/fharookshaik/Major Project/dataset/ReadImages'
TRAIN_JSON = '/mnt/DATA/fharookshaik/Major Project/notebooks/train.json'
MODIFIED_TRAIN = '/mnt/DATA/fharookshaik/Major Project/notebooks/modified_train.xlsx'

LAST_KEY = 0

class Item:
    def __init__(self,OCR,image,hero,villain,victim,other) -> None:
        self.OCR = OCR
        self.image = image
        self.hero = hero
        self.villain = villain
        self.victim = victim
        self.other = other
    
    def print_info(self,idx=None):
        print('-'*20)
        if idx is not None:
            print('Index : ',idx)
        print('OCR : ',self.OCR)
        print('Image : ', self.image)
        print('Hero : ',self.hero)
        print('Villain : ',self.villain)
        print('Victim : ',self.victim)
        print('Other : ',self.other)

    def to_json(self):
        return {
            'OCR' : self.OCR,
            'image' : self.image,
            'hero' : self.hero,
            'villain' : self.villain,
            'victim' : self.victim,
            'other' : self.other 
        }

def render_info(item):
    with web.output.use_scope(name='actual',clear=True):
        web.output.put_markdown('# Actual Information'),
        web.output.put_table([
            ['Key','Value'],
            ['OCR',web.output.put_text(item.OCR)],
            ['Image',web.output.put_image(src=open(os.path.join(IMAGES_DIR,item.image),'rb').read(),title=item.image,width='500px',height='500px')],
            ['Hero',web.output.put_text(item.hero)],
            ['Villain',web.output.put_text(item.villain)],
            ['Victim',web.output.put_text(item.victim)],
            ['Other',web.output.put_text(item.other)]
        ])
        web.output.put_html('<hr>')
    
    with web.output.use_scope(name='final',clear=True):
        web.output.put_markdown('# Final Information')
        data = web.input.input_group(inputs=[
            web.input.textarea('OCR',value=item.OCR,name='OCR'),
            web.input.input('Image',value=item.image,readonly=True,name='image'),
            web.input.input('Hero',value=item.hero,name='hero'),
            web.input.input('Villain',value=item.villain,name='villain'),
            web.input.input('Victim',value=item.victim,name='victim'),
            web.input.input('Other',value=item.other,name='other')]
        )
    return Item(data['OCR'],data['image'],data['hero'],data['villain'],data['victim'],data['other'])


# Read JSON file
with open(TRAIN_JSON,'r') as f:
    data = json.load(f)

if not os.path.exists(MODIFIED_TRAIN):
    df = pd.DataFrame(columns=['OCR','image','hero','villain','victim','other'])
else:
    df = pd.read_excel(MODIFIED_TRAIN,engine='openpyxl')
    LAST_KEY = df.shape[0]
    print(f'Total entries found in db : {LAST_KEY}')

for key,val in data.items():
    if LAST_KEY <= int(key): 
        item = Item(OCR=val.get("OCR"),image=val.get("image"),hero=val.get("hero"),villain=val.get("villain"),victim=val.get('victim'),other=val.get("other"))
        out = render_info(item)

        df.loc[key] = out.to_json()
        df.to_excel(MODIFIED_TRAIN)
        web.output.toast(f'Added {key} to dataset',position='right')
        print(out.print_info(idx=key))
    else:
        print(f'{key} already found in db')
# for key,val in data.items():
#     actual_items.append(Item(val.get("OCR"),val.get("image"),val.get("hero"),val.get("villain"),val.get("other")))

# for idx,val in enumerate(actual_items):
#     final_items.append(render_info(val))
#     web.output.toast(f'{idx} Updated',position='right')
#     final_items[-1].print_info(idx)
    