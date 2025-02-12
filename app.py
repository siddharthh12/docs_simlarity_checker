from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import string
import os
import difflib

nltk.download('stopwords')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

def highlight_similar_words(doc1, doc2):
    words1 = doc1.split()
    words2 = doc2.split()
    matcher = difflib.SequenceMatcher(None, words1, words2)
    highlighted = []
    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == 'equal':
            highlighted.append(f'<span style="background-color: yellow;">{" ".join(words1[a0:a1])}</span>')
        else:
            highlighted.append(" ".join(words1[a0:a1]))
    return " ".join(highlighted)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_documents():
    if 'file1' in request.files and 'file2' in request.files:
        file1 = request.files['file1']
        file2 = request.files['file2']
        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'Please upload both files'}), 400
        
        doc1 = file1.read().decode('utf-8')
        doc2 = file2.read().decode('utf-8')
    else:
        data = request.json
        doc1 = data.get('doc1', '')
        doc2 = data.get('doc2', '')
    
    doc1_clean = preprocess_text(doc1)
    doc2_clean = preprocess_text(doc2)
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([doc1_clean, doc2_clean])
    similarity_score = round(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0] * 100, 2)
    
    highlighted_text = highlight_similar_words(doc1, doc2)
    
    return jsonify({'similarity_score': f'{similarity_score}%', 'highlighted_text': highlighted_text})

if __name__ == '__main__':
    app.run(debug=True)
