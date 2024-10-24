import pytest
import json
from flask import Flask
from app import app, remove_duplicates, load_json_files_from_directory, find_top_n_answers
import os

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_remove_duplicates():
    # Sample dataset with duplicate questions
    data = [
        {'question': 'What is AI?', 'answer': 'AI stands for Artificial Intelligence.'},
        {'question': 'What is AI?', 'answer': 'AI stands for Artificial Intelligence.'},
        {'question': 'What is ML?', 'answer': 'ML stands for Machine Learning.'}
    ]
    result = remove_duplicates(data)
    assert len(result) == 2  # Only 2 unique questions remain
    assert result[0]['question'] == 'What is AI?'
    assert result[1]['question'] == 'What is ML?'

def test_load_json_files_from_directory(tmpdir):
    # Create a temporary directory and files
    data1 = [{'question': 'What is AI?', 'answer': 'AI stands for Artificial Intelligence.'}]
    data2 = [{'question': 'What is ML?', 'answer': 'ML stands for Machine Learning.'}]
    
    # Create two json files
    file1 = tmpdir.join('file1.json')
    file1.write(json.dumps(data1))
    file2 = tmpdir.join('file2.json')
    file2.write(json.dumps(data2))

    # Load and combine the data
    combined_data = load_json_files_from_directory(str(tmpdir))
    assert len(combined_data) == 2
    assert combined_data[0]['question'] == 'What is AI?'
    assert combined_data[1]['question'] == 'What is ML?'

def test_find_top_n_answers():
    dataset = [
        {'question': 'What is AI?', 'answer': 'AI stands for Artificial Intelligence.'},
        {'question': 'What is ML?', 'answer': 'ML stands for Machine Learning.'}
    ]
    question_embeddings = [
        [0.9, 0.1],  # Mock embeddings for 'What is AI?'
        [0.1, 0.9]   # Mock embeddings for 'What is ML?'
    ]
    
    # Test a similar question
    customer_question = 'What is artificial intelligence?'
    top_answers = find_top_n_answers(customer_question, dataset, question_embeddings, top_n=1, similarity_threshold=0.1)
    assert len(top_answers) == 1
    assert top_answers[0]['question'] == 'What is AI?'

def test_get_answers(client):
    # Test with valid question
    response = client.post('/get_answers', json={'question': 'What is AI?'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'response' in data

    # Test with empty question
    response = client.post('/get_answers', json={'question': ''})
    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'No question provided'}

def test_index(client):
    # Test index route renders the homepage
    response = client.get('/')
    assert response.status_code == 200
    assert b'<form' in response.data  # Assuming your homepage contains a form
