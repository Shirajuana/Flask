from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import mysql.connector
from mysql.connector import Error
import json
import xmltodict
from auth import AuthManager
from utils import DatabaseConnection, ResponseFormatter
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize JWT
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
jwt = JWTManager(app)
# Error handlers
@app.errorhandler(404)
def not_found(error):
    return ResponseFormatter.format_response(
        {'error': 'Resource not found', 'status': 404}, 
        request.args.get('format', 'json')
    )[0], 404

@app.errorhandler(500)
def internal_error(error):
    return ResponseFormatter.format_response(
        {'error': 'Internal server error', 'status': 500}, 
        request.args.get('format', 'json')
    )[0], 500

@app.errorhandler(400)
def bad_request(error):
    return ResponseFormatter.format_response(
        {'error': 'Bad request', 'status': 400}, 
        request.args.get('format', 'json')
    )[0], 400

# ============ AUTHENTICATION ENDPOINTS ============

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """User login endpoint - FIXED VERSION"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Simple authentication (replace with your actual auth logic)
        users = {
            "admin": {"password": "admin123", "role": "admin"},
            "user": {"password": "user123", "role": "user"}
        }
        
        user = users.get(username)
        if user and user['password'] == password:
            # FIX: Identity MUST be a string, not a dictionary
            access_token = create_access_token(identity=username)
            
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': {
                    'username': username,
                    'role': user['role']
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': f'Login error: {str(e)}'}), 500

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return ResponseFormatter.format_response(
                {'error': 'Username and password required'}, 
                request.args.get('format', 'json')
            )[0], 400
        
        success, message = AuthManager.register_user(
            data['username'], 
            data['password'],
            data.get('role', 'user')
        )
        
        if success:
            return ResponseFormatter.format_response(
                {'message': message}, 
                request.args.get('format', 'json')
            )[0], 201
        else:
            return ResponseFormatter.format_response(
                {'error': message}, 
                request.args.get('format', 'json')
            )[0], 400
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

# ============ ANIME ENDPOINTS ============

@app.route(f'/api/{Config.API_VERSION}/anime', methods=['GET'])
def get_all_anime():
    """Get all anime records"""
    try:
        format_type = request.args.get('format', 'json')
        search = request.args.get('search', '')
        min_rating = request.args.get('min_rating')
        max_rating = request.args.get('max_rating')
        year = request.args.get('year')
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Build query with filters
        query = "SELECT * FROM anime WHERE 1=1"
        params = []
        
        if search:
            query += " AND Title LIKE %s"
            params.append(f"%{search}%")
        
        if min_rating:
            query += " AND Rating >= %s"
            params.append(float(min_rating))
        
        if max_rating:
            query += " AND Rating <= %s"
            params.append(float(max_rating))
        
        if year:
            query += " AND ReleaseYear = %s"
            params.append(int(year))
        
        query += " ORDER BY Title"
        
        cursor.execute(query, params)
        anime_list = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        response, content_type = ResponseFormatter.format_response(
            {
                'status': 'success',
                'count': len(anime_list),
                'data': anime_list
            },
            format_type
        )
        
        return make_response(response, 200, {'Content-Type': content_type})
        
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

@app.route(f'/api/{Config.API_VERSION}/anime/<string:title>', methods=['GET'])
def get_anime(title):
    """Get specific anime by title"""
    try:
        format_type = request.args.get('format', 'json')
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM anime WHERE Title = %s", (title,))
        anime = cursor.fetchone()
        
        # FIX: Consume any remaining unread results
        try:
            cursor.fetchall()  # Consume any remaining results
        except mysql.connector.errors.InterfaceError:
            pass  # No more results to fetch
        
        cursor.close()
        connection.close()
        
        if anime:
            response, content_type = ResponseFormatter.format_response(
                {
                    'status': 'success',
                    'data': anime
                },
                format_type
            )
            return make_response(response, 200, {'Content-Type': content_type})
        else:
            return ResponseFormatter.format_response(
                {'error': 'Anime not found'}, format_type
            )[0], 404
            
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

@app.route(f'/api/{Config.API_VERSION}/anime', methods=['POST'])
@jwt_required()
def create_anime():
    """Create new anime record"""
    try:
        format_type = request.args.get('format', 'json')
        data = request.get_json()
        
        # Input validation
        if not data or 'Title' not in data:
            return ResponseFormatter.format_response(
                {'error': 'Title is required'}, format_type
            )[0], 400
        
        title = data['Title'].strip()
        release_year = data.get('ReleaseYear')
        rating = data.get('Rating')
        
        # Validate rating
        if rating is not None:
            try:
                rating = float(rating)
                if not (0 <= rating <= 10):
                    return ResponseFormatter.format_response(
                        {'error': 'Rating must be between 0 and 10'}, format_type
                    )[0], 400
            except ValueError:
                return ResponseFormatter.format_response(
                    {'error': 'Invalid rating format'}, format_type
                )[0], 400
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor()
        
        # Check if anime already exists
        cursor.execute("SELECT Title FROM anime WHERE Title = %s", (title,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return ResponseFormatter.format_response(
                {'error': 'Anime already exists'}, format_type
            )[0], 409
        
        # Insert new anime
        cursor.execute(
            "INSERT INTO anime (Title, ReleaseYear, Rating) VALUES (%s, %s, %s)",
            (title, release_year, rating)
        )
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return ResponseFormatter.format_response(
            {
                'status': 'success',
                'message': 'Anime created successfully',
                'data': {
                    'Title': title,
                    'ReleaseYear': release_year,
                    'Rating': rating
                }
            },
            format_type
        )[0], 201
        
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

@app.route(f'/api/{Config.API_VERSION}/anime/<string:title>', methods=['PUT'])
@jwt_required()
def update_anime(title):
    """Update anime record"""
    try:
        format_type = request.args.get('format', 'json')
        data = request.get_json()
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Check if anime exists
        cursor.execute("SELECT * FROM anime WHERE Title = %s", (title,))
        existing_anime = cursor.fetchone()
        
        if not existing_anime:
            cursor.close()
            connection.close()
            return ResponseFormatter.format_response(
                {'error': 'Anime not found'}, format_type
            )[0], 404
        
        # Update fields
        new_title = data.get('Title', existing_anime['Title'])
        release_year = data.get('ReleaseYear', existing_anime['ReleaseYear'])
        rating = data.get('Rating', existing_anime['Rating'])
        
        # Validate rating
        if rating is not None:
            try:
                rating = float(rating)
                if not (0 <= rating <= 10):
                    return ResponseFormatter.format_response(
                        {'error': 'Rating must be between 0 and 10'}, format_type
                    )[0], 400
            except ValueError:
                return ResponseFormatter.format_response(
                    {'error': 'Invalid rating format'}, format_type
                )[0], 400
        
        # FIX: Consume any unread results before executing another query
        try:
            # Try to fetch any remaining results from the previous query
            cursor.fetchall()
        except mysql.connector.errors.InterfaceError:
            # No more results to fetch, which is fine
            pass
        
        # Now execute the UPDATE query
        cursor.execute(
            "UPDATE anime SET Title = %s, ReleaseYear = %s, Rating = %s WHERE Title = %s",
            (new_title, release_year, rating, title)
        )
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return ResponseFormatter.format_response(
            {
                'status': 'success',
                'message': 'Anime updated successfully',
                'data': {
                    'Title': new_title,
                    'ReleaseYear': release_year,
                    'Rating': rating
                }
            },
            format_type
        )[0], 200
        
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

@app.route(f'/api/{Config.API_VERSION}/anime/<string:title>', methods=['DELETE'])
@jwt_required()
def delete_anime(title):
    """Delete anime record"""
    try:
        format_type = request.args.get('format', 'json')
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor()
        
        # Check if anime exists
        cursor.execute("SELECT Title FROM anime WHERE Title = %s", (title,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            return ResponseFormatter.format_response(
                {'error': 'Anime not found'}, format_type
            )[0], 404
        
        # Delete anime
        cursor.execute("DELETE FROM anime WHERE Title = %s", (title,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return ResponseFormatter.format_response(
            {
                'status': 'success',
                'message': 'Anime deleted successfully'
            },
            format_type
        )[0], 200
        
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

# ============ CARTOONS ENDPOINTS ============

@app.route(f'/api/{Config.API_VERSION}/cartoons', methods=['GET'])
def get_all_cartoons():
    """Get all cartoons"""
    try:
        format_type = request.args.get('format', 'json')
        search = request.args.get('search', '')
        min_episodes = request.args.get('min_episodes')
        max_episodes = request.args.get('max_episodes')
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Build query with filters
        query = "SELECT * FROM cartoons WHERE 1=1"
        params = []
        
        if search:
            query += " AND Title LIKE %s"
            params.append(f"%{search}%")
        
        if min_episodes:
            query += " AND Episode >= %s"
            params.append(int(min_episodes))
        
        if max_episodes:
            query += " AND Episode <= %s"
            params.append(int(max_episodes))
        
        query += " ORDER BY Title"
        
        cursor.execute(query, params)
        cartoons = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        response, content_type = ResponseFormatter.format_response(
            {
                'status': 'success',
                'count': len(cartoons),
                'data': cartoons
            },
            format_type
        )
        
        return make_response(response, 200, {'Content-Type': content_type})
        
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

@app.route(f'/api/{Config.API_VERSION}/cartoons/<int:cartoon_id>', methods=['GET'])
def get_cartoon(cartoon_id):
    """Get specific cartoon by ID"""
    try:
        format_type = request.args.get('format', 'json')
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cartoons WHERE cartoon_id = %s", (cartoon_id,))
        cartoon = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if cartoon:
            response, content_type = ResponseFormatter.format_response(
                {
                    'status': 'success',
                    'data': cartoon
                },
                format_type
            )
            return make_response(response, 200, {'Content-Type': content_type})
        else:
            return ResponseFormatter.format_response(
                {'error': 'Cartoon not found'}, format_type
            )[0], 404
            
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

# ============ MOVIES ENDPOINTS ============

@app.route(f'/api/{Config.API_VERSION}/movies', methods=['GET'])
def get_all_movies():
    """Get all movies"""
    try:
        format_type = request.args.get('format', 'json')
        search = request.args.get('search', '')
        start_year = request.args.get('start_year')
        end_year = request.args.get('end_year')
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Build query with filters
        query = "SELECT * FROM movies WHERE 1=1"
        params = []
        
        if search:
            query += " AND Title LIKE %s"
            params.append(f"%{search}%")
        
        if start_year:
            query += " AND ReleaseYear >= %s"
            params.append(int(start_year))
        
        if end_year:
            query += " AND ReleaseYear <= %s"
            params.append(int(end_year))
        
        query += " ORDER BY Title"
        
        cursor.execute(query, params)
        movies = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        response, content_type = ResponseFormatter.format_response(
            {
                'status': 'success',
                'count': len(movies),
                'data': movies
            },
            format_type
        )
        
        return make_response(response, 200, {'Content-Type': content_type})
        
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

@app.route(f'/api/{Config.API_VERSION}/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get specific movie by ID"""
    try:
        format_type = request.args.get('format', 'json')
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies WHERE Mies_id = %s", (movie_id,))
        movie = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if movie:
            response, content_type = ResponseFormatter.format_response(
                {
                    'status': 'success',
                    'data': movie
                },
                format_type
            )
            return make_response(response, 200, {'Content-Type': content_type})
        else:
            return ResponseFormatter.format_response(
                {'error': 'Movie not found'}, format_type
            )[0], 404
            
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

