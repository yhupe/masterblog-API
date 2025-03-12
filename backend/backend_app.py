from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    new_post = request.get_json()

    if "title" not in new_post or len(new_post['title']) == 0:
        return jsonify({"error": "key 'title' must exist / can't be empty"}), 400

    elif "content" not in new_post or len(new_post['content']) == 0:
        return jsonify({"error": "key 'content' must exist / can't be empty"}), 400

    else:
        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id

        POSTS.append(new_post)
        print(f"Post with ID {new_id} added successfully.")
        return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
