import openai
import config

def call_api(instructions, prompt):
    openai.api_key = config.API_KEY

    response = openai.ChatCompletion.create(
        #model = "gpt-4",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    

    return response
