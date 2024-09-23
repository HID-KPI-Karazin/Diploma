import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import numpy as np
import logging
import time

nltk.download('stopwords')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CBRSystem:
    def __init__(self, google_sheets_client):
        self.google_sheets_client = google_sheets_client
        self.ukrainian_stop_words = self.load_ukrainian_stopwords()
        self.punctuation = set(string.punctuation)

    def load_ukrainian_stopwords(self):
        stopwords_path = 'C:/Users/Midna/Desktop/Diploma/ukrainian_stopwords.txt'
        with open(stopwords_path, 'r', encoding='utf-8') as file:
            stopwords_list = file.read().splitlines()
        return set(stopwords_list)

    def preprocess_text(self, text):
        tokens = nltk.word_tokenize(text)

        tokens = [word.lower() for word in tokens if word.isalpha()]
        tokens = [word for word in tokens if word not in self.ukrainian_stop_words and word not in self.punctuation]
        return ' '.join(tokens)
    def get_cases(self):
        records = self.google_sheets_client.get_all_records()
        cases = []
        for record in records:
            case = {
                'Problem Description': record['Problem Description'],
                'Solution': record['Solution'],
                'Date': record['Date'],
                'Tags': record['Tags']
            }
            cases.append(case)
        logger.info("Cases retrieved from Google Sheets: %s", cases)
        return cases

    def find_most_similar_case(self, problem_description, cases):
        start_time = time.time()

        processed_descriptions = [self.preprocess_text(case['Problem Description']) for case in cases]
        processed_problem = self.preprocess_text(problem_description)


        vectorizer = TfidfVectorizer().fit_transform(processed_descriptions + [processed_problem])
        vectors = vectorizer.toarray()
        similarity_matrix = cosine_similarity([vectors[-1]], vectors[:-1])
        most_similar_index = np.argmax(similarity_matrix)
        most_similar_case = cases[most_similar_index]

        search_time = time.time() - start_time
        logger.info("Processed descriptions: %s", processed_descriptions)
        logger.info("Similarity matrix: %s", similarity_matrix)
        logger.info("Most similar case index: %s", most_similar_index)
        logger.info("Search time: %s ms", search_time * 1000)

        return most_similar_case, search_time