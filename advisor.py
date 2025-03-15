from openai import OpenAI
from flask import Flask
import os
from dotenv import load_dotenv
import json


load_dotenv()

client = OpenAI(
	api_key=os.getenv("OPENAI_API_KEY")
)


def ask_chatGPT(uv_index, weather, temperature, skin_type, age, gender, skin_conditions):
	prompt = f"""
		Provide a short and clear advice (max 2 sentences) for a {age}-year-old {gender} with {skin_type} skin and {skin_conditions if skin_conditions else 'no skin conditions'}.
		The current UV index is {uv_index}, the temperature is {temperature} and the weather is {weather}. 
		The advice should include necessary skincare (like sunscreen SPF) and clothing recommendations.
		Return the response in JSON format like this: {
			{"advice": "your_advice_here"},
			{"skincare": "factor_number_here"},
			{"recomended_outdor_time": "time_here(in hours)"}
		}
		"""

	advice = client.chat.completions.create(
		model="gpt-4o-mini",
		store=True,
		messages=[{"role": "system", "content": "You are a skincare and weather expert giving concise outdoor advice."},
					{"role": "user", "content": prompt}
		]
	)

	advice_text = advice.choices[0].message.content

	try:
		advice_json = json.loads(advice_text)
	except json.JSONDecodeError:
		advice_json = {"Advice": advice_text.strip()}

	return advice_json


uv_index = 7
weather = "sunny and warm"
temperature = 25
skin_type = "fair"
age = 25
gender = "female"
skin_conditions = "eczema"


advice = ask_chatGPT(uv_index, weather, temperature, skin_type, age, gender, skin_conditions)
print(json.dumps(advice, indent=4))
	