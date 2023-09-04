import streamlit as st
import functions as f
import prompts
st.set_page_config(layout="wide")

def main():
    st.title("Goal Setter/Helper Application")
    
    if "step" not in st.session_state:
        st.session_state.step = "input_goal"
    
    st.write(f"Current Step: {st.session_state.step}")  #Debug message

    if st.session_state.step == "input_goal":
        input_goal()
    elif st.session_state.step == "clarify_goal":
        clarify_goal()
    elif st.session_state.step == "confirm_goal":
        confirm_goal()
    elif st.session_state.step == "longterm_plan":
        longterm_plan()
    elif st.session_state.step == "dashboard":
        dashboard()
    # Add more steps as needed

def input_goal():
    st.header("Goal Creation")
    initial_goal = st.text_input("What is your goal?")

    # Adding a date picker for goal deadline
    goal_deadline = st.date_input("By when would you like to achieve it?")
    # Asking user how they'll measure the goal's completion
    goal_measure = st.text_input("How will you measure the completion of your goal?")

    if st.button('Submit'):
        st.session_state.initial_goal = initial_goal
        st.session_state.goal_deadline = goal_deadline
        st.session_state.goal_measure = goal_measure
        
        instructions, prompt = prompts.clarify_goal(st.session_state.initial_goal, st.session_state.goal_deadline, st.session_state.goal_measure)
        st.session_state.response = f.call_api(instructions, prompt)
        st.session_state.step = "clarify_goal"
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
        st.session_state.step = "longterm_plan"
        instructions, prompt = prompts.create_longterm_plan(st.session_state.finalized_goal)
        st.session_state.response = f.call_api(instructions, prompt)
        st.experimental_rerun() 

def longterm_plan():
    st.header("Longterm Plan")
    st.session_state.longterm_plan = st.session_state.response['choices'][0]['message']['content']
    st.write(st.session_state.longterm_plan)

    if st.button('Confirm'):
        st.session_state.step = "dashboard"
        instructions, prompt = prompts.create_shortterm_plan(st.session_state.longterm_plan)
        st.session_state.response = f.call_api(instructions, prompt)
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
