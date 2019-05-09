import pandas as pd

def handlequestions(name, questions):
    columns = questions.columns.tolist()
    drop = []
    for i in range(len(columns)):
        if 'id' not in columns[i]:
            if 'text' not in columns[i]:
                drop.append(columns[i])
    questions = questions.drop(drop, axis=1)
    question_id = questions['Question_id'].tolist()
    return questions, question_id


def handleanswers(answers):
    overall_score = []
    correct = []
    for index, data in answers.iterrows():
        overall_score.append((data.Quiz_score + data.Average_quizzes_score) / 2)
        if data.Student_score_on_question == 1:
            correct.append(1)
        elif data.Student_score_on_question == 0:
            correct.append(0)
        else:
            correct.append(0.5)

    answers['Overall_performance'] = overall_score
    answers['Correct'] = correct

    return answers


def finalclean(q):
    overall_average = q['Overall_performance'].mean()
    for index, data in q.iterrows():
        if data.Correct == 0.5:
            if data.Student_score_on_question >= 0.75:
                if data.Overall_performance >= overall_average:
                    q.at[index, 'Correct'] = 1
                else:
                    q.at[index, 'Correct'] = 0.5
            elif 0.5 <= data.Student_score_on_question < 0.75:
                if data.Overall_performance >= overall_average:
                    q.at[index, 'Correct'] = 0.5
                else:
                    q.at[index, 'Correct'] = 0
            else:
                q.at[index, 'Correct'] = 0

    return q


def separatetable(name, questions, answers, question_id):
    q = {}

    for i in question_id:
        q[i] = pd.DataFrame()
        q[i] = answers.loc[answers['Question_id'] == i]

        finalclean(q[i])

        q[i] = q[i][q[i].Correct != 0.5]

    return q
