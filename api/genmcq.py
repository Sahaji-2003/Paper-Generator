from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError,RootModel, conlist
from typing import Literal, Optional, List
import google.generativeai as generativeai

# Initialize Google Generative AI
generativeai.configure(api_key="AIzaSyD6B8FQ19KeeWxBa_wJSQexiDhsk8AHrjk")

# Flask app initialization
app = Flask(__name__)

# Define the schema for a question using Pydantic
class QuestionSchema(BaseModel):
    questionType: Literal['MCQ', 'SingleChoice', 'TrueFalse']  # Use Literal for fixed value strings
    question: str
    options: Optional[List[str]] = None  # Options are optional for True/False
    answer: str
    explanation: Optional[str] = None

class QuestionArraySchema(RootModel[List[QuestionSchema]]):
    pass

# Generate questions using Google Generative AI
def generate_questions(topic, num_questions, context, question_type):
    # Create a prompt based on the selected question type
    if question_type == 'TrueFalse':
        prompt_type = f"Generate {num_questions} True/False questions on the topic '{topic}' Given Context '{context}'."
    elif question_type == 'SingleChoice':
        prompt_type = f"Generate {num_questions} single-choice questions (only one correct answer) on the topic '{topic}' Given Context '{context}'."
    elif question_type == 'MCQ':
        prompt_type = f"Generate {num_questions} multiple-choice questions (with more than one correct answer) on the topic '{topic}' Given Context '{context}'."
    else:
        raise ValueError("Invalid question type selected.")

    # Call the generative AI model to generate questions
    result = generativeai.generate_text(prompt=prompt_type)(
        model='gemini-1.5-flash',
        prompt=prompt_type
    )

    # Assuming result['text'] returns the generated questions in a suitable format
    return result['text']

# Flask route to handle the request
@app.route('/mcq', methods=['POST'])
def generate_questions_route():
    try:
        # Parse the incoming JSON request
        data = request.json
        topic = data.get('topic')
        num_questions = data.get('numQuestions')
        context = data.get('context')
        question_type = data.get('questionType')

        # Generate questions
        questions = generate_questions(topic, num_questions, context, question_type)

        # Parse and validate the result using Pydantic
        question_array = QuestionArraySchema.parse_raw(questions)

        return jsonify(question_array.dict()), 200

    except ValidationError as e:
        # Handle validation errors
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
    except Exception as e:
        # Handle other errors
        return jsonify({"error": str(e)}), 500

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
