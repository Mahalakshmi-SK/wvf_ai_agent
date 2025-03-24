# from flask import Flask, render_template, request, jsonify
# import json
# import os
# from groq import Groq

# app = Flask(__name__)

# # Secure API Key Handling
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise ValueError("API key is missing! Please set the GROQ_API_KEY environment variable.")

# # Initialize Groq AI client
# client = Groq(api_key=GROQ_API_KEY)

# # Load JSON data
# def load_json(file_path):
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             data = json.load(file)
#             if not isinstance(data, dict) or "course" not in data:
#                 return None
#             return data
#     except (FileNotFoundError, json.JSONDecodeError):
#         return None

# json_file_path = "data.json"
# json_data = load_json(json_file_path)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/get_courses', methods=['GET'])
# def get_courses():
#     """Return a list of available courses"""
#     if json_data:
#         return jsonify({"courses": json_data.get("course", [])})
#     return jsonify({"error": "Course data not available"}), 500

# @app.route('/get_topics', methods=['POST'])
# def get_topics():
#     """Return available topics for a selected course"""
#     data = request.json
#     course_name = data.get("course")
    
#     if json_data and course_name in json_data:
#         return jsonify({"topics": json_data[course_name]})
    
#     return jsonify({"error": "Course not found"}), 400

# @app.route('/get_response', methods=['POST'])
# def get_response():
#     """Fetch AI-generated response based on selected course and topic"""
#     data = request.json
#     course_name = data.get("course")
#     topic_name = data.get("topic")

#     if not course_name or not topic_name:
#         return jsonify({"error": "Course and topic required"}), 400

#     # Define prompts
#     topic_prompts = {
#         "Introduction": f"Provide a beginner-friendly introduction to {course_name}. Include its history, importance, and applications.",
#         "Applications": f"List and explain the real-world applications of {course_name}.",
#         "Key Features": f"Describe the key features of {course_name}.",
#         "Common Mistakes & Best Practices": f"Provide common mistakes and best practices in {course_name}.",
#         "Why should we use it": f"Explain the benefits and importance of {course_name}.",
#     }

#     prompt = topic_prompts.get(topic_name, f"Provide a detailed explanation of {topic_name} in {course_name}.")

#     try:
#         response = client.chat.completions.create(
#             model="mixtral-8x7b-32768",
#             messages=[{"role": "user", "content": prompt}]
#         )

#         if response and response.choices:
#             return jsonify({"response": response.choices[0].message.content.strip()})
#         else:
#             return jsonify({"error": "No response received from AI"}), 500
#     except Exception as e:
#         return jsonify({"error": f"Error fetching AI response: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)





# from flask import Flask, render_template, request, jsonify
# import json
# import os
# from groq import Groq

# app = Flask(__name__)

# # Load API key securely
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise ValueError("API key is missing! Please set the GROQ_API_KEY environment variable.")

# # Initialize Groq AI client
# client = Groq(api_key=GROQ_API_KEY)

# # Load JSON data
# with open("data.json", "r", encoding="utf-8") as file:
#     json_data = json.load(file)

# @app.route('/')
# def index():
#     courses = json_data.get("course", [])
#     return render_template("index.html", courses=courses)

# @app.route('/get_courses')  # Add this route here
# def get_courses():
#     courses = json_data.get("course", [])
#     return jsonify({"courses": courses})

# @app.route('/get_topics', methods=['POST'])
# def get_topics():
#     data = request.json
#     course = data.get("course")
#     topics = json_data.get(course, [])
#     return jsonify({"topics": topics})

# @app.route('/get_response', methods=['POST'])
# def get_response():
#     data = request.json
#     course = data.get("course")
#     topic = data.get("topic")


#     if not course or not topic:
#         return jsonify({"response": "Invalid input. Please select a course and topic."})

#     prompt = f"Provide a detailed explanation of {topic} in {course}."
#     try:
#         response = client.chat.completions.create(
#             model="mixtral-8x7b-32768",
#             messages=[{"role": "user", "content": prompt}]
#         )
#         ai_response = response.choices[0].message.content.strip()
#     except Exception as e:
#         ai_response = f"Error fetching AI response: {str(e)}"
    
#     return jsonify({"response": ai_response})