# ============ SEARCH ENDPOINTS ============

@app.route(f'/api/{Config.API_VERSION}/search', methods=['GET'])
def search_all():
    """Search across all tables"""
    try:
        format_type = request.args.get('format', 'json')
        query = request.args.get('q', '')
        
        if not query:
            return ResponseFormatter.format_response(
                {'error': 'Search query required'}, format_type
            )[0], 400
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor(dictionary=True)
        results = {}
        
        # Search anime
        cursor.execute("SELECT Title, ReleaseYear, Rating FROM anime WHERE Title LIKE %s", (f"%{query}%",))
        results['anime'] = cursor.fetchall()
        
        # Search cartoons
        cursor.execute("SELECT cartoon_id, Title, Episode FROM cartoons WHERE Title LIKE %s", (f"%{query}%",))
        results['cartoons'] = cursor.fetchall()
        
        # Search movies
        cursor.execute("SELECT Mies_id, Title, ReleaseYear FROM movies WHERE Title LIKE %s", (f"%{query}%",))
        results['movies'] = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        # Calculate totals
        total_results = sum(len(v) for v in results.values())
        
        response, content_type = ResponseFormatter.format_response(
            {
                'status': 'success',
                'query': query,
                'total_results': total_results,
                'data': results
            },
            format_type
        )
        
        return make_response(response, 200, {'Content-Type': content_type})
        
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500

