from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟数据库和 TRTC API
class MockDatabase:
    def check_user_in_room(self, room_id, user_id):
        # TODO: 实现实际的数据库检查逻辑
        print(f"Checking if user {user_id} is in business room {room_id}")
        return False  # 返回 False 表示用户不在业务房间

class MockTRTCApi:
    def remove_user(self, room_id, user_id):
        # TODO: 实现实际的 TRTC API 踢出用户逻辑
        print(f"Removing user {user_id} from room {room_id}")

# 实例化模拟数据库和 TRTC API
db = MockDatabase()
trtc_api = MockTRTCApi()

@app.route('/trtc/callback', methods=['POST'])
def trtc_callback():
    data = request.get_json()

    if not data or 'EventType' not in data or 'EventInfo' not in data:
        return jsonify(code=1, message='Invalid request: missing EventType or EventInfo'), 400

    # 仅处理 103 进房事件
    if data['EventType'] == 103:
        info = data['EventInfo']

        # 检查 RoomId 和 UserId 是否存在
        if 'RoomId' not in info or 'UserId' not in info:
            return jsonify(code=1, message='Invalid request: missing RoomId or UserId'), 400

        # 查询业务侧：该用户是否在业务房间中
        if not db.check_user_in_room(info['RoomId'], info['UserId']):
            # 幽灵麦 → 踢出房间
            trtc_api.remove_user(info['RoomId'], info['UserId'])

    return jsonify(code=0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
