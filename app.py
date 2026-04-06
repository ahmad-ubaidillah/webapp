from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

users = {}
posts = {}


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return decorated


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/users", methods=["GET"])
@require_auth
def get_users():
    return jsonify(list(users.values()))


@app.route("/api/users", methods=["POST"])
@require_auth
def create_user():
    data = request.json
    user_id = len(users) + 1
    user = {"id": user_id, "name": data.get("name"), "email": data.get("email")}
    users[user_id] = user
    return jsonify(user), 201


@app.route("/api/users/<int:user_id>", methods=["GET"])
@require_auth
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
@require_auth
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return jsonify({"message": "User deleted"}), 200


@app.route("/api/posts", methods=["GET"])
def get_posts():
    return jsonify(list(posts.values()))


@app.route("/api/posts", methods=["POST"])
@require_auth
def create_post():
    data = request.json
    post_id = len(posts) + 1
    post = {
        "id": post_id,
        "title": data.get("title"),
        "content": data.get("content"),
        "author_id": data.get("author_id"),
    }
    posts[post_id] = post
    return jsonify(post), 201


@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = posts.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