# ============ STATISTICS ENDPOINT ============

@app.route(f'/api/{Config.API_VERSION}/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        format_type = request.args.get('format', 'json')
        
        connection = DatabaseConnection.get_connection()
        if not connection:
            return ResponseFormatter.format_response(
                {'error': 'Database connection failed'}, format_type
            )[0], 500
        
        cursor = connection.cursor(dictionary=True)
        stats = {}
        
        # Anime stats
        cursor.execute("SELECT COUNT(*) as count, AVG(Rating) as avg_rating FROM anime")
        anime_stats = cursor.fetchone()
        stats['anime'] = anime_stats
        
        # Cartoons stats
        cursor.execute("SELECT COUNT(*) as count, AVG(Episode) as avg_episodes FROM cartoons")
        cartoons_stats = cursor.fetchone()
        stats['cartoons'] = cartoons_stats
        
        # Movies stats
        cursor.execute("SELECT COUNT(*) as count, MIN(ReleaseYear) as oldest, MAX(ReleaseYear) as newest FROM movies")
        movies_stats = cursor.fetchone()
        stats['movies'] = movies_stats
        
        cursor.close()
        connection.close()
        
        response, content_type = ResponseFormatter.format_response(
            {
                'status': 'success',
                'data': stats
            },
            format_type
        )
        
        return make_response(response, 200, {'Content-Type': content_type})
        
    except Exception as e:
        return ResponseFormatter.format_response(
            {'error': str(e)}, 
            request.args.get('format', 'json')
        )[0], 500
    
@app.route('/')
def index():
    """Root endpoint with API documentation"""
    documentation = {
        'message': 'VELUYA Database REST API',
        'version': Config.API_VERSION,
        'endpoints': {
            'authentication': {
                'login': 'POST /api/v1/auth/login',
                'register': 'POST /api/v1/auth/register'
            },
            'anime': {
                'get_all': 'GET /api/v1/anime',
                'get_by_title': 'GET /api/v1/anime/<title>',
                'create': 'POST /api/v1/anime (requires auth)',
                'update': 'PUT /api/v1/anime/<title> (requires auth)',
                'delete': 'DELETE /api/v1/anime/<title> (requires auth)'
            },
            'cartoons': {
                'get_all': 'GET /api/v1/cartoons',
                'get_by_id': 'GET /api/v1/cartoons/<id>'
            },
            'movies': {
                'get_all': 'GET /api/v1/movies',
                'get_by_id': 'GET /api/v1/movies/<id>'
            },
            'search': 'GET /api/v1/search?q=<query>',
            'statistics': 'GET /api/v1/stats'
        },
        'formats': 'Add ?format=xml for XML, ?format=json for JSON (default)'
    }
    return jsonify(documentation), 200

@app.route('/api')
def api_index():
    """API base endpoint"""
    return jsonify({
        'message': 'VELUYA Database API',
        'version': Config.API_VERSION,
        'documentation': '/',
        'endpoints': '/api/v1/'
    }), 200

@app.route('/api/v1')
def api_v1_index():
    """API v1 endpoint"""
    return jsonify({
        'message': 'VELUYA Database API v1',
        'endpoints': {
            'anime': '/api/v1/anime',
            'cartoons': '/api/v1/cartoons',
            'movies': '/api/v1/movies',
            'search': '/api/v1/search',
            'stats': '/api/v1/stats',
            'auth': {
                'login': '/api/v1/auth/login',
                'register': '/api/v1/auth/register'
            }
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)