@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = posts.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post)


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@require_auth
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    del users[user_id]
    return jsonify({'message': 'User deleted'}), 200
