from flask import request, jsonify
from flask_cors import cross_origin
import json

def load(app):
    # Endpoint: GET /words with pagination (50 words per page)
    @app.route('/words', methods=['GET'])
    @cross_origin()
    def get_words():
        try:
            cursor = app.db.cursor()

            # Get the current page number from query parameters (default is 1)
            page = int(request.args.get('page', 1))
            page = max(1, page)  # Ensure page number is positive
            words_per_page = 50
            offset = (page - 1) * words_per_page

            # Get sorting parameters from the query string
            sort_by = request.args.get('sort_by', 'catalan')  # Default sorting
            order = request.args.get('order', 'asc')  # Default ordering

            # Validate sorting
            valid_columns = ['catalan', 'english', 'correct_count', 'wrong_count']
            if sort_by not in valid_columns:
                sort_by = 'catalan'
            if order not in ['asc', 'desc']:
                order = 'asc'

            # Query to fetch words and aggregate review counts from word_review_items
            cursor.execute(f'''
                SELECT 
                    w.id, 
                    w.catalan, 
                    w.english,
                    COALESCE(SUM(i.correct_count), 0) AS correct_count,
                    COALESCE(COUNT(i.id) - SUM(i.correct_count), 0) AS wrong_count
                FROM words w
                LEFT JOIN word_review_items i ON w.id = i.word_id
                GROUP BY w.id
                ORDER BY {sort_by} {order}
                LIMIT ? OFFSET ?
            ''', (words_per_page, offset))

            words = cursor.fetchall()

            # Query the total number of words for pagination
            cursor.execute('SELECT COUNT(*) FROM words')
            total_words = cursor.fetchone()[0]
            total_pages = (total_words + words_per_page - 1) // words_per_page

            # Format the response
            words_data = [
                {
                    "id": word["id"],
                    "catalan": word["catalan"],
                    "english": word["english"],
                    "correct_count": word["correct_count"],
                    "wrong_count": word["wrong_count"]
                }
                for word in words
            ]

            return jsonify({
                "words": words_data,
                "total_pages": total_pages,
                "current_page": page,
                "total_words": total_words
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Endpoint: GET /words/:id to get a single word with its details
    @app.route('/words/<int:word_id>', methods=['GET'])
    @cross_origin()
    def get_word(word_id):
        try:
            cursor = app.db.cursor()
            
            # Fetch the word details with aggregated review counts
            cursor.execute('''
                SELECT 
                    w.id, 
                    w.catalan, 
                    w.english,
                    COALESCE(SUM(i.correct_count), 0) AS correct_count,
                    COALESCE(COUNT(i.id) - SUM(i.correct_count), 0) AS wrong_count,
                    GROUP_CONCAT(g.id || '::' || g.name, ',') AS groups
                FROM words w
                LEFT JOIN word_review_items i ON w.id = i.word_id
                LEFT JOIN word_groups wg ON w.id = wg.word_id
                LEFT JOIN groups g ON wg.group_id = g.id
                WHERE w.id = ?
                GROUP BY w.id
            ''', (word_id,))

            word = cursor.fetchone()
            if not word:
                return jsonify({"error": "Word not found"}), 404

            # Parse groups into a list
            groups = []
            if word["groups"]:
                for group_str in word["groups"].split(','):
                    group_id, group_name = group_str.split('::')
                    groups.append({"id": int(group_id), "name": group_name})

            return jsonify({
                "word": {
                    "id": word["id"],
                    "catalan": word["catalan"],
                    "english": word["english"],
                    "correct_count": word["correct_count"],
                    "wrong_count": word["wrong_count"],
                    "groups": groups
                }
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500
