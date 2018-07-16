# FlaskML
Proof of concept for running ML behind a flask app


## test strings

> curl -i -H "Content-Type: application/json" -X POST -d "{"""extract_text""":"""cerealx 84 mg daily"""}" http://localhost:5000/medlp/annotate/phi

> curl -i -H "Content-Type: application/json" -X POST -d "{"""extract_text""":"""cerealx 84 mg daily"""}" http://localhost:5000/preprocess/