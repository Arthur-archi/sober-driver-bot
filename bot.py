from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    return '✅ Webhook работает (POST)', 200

@app.route('/', methods=['GET'])
def index():
    return '✅ Webhook работает (GET)', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
