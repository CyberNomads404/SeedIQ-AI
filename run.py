from src.main.server.server import app

server_app = app

if __name__ == '__main__':
    server_app.run(host='0.0.0.0', port=3000, debug=True)
