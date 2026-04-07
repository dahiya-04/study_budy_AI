import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helper import *
from src.generator.question_genrator import QuestionGenerator

load_dotenv()

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Study Buddy AI", page_icon=":mortar_board:", layout="centered")
    st.title("Study Buddy AI :mortar_board:")

    if 'quiz_manager' not in st.session_state:
        st.session_state.quiz_manager = QuizManager()
    if 'quiz_generator' not in st.session_state:
        st.session_state.quiz_generator = False
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'rerun_trigger' not in st.session_state:
        st.session_state.rerun_trigger = False

    st.sidebar.header("Quiz Settings")
    question_type = st.sidebar.selectbox("Select Question Type", ["MCQ", "Fill in the Blank"],index=0)

    topic = st.sidebar.text_input("Enter Topic", placeholder="Python")
    difficulty = st.sidebar.selectbox("Select Difficulty", ["easy", "medium", "hard"], index=1)

    num_questions = st.sidebar.number_input(
        "Number of Questions",
        min_value=1,
        max_value=8,
        value=3)
    
    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False
        generator = QuestionGenerator()
        success = st.session_state.quiz_manager.generate_question(
            generator,
            topic=topic,
            difficulty=difficulty,
            question_type=question_type,
            num_questions=num_questions)
        st.session_state.quiz_generator =  success

        st.rerun()
    if st.session_state.quiz_generator and st.session_state.quiz_manager.questions:
        st.header("Your Quiz")
        st.session_state.quiz_manager.attempt_quiz()

        if st.button("Submit Answers"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            st.rerun()
    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_results_dataframe()

        if not results_df.empty:
            correct_count = results_df['is_correct'].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count / total_questions) * 100
            st.write(f"Your Score: {score_percentage:.2f}%")

            for _,result in results_df.iterrows():
                q_num = result['question_number']
                if result['is_correct']:
                    st.success(f"Question {q_num}: Correct! ✅")
                else:
                    st.error(f"Question {q_num}: Incorrect! ❌")
                    st.write(f"Your Answer: {result['user_answer']}")
                    st.write(f"Correct Answer: {result['correct_answer']}")

                st.markdown("---")
            if st.button("Save Results"):
                save_file = st.session_state.quiz_manager.save_to_csv()
                if save_file:
                    with open(save_file, "rb") as f:
                        st.download_button(
                            label="Download Quiz Results",
                            data=f.read(),
                            file_name=os.path.basename(save_file), 
                            mime="text/csv")

                else:
                    st.warn("No results to save.")

if __name__ == "__main__":
    main()
