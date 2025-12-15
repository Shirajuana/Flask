import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestAnimeAPI:
    """Test cases for Anime endpoints"""
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_get_all_anime(self, client):
        """Test GET /api/v1/anime"""
        response = client.get('/api/v1/anime')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert 'data' in data
        assert isinstance(data['data'], list)
    
    def test_get_anime_by_title(self, client):
        """Test GET /api/v1/anime/{title}"""
        response = client.get('/api/v1/anime/Attack%20on%20Titan')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['Title'] == 'Attack on Titan'
    
    def test_get_nonexistent_anime(self, client):
        """Test GET non-existent anime"""
        response = client.get('/api/v1/anime/NonexistentAnime')
        assert response.status_code == 404
    
    def test_search_anime(self, client):
        """Test search functionality"""
        response = client.get('/api/v1/anime?search=Titan')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['data']) > 0
    
    def test_filter_anime_by_rating(self, client):
        """Test filter by rating"""
        response = client.get('/api/v1/anime?min_rating=9.0')
        assert response.status_code == 200
        data = json.loads(response.data)
        for anime in data['data']:
            assert float(anime['Rating']) >= 9.0
    
    def test_xml_format(self, client):
        """Test XML response format"""
        response = client.get('/api/v1/anime?format=xml')
        assert response.status_code == 200
        assert 'application/xml' in response.content_type
    
    def test_json_format_default(self, client):
        """Test JSON response format (default)"""
        response = client.get('/api/v1/anime')
        assert response.status_code == 200
        assert 'application/json' in response.content_type

class TestCartoonsAPI:
    """Test cases for Cartoons endpoints"""
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_get_all_cartoons(self, client):
        """Test GET /api/v1/cartoons"""
        response = client.get('/api/v1/cartoons')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert 'data' in data
    
    def test_get_cartoon_by_id(self, client):
        """Test GET /api/v1/cartoons/{id}"""
        response = client.get('/api/v1/cartoons/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['Title'] == 'SpongeBob SquarePants'

class TestMoviesAPI:
    """Test cases for Movies endpoints"""
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_get_all_movies(self, client):
        """Test GET /api/v1/movies"""
        response = client.get('/api/v1/movies')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert 'data' in data
    
    def test_search_movies(self, client):
        """Test movie search"""
        response = client.get('/api/v1/movies?search=Dark')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['data']) > 0

class TestSearchAPI:
    """Test cases for Search endpoints"""
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_global_search(self, client):
        """Test global search endpoint"""
        response = client.get('/api/v1/search?q=Titan')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total_results' in data
        assert 'data' in data
    
    def test_empty_search(self, client):
        """Test search with empty query"""
        response = client.get('/api/v1/search?q=')
        assert response.status_code == 400

class TestAuthentication:
    """Test cases for Authentication"""
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_login_success(self, client):
        """Test successful login"""
        response = client.post('/api/v1/auth/login',
                              json={'username': 'admin', 'password': 'admin123'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
    
    def test_login_failure(self, client):
        """Test failed login"""
        response = client.post('/api/v1/auth/login',
                              json={'username': 'admin', 'password': 'wrong'})
        assert response.status_code == 401
    
    def test_register_user(self, client):
        """Test user registration"""
        response = client.post('/api/v1/auth/register',
                              json={'username': 'testuser', 'password': 'test123'})
        assert response.status_code == 201

if __name__ == '__main__':
    pytest.main([__file__, '-v'])