# FlasClinicalNLP
An application for preprocessing clinical narrative text, including sectioning and Named Entity Recogition using AWS's Comprehend Medical

Further details about [Sectioning](https://github.com/FredHutch/SectionerEx) and [NER](https://github.com/FredHutch/ComprehendMedicalInterface) can be found in their respective repositories

## test strings

> curl -i -H "Content-Type: application/json" -X POST -d "{"""extract_text""":"""Mr. Doe was diagnosed with Stage III adenocarcinoma of the left lung on 3/14/2018"""}" http://localhost:5000/preprocess/
