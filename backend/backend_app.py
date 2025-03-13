from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Third post", "content": "This is the third post."},
    {"id": 4, "title": "Fourth post", "content": "This is the fourth post."},
    {"id": 5, "title": "Fifth post", "content": "This is the fifth post."},
    {"id": 6, "title": "Sixth post", "content": "This is the sixth post."}
]

def find_post_by_id(post_id: int) -> dict:

    post = next((post for post in POSTS if post["id"] == post_id), None)

    return post


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


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):

    post = find_post_by_id(id)

    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    else:
        POSTS.remove(post)
        print(f"Post with id {id} has been deleted successfully.")
        return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):

    post = find_post_by_id(id)

    data = request.get_json()
    updated_title = data.get('title', None)
    updated_content = data.get('content', None)

    # checking that 'old' post exists
    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    # checking that either updated_title or updated_content exists
    if updated_title is None and updated_content is None:
        return jsonify({"error": f"Neither 'title' nor 'content' has been changed due to missing or wrong input"}), 400

    # checking if only one value has been requested to update
    if 'title' in data and 'content' not in data:
        post['title'] = updated_title
        print(f"Post title has been updated successfully.")
        return jsonify(post), 200

    elif 'content' in data and 'title' not in data:
        post['content'] = updated_content
        print(f"Post content has been updated successfully.")
        return jsonify(post), 200

    # checking if both values have been requested to update
    elif 'content' in data and 'title' in data:
        post.update(data)
        print(f"Post title and content have been updated successfully.")
        return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_in_posts():

    title = request.args.get('title', None)
    content = request.args.get('content', None)

    list_of_matches = []

    # checking that either one of the search terms exist
    if title is None and content is None:
        return jsonify({"error": f"Bad search input, can only search for 'title' and 'content'"}), 404

    # checking if search term for title exists - looking for matches in db, not case-sensitive
    if title is not None:
        for post in POSTS:
            if title.lower() in post['title'].lower():
                list_of_matches.append(post)

    # checking if search term for content exists - looking for matches in db, not case-sensitive
    if content is not None:
        for post in POSTS:
            if content.lower() in post['content'].lower():
                list_of_matches.append(post)

    if len(list_of_matches) > 0:

        #removing redundant posts
        tuple_of_matches = tuple(list_of_matches)

        return jsonify(tuple_of_matches), 200

    else:
        return jsonify({"Notice": f"Nothing found for '{title}' or '{content}'"}), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
