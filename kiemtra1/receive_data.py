# Thư viện MQTT dùng để kết nối, subscribe và nhận/gửi dữ liệu qua giao thức MQTT
import paho.mqtt.client as mqtt 

# Thư viện datetime dùng để lấy thời gian hiện tại (để hiển thị timestamp khi nhận dữ liệu)
from datetime import datetime

# Channel ID: 3153408
# username    = "IRU6PSACOwQPHy4PKiczCiI"
# clientID    = "IRU6PSACOwQPHy4PKiczCiI"
# password    = "gHzqnX35vjOPS0jeNUVtBdfV"

# Biến lưu trữ dữ liệu từ các field
data = {
    "field1": None,  # Nhiệt độ
    "field2": None,  # Độ ẩm
    "field3": None,  # LED vàng
    "field4": None   # LED đỏ
}

def convert_led_status(value):
    """Chuyển đổi giá trị 1/0 sang BẬT/TẮT"""
    try:
        return "BẬT" if int(float(value)) == 1 else "TẮT"
    except:
        return "N/A"

def display_data():
    """Hiển thị dữ liệu theo dạng ngang"""
    if all(v is not None for v in data.values()):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print("\n" + "="*80)
        print(f"[{timestamp}] Nhiệt độ: {data['field1']}°C | Độ ẩm: {data['field2']}% | "
              f"LED Vàng: {convert_led_status(data['field3'])} | "
              f"LED Đỏ: {convert_led_status(data['field4'])}")
        print("="*80)

def on_connect(client, userdata, flags, rc):
    print("Kết nối thành công với ThingSpeak MQTT Broker (Code: {})".format(rc))
    print("Đang lắng nghe dữ liệu từ Channel {}...".format(channel_ID))
    # Subscribe tới tất cả 4 fields
    client.subscribe("channels/%s/subscribe/fields/field1" % (channel_ID))  # Nhiệt độ
    client.subscribe("channels/%s/subscribe/fields/field2" % (channel_ID))  # Độ ẩm
    client.subscribe("channels/%s/subscribe/fields/field3" % (channel_ID))  # LED vàng
    client.subscribe("channels/%s/subscribe/fields/field4" % (channel_ID))  # LED đỏ

def on_disconnect(client, userdata, rc):
    print("\nNgắt kết nối khỏi Broker")

def on_message(client, userdata, message):
    """Xử lý tin nhắn nhận được từ MQTT"""
    topic = message.topic
    payload = message.payload.decode().strip()
    
    # Xác định field nào nhận được dữ liệu
    if "field1" in topic:
        data["field1"] = payload
    elif "field2" in topic:
        data["field2"] = payload
    elif "field3" in topic:
        data["field3"] = payload
    elif "field4" in topic:
        data["field4"] = payload
    
    # Hiển thị dữ liệu khi đã nhận đủ
    display_data()

# Cấu hình MQTT
channel_ID = "3153408"
client_id  = "IRU6PSACOwQPHy4PKiczCiI"

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.username_pw_set(username = "IRU6PSACOwQPHy4PKiczCiI",
                       password = "gHzqnX35vjOPS0jeNUVtBdfV")

print("=== HỆ THỐNG NHẬN DỮ LIỆU TỪ THINGSPEAK ===")
print("Đang kết nối tới mqtt3.thingspeak.com...")

client.connect("mqtt3.thingspeak.com", 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\n\nĐang ngắt kết nối...")
    client.disconnect()
    print("Đã ngắt kết nối.")