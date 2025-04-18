from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("API key is missing! Please set the GROQ_API_KEY environment variable.")

client = Groq(api_key=GROQ_API_KEY)

# Load course data
with open("data.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

# App state - Now managed per session
class SessionState:
    def __init__(self):
        self.conversation_state = "waiting_for_course"
        self.selected_course = None
        self.topics = []
        self.current_topic_index = 0
        self.explanations = {}
        self.quiz_data = {}
        self.quiz_questions = []
        self.current_quiz_index = 0

# Store states for different sessions (in production, use a proper session management system)
sessions = {}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/courses', methods=['GET'])
def get_courses():
    return jsonify(list(json_data.keys()))

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id', 'default')
    message = data.get('message')

    if session_id not in sessions:
        sessions[session_id] = SessionState()

    state = sessions[session_id]

    if not message:
        return jsonify({"response": "Please type a message."})

    # Handle different conversation states
    if state.conversation_state == "waiting_for_course":
        matched = get_matched_course(message)
        if matched:
            state.selected_course = matched
            state.topics = list(json_data[matched].keys())
            state.current_topic_index = 0
            state.conversation_state = "explaining_topic"
            return jsonify({"response": explain_next_topic(state)})
        else:
            courses = "\n".join(f"- {course}" for course in json_data)
            return jsonify({
                "response": f"I couldn't find that course. Here are the available ones:\n\n{courses}"
            })

    if state.conversation_state == "awaiting_next_topic_permission":
        if message.lower() in ["yes", "y"]:
            state.current_topic_index += 1
            state.conversation_state = "explaining_topic"
            return jsonify({"response": explain_next_topic(state)})
        else:
            state.conversation_state = "awaiting_clarification"
            return jsonify({
                "response": "Could you please specify which part you didn't understand?"
            })

    if state.conversation_state == "awaiting_clarification":
        return jsonify({"response": simplify_current_topic(state, message)})

    if state.conversation_state == "awaiting_quiz_choice":
        if message.lower() in ["yes", "y"]:
            state.conversation_state = "quiz_question"
            return jsonify({"response": start_quiz(state)})
        else:
            state.current_topic_index += 1
            state.conversation_state = "explaining_topic"
            return jsonify({"response": explain_next_topic(state)})

    if state.conversation_state == "quiz_question":
        return jsonify({"response": handle_quiz_answer(state, message)})

    if state.conversation_state == "awaiting_next_quiz_question":
        return jsonify({"response": send_next_quiz_question(state)})

    # Check if message matches a course name
    matched = get_matched_course(message)
    if matched:
        state.selected_course = matched
        state.topics = list(json_data[matched].keys())
        state.current_topic_index = 0
        state.conversation_state = "explaining_topic"
        return jsonify({"response": explain_next_topic(state)})

    return jsonify({
        "response": "I'm here to assist you! Please type a valid course name."
    })

def get_matched_course(user_input):
    return next((course for course in json_data if course.lower() == user_input.lower()), None)

def explain_next_topic(state):
    topics = state.topics
    index = state.current_topic_index

    if index >= len(topics):
        return "🎉 You've completed all the topics and quizzes. Well done!"

    topic = topics[index]
    course = state.selected_course

    if topic in state.explanations:
        explanation = state.explanations[topic]
    else:
        explanation, quiz_questions = fetch_topic_explanation(course, topic)
        state.explanations[topic] = explanation
        state.quiz_data[topic] = quiz_questions

    state.quiz_questions = state.quiz_data.get(topic, [])
    state.current_quiz_index = 0
    state.conversation_state = "awaiting_quiz_choice"

    return f"**{topic}**:\n{explanation}\n\nWould you like to try a quiz on this topic? (yes/no)"

def fetch_topic_explanation(course, topic):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"You are an expert in {course}. Provide clear and detailed explanations about topics related to {course}."},
                {"role": "user", "content": f"Explain the topic '{topic}' in detail as it relates to {course}."}
            ],
            temperature=0.7
        )
        explanation = response.choices[0].message.content.strip()
        quiz_questions = generate_quiz_questions(course, topic)
        return explanation, quiz_questions
    except Exception as e:
        return f"Error fetching explanation: {str(e)}", []

