from flask import Flask, render_template, request
from inf_eng import SimpleQAExpertSystem

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
system = SimpleQAExpertSystem()

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Home page with 'Get Started' button

@app.route('/quiz', methods=['POST'])
def quiz():
    """Handle user input and start the quiz."""
    role = request.form['role']
    experience = request.form['experience']
    num_questions = int(request.form['num_questions'])
    
    # Initialize the expert system
    engine = SimpleQAExpertSystem(role, experience, num_questions)
    engine.reset()
    engine.declare(Fact(start=True))
    engine.run()

    # Pass questions to the template
    return render_template('quiz.html', questions=engine.questions, role=role, experience=experience)

'''@app.route('/select', methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        job_role = request.form['job_role']
        experience = request.form['experience']
        num_questions = int(request.form['num_questions'])
        time_bound = 'time_bound' in request.form


        # Get advice from the inference engine
        role_tip, experience_tip = system.process_inputs(job_role, experience, num_questions, time_bound)
        return render_template('result.html', job_role=job_role, experience=experience, role_tip=role_tip, experience_tip=experience_tip)
    
    return render_template('form.html')'''



# Route for the form selection page
@app.route('/form')
def form_page():
    return render_template('form.html')  # Form page for role and experience selection

@app.route('/result', methods=['POST'])
def results():
    """Show quiz results and provide domain-specific tips."""
    user_answers = request.form.getlist('answer')
    correct_answers = request.form.getlist('correct_answer')
    role = request.form['role']  # Retrieve the role (job domain)
    experience = request.form['experience']

    def normalize_answer(text):
        # Remove punctuation, convert to lowercase, and strip spaces
        return re.sub(r'[^\w\s]', '', text.lower().strip())

    # Evaluate answers
    feedback = []
    for user_answer, correct_answer in zip(user_answers, correct_answers):
        # Normalize both answers before comparing
        if normalize_answer(user_answer) == normalize_answer(correct_answer):
            feedback.append('Correct')
        else:
            feedback.append(f'You missed some key points. Correct answer: {correct_answer}')


    
    # Get domain-specific tip
    role_tip = ROLE_TIPS.get(role, "Keep learning and practicing in your domain!")
    experience_tip = EXPERIENCE_TIPS.get(experience, "Keep learning and practicing in your domain!")

    return render_template('result.html', feedback=feedback, role_tip=role_tip, role=role, experience_tip=experience_tip,experience=experience)
# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    job_role = request.form.get('job_role')
    experience_level = request.form.get('experience_level')
    num_questions = int(request.form.get('num_questions'))
    time_bound = request.form.get('time bound') == 'yes'
    
    engine = SimpleQAExpertSystem()

    # Get advice from the inference engine
    role_tip, experience_tip = engine.get_advice(job_role, experience_level, num_questions, time_bound)

    # Render the result page with the advice
    return render_template('result.html', role_tip=role_tip, experience_tip=experience_tip)

if __name__ == '__main__':
    app.run(debug=True)
