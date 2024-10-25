import requests
import sys

def get_todos(user_id=None):
    """Fetches and prints todos from JSONPlaceholder."""
    if user_id:
        response = requests.get(f'https://jsonplaceholder.typicode.com/todos?userId={user_id}')
    else:
        response = requests.get('https://jsonplaceholder.typicode.com/todos')
    todos = response.json()
    for todo in todos:
        print(f"ID: {todo['id']}, Title: {todo['title']}, Completed: {todo['completed']}")

def get_posts(user_id=None):
    """Fetches and prints posts from JSONPlaceholder."""
    if user_id:
        response = requests.get(f'https://jsonplaceholder.typicode.com/posts?userId={user_id}')
    else:
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json()
    for post in posts:
        print(f"ID: {post['id']}, Title: {post['title']}, Body: {post['body']}")

def get_comments(post_id=None):
    """Fetches and prints comments from JSONPlaceholder."""
    if post_id:
        response = requests.get(f'https://jsonplaceholder.typicode.com/comments?postId={post_id}')
    else:
        response = requests.get('https://jsonplaceholder.typicode.com/comments')
    comments = response.json()
    for comment in comments:
        print(f"ID: {comment['id']}, Name: {comment['name']}, Email: {comment['email']}")

def get_albums(user_id=None):
    """Fetches and prints albums from JSONPlaceholder."""
    if user_id:
        response = requests.get(f'https://jsonplaceholder.typicode.com/albums?userId={user_id}')
    else:
        response = requests.get('https://jsonplaceholder.typicode.com/albums')
    albums = response.json()
    for album in albums:
        print(f"ID: {album['id']}, Title: {album['title']}")

def get_photos(album_id=None):
    """Fetches and prints photos from JSONPlaceholder."""
    if album_id:
        response = requests.get(f'https://jsonplaceholder.typicode.com/photos?albumId={album_id}')
    else:
        response = requests.get('https://jsonplaceholder.typicode.com/photos')
    photos = response.json()
    for photo in photos:
        print(f"ID: {photo['id']}, Title: {photo['title']}, URL: {photo['url']}")

def get_users():
    """Fetches and prints users from JSONPlaceholder."""
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    users = response.json()
    for user in users:
        print(f"ID: {user['id']}, Name: {user['name']}, Username: {user['username']}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "todos":
            if len(sys.argv) > 2:
                try:
                    user_id = int(sys.argv[2])
                    get_todos(user_id)
                except ValueError:
                    print("Invalid user ID. Please provide an integer.")
            else:
                get_todos()
        elif command == "posts":
            if len(sys.argv) > 2:
                try:
                    user_id = int(sys.argv[2])
                    get_posts(user_id)
                except ValueError:
                    print("Invalid user ID. Please provide an integer.")
            else:
                get_posts()
        elif command == "comments":
            if len(sys.argv) > 2:
                try:
                    post_id = int(sys.argv[2])
                    get_comments(post_id)
                except ValueError:
                    print("Invalid post ID. Please provide an integer.")
            else:
                get_comments()
        elif command == "albums":
            if len(sys.argv) > 2:
                try:
                    user_id = int(sys.argv[2])
                    get_albums(user_id)
                except ValueError:
                    print("Invalid user ID. Please provide an integer.")
            else:
                get_albums()
        elif command == "photos":
            if len(sys.argv) > 2:
                try:
                    album_id = int(sys.argv[2])
                    get_photos(album_id)
                except ValueError:
                    print("Invalid album ID. Please provide an integer.")
            else:
                get_photos()
        elif command == "users":
            get_users()
        else:
            print("Invalid command.")
    else:
        print("Usage: python sdk.py [todos|posts|comments|albums|photos|users] [id]")