from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

LINKS_FILE = 'links.json'

# Ensure the links file exists
if not os.path.exists(LINKS_FILE):
    with open(LINKS_FILE, 'w') as file:
        json.dump([], file)

@app.route('/get-links', methods=['GET'])
def get_links():
    try:
        with open(LINKS_FILE, 'r') as file:
            links = json.load(file)
        return jsonify({"links": links}), 200
    except Exception as e:
        app.logger.error(f"Error loading links: {e}")
        return jsonify({"error": "Failed to load links"}), 500

@app.route('/add-link', methods=['POST'])
def add_link():
    data = request.get_json()
    if not data or 'title' not in data or 'url' not in data:
        return jsonify({"error": "Title and URL are required"}), 400

    try:
        with open(LINKS_FILE, 'r') as file:
            links = json.load(file)
        links.append({"title": data['title'], "url": data['url']})
        with open(LINKS_FILE, 'w') as file:
            json.dump(links, file, indent=2)
        return jsonify({"message": "Link added successfully"}), 201
    except Exception as e:
        app.logger.error(f"Error saving link: {e}")
        return jsonify({"error": "Failed to save link"}), 500

@app.route('/delete-link', methods=['DELETE'])
def delete_link():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400

    try:
        with open(LINKS_FILE, 'r') as file:
            links = json.load(file)

        links = [link for link in links if link['url'] != data['url']]  # Remove link by URL

        with open(LINKS_FILE, 'w') as file:
            json.dump(links, file, indent=2)

        return jsonify({"message": "Link deleted successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error deleting link: {e}")
        return jsonify({"error": "Failed to delete link"}), 500

@app.route('/edit-link', methods=['PUT'])
def edit_link():
    data = request.get_json()
    if not data or 'old_url' not in data or 'new_title' not in data or 'new_url' not in data:
        return jsonify({"error": "Old URL, new title, and new URL are required"}), 400

    try:
        with open(LINKS_FILE, 'r') as file:
            links = json.load(file)

        for link in links:
            if link['url'] == data['old_url']:
                link['title'] = data['new_title']
                link['url'] = data['new_url']
                break

        with open(LINKS_FILE, 'w') as file:
            json.dump(links, file, indent=2)

        return jsonify({"message": "Link edited successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error editing link: {e}")
        return jsonify({"error": "Failed to edit link"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)