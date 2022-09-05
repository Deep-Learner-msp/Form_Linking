import os
print("Installing tesseract on machine")
os.system('apt-get install tesseract-ocr -y')
print("tesseract should be installed")

import time
from transformers import LayoutLMv2Processor, LayoutLMv2ForTokenClassification,LayoutLMv2FeatureExtractor
from datasets import load_dataset
from PIL import Image, ImageDraw, ImageFont
import argparse

dataset = load_dataset("nielsr/funsd", split="test")

# define id2label, label2color
labels = dataset.features['ner_tags'].feature.names
id2label = {v: k for v, k in enumerate(labels)}
label2color = {'question':'blue', 'answer':'green', 'header':'orange', 'other':'violet'}



processor = LayoutLMv2Processor.from_pretrained("microsoft/layoutlmv2-base-uncased", revision="no_ocr")
model = LayoutLMv2ForTokenClassification.from_pretrained("nielsr/layoutlmv2-finetuned-funsd")
feature_extractor = LayoutLMv2FeatureExtractor()

def iob_to_label(label):
    label = label[2:]
    if not label:
      return 'other'
    return label

def unnormalize_box(bbox, width, height):
     return [
         width * (bbox[0] / 1000),
         height * (bbox[1] / 1000),
         width * (bbox[2] / 1000),
         height * (bbox[3] / 1000),
     ]

import json
def normalize_box(box, width, height):
    return [
        int(1000 * (box[0] / width)),
        int(1000 * (box[1] / height)),
        int(1000 * (box[2] / width)),
        int(1000 * (box[3] / height)),
    ]

def parsing(true_predictions,token_boxes,bbdict):  
  cluster_master=[]
  cluster=[]
  picked=[]
  prev=''

  for prediction,tbox in zip(true_predictions,token_boxes):
    x,y=tbox[:2]
    if tbox not in picked:
      picked.append(tbox)
    else:
      continue
    try:

      word=bbdict[str(tbox)]
      gap=False
      if x-prevx > 150 or y-prevy > 20 :
        gap=True

      if prediction in ['B-QUESTION','I-QUESTION','I-HEADER','B-HEADER']:
        if prev=='value':
          cluster_master.append((cluster,'value',x,y))
          cluster=[]
        elif gap:
          cluster_master.append((cluster,prev,x,y))
          cluster=[]

        cluster.append(word)
        prev='key'
      else:
        if prev=='key' :
          cluster_master.append((cluster,'key',x,y))
          cluster=[]
        elif gap:
          cluster_master.append((cluster,prev,x,y))
          cluster=[]
        cluster.append(word)
        prev='value'
      
      
    except:
      pass
    prevx=x
    prevy=y
    
  cluster_master.append((cluster,prev,x,y))
  # return cluster_master


  key_value=dict()
  for item in cluster_master:
    typ=item[1]
    text=' '.join(item[0])
    x,y=item[2:]
    
    if typ=='value' and prevtyp=='key':
      key_value[prevtext]=text


    prevtext=text
    prevtyp=typ
    prevx=x
    prevy=y

  return key_value,cluster_master



def main(image):

  image = image.convert("RGB")
  width, height = image.size
  features = feature_extractor(image, return_tensors="pt")
  words,boxes=features['words'][0],features['boxes'][0]

  bbdict=dict()
  for word,box in zip(words,boxes):
    bbdict[str(box)]=word

  start=time.time()
  encoding = processor(image, words, boxes=boxes, return_tensors="pt")
  outputs = model(**encoding)
  print(time.time()-start,'Sucessfully created the output file')
  # print('outputs',outputs)


  # get predictions
  predictions = outputs.logits.argmax(-1).squeeze().tolist()
  token_boxes = encoding.bbox.squeeze().tolist()
  # print('token_boxes',token_boxes)

  # only keep non-subword predictions
  true_predictions = [id2label[pred] for idx, pred in enumerate(predictions)]
  true_boxes = [unnormalize_box(box, width, height) for idx, box in enumerate(token_boxes)]


    # draw predictions over the image
  draw = ImageDraw.Draw(image)
  font = ImageFont.load_default()
  for prediction, box in zip(true_predictions, true_boxes):
      predicted_label = iob_to_label(prediction).lower()
      draw.rectangle(box, outline=label2color[predicted_label])
      draw.text((box[0]+10, box[1]-10), text=predicted_label, fill=label2color[predicted_label], font=font)
  output,cluster_master=parsing(true_predictions,token_boxes,bbdict)
  filename = str(image.filename.split('/')[-1].split('.')[0]) + '_annotated' + '.jpg'
  image.save(filename)
  return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, required=True, help='Input Image')
    args = parser.parse_args()
    im = Image.open(args.i)
    main(im)
