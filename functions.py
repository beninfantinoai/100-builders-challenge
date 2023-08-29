import openai

def generate_prompt(user_responses):
    
    # Constructing the prompt for your Goal Setter/Helper application
    prompt = f"""
Acting as a supportive mentor, I am a person who has successfully achieved numerous personal goals over the years. I understand the challenges that come with it and the determination it requires. 

Considering the following information about someone aspiring to achieve their personal goal, can you provide:

- An insightful understanding of their goal and the time they're willing to dedicate.
- Actionable tips and tricks to maintain consistency.
- A brief plan to help them stay on track.
- Counterarguments discussing potential challenges and ways to overcome them.

--Goal Information--
Goal: {user_responses['goal']}
Minutes per day: {user_responses['minutes_per_day']} minutes

--Potential Fallbacks--
Pitfalls:
{user_responses['pitfalls']}
Avoidance Strategies:
{user_responses['avoidance_strategies']}

End with a motivational call to action.
    """
    return prompt

def call_api(prompt):
    #openai.api_key = your api key here
    
    temperatures = [0, 0.3, 0.7]
    responses = {}
    
    for temp in temperatures:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=temp,
        )
        responses[f'temperature_{temp}'] = response['choices'][0]['message']['content']

    return responses
