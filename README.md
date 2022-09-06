
# Form Linking

Form Linking uses SOTA Layoutlm (Dual modality) Models to generate automatic Labelling/Annotations for Key value pairs on different types of documents.

## Installation of tesseract

### **Linux**
```
sudo apt install tesseract-ocr -y
```
### **MacOS**
```
brew install tesseract
```
### **Windows**
```
Download [tesseract](https://digi.bib.uni-mannheim.de/tesseract/) and add into the System Environment Variables
```
## Usage

```
1.pip install -r requirements.txt
2.python form_linking.py -i {image_file}
```

## Examples

#### Original_reciept                                                                                         
![Alt text](https://github.com/Deep-Learner-msp/Form_Linking/blob/main/examples/key_value_doc.jpeg "reciept") 
#### KEY_VALUE_Classification 
![Alt text](https://github.com/Deep-Learner-msp/Form_Linking/blob/main/results/Funsd_results/key_value_image_annotated.jpeg "funsd_key_value_classification")
#### Value_Mapping with Key
![Alt text](https://github.com/Deep-Learner-msp/Form_Linking/blob/main/results/Post_Process_results/key_value_doc_annotated.png "labelled values with keys")




### Output
```

{'DATE;': '2-23-2019',
 'DATE': '2-23-2019',
 'TIME:': '17:30:22',
 'INVOICE #:': '7124',
 'PHONE:': '123-456-7890',
 'EMAIL:': 'SALES@XYZ.COM',
 'WEB:': 'WWW.XYZ.COM',
 'AMOUNT DUE:': '$882 USD',
 'PAYMENT DUE BY:': '2-28-2019'}
 ```
