import mysql.connector
from mysql.connector import Error
import json
import xmltodict
from config import Config

class DatabaseConnection:
    """Database connection handler"""
    
    @staticmethod
    def get_connection():
        """Create database connection"""
        try:
            connection = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

class ResponseFormatter:
    """Format response as JSON or XML"""
    
    @staticmethod
    def format_response(data, format_type='json'):
        """Format response based on requested format"""
        if format_type.lower() == 'xml':
            # Convert to XML
            if isinstance(data, dict):
                xml_data = xmltodict.unparse({'response': data}, pretty=True)
            elif isinstance(data, list):
                xml_data = xmltodict.unparse({'response': {'items': data}}, pretty=True)
            else:
                xml_data = xmltodict.unparse({'response': {'message': str(data)}}, pretty=True)
            return xml_data, 'application/xml'
        else:
            # Default to JSON
            return json.dumps(data, default=str), 'application/json'