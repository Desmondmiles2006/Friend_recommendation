from flask import Flask, render_template, request
import networkx as nx

app = Flask(__name__)

# Create an empty graph
G = nx.Graph()

# Add more users (nodes)
users = [
    "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace",
    "Heidi", "Ivan", "Judy", "Mallory", "Niaj", "Oscar", "Peggy"
]

# Add nodes to the graph
G.add_nodes_from(users)

# Add more edges (friendships)
friendships = [
    ("Alice", "Bob"), ("Alice", "Charlie"), ("Alice", "Eve"),
    ("Bob", "Charlie"), ("Bob", "David"), ("Bob", "Eve"),
    ("Charlie", "David"), ("Charlie", "Frank"), ("Eve", "Grace"),
    ("David", "Grace"), ("Frank", "Heidi"), ("Grace", "Heidi"),
    ("Heidi", "Ivan"), ("Ivan", "Judy"), ("Judy", "Mallory"),
    ("Mallory", "Niaj"), ("Niaj", "Oscar"), ("Oscar", "Peggy")
]

# Add edges to the graph
G.add_edges_from(friendships)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/suggest_friends", methods=["POST"])
def suggest_friends():
    user = request.form["user"]
    if user not in G:
        return render_template("suggestions.html", user=user, suggestions=[], error=f"No such user '{user}' found in the network")

    mutual_friends = set()

    # Find mutual friends
    for friend in G.neighbors(user):
        for friend_of_friend in G.neighbors(friend):
            if friend_of_friend != user and friend_of_friend not in G.neighbors(user):
                mutual_friends.add(friend_of_friend)

    # Calculate similarity scores based on common friends
    similarity_scores = {}
    for friend_of_friend in mutual_friends:
        mutual_count = len(set(G.neighbors(user)) & set(G.neighbors(friend_of_friend)))
        similarity_scores[friend_of_friend] = mutual_count

    # Sort suggestions by similarity score
    ranked_suggestions = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

    return render_template("suggestions.html", user=user, suggestions=ranked_suggestions)

if __name__ == "__main__":
    app.run(debug=True)
