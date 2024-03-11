from flask import Flask, request, render_template
import openai
import config

app = Flask(__name__)

# API Token
openai.api_key = config.API_KEY

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Code Errr
        code = request.form["code"]
        error = request.form["error"]

        explanation_prompt = (f"Explain the error in this code without fixing it:"
                  f"\n\n{code}\n\nError:\n\n{error}")
        model_engine = "gpt-3.5-turbo"
        explanation_completions = openai.chat.completions.create(
            model=model_engine,
            messages=[
	        {
		        "role": "user",
		        "content": explanation_prompt
	        }
	        ],            
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.9,
        )

        explanation = explanation_completions.choices[0].message.content
        print(explanation)

        fixed_code_prompt = (f"Fix this code: \n\n{code}\n\nError:\n\n{error}."
                             f" \n Respond only with the fixed code.")
        fixed_code_completions = openai.chat.completions.create(
            model=model_engine,
            messages=[
	        {
		        "role": "user",
		        "content": fixed_code_prompt
	        }
	        ],            
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.9,
        )
        fixed_code = fixed_code_completions.choices[0].message.content

        return render_template("index.html",
                           explanation=explanation,
                           fixed_code=fixed_code)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run()