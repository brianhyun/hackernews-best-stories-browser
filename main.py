import os
import json
import requests 
import webbrowser

def load_visited_stories():
    if os.path.exists('visited_stories.json'):
        with open('visited_stories.json', 'r') as f:
            return set(json.load(f))
    else:
        return set()


def save_visited_stories(stories):
    with open('visited_stories.json', 'w') as f:
        json.dump(list(stories), f)


def get_best_stories():
    visited_stories = load_visited_stories()

    response = requests.get('https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty')
    best_stories = response.json()

    story_urls = []

    for story in best_stories: 
        if story not in visited_stories:
            visited_stories.add(story)

            story_data = get_story_details(story)

            if story_data:
                story_urls.append(story_data['url'])
                
                if len(story_urls) == 10:
                    break

    if len(story_urls) < 10:
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

    for story in best_stories:
        webbrowser.open(story)


if __name__ == "__main__":
    main()