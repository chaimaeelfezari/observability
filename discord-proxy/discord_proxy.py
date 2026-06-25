from flask import Flask, request
import requests
import json

app = Flask(__name__)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1517564415363387603/GOksgqJMG3lmwGqxHsA3rQK9KFjz7BJ3x1Q-M0AsqmMXTML9TTWrsSa3eEGEjE1osW-P"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    alerts = data.get('alerts', [])
    
    for alert in alerts:
        status = alert.get('status', 'unknown')
        name = alert.get('labels', {}).get('alertname', 'Unknown')
        severity = alert.get('labels', {}).get('severity', 'unknown')
        summary = alert.get('annotations', {}).get('summary', '')

        if status == 'firing':
            emoji = '🔴'
            color = 15158332  # red
        else:
            emoji = '✅'
            color = 3066993   # green

        embed = {
            "title": f"{emoji} {name}",
            "color": color,
            "fields": [
                {"name": "Status", "value": status.upper(), "inline": True},
                {"name": "Severity", "value": severity, "inline": True},
            ]
        }
        
        if summary:
            embed["description"] = summary

        requests.post(DISCORD_WEBHOOK, json={"embeds": [embed]})
    
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)