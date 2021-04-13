# BERT-QuestionAns-API
BERT Question Answering API uses the Google's BERT technique for Question Answering, In this repo we are using pretrained model of distilbert.

### Prerequisites 
Python3 and NodeJS

### How to Run ?
Run `start.py` using Python3 on your local machine. Before running, make sure you update `context.txt` with the information you want the API to use for answering the questions.

### How to Use the API ?
Send POST Request to https://localhost:5000 with "question" field as Data.

#### NOTE : IN THIS REPO YOU CAN SEE THERE ARE 2 API's, You can use just the Python Flask API really. I've put NodeJS API since this repo is just a part of another PROJECT and I've only posted the required files.