# if __name__ == '__main__':
#     app.run(debug=True)





# proper AI chatbot
# from flask import Flask, render_template, request, jsonify
# import json
# import os
# from groq import Groq

# app = Flask(__name__)

# # Load API key securely
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise ValueError("API key is missing! Please set the GROQ_API_KEY environment variable.")

# # Initialize Groq AI client
# client = Groq(api_key=GROQ_API_KEY)

# # Load JSON data
# with open("data.json", "r", encoding="utf-8") as file:
#     json_data = json.load(file)

# @app.route('/')
# def index():
#     return render_template("index.html")

# @app.route('/get_response', methods=['POST'])
# def get_response():
#     data = request.json
#     user_message = data.get("message")

#     if not user_message:
#         return jsonify({"response": "Please type a message."})

#     prompt = f"User: {user_message}\nAI:"
#     try:
#         response = client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[{"role": "user", "content": prompt}]
#         )
#         ai_response = response.choices[0].message.content.strip()
#     except Exception as e:
#         ai_response = f"Error fetching AI response: {str(e)}"
    
#     return jsonify({"response": ai_response})

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, threaded=True, use_reloader=False)








# from flask import Flask, render_template, request, jsonify
# import json
# import os
# from groq import Groq

# app = Flask(__name__)

# # Load API key securely
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise ValueError("API key is missing! Please set the GROQ_API_KEY environment variable.")

# # Initialize Groq AI client
# client = Groq(api_key=GROQ_API_KEY)

# # Load JSON data
# with open("data.json", "r", encoding="utf-8") as file:
#     json_data = json.load(file)

# @app.route('/')
# def index():
#     return render_template("index.html")

# @app.route('/get_response', methods=['POST'])
# def get_response():
#     data = request.json
#     user_message = data.get("message", "").lower()  # Convert input to lowercase for better matching

#     if not user_message:
#         return jsonify({"response": "Please type a message."})

#     # Check if the user is asking for available courses
#     if "available courses" in user_message or "show me courses" in user_message:
#         courses_list = format_courses(json_data)
#         return jsonify({"response": courses_list})

#     # Otherwise, use Groq AI
#     prompt = f"User: {user_message}\nAI:"
#     try:
#         response = client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[{"role": "user", "content": prompt}]
#         )
#         ai_response = response.choices[0].message.content.strip()
#     except Exception as e:
#         ai_response = f"Error fetching AI response: {str(e)}"
    
#     return jsonify({"response": ai_response})

# def format_courses(json_data):
#     """Format courses into a readable string."""
#     response_text = "Here are the available courses:\n\n"
#     for category, courses in json_data.items():
#         response_text += f"**{category}**\n"
#         for course in courses:
#             response_text += f"- {course}\n"
#         response_text += "\n"
#     return response_text.strip()

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, threaded=True, use_reloader=False)









from flask import Flask, render_template, request, jsonify
import json
import os
from groq import Groq

app = Flask(__name__)

# Load API key securely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("API key is missing! Please set the GROQ_API_KEY environment variable.")

# Initialize Groq AI client
client = Groq(api_key=GROQ_API_KEY)

# Load JSON data
with open("data.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_message = data.get("message", "").lower().strip()  # Convert input to lowercase and remove extra spaces

    if not user_message:
        return jsonify({"response": "Please type a message."})

    # Check if the user is asking for available courses
    if "available courses" in user_message or "show me courses" in user_message:
        courses_list = list(json_data.keys())  # Extract course names only
        return jsonify({"response": "Here are the available courses:\n\n" + "\n".join(f"- {course}" for course in courses_list)})

    # Check if the user is asking for topics of a specific course
    for course_name in json_data.keys():
        if f"topics of {course_name.lower()}" in user_message:
            topics_list = json_data[course_name]  # Extract topics for the requested course
            return jsonify({"response": f"Topics for **{course_name}**:\n\n" + "\n".join(f"- {topic}" for topic in topics_list)})

    # Otherwise, use Groq AI for general queries
    prompt = f"User: {user_message}\nAI:"
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_response = response.choices[0].message.content.strip()
    except Exception as e:
        ai_response = f"Error fetching AI response: {str(e)}"
    
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True, use_reloader=False)
