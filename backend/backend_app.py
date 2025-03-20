from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
from storage import storage_handler


app = Flask(__name__)

#enable CORS for all routes
CORS(app)

SWAGGER_URL="/api/docs"
API_URL="/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/api/posts/', methods=['GET'])
def get_posts():
    """ Directing to this endpoint via GET request, all posts from storage
    are returned in default order. By adding query parameters to the url,
    the function will sort by certain values in either
    descending or ascending order. """

    blogposts = storage_handler.load_json_posts('backend/storage/blogposts.json')

    sort = request.args.get('sort', None)
    direction = request.args.get('direction', None)

    # returning the database with all posts as it is, if no query parameter found
    if sort is None and direction is None:
        return jsonify(blogposts)

    else:

        #defining the sorting when the right query parameters are found
        if sort == 'title' and direction == 'asc':
            sorted_posts_by_title = sorted(blogposts, key=lambda x: x["title"],
                                           reverse=False)
            return jsonify(sorted_posts_by_title), 200

        elif sort == 'title' and direction == 'desc':
            sorted_posts_by_title = sorted(blogposts, key=lambda x: x["title"],
                                           reverse=True)
            return jsonify(sorted_posts_by_title), 200

        elif sort == 'content' and direction == 'asc':
            sorted_posts_by_content = sorted(blogposts, key=lambda x: x["content"],
                                             reverse=False)
            return jsonify(sorted_posts_by_content), 200

        elif sort == 'content' and direction == 'desc':
            sorted_posts_by_content = sorted(blogposts, key=lambda x: x["title"],
                                             reverse=False)
            return jsonify(sorted_posts_by_content), 200

        elif sort == 'author' and direction == 'asc':
            sorted_posts_by_title = sorted(blogposts, key=lambda x: x["author"],
                                           reverse=False)
            return jsonify(sorted_posts_by_title), 200

        elif sort == 'author' and direction == 'desc':
            sorted_posts_by_title = sorted(blogposts, key=lambda x: x["author"],
                                           reverse=True)
            return jsonify(sorted_posts_by_title), 200

        # sorting by date --> with datetime instead of alphabet
        elif sort == 'date' and direction == 'asc':
            sorted_posts_by_title = sorted(blogposts, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=False)
            return jsonify(sorted_posts_by_title), 200

        elif sort == 'date' and direction == 'desc':
            sorted_posts_by_title = sorted(blogposts, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
            return jsonify(sorted_posts_by_title), 200

        # if only one of the two parameters is used or parameters other than 'sort' and 'direction' are used:
        else:
            return jsonify({"message": f"Sorting by these parameters "
                                       f"or only one parameter is not possible."}), 404


@app.route('/api/posts', methods=['POST'])
def add_post():
    """ Navigating to this endpoint via POST request, new posts
    can be added to the database by following a given format
    in the POST request body. All appended posts will get a
    unique identifier (id)"""

    blogposts = storage_handler.load_json_posts('backend/storage/blogposts.json')
    new_post = request.get_json()

    if "title" not in new_post or len(new_post['title']) == 0:
        return jsonify({"error": "key 'title' must exist / can't be empty"}), 400

    elif "content" not in new_post or len(new_post['content']) == 0:
        return jsonify({"error": "key 'content' must exist / can't be empty"}), 400

    else:
        new_id = max(post['id'] for post in blogposts) + 1
        new_post['id'] = new_id

        blogposts.append(new_post)
        storage_handler.save_json_posts('backend/storage/blogposts.json', blogposts)
        print(f"Post with ID {new_id} added successfully.")
        return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """ Via DELETE request, the unique ID as passed in the url
     identifies the post to be deleted from the database. """

    blogposts = storage_handler.load_json_posts('backend/storage/blogposts.json')
    post = storage_handler.find_post_by_id(id, blogposts)

    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    else:
        blogposts.remove(post)
        storage_handler.save_json_posts('backend/storage/blogposts.json', blogposts)
        print(f"Post with id {id} has been deleted successfully.")
        return jsonify({"message": f"Post with id {id} has been deleted "
                                   f"successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """ The unique ID passed along with the PUT request leads to
    first changing and then saving changed attributes of the blog post,
    if the user follows a certain format in the PUT request body.
    It can be that only one or up to all four post attributes
    such as title, author, content and date can be changed and updated."""

    blogposts = storage_handler.load_json_posts('backend/storage/blogposts.json')
    post = storage_handler.find_post_by_id(id, blogposts)

    data = request.get_json()
    updated_title = data.get('title', None)
    updated_content = data.get('content', None)
    updated_author = data.get('author', None)
    updated_date = data.get('date', None)

    # checking that 'old' post exists
    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    # checking that at least one field is provided for update
    if not any([updated_title, updated_content, updated_author, updated_date]):
        return jsonify({"error": "No valid fields provided for update"}), 400

    # updating provided fields
    if updated_title is not None:
        post['title'] = updated_title

    if updated_content is not None:
        post['content'] = updated_content

    if updated_author is not None:
        post['author'] = updated_author

    if updated_date is not None:
        post['date'] = updated_date

    storage_handler.save_json_posts('backend/storage/blogposts.json', blogposts)
    print(f"Post with id {id} has been updated successfully.")
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_in_posts():
    """ By passing certain keywords as query parameter to this endpoint, the
    return will be a json-ified list of all posts matching the search criteria
    as passed in within the query parameter"""

    blogposts = storage_handler.load_json_posts('backend/storage/blogposts.json')

    title = request.args.get('title', None)
    content = request.args.get('content', None)
    author = request.args.get('author', None)
    date = request.args.get('date', None)

    list_of_matches = []

    # checking that either one of the search terms exist
    if not any([title, content, author, date]):
        return jsonify({"error": f"Bad search input, can only search "
                                 f"for 'title', 'content', 'author' and 'date'"}), 404

    # checking if search term for title exists - looking for matches in db, not case-sensitive
    if title is not None:
        for post in blogposts:
            if title.lower() in post['title'].lower():
                list_of_matches.append(post)

    # checking if search term for content exists - looking for matches in db, not case-sensitive
    if content is not None:
        for post in blogposts:
            if content.lower() in post['content'].lower():
                list_of_matches.append(post)

    # checking if search term for author exists - looking for matches in db, not case-sensitive
    if author is not None:
        for post in blogposts:
            if author.lower() in post['author'].lower():
                list_of_matches.append(post)

    # checking if search term for date exists - looking for matches in db, not case-sensitive
    if date is not None:
        for post in blogposts:
            if date in post['date']:
                list_of_matches.append(post)

    if len(list_of_matches) > 0:

        #removing redundant posts
        tuple_of_matches = tuple(list_of_matches)

        matching_posts = list(tuple_of_matches)

        return jsonify(matching_posts), 200

    else:
        return jsonify(list_of_matches), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
