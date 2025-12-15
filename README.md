# Flask REST API

A CRUD REST API for managing anime, cartoons, and movies database with JWT authentication and XML/JSON response formats.

## Features

- **CRUD Operations**: Full Create, Read, Update, Delete for anime
- **Authentication**: JWT-based secure authentication
- **Multiple Formats**: JSON and XML response formats
- **Search Functionality**: Advanced search across all tables
- **Filtering**: Filter by various criteria (rating, year, episodes)
- **Testing**: Comprehensive test suite
- **Error Handling**: Proper HTTP status codes and error messages

## Installation
### 1. Clone the repository
git clone https://github.com/Shirajuana/Flask.git
cd Flask

### 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Configure MySQL
Import veluya_db.sql via a chosen MySQL connection:
1. In Navigator, click "Administration" tab
2. Click "Data Import/Restore"
3. Toggle "Import from Self-Contained File"
4. Navigate to dump.sql
5. Click "Start Import"

Create your .env file at Flask\.env:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=veluya_db
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

### 5. Run the server
python app.py

Server runs at:  http://127.0.0.1:5000


## Authentication
username: admin
password: admin123

## Login
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'


## Cartoons API

### Get all anime
curl http://127.0.0.1:5000/api/v1/anime

### Search anime
curl "http://127.0.0.1:5000/api/v1/anime?search=Naruto"

### Get specific anime
curl http://127.0.0.1:5000/api/v1/anime/Naruto

### Create anime
curl -X POST http://127.0.0.1:5000/api/v1/anime \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "Title": "Pikachu",
    "ReleaseYear": 2011,
    "Rating": 9.0
  }'

### Update anime with the token
 curl -X POST http://127.0.0.1:5000/api/v1/anime \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "Title": "Pikachu",
    "ReleaseYear": 2011,
    "Rating": 9.0
  }'

### Delete anime by title
curl -X DELETE "http://127.0.0.1:5000/api/v1/anime/Pikachu" \
  -H "Authorization: Bearer $TOKEN"

## Author
<div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 30px;">

<div style="flex: 1; min-width: 300px; border: 1px solid #444; border-radius: 10px; padding: 20px; background: #000; color: white;">
    <div style="text-align: center;">
        <a href="https://github.com/Shirajuana">
            <img src="https://github.com/Shirajuana.png" width="120" height="120" style="border-radius: 50%; border: 3px solid #fff;">
        </a>
    </div>
    <h3 style="text-align: center; margin-top: 15px; color: white;">SHEILA MAE VELUYA (Owner)</h3>
    <p style="text-align: center; margin: 10px 0; color: #ccc;">
        <strong>Email:</strong> 202380038@psu.palawan.edu.ph
    </p>
    <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
        <a href="https://github.com/Shirajuana" style="text-decoration: none;">
            <img src="https://img.shields.io/badge/-GitHub-181717?logo=github&logoColor=white&style=for-the-badge" alt="GitHub">
        </a>
        <a href="https://facebook.com/shielamae.veluya" style="text-decoration: none;">
            <img src="https://img.shields.io/badge/-Facebook-1877F2?logo=facebook&logoColor=white&style=for-the-badge" alt="Facebook">
        </a>
    </div>
</div>
