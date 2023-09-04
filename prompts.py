def clarify_goal(initial_goal, goal_deadline):
    instructions = """
    You are a renowned expert in goal-setting and personal development, assisting individuals in creating clear, actionable, and achievable objectives.
    You are going to guide users in refining their goals using the principles of what makes a great goal.
    """

    # Adjusting the prompt to account for the new details
    prompt = f"""
    Given a user's initial goal, deadline, and method of measurement, generate three sequential, context-aware clarifying questions. For context:

    If the goal is related to 'Health & Fitness', such as 'I want to lose weight' with a deadline 'by the end of the year':
    - A question could be 'How much do you currently weigh and what is your target weight?'
    - Based on the answer, the next could be 'How much time per week will you dedicate to exercising?'
    - And, 'Are you considering hiring a personal trainer within a budget of $100 - $200 per month?'

    If the goal concerns 'Financial Security', like 'I want to save more money' in the next '6 months':
    - A question could be 'How much do you currently have in savings and what's your target amount?'
    - Depending on the reply, 'What expenses are you willing to cut down on or eliminate?'
    - Lastly, 'Do you plan to seek financial advice or use budgeting tools?'

    For 'Personal Development' goals such as 'I want to learn how to code' in '6 months':
    - A possible question is 'What specifically do you wish to create – a website, mobile app, etc.?'
    - Depending on the reply, 'Which programming languages do you want to learn?'
    - Finally, 'How many hours a week are you planning to practise & study?'

    Now, given the user's goal, deadline, and measure, please provide three contextually relevant questions.

    --Goal Information--
    The user's goal is: {initial_goal}
    The goal's deadline is: {goal_deadline}

    -- Output Format --
    1. ... 
    2. ...
    3. ...
    """
    return instructions, prompt



def finalize_goal(goal, user_responses, feedback=None, regenerate=False):
    instructions = """
    As a renowned expert in goal-setting and personal development, your task is to assist individuals in refining their goals using key principles. Using the details provided, generate a clarified goal that embodies:
    - Specificity: What exactly do they want to achieve?
    - Measurability: How will they measure progress or know they've achieved it?
    - Time-Bound: When do they plan to achieve it?

    Below are the user's initial inputs, clarifying questions and answers, and any feedback if provided.
    """

    # Iterate through the clarification answers and format them
    clarifications = "\n".join([f"{question}: {answer}" for question, answer in user_responses.items()])

    base_prompt = """
    EXAMPLE:
    Given a user's goal to "travel more", clarifications might include:
    - Desired destinations: Europe and Asia
    - Frequency: 4 times a year
    A refined goal could be: "Travel to Europe and Asia 4 times within the next year."

    --Goal Information--
    {goal_info}

    --Clarifying Questions and Answers--
    {clarifications}
    """

    if regenerate:
        base_prompt += """
        --Feedback--
        {feedback}
        """

    base_prompt += "\nYour task is to provide:\nClarified goal: 'clarified goal'"

    prompt = base_prompt.format(
        goal_info=goal if not regenerate else f"Previous Goal: {goal}",
        clarifications=clarifications,
        feedback=feedback if regenerate else ""
    )

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