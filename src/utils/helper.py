import os
import streamlit as st
import pandas as pd
from src.generator.question_genrator import QuestionGenerator

def rerun():
    """Trigger a rerun of the Streamlit app."""
    st.session_state['rerun_trigger'] = not st.session_state.get('rerun_trigger', False)

class QuizManager:

    def __init__(self):
        self.questions=[]
        self.user_answers=[]
        self.results=[]

    def generate_question(self,generator: QuestionGenerator,topic:str,difficulty:str,question_type:str,num_questions:int):

        self.questions=[]
        self.user_answers=[]
        self.results=[]

        try:
            for _ in range(num_questions):
                 
                if question_type == "MCQ":
                    question = generator.generate_mcq(topic=topic,difficulty=difficulty)
                    self.questions.append({
                        "type": "MCQ",
                        "question": question.question,
                        "options": question.options,
                        "correct_answer": question.correct_answer})
                else:
                    question = generator.generate_fill_in_blank(topic=topic,difficulty=difficulty)
                    self.questions.append({
                        "type": "FillInTheBlank",
                        "question": question.question,
                        "correct_answer": question.correct_answer})
        except Exception as e:
            st.error(f"Error generating questions: {e}")
            return False
        return True

    def attempt_quiz(self):
        """Display questions and capture user answers in the Streamlit app."""
        if len(self.user_answers) != len(self.questions):
            self.user_answers = [None] * len(self.questions)
        for i,q in enumerate(self.questions):
            st.markdown(f"### Question {i+1} : {q['question']}")

            if q['type'] == "MCQ":
                user_answer = st.radio("Select an option:", q['options'], key=f"q{i}")
                self.user_answers[i] = user_answer
            else:
                user_answer = st.text_input("Your answer for fill in the blank:",key=f"q{i}")
                self.user_answers[i] = user_answer

    def evaluate_quiz(self):
        """Evaluate user answers against correct answers and store results."""
        self.results=[]
        for i,(q,usr_ans) in enumerate(zip(self.questions,self.user_answers)):
            result_dict ={
                "question_number": i+1,
                "question": q['question'],
                'question_type': q['type'],
                "user_answer": usr_ans,
                "correct_answer": q['correct_answer'],
                "is_correct": False
            }
            if q['type'] == "MCQ":
                result_dict["is_correct"] = (usr_ans == q['correct_answer'])
            else:
                result_dict["is_correct"] = (usr_ans.strip().lower() == q['correct_answer'].strip().lower())
            self.results.append(result_dict)
    
    def generate_results_dataframe(self):
        """Generate a pandas DataFrame from the results for display."""
        if not self.results:
            return pd.DataFrame()  # Return empty DataFrame if no results
        return pd.DataFrame(self.results)

    def save_to_csv(self,filename_prefix="quizresults"):
        """Save the results to a CSV file."""
        if not self.results:
            st.warning("No results to save.")
            return
        df = self.generate_results_dataframe()
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.csv"
        os.makedirs("results", exist_ok=True)
        full_path = os.path.join("results", filename)

        try:
            df.to_csv(full_path,index=False)
            st.success("Results saved sucesfully....")
            return full_path
        
        except Exception as e:
            st.error(f"Failed to save results {e}")
            return None