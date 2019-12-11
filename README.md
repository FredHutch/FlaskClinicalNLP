# FlaskBlobNLP
An application for preprocessing clinical narrative text, including sectioning and Named Entity Recogition using AWS's Comprehend Medical

Further details about [Sectioning](https://github.com/FredHutch/SectionerEx) and [NER](https://github.com/FredHutch/HDCMedLPInterface) can be found in their respective repositories

## test strings

> curl -i -H "Content-Type: application/json" -X POST -d "{"""extract_text""":"""cerealx 84 mg daily"""}" http://localhost:5000/preprocess/
