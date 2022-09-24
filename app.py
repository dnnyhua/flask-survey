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

  return redirect("/questions/0")

# this is the global counter
counter = 0

@app.route('/questions/<int:question_num>')
def show_question(question_num):
  """ Show current question """
  global counter, temp_memory

  if temp_memory is None:
    # trying to access question page too soon
    return redirect("/")

  if len(temp_memory) == len(survey.questions):
    """ If length of temp memory is as long as the number of survey questions
        then the user has completed the survey.
    """
    return render_template('survey_complete.html',temp_memory=temp_memory)  

  if len(temp_memory) != question_num:
    return redirect(f"/questions/{len(temp_memory)}")

  else:
    question = survey.questions[question_num]
    return render_template('questions.html',question=question, question_num = question_num+1)


@app.route('/answer', methods=['POST'])
def answer():
  
  global counter, temp_memory 

  # get answer from survey question
  # don't want to keep appending values if we already answered everything
  if len(temp_memory) != len(survey.questions):
    choice = request.form['answer']
    # add answer to temp memory 
    temp_memory.append(choice)

  

  if counter == len(survey.questions):
    return render_template('survey_complete.html', temp_memory=temp_memory)
  
  else:
    counter += 1
    return redirect(f"/questions/{counter}")