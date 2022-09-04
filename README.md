
# Form Linking

Form Linking uses SOTA Layoutlm (Dual modality) Models to generate automatic Labelling/Annotations for Key value pairs on different types of documents.

## Usage

```
python form_linking.py -i {image_file}
```

## Examples

![Alt text](https://github.com/Deep-Learner-msp/Form_Linking/blob/main/examples/key_value_doc.jpeg "Title")




### Output
```json

{'DATE;': '2-23-2019',
 'DATE': '2-23-2019',
 'TIME:': '17:30:22',
 'INVOICE #:': '7124',
 'PHONE:': '123-456-7890',
 'EMAIL:': 'SALES@XYZ.COM',
 'WEB:': 'WWW.XYZ.COM',
 'AMOUNT DUE:': '$882 USD',
 'PAYMENT DUE BY:': '| 2-28-2019'}
 ```
