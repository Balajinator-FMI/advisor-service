from openai import OpenAI
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import json


app = Flask(__name__)

load_dotenv()

client = OpenAI(
	api_key=os.getenv("OPENAI_API_KEY")
)


def ask_chatGPT(uv_index, temperature, skin_type, age, gender, skin_conditions):
	prompt = f"""
		Provide a short and clear advice (max 2 sentences) for a {age}-year-old {gender} with {skin_type} skin and {skin_conditions if skin_conditions else 'no skin conditions'}.
		The current UV index is {uv_index} and the temperature is {temperature}. 
		The advice should include necessary skincare (like sunscreen SPF) and clothing recommendations.
		Return the response in JSON format like this: 
		{{
			"advice": "your_advice_here",
			"skincare": "factor_number_here",
			"recomended_outdor_time": "time_number_here(in hours)",
		}}
		Ensure "skincare" and "recommended_outdoor_time" are numbers, not strings.
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
		advice_json = {advice_text.strip()}

	return advice_json


@app.route("/advice", methods=["POST"])
def get_user_data():
	try:
		data = request.json
		uv_index = data["uv_index"]
		temperature = data["temperature"]
		skin_type = data["skin_type"]
		age = data["age"]
		gender = data["gender"]

		if "skin_conditions" in data:
			skin_conditions = data["skin_conditions"]
		else:
			skin_conditions = None


		advice = ask_chatGPT(uv_index, temperature, skin_type, age, gender, skin_conditions)

		return jsonify(advice), 200
	
	except Exception as e:
		return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=9093, debug=True)
	