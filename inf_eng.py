from experta import *
import pandas as pd
import time

df = pd.read_csv('data/combined_file(3).csv', encoding='ISO-8859-1')

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
        
        # Filter questions by the selected role (Category) and handle case insensitivity
        filtered_data = df[df['Category'].str.lower() == role.lower()].dropna(subset=['Question'])
        
        if filtered_data.empty:
            print(f"No questions available for the role '{role}'.")
            return

        # Limit the number of questions based on user input
        questions_to_ask = filtered_data.head(num_questions)

        # Loop through the filtered questions and provide Q&A
        for i, row in questions_to_ask.iterrows():
            print(f"Q{i+1}: {row['Question']}")

            # If time-bound mode is enabled, use the timed input function
            if self.time_bound:
                user_answer = self.timed_input("Your Answer: ", timeout=10)
                if user_answer is None:
                    print("You ran out of time!\n")
                    continue
            else:
                user_answer = input("Your Answer: ").strip().lower()

            correct_answer = row['Answer'].strip().lower()
            self.evaluate_answer(user_answer, correct_answer)

        self.provide_tips(role, experience)

    def timed_input(self, prompt, timeout=10):
        """Time-limited input function."""
        print(f"You have {timeout} seconds to answer.")
        start_time = time.time()
        user_answer = input(prompt)
        end_time = time.time()
        
        if end_time - start_time > timeout:
            return None 
        return user_answer.strip().lower()

    def evaluate_answer(self, user_answer, correct_answer):
        # Split both user and correct answers into sets of keywords
        correct_keywords = set(correct_answer.lower().split())
        user_keywords = set(user_answer.lower().split())
    
    # Find the matching keywords
        matching_keywords = correct_keywords.intersection(user_keywords)

    # Set a threshold for matching (e.g., 30% of correct answer's keywords must match)
        threshold = 0.3  # 30% of the correct answer's keywords

        if len(matching_keywords) / len(correct_keywords) >= threshold:
          print(f"Good job! You mentioned key points: {', '.join(matching_keywords)}\n")
        else:
          print(f"You missed some key points. Here's the full answer:\n{correct_answer}\n")
    
    

    def provide_tips(self, role, experience):
        print("\n------------------------------- Tips for Improvement ----------------------------------------")
        
        # Provide role-specific tips
        role_tip = ROLE_TIPS.get(role, "Keep learning and practicing in your domain!")
        print(f"Role-specific Tip ({role}): {role_tip}")
        
        # Provide experience-specific tips
        experience_tip = EXPERIENCE_TIPS.get(experience, "Keep progressing based on your current level.")
        print(f"Experience-specific Tip ({experience} level): {experience_tip}")
    def get_user_input():
        available_categories = df['Category'].unique()
        print("Available job roles:")
        for category in available_categories:
          print(f"- {category}")
    
        role_input = input("\nEnter the job role (from the available categories): ").strip()
        experience_input = input("Enter the experience level (Entry, Mid, Senior): ").strip()

    # Get number of questions user wants to answer
        num_questions = int(input("How many questions would you like to answer? ").strip())

    # Ask if the user wants time-bound mode
        time_bound_input = input("Would you like to enable time-bound mode? (yes/no): ").strip().lower()
        time_bound = time_bound_input == 'yes'

        return role_input, experience_input, num_questions, time_bound
    def get_advice(self, role_input, experience_input, num_questions, time_bound):
        # This method will act as a wrapper for the inference engine logic
        self.time_bound = time_bound
        self.reset()
        
        # Declare facts based on input parameters
        self.declare(Fact(role=role_input, experience=experience_input, num_questions=num_questions))
        self.run()

        # Collect tips for the user
        role_tip = ROLE_TIPS.get(role_input, "Keep learning and practicing in your domain!")
        experience_tip = EXPERIENCE_TIPS.get(experience_input, "Keep progressing based on your current level.")

        return role_tip, experience_tip

    


if __name__ == "__main__":

    engine = SimpleQAExpertSystem()
    engine.reset()
    role_input, experience_input, num_questions, time_bound = get_advice()
    
    # Set time-bound mode based on user input
    engine.time_bound = time_bound

    engine.declare(Fact(role=role_input, experience=experience_input, num_questions=num_questions))

    engine.run()




  
    
   
