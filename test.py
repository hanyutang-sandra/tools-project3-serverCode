from flask import jsonify
import pandas as pd
import random
import os

def checkAvailability(name, id):
    answer_file_name = str(name) + '_q' + str(id) + 'answers.csv'
    answer_file = pd.read_csv(os.path.join('./files/' + str(name) + '/', answer_file_name))
    wrong_answer = answer_file.loc[answer_file['Correct'] == 0].Answer_text.tolist()
    correct_answer = answer_file.loc[answer_file['Correct'] == 1].Answer_text.tolist()

    if len(correct_answer) >= 1 and len(wrong_answer) >=3:
        return True
    else:
        return False


def generateMC(name, id):
    question_file_name = str(name) +'_questions.csv'
    answer_file_name = str(name) + '_q' + str(id) + 'answers.csv'

    question_file = pd.read_csv(os.path.join('./files/' + str(name) + '/', question_file_name))
    answer_file = pd.read_csv(os.path.join('./files/' + str(name) + '/', answer_file_name))

    question = question_file.loc[question_file['Question_id'] == id].Question_text.tolist()
    number = len(question_file)

    correct_answer = random.choice(answer_file.loc[answer_file['Correct'] == 1].Answer_text.tolist())
    answer = random.sample(answer_file.loc[answer_file['Correct'] == 0].Answer_text.tolist(), 3)
    answer.append(correct_answer)
    random.shuffle(answer)

    return question, answer, number


def generateSA(name, id):
    question_file_name = str(name) + '_questions.csv'
    answer_file_name = str(name) + '_q' + str(id) + 'answers.csv'

    question_file = pd.read_csv(os.path.join('./files/' + str(name) + '/', question_file_name))
    number = len(question_file)
    answer_file = pd.read_csv(os.path.join('./files/' + str(name) + '/', answer_file_name))

    question = question_file.loc[question_file['Question_id'] == id].Question_text.tolist()
    correct_answer = answer_file.loc[answer_file['Correct'] == 1].Answer_text.tolist()
    wrong_answer = answer_file.loc[answer_file['Correct'] == 0].Answer_text.tolist()

    if len(wrong_answer) >= 3:
        r = random.randint(1,4)
    else:
        r = random.randint(4-len(wrong_answer), 4)

    correct_answer_list = random.sample(correct_answer, r)
    wrong_answer_list = random.sample(answer_file.loc[answer_file['Correct'] == 0].Answer_text.tolist(), 4-r)
    answer = correct_answer_list + wrong_answer_list

    random.shuffle(answer)

    return question, answer, number


def getTestId(name, id):
    question_file_name = str(name) + '_questions.csv'
    question_file = pd.read_csv(os.path.join('./files/' + str(name) + '/', question_file_name))
    question_id = question_file['Question_id'].tolist()
    print(question_id)
    testid = int(question_id.index(int(id))) + 1
    return testid
