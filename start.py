from transformers import TFAutoModelForQuestionAnswering, AutoTokenizer
import tensorflow as tf
import numpy as np
import os
import sys
from flask import Flask, request, jsonify, Response

from sec import generate_token

SEC_TOKEN = ''

app = Flask(__name__)

@app.route('/chat',methods=['GET'])
def chat():
	if (request.args.get("sec_token") != SEC_TOKEN):
		return Response(status=401)
	response = jsonify(response=answer(request.args.get("question")))
	response.headers.add('Access-Control-Allow-Origin','*')
	return response

context_ids = []
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')

def construct_answer(tokens):
    for idx, curr_token in enumerate(tokens):
        if idx == 0:
            out_string = curr_token
        elif idx > 0:
            if curr_token[0] == '#':
                curr_token = curr_token.replace("##", "")
            else:
                curr_token = " " + curr_token
            out_string += curr_token
    out_string = out_string.strip()
    return out_string

def get_ans(decoded_ids, answer_start, answer_stop):
    start_pos = -1
    stop_pos = -1
    sum_max = -np.inf
    for curr_start in range(len(answer_start)):
        for curr_stop in range(curr_start, len(answer_stop)):
            if answer_start[curr_start] + answer_stop[curr_stop] > sum_max:
                sum_max = answer_start[curr_start] + answer_stop[curr_stop]
                start_pos = curr_start
                stop_pos = curr_stop
    answer = construct_answer(decoded_ids[start_pos:stop_pos + 1])

    return answer

def answer(question):
	question_ids = tokenizer.encode(question)
	question_context_ids = question_ids + context_ids
	segment_ids = [0] * len(question_ids) + [1] * len(context_ids)
	bert_input_data = [question_context_ids,segment_ids]
	output = bert_model.predict(bert_input_data)
	decoded_ids = tokenizer.convert_ids_to_tokens(question_context_ids)
	answer = get_ans(decoded_ids,output[0][0],output[1][0])
	return answer

def get_context():
	if os.path.isfile('context.txt'):
		context_file = open("context.txt","r")
		return context_file.read()
	print("\n\nError : context.txt File not found. Please Create 'context.txt' file with Context Information\n\n")
	input("Press any key to Continue...")
	exit(0)

if __name__ == '__main__':
	print("Initializing ...")
	bert_model = TFAutoModelForQuestionAnswering.from_pretrained('distilbert-base-cased-distilled-squad')
	context = get_context()
	context_ids = tokenizer.encode(context)
	context_ids.pop(0)
	SEC_TOKEN = generate_token()
	os.system('start cmd.exe /k node app.js ' + SEC_TOKEN)
	app.run(host='0.0.0.0',port=5001)