def generate_quiz_questions(course, topic):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"You are an expert in {course}. Generate two quiz questions related to {topic} along with the correct answer."},
                {"role": "user", "content": f"Provide two multiple-choice quiz questions for the topic '{topic}' in {course}. Format them as:\nQ1: Question?\nA) Option1\nB) Option2\nC) Option3\nD) Option4\nCorrect Answer: X\n\nQ2: Question?\nA) Option1\nB) Option2\nC) Option3\nD) Option4\nCorrect Answer: Y"}
            ],
            temperature=0.7
        )
        quiz_text = response.choices[0].message.content.strip()

        quiz_list = []
        current_question = ""
        current_answer = ""

        lines = quiz_text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("Q"):
                if current_question and current_answer:
                    quiz_list.append({"question": current_question.strip(), "answer": current_answer.strip()})
                current_question = line
                current_answer = ""
            elif line.startswith(("A)", "B)", "C)", "D)")):
                current_question += "\n" + line
            elif "Correct Answer:" in line:
                current_answer = line.split("Correct Answer:")[-1].strip()

        if current_question and current_answer:
            quiz_list.append({"question": current_question.strip(), "answer": current_answer.strip()})

        return quiz_list
    except Exception as e:
        return [{"question": f"Error generating quiz: {str(e)}", "answer": ""}]

def start_quiz(state):
    if not state.quiz_questions:
        state.current_topic_index += 1
        state.conversation_state = "explaining_topic"
        return "No quiz questions available. Moving to the next topic..."
    return f"Let's start the quiz!\n\n{state.quiz_questions[0]['question']}"

def handle_quiz_answer(state, user_answer):
    index = state.current_quiz_index
    quiz_questions = state.quiz_questions

    if index >= len(quiz_questions):
        return "✅ You've already completed the quiz. Type 'yes' to proceed to the next topic."

    current_q = quiz_questions[index]
    correct = current_q["answer"]
    course = state.selected_course
    topic = state.topics[state.current_topic_index]

    try:
        explanation_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"You are an expert in {course}. Provide a short, clear explanation for why the given answer is correct."},
                {"role": "user", "content": f"Explain in 2 to 3 lines why this answer is correct:\n{current_q['question']}\nAnswer: {correct}"}
            ],
            temperature=0.7
        )
        explanation = explanation_response.choices[0].message.content.strip()
    except Exception as e:
        explanation = f"Error getting explanation: {str(e)}"

    result = "✅ Correct!" if user_answer.strip().upper() == correct.upper() else f"❌ Incorrect. The correct answer is {correct}."
    state.current_quiz_index += 1

    if state.current_quiz_index < len(quiz_questions):
        state.conversation_state = "awaiting_next_quiz_question"
        return f"{result}\n{explanation}\n\nType 'next' for the next question."
    else:
        state.conversation_state = "awaiting_next_topic_permission"
        return f"{result}\n{explanation}\n\n🎉 You've completed this quiz. Would you like to continue to the next topic? (yes/no)"

def send_next_quiz_question(state):
    index = state.current_quiz_index
    quiz_questions = state.quiz_questions

    if index >= len(quiz_questions):
        state.conversation_state = "awaiting_next_topic_permission"
        return "🎉 You've completed the quiz. Would you like to proceed to the next topic? (yes/no)"

    state.conversation_state = "quiz_question"
    return quiz_questions[index]["question"]

def simplify_current_topic(state, clarification):
    topic = state.topics[state.current_topic_index]
    course = state.selected_course
    try:
        simplified_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"You are an expert in {course}. Re-explain the topic '{topic}' in a simpler way for a student who didn't understand the following part: '{clarification}'"},
                {"role": "user", "content": f"Please simplify this part: {clarification}"}
            ],
            temperature=0.7
        )
        simple_explanation = simplified_response.choices[0].message.content.strip()
    except Exception as e:
        simple_explanation = f"Sorry, I couldn't fetch a simplified explanation due to an error: {str(e)}"

    state.conversation_state = "awaiting_next_topic_permission"
    return f"{simple_explanation}\n\nWould you like to proceed to the next topic? (yes/no)"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
