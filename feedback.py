import pandas as pd
import os

def rightorwrong(id, choice, name):
    answer_file_name = str(name) + '_q' + str(id) + 'answers.csv'
    answer_file = pd.read_csv(os.path.join('./files/' + str(name) + '/', answer_file_name))
    correct_answer = answer_file.loc[answer_file['Correct'] == 1].Answer_text.tolist()


    for i in choice:
        if i not in correct_answer:
            print(i)
            return False

    return True


def generatecorrect(id, choice, name):
    answer_file_name = str(name) + '_q' + str(id) + 'answers.csv'
    answer_file = pd.read_csv(os.path.join('./files/' + str(name) + '/', answer_file_name))
    correct_answer = answer_file.loc[answer_file['Correct'] == 1].Answer_text.tolist()

    feedback = finddifferent(choice[0], correct_answer)

    return feedback


def generatewrong(id, choice, name):
    answer_file_name = str(name) + '_q' + str(id) + 'answers.csv'
    answer_file = pd.read_csv(os.path.join('./files/' + str(name) + '/', answer_file_name))
    correct_answer = answer_file.loc[answer_file['Correct'] == 1].Answer_text.tolist()

    feedback = findsimiliar(choice[0], correct_answer)

    return feedback


def findsimiliar(choice, correct_answer):
    words = choice.split()
    counts = [0] * len(correct_answer)
    rate = []

    for i in range(len(words)):
        for j in range(len(correct_answer)):
            if words[i] in correct_answer[j]:
                counts[j] += 1

    for i in range(len(counts)):
        rate.append(counts[i]/len(correct_answer[i]))

    similiar = rate.index(max(rate))
    feedback = correct_answer[similiar]

    return feedback


def finddifferent(choice, correct_answer):
    words = choice.split()
    counts = [0] * len(correct_answer)
    rate = []

    for i in range(len(words)):
        for j in range(len(correct_answer)):
            if words[i] in correct_answer[j]:
                counts[j] += 1

    for i in range(len(counts)):
        rate.append(counts[i] / len(correct_answer[i]))

    different = rate.index(min(rate))
    feedback = correct_answer[different]

    return feedback


def getgeneralfeedback(id, choices, name):
    answer_file_name = str(name) + '_q' + str(id) + 'answers.csv'
    answer_file = pd.read_csv(os.path.join('./files/' + str(name) + '/', answer_file_name))
    correct_answer = answer_file.loc[answer_file['Correct'] == 1].Answer_text.tolist()

    generalright = []
    generalwrong = []

    for i in range(len(choices)):
        if choices[i] in correct_answer:
            generalright.append(i)
        else:
            generalwrong.append(i)

    return generalright, generalwrong