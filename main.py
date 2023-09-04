import streamlit as st
import functions as f
import prompts
from datetime import datetime, timedelta
st.set_page_config(layout="wide")

def main():
    st.title("Goal Setter/Helper Application")
    
    if "step" not in st.session_state:
        st.session_state.step = "initial_goal"
    
    st.write(f"Current Step: {st.session_state.step}")  #Debug message

    if st.session_state.step == "initial_goal": #what by when 
        initial_goal()
    elif st.session_state.step == "clarying_questions": #clarying questions
        clarify_goal()
    elif st.session_state.step == "confirm_goal":
        confirm_goal()
    elif st.session_state.step == "additonal_context":
        additional_context()
    elif st.session_state.step == "dashboard":
        dashboard()
    # Add more steps as needed

def initial_goal():
    st.header("Goal Creation")
    initial_goal = st.text_input("What is your goal?")
    
    # Add a row of buttons for goal duration
    durations = {
        "1 month": timedelta(days=30),
        "6 months": timedelta(days=180),
        "1 year": timedelta(days=365),
        "3 years": timedelta(days=3*365),
        "5 years": timedelta(days=5*365)
    }
    
    
    # Show the date input box
    if 'goal_deadline' not in st.session_state:
        default_deadline = datetime.now()
    else:
        default_deadline = st.session_state.goal_deadline

    goal_deadline = st.date_input("By when would you like to achieve it?", default_deadline)
    # Create columns for the buttons
    cols = st.columns(len(durations))

    for idx, (duration, delta) in enumerate(durations.items()):
        with cols[idx]:
            if st.button(duration):
                # When a button is pressed, adjust the goal_deadline by the selected duration
                st.session_state.goal_deadline = datetime.now() + delta
                st.experimental_rerun()



    if st.button('Submit'):
        st.session_state.initial_goal = initial_goal
        st.session_state.goal_deadline = goal_deadline

        #goal structure so far: initial goal by when         
        instructions, prompt = prompts.clarify_goal(st.session_state.initial_goal, st.session_state.goal_deadline)
        
        st.session_state.response = f.call_api(instructions, prompt)
        st.session_state.step = "clarying_questions"
        st.experimental_rerun()

def clarify_goal():
    clarification_questions = st.session_state.response['choices'][0]['message']['content'].split("\n")
    st.session_state.clarying_questions = {}
    
    st.header("Clarify Your Goal")
    for idx, question in enumerate(clarification_questions, start=1):
        if question.strip():  
            st.write(question)  
            key_name = f"clarying_question_{idx}"
            answer = st.text_input("", key=key_name)
            st.session_state.clarying_questions[key_name] = answer

    if st.button('Continue with these Answers'):
        instructions, prompt = prompts.finalize_goal(st.session_state.initial_goal, st.session_state.clarying_questions)
        st.session_state.response = f.call_api(instructions, prompt)
        st.session_state.step = "confirm_goal"
        st.experimental_rerun()


def confirm_goal():
    st.header("Confirm Your Goal")
    goal = st.session_state.response['choices'][0]['message']['content']
    st.write(goal)

    feedback = st.text_input("If you're not satisfied with the goal, please explain why or describe changes you'd like to see:")

    if st.button('Regenerate'):
        st.session_state.feedback = feedback
        instructions, prompt = prompts.finalize_goal(st.session_state.initial_goal, st.session_state.clarying_questions, st.session_state.feedback, regenerate=True)
        st.session_state.response = f.call_api(instructions, prompt)
        st.experimental_rerun()

    if st.button('Confirm'):
        st.session_state.finalized_goal = goal
        st.session_state.step = "additonal_context"
        instructions, prompt = prompts.additional_context(st.session_state.finalized_goal)
        st.experimental_rerun() 

def additional_context():
    st.header("Additional Context")

    # Initializing the question counter and questions storage if not present
    if "question_number" not in st.session_state:
        st.session_state.question_number = 1
        st.session_state.dialogue = ""

    # Get the finalized goal to provide as input to the prompt function
    goal = st.session_state.finalized_goal

    # If the current question isn't loaded or we're starting fresh, get a new one
    if "current_question" not in st.session_state or st.session_state.question_number == 1:
        # Use the goal and current dialogue to get the next question
        instructions, prompt = prompts.additional_context(goal, st.session_state.dialogue)
    
        st.session_state.response = f.call_api(instructions, prompt)
        st.session_state.current_question = st.session_state.response['choices'][0]['message']['content']

    # Display the current question and capture the user's answer
    answer = st.text_input(st.session_state.current_question)

    # If user answers and clicks on "Next Question" or "Confirm" if it's the last question
    if st.button("Next Question" if st.session_state.question_number < 5 else "Confirm"):
        # Append the question and answer to the dialogue
        st.session_state.dialogue += "\nQ: " + st.session_state.current_question + "\nA: " + answer

        # If there are more questions, increment the counter and clear the current_question so a new one is loaded
        if st.session_state.question_number < 5:
            st.session_state.question_number += 1
            del st.session_state.current_question
            st.experimental_rerun()
        else:
            # All questions answered, store the dialogue in the 'additional_context'
            st.session_state.additional_context = st.session_state.dialogue
            st.session_state.step = "dashboard"
            st.experimental_rerun()



def dashboard():

    st.header("Your Longterm Plan Dashboard")

    # Extract and split the steps from the long-term plan
    plan_steps = [step.strip() for step in st.session_state.longterm_plan.split("-") if step]

    # Using Streamlit's columns feature to split the layout
    left_column, right_column = st.columns(2)

    # If the selected_step isn't initialized, set it to the first step
    if 'selected_step' not in st.session_state:
        st.session_state.selected_step = plan_steps[0]

    # Use radio buttons in the left column to ensure only one step can be selected at a time
    st.session_state.selected_step = left_column.radio("Select a step from your Longterm Plan:", plan_steps, index=plan_steps.index(st.session_state.selected_step))

    # Generate and display a weekly plan for the selected step in the right column
    instructions, prompt = prompts.create_weekly_plan_for_step(st.session_state.selected_step)
    weekly_plan_response = f.call_api(instructions, prompt)
    weekly_plan = weekly_plan_response['choices'][0]['message']['content']

    right_column.header("Weekly Plan for the Selected Step")
    right_column.write(weekly_plan)


# Run the main function
if __name__ == "__main__":
    main()
