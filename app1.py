from flask import Flask, render_template, request
from inf_eng import SimpleQAExpertSystem
from experta import *
import pandas as pd

app = Flask(__name__)
system = SimpleQAExpertSystem()
df = pd.read_csv(r'data/combined_file(3).csv', encoding='ISO-8859-1')

# Define available job roles (domains)
JOB_ROLES = [
    'Artificial Intelligence', 'Machine Learning', 'Cybersecurity', 'Data Engineering', 'DSA', 'Database and SQL', 'Web Development', 'Software Testing'
]

# Tips based on role (domain)
ROLE_TIPS = {
    'Artificial Intelligence': "Focus on understanding the math behind machine learning models, and stay updated with recent research in AI.",
    'Machine Learning': "Brush up on your algorithms and practical applications like model deployment and optimization.",
    'Cybersecurity': "Stay informed about the latest vulnerabilities and focus on learning cryptographic methods.",
    'Data Engineering': "Learn about the latest tools for data pipelines and cloud platforms like AWS and Azure.",
    'DSA': "Practice data structures and algorithms regularly, and focus on improving problem-solving skills.",
    'Database and SQL': "When dealing with complicated queries, break them down into smaller parts, test them, and then combine them.",
    'Web Development': "Understand the purpose of your website and the needs of your users before writing any code. This will help you create a more focused and efficient web application.",
    'Software Testing': " Focus on critical areas of the application first, like core functionality, security features, and high-risk areas. Ensure high-priority and high-impact features are tested thoroughly."
}

EXPERIENCE_TIPS = {
    'Entry': "Focus on building a solid foundation by learning core concepts and practicing frequently.",
    'Mid': "Work on optimizing your existing knowledge and learn new tools to improve productivity.",
    'Senior': "Focus on leadership skills, mentoring others, and handling complex projects."
}

class SimpleQAExpertSystem(KnowledgeEngine):
    def __init__(self, role, experience, num_questions):
        super().__init__()
        self.role = role
        self.experience = experience
        self.num_questions = num_questions
        self.questions = []

    @Rule(Fact(start=True))
    def start_quiz(self):
        # Filter questions based on role
        filtered_data = df[df['Category'].str.lower() == self.role.lower()].dropna(subset=['Question'])
        questions_to_ask = filtered_data.head(self.num_questions)
        self.questions = questions_to_ask.to_dict('records')


# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')  # Home page with 'Get Started' button


@app.route('/quiz1', methods=['POST'])
def quiz1():
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
    return render_template('quiz1.html', questions=engine.questions, role=role, experience=experience)


# Route for the form selection page
@app.route('/index1')
def index1():
    return render_template('index1.html')  # Form page for role and experience selection


def timed_input(self, prompt, timeout=10):
        """Time-limited input function."""
        print(f"You have {timeout} seconds to answer.")
        start_time = time.time()
        user_answer = input(prompt)
        end_time = time.time()
        
        if end_time - start_time > timeout:
            return None 
        return user_answer.strip().lower()

@app.route('/results', methods=['POST'])
def results():
    """Show quiz results and provide domain-specific tips."""
    user_answers = request.form.getlist('answer')  # List of user's answers
    correct_answers = request.form.getlist('correct_answer')  # List of correct answers
    role = request.form['role']  # Retrieve the role (job domain)
    experience = request.form['experience']

    # Initialize variables to keep track of correct responses and detailed feedback
    total_questions = len(correct_answers)
    correct_count = 0
    feedback = []  # To store feedback on each question

    # Evaluate answers question by question
    for idx, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answers)):
        correct_keywords = set(correct_answer.split())  # Split the correct answer into keywords
        user_keywords = set(user_answer.split())  # Split the user's answer into keywords
        matching_keywords = correct_keywords.intersection(user_keywords)

        # Set a threshold for matching keywords (e.g., 30%)
        threshold = 0.3
        if len(matching_keywords) / len(correct_keywords) >= threshold:
            correct_count += 1  # Increment if the answer is considered correct
            feedback.append(f"Question {idx + 1}: Good job! You mentioned key points: {', '.join(matching_keywords)}.")
        else:
            feedback.append(f"Question {idx + 1}: You missed some key points. Correct answer: {correct_answer}.")

    # Calculate the score
    score_percentage = (correct_count / total_questions) * 100

    # Get role and experience tips
    role_tip = ROLE_TIPS.get(role, "No specific tips for this role.")
    experience_tip = EXPERIENCE_TIPS.get(experience, "No specific tips for this experience level.")


    # Pass the feedback and tips to the results template
    return render_template('results.html', score=score_percentage, total_questions=total_questions, feedback=feedback, role_tip=role_tip, experience_tip=experience_tip)


if __name__ == '__main__':
    app.run(debug=True)
