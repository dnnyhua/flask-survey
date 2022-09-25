from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.debug = True # why does this not work???
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


temp_memory=[]


@app.route('/')
def home_page():
  """ This is the survey home page """
  return render_template('home.html', survey=survey)


@app.route('/start_survey', methods = ['POST'])
def start_survey():
  """ Starts the survey and returns the first question """
  return redirect("/questions/0")


@app.route('/questions/<int:question_num>')
def show_question(question_num):
  """ Show current question """

  if len(temp_memory) == len(survey.questions):
    """ If length of temp memory is as long as the number of survey questions
        then the user has completed the survey.
    """
    return render_template('survey_complete.html',temp_memory=temp_memory)  

  elif len(temp_memory) != question_num:
    return redirect(f"/questions/{len(temp_memory)}")

  else:
    cur_question = survey.questions[question_num]
    return render_template('questions.html',cur_question=cur_question, question_num = question_num+1)


@app.route('/answer', methods=['POST'])
def answer():
  # global counter
  # get answer from survey question
  # don't want to keep appending values if we already answered everything
  if len(temp_memory) != len(survey.questions):
    choice = request.form['answer']
    # add answer to temp memory 
    temp_memory.append(choice)

  if len(temp_memory) == len(survey.questions):
    return render_template('survey_complete.html', temp_memory=temp_memory)
  
  else:
    return redirect(f"/questions/{len(temp_memory)}")