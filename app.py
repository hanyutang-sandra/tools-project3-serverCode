from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
import psycopg2
import io
import csv
import os
import shutil
import pandas as pd


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return """
            <html>
                <body>
                    <h1>Upload files</h1>

                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <label for = "questions"> Questions </label>
                        <input type="file" name="questions" />
                        
                        <label for = "answers"> Answers </label>
                        <input type="file" name="answers" />
                        
                        <input type="submit" />
                    </form>
                </body>
            </html>
        """


from helpers import *
from pre_process import *
@app.route('/upload', methods=['POST'])
def handleUpload():
    name = request.form.get('name')
    questions = request.files['questions']
    answers = request.files['answers']

    try:
        questions = pd.read_csv(questions)
        questions_file, question_id = handlequestions(name, questions)

        answers = pd.read_csv(answers)
        handleanswers(answers)
        answers_files = separatetable(name, questions, answers, question_id)
    except:
        data = {"error": "File parsing failed"}
        return jsonify(data)

    shutil.rmtree('./files')
    os.mkdir('./files')
    os.mkdir('./files/'+ str(name))
    questions_file.to_csv('./files/' + str(name) + '/' + str(name) + '_questions.csv', index=False)

    for i in question_id:
        answers_files[i].to_csv('./files/' + str(name) + '/' + str(name) + '_q' + str(i) + 'answers.csv', index=False)

    data = {
        "name": name,
        "start": question_id[0]
    }
    return jsonify(data)


from test import *
@app.route('/info', methods=['GET'])
def handleInfo():
    dir = os.path.dirname('./files/')

    try:
        project_name = os.listdir(dir)[0]

    except:
        project_name = 'Nothing here yet. Please upload a project first.'
        project_info = {
            "name": project_name
        }
        return jsonify(project_info)

    question_file_name = str(project_name) + '_questions.csv'
    question_file = pd.read_csv(os.path.join('./files/' + str(project_name) + '/', question_file_name))
    question_id = question_file['Question_id'].tolist()

    project_info = {
        'name': project_name,
        "start": question_id[0]
    }
    return jsonify(project_info)


@app.route('/gettest', methods=['GET', 'POST'])
def generateTest():

    name = request.form.get('name')
    id = request.form.get('id')
    type= request.form.get('type')


    if type == 'MC':
        if checkAvailability(name, id):
            question, answer, number = generateMC(name, int(id))
        else:
            type = 'SA'
            question, answer, number = generateSA(name, int(id))
    else:
        question, answer, number = generateSA(name, int(id))

    testid = getTestId(name, id)
    data = {
        'name': name,
        'id': str(id),
        'testid': testid,
        'number': str(number),
        'question': question,
        'type': type,
        'answer': answer
    }


    return jsonify(data)


from feedback import *
@app.route('/getfeedback', methods=['GET', 'POST'])
def generateFeedback():
    dir = os.path.dirname('./files/')
    name = os.listdir(dir)[0]

    id = str(request.form.get('id'))
    number = request.form.get('number')
    type = request.form.get('type')

    choice = []
    choice.append(request.form.get('choice_0'))
    if type == 'SA':
        try:
            choice.append(request.form.get('choice_1'))
        except:
            pass
        try:
            choice.append(request.form.get('choice_2'))
        except:
            pass
        try:
            choice.append(request.form.get('choice_3'))
        except:
            pass

    choices = []
    choices.append(request.form.get('choices_0'))
    choices.append(request.form.get('choices_1'))
    choices.append(request.form.get('choices_2'))
    choices.append(request.form.get('choices_3'))

    result = rightorwrong(id, choice, name)

    if result:
        feedback = generatecorrect(id, choice, name)
    else:
        feedback = generatewrong(id, choice, name)

    generalright, generalwrong = getgeneralfeedback(id, choices, name)

    testid = getTestId(name, id)

    data = {
        'name': name,
        'id': str(id),
        'testid': str(testid),
        'number': str(number),
        'type': type,
        'result': str(result),
        'feedback': feedback,
        'generalright': generalright,
        'generalwrong': generalwrong
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run()