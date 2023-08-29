import streamlit as st
import functions as f

st.title("Goal Setter/Helper Application")

# Ask the user about their goal
st.header("Goal Creation")
goal_description = st.text_input("What is your goal?")

# Ask the user how many minutes per day they can spend on it
st.header("Time Commitment")
minutes_per_day = st.slider("How many minutes per day are you willing to dedicate to this goal?", min_value=0, max_value=240, step=10)

# Ask about potential pitfalls and how they can be avoided
st.header("Potential Fallbacks and Solutions")
pitfalls = st.text_area("List potential distractions or obstacles that might hinder your progress:")
avoidance_strategies = st.text_area("How do you think you can avoid or overcome these pitfalls?")

if st.button('Submit'):

    user_responses = {
        'goal': goal_description,
        'minutes_per_day': minutes_per_day,
        'pitfalls': pitfalls,
        'avoidance_strategies': avoidance_strategies
    }
    prompt = f.generate_prompt(user_responses)
    response = f.call_api(prompt)
    # Send the user_responses to the call_api function
    #response = call_api(user_responses)  # Assuming call_api is a function that takes a dictionary as input
    st.write(response['temperature_0'])


