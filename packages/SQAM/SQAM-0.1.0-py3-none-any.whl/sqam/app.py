from flask import Flask, request, jsonify, render_template
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import json

app = Flask(__name__)

# Initialize the SBERT model (load only once)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Function to load and combine JSON files from a directory
def load_json_files_from_directory(directory):
    combined_data = []
    # Get all JSON files in the directory
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    # Load and combine all JSON files
    for file in json_files:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
            combined_data.extend(data)  # Assuming data is a list of question-answer pairs
    
    return combined_data

# Remove duplicate questions
def remove_duplicates(data):
    seen = set()
    unique_data = []
    for entry in data:
        question = entry['question']
        if question not in seen:
            unique_data.append(entry)
            seen.add(question)
    return unique_data

# Precompute question embeddings for all questions in the combined dataset
def precompute_embeddings():
    dataset_directory = '.'  # Directory where dataset is located
    dataset = load_json_files_from_directory(dataset_directory)
    dataset = remove_duplicates(dataset)
    
    questions = [entry['question'] for entry in dataset]
    question_embeddings = model.encode(questions)
    return dataset, question_embeddings

# Load dataset and embeddings on app startup
dataset, question_embeddings = precompute_embeddings()

# Function to find top N similar answers
def find_top_n_answers(customer_question, dataset, question_embeddings, top_n=3, similarity_threshold=0.1):
    # Encode the customer question into an embedding
    customer_embedding = model.encode([customer_question])
    
    # Compute cosine similarity between customer question and all dataset questions
    similarities = cosine_similarity(customer_embedding, question_embeddings).flatten()
    
    # Sort the similarities and select top N that exceed the similarity threshold
    top_n_indices = np.argsort(similarities)[-top_n:][::-1]  # Get indices of top N similar questions
    
    top_answers = []
    for rank, index in enumerate(top_n_indices, start=1):
        if similarities[index] >= similarity_threshold:
            question = dataset[index]['question']
            answer = dataset[index]['answer']
            similarity_score = float(similarities[index])  # Convert similarity score to Python float
            
            top_answers.append({
                'rank': rank,  # Add rank (1, 2, 3)
                'question': question,
                'answer': answer,
                'similarity_score': similarity_score  # Ensure this is a Python float
            })
    
    return top_answers

# Serve the homepage with the form
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for the API to handle POST requests from the web page
@app.route('/get_answers', methods=['POST'])
def get_answers():
    try:
        # Get customer question from POST request JSON data
        data = request.get_json()
        customer_question = data.get('question', '')
        
        if not customer_question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Get top N answers
        top_answers = find_top_n_answers(customer_question, dataset, question_embeddings, top_n=3)
        
        # Return the top answers as a JSON response
        return jsonify({'response': top_answers}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
