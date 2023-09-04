def clarify_goal(initial_goal, goal_deadline, goal_measure):
    instructions = """
    You are a renowned expert in goal-setting and personal development, assisting individuals in creating clear, actionable, and achievable objectives.
    You are going to guide users in refining their goals using the principles of what makes a great goal.
    """

    # Adjusting the prompt to account for the new details
    prompt = f"""
    Given the initial goal from the user, your task is to help them clarify and refine it, making it more actionable and aligned with the 
    principles of an effective goal. 

    You can ask up to 3 questions.

    --Goal Information--
    The user's goal is: {initial_goal}
    The goal's deadline is: {goal_deadline}
    The measure for the goal's completion is: {goal_measure}


    Your output should help the user refine their goal, so it MUST look like:
    1. ... 
    2. ...
    3. ...
    """
    return instructions, prompt



def finalize_goal(goal, user_responses, feedback = None, regenerate=False):
    instructions = """
    You are a renowned expert in goal-setting and personal development, assisting individuals in creating clear, actionable, 
    and achievable objectives. You are going to guide users in refining their goals using the principles of what makes a great goal.
    """

    # Iterate through the clarification answers and format them
    clarifications = "\n".join([f"{question}: {answer}" for question, answer in user_responses.items()])

    # Constructing the prompt for your Goal Setter/Helper application
    if not regenerate:
        prompt = f"""
        You will receive the first iteration of a goal from the user as well as clarifying questions and answers from the user. Given the user's first iteration goal and their answers to your questions please create a finalize goal for them. 

        The goal should be:
            - Specific - What?
            - Measurable - How much?
            - Time-Bound - By when?   

        --Goal Information--
        {goal}

        --Clarifying Questions and Answers--
        {clarifications}

        The response should be as follows: 
        Clarified goal: 'clarified goal'
        """
    elif regenerate:
        prompt = f"""
        You will receive the an iteration of a goal from the user as well as clarifying questions and answers and feedback regarding their previous goal from the user. Given the user's first iteration goal and their answers to your questions please create a finalize goal for them. 

        The goal should be:
            - Specific - What?
            - Measurable - How much?
            - Time-Bound - By when?

        --Previous Goal--
        {goal}

        --Clarifying Questions and Answers--
        {clarifications}

        --Feedback--
        {feedback}

        The response should be as follows: 
        Clarified goal: 'clarified goal'
        """

    # After formatting, we put back the initial goal into user_responses

    return instructions, prompt

def create_longterm_plan(goal):
    instructions = """
    You are a strategic planning specialist, adept at designing both visionary long-term blueprints and actionable short-term roadmaps to guide 
    individuals seamlessly towards their desired outcomes.

    Given a user's finalized goal, please create a structured long term plan for them. Consider the best practices for creating a long-term plan and its key components.

    If there's no timeframe specified, devise a reasonable one. Always start with the immediate next step the user should take.

    Ensure each step begins on a new line and follows this format:
    - Timeframe (e.g., Month 1): Action/Task
    """

    prompt = f"""
    {instructions}

    --Goal Information--
    {goal}
    """
    return instructions, prompt



def create_shortterm_plan(longterm_plan):
    instructions = "You are a world class life coach and business operator with a bias towards action. However, you also understand what it is like for someone who is just starting out on their journey. You are going to help users create a long term plan for their goals."

    prompt = f"""
    You will recieve a users long term plan. Given the user's long term plan, please create a short term plan for them.
    {longterm_plan}
    """


    return instructions, prompt

def create_weekly_plan_for_step(step):
    instructions = """
    Given a specific step from a long-term plan, break it down into a detailed weekly plan for the user.
    """

    prompt = f"""
    {instructions}

    --Step Information--
    {step}

    Please return the plan in the following format:
    - Day 1: Do this
    - Day 2: Do this
    ...
    """
    return instructions, prompt