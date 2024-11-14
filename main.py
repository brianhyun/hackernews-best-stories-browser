import os
import json
import requests 
import webbrowser
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_visited_stories():
    if os.path.exists('visited_stories.json'):
        with open('visited_stories.json', 'r') as f:
            content = f.read()

            if content:
                return set(json.loads(content))
            else:
                return set()
    else:
        return set()


def save_visited_stories(stories):
    with open('visited_stories.json', 'w') as f:
        json.dump(list(stories), f)


def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(
        input=text,
        model=model
    )

    return np.array(response['data'][0]['embedding'])



def compute_topic_similarity(text, favorite_topics):
    corpus = [text] + favorite_topics
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()
    similarity = cosine_similarity([vectors[0]], vectors[1:]).flatten()
    return similarity.mean() 


def load_favorite_topics(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    return " ".join(data["topics"])  # Combine topics into a single string


def get_best_stories():
    visited_stories = load_visited_stories()

    response = requests.get('https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty')
    best_stories = response.json()

    interests_text = load_favorite_topics("interests.json")
    interests_embedding = get_embedding(interests_text)

    story_urls = []

    for story in best_stories: 
        if story not in visited_stories:
            visited_stories.add(story)

            story_data = get_story_details(story)

            title = story_data.get('title', '')
            text = story_data.get('text', '')
            story_embedding = get_embedding(title + " " + text)
            similarity = cosine_similarity([interests_embedding], [story_embedding])[0][0]
            print(similarity)

            if story_data:
                story_urls.append(story_data['url'])
                
                if len(story_urls) == 5:
                    break

    if len(story_urls) < 5:
        return story_urls

    save_visited_stories(visited_stories)
    
    return story_urls

def get_story_details(story_url): 
    response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_url}.json?print=pretty')
    story_data = response.json()

    if story_data["url"]: 
        if "dead" in story_data and story_data["dead"]:
            return None 
        
        return story_data
    else: 
        return None

def main():
    best_stories = get_best_stories()

    # for story in best_stories:
    #     webbrowser.open(story)


if __name__ == "__main__":
    main()