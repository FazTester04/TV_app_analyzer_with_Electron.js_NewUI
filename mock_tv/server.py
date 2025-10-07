from flask import Flask, jsonify, request
import time

app = Flask(__name__)

@app.route('/')
def home():
    return """<html><head><title>Mock TV API Server</title></head><body><h1>Mock TV API Server</h1><p>Use /power, /app/launch, /app/play, /status</p></body></html>"""

state = {
    "power": False,
    "volume": 10,
    "app": None,
    "playing": False
}

@app.route('/api/ping')
def ping():
    return jsonify({"ok": True, "time": time.time()})

@app.route('/power', methods=['POST'])
def power():
    data = request.get_json() or {}
    state['power'] = bool(data.get('on', not state['power']))
    if not state['power']:
        state['playing'] = False
        state['app'] = None
    return jsonify({"status": "ok", "power": state['power']})

@app.route('/app/launch', methods=['POST'])
def launch_app():
    data = request.get_json() or {}
    app_name = data.get('app')
    if not app_name:
        return jsonify({"error": "no app specified"}), 400
    time.sleep(0.3)
    state['app'] = app_name
    state['playing'] = False
    return jsonify({"status":"ok","launched": app_name})

@app.route('/app/play', methods=['POST'])
def play():
    data = request.get_json() or {}
    title = data.get('title')
    if not state['power']:
        return jsonify({"error":"TV is off"}), 400
    if not state['app']:
        return jsonify({"error":"no app launched"}), 400
    if title and 'crash' in title.lower():
        return jsonify({"error":"playback crashed","code":"TimeoutError"}), 500
    state['playing'] = True
    return jsonify({"status":"ok","playing": True, "title": title})

@app.route('/status')
def status():
    return jsonify(state)

if __name__ == '__main__':
    print("Mock TV API Server running at http://127.0.0.1:5000/")
    app.run(debug=True)
