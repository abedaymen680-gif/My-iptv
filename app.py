from flask import Flask, jsonify, request, redirect
import os

app = Flask(__name__)

# بيانات الدخول
USERNAME = "sniper"
PASSWORD = "123"

# قائمة القنوات (يمكنك إضافة المزيد هنا لاحقاً)
CHANNELS = {
    "1000": {"name": "TF1 HD", "url": "http://41.205.93.154/TF1/mpegts"},
    "1001": {"name": "FRANCE 2 HD", "url": "http://41.205.93.154/FRANCE2/mpegts"},
}

@app.route('/')
def home():
    return "SNIPER Server is Running!"

@app.route('/player_api.php')
def xtream_api():
    u = request.args.get('username')
    p = request.args.get('password')
    action = request.args.get('action')

    # التحقق من المستخدم
    if u != USERNAME or p != PASSWORD:
        return jsonify({"user_info": {"auth": 0}}), 200

    # طلب الأقسام
    if action == "get_live_categories":
        return jsonify([{"category_id": "1", "category_name": "SNIPER LIVE"}])

    # طلب القنوات
    if action == "get_live_streams":
        output = []
        for s_id, info in CHANNELS.items():
            output.append({
                "num": int(s_id) - 999,
                "name": info["name"],
                "stream_id": int(s_id),
                "stream_type": "live",
                "category_id": "1",
                "container_extension": "ts",
                "tv_archive": 0,
                "direct_source": ""
            })
        return jsonify(output)

    # رد الدخول الافتراضي (Login)
    return jsonify({
        "user_info": {
            "username": u,
            "password": p,
            "auth": 1,
            "status": "Active",
            "exp_date": "1999999999",
            "is_trial": "0",
            "active_cons": 0,
            "max_connections": 1,
            "allowed_output_formats": ["ts", "m3u8"]
        },
        "server_info": {
            "url": "my-tv-server.onrender.com",
            "port": "80",
            "https_port": "443",
            "server_protocol": "http",
            "timezone": "Africa/Algiers",
            "timestamp_now": 1609459200
        }
    })

@app.route('/live/<u>/<p>/<s_id>.ts')
@app.route('/live/<u>/<p>/<s_id>')
def stream(u, p, s_id):
    if u == USERNAME and p == PASSWORD and s_id in CHANNELS:
        return redirect(CHANNELS[s_id]["url"])
    return "Error", 404

if __name__ == "__main__":
    # ملاحظة: رندر يحتاج لمنفذ متغير، هذا السطر مهم جداً
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
      
