from flask import Flask, jsonify, request
import os
import socket
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask App on AWS ECS</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #FF9900;
            }
            .info {
                background-color: #f0f0f0;
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
            }
            .success {
                color: #28a745;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Flask App Successfully Deployed on AWS ECS! WITH GITHUB ACTIONS</h1>
            <p class="success">✓ Deployment Successful</p>
            
            <div class="info">
                <h3>Container Information:</h3>
                <p><strong>Hostname:</strong> ''' + socket.gethostname() + '''</p>
                <p><strong>Time:</strong> ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
                <p><strong>Environment:</strong> ''' + os.getenv('ENVIRONMENT', 'production') + '''</p>
            </div>
            
            <h3>Available Endpoints:</h3>
            <ul>
                <li><a href="/">/ - Home (this page)</a></li>
                <li><a href="/health">/health - Health check</a></li>
                <li><a href="/api/info">/api/info - API information</a></li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    """Health check endpoint for ALB"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'hostname': socket.gethostname()
    }), 200

@app.route('/api/info')
def info():
    """API endpoint with container information"""
    return jsonify({
        'application': 'Flask on AWS ECS',
        'version': '1.0.0',
        'hostname': socket.gethostname(),
        'timestamp': datetime.now().isoformat(),
        'environment': os.getenv('ENVIRONMENT', 'production'),
        'message': 'Application is running successfully!'
    })

@app.route('/api/echo', methods=['POST'])
def echo():
    """Echo endpoint for testing"""
    data = request.get_json()
    return jsonify({
        'received': data,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)