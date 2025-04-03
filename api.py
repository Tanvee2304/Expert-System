from flask import Flask, request, jsonify, render_template
from experta import *
import pandas as pd

app = Flask(__name__)

# Load CSV data
df = pd.read_csv(r'data/combined_file(3).csv', encoding='ISO-8859-1')

# Static tips for different roles and experience levels
ROLE_TIPS = {
    'Artificial Intelligence': "Focus on understanding the math behind machine learning models, and always be curious about the latest research in the AI domain.",
    'Machine Learning': "Brush up on algorithms, and focus on practical applications such as model deployment and optimization techniques.",
    'Cybersecurity': "Focus on understanding cryptographic methods, and always stay updated with the latest security vulnerabilities and patches.",
    'Data Engineering': "Keep learning about new data pipeline tools, and ensure you understand cloud platforms like AWS and Azure.",
    'DSA': "Practice data structures and algorithms regularly, and focus on solving problems efficiently."
}

EXPERIENCE_TIPS = {
    'Entry': "Focus on building a solid foundation by practicing frequently and learning the basics thoroughly.",
    'Mid': "Work on improving your optimization skills, and focus on learning new tools to increase productivity.",
    'Senior': "Concentrate on improving leadership skills, managing complex projects, and mentoring others."
}

class SimpleQAExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.time_bound = False  # Time-bound mode flag

    @Rule(Fact(role=MATCH.role, experience=MATCH.experience, num_questions=MATCH.num_questions))
    def provide_questions(self, role, experience, num_questions):
        print(f"Expert System triggered for role: {role}, experience: {experience}\n")
        
        # Filter questions by the selected role (Category)
        filtered_data = df[df['Category'].str.lower() == role.lower()].dropna(subset=['Question'])
        
        if filtered_data.empty:
            return []

        questions_to_ask = filtered_data.head(num_questions)
        questions = []
        for i, row in questions_to_ask.iterrows():
            questions.append(f"Q{i+1}: {row['Question']}")
        
        return questions

    def provide_tips(self, role, experience):
        # Provide role-specific tips
        role_tip = ROLE_TIPS.get(role, "Keep learning and practicing in your domain!")
        
        # Provide experience-specific tips
        experience_tip = EXPERIENCE_TIPS.get(experience, "Keep progressing based on your current level.")
        
        return {
            "role_tip": role_tip,
            "experience_tip": experience_tip
        }

# Define a route to render the HTML page
@app.route('/')
def home():
    return render_template('page.html')  # Make sure 'index.html' is in the templates folder

# Define an API endpoint for processing input
@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.json
    role_input = data.get('role', '').strip()
    experience_input = data.get('experience', '').strip()
    num_questions = int(data.get('num_questions', 3))

    # Create an instance of the expert system and pass the input
    engine = SimpleQAExpertSystem()
    engine.reset()
    engine.declare(Fact(role=role_input, experience=experience_input, num_questions=num_questions))
    questions = engine.provide_questions(role_input, experience_input, num_questions)
    tips = engine.provide_tips(role_input, experience_input)
    
    # Return the result as JSON
    return jsonify({
        'questions': questions,
        'tips': tips
    })

if __name__ == '__main__':
    app.run(debug=True)
