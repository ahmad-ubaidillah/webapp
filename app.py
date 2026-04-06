@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = posts.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post)
