import os
import json
import time
from urllib import request, parse
from datetime import datetime, timezone

# Channel config
# Channel ID: 3127848 | Author: toltalbiuh
# API Key (Read): N251PNZ5EG0MWI2Y (can be overridden by env THINGSPEAK_READ_API_KEY)
CHANNEL_ID = os.getenv("THINGSPEAK_CHANNEL_ID", "3127848")
READ_API_KEY = os.getenv("THINGSPEAK_READ_API_KEY", "N251PNZ5EG0MWI2Y")


def thingspeak_get_latest():
    """Fetch the latest feed containing field1 (temperature) and field2 (humidity)."""
    base = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results=1"
    url = base + (f"&api_key={READ_API_KEY}" if READ_API_KEY else "")
    req = request.Request(url, method="GET")
    with request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode())

    feeds = data.get("feeds", [])
    if not feeds:
        return None

    latest = feeds[0]
    created_at = latest.get("created_at")
    f1 = latest.get("field1")
    f2 = latest.get("field2")

    # Convert to float if possible
    def to_float(x):
        try:
            return float(x) if x is not None else None
        except Exception:
            return None

    temperature = to_float(f1)
    humidity = to_float(f2)
    return {
        "created_at": created_at,
        "temperature": temperature,
        "humidity": humidity,
        "raw": latest,
    }


def main():
    print("Nhận dữ liệu DHT11 từ ThingSpeak (field1=temp °C, field2=hum %) – cập nhật mỗi 20 giây…")
    while True:
        try:
            latest = thingspeak_get_latest()
            if not latest:
                print("Chưa có dữ liệu (feeds trống).")
            else:
                t = latest["temperature"]
                h = latest["humidity"]
                ts_utc = latest["created_at"]  # ví dụ: 2025-10-24T08:07:55Z (UTC)
                # Chuyển về local time của hệ thống để hiển thị
                def to_local_str(ts):
                    try:
                        # Thay 'Z' bằng offset UTC để parse chuẩn
                        dt_utc = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                        dt_local = dt_utc.astimezone()  # về múi giờ local của hệ thống
                        return dt_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')
                    except Exception:
                        return ts
                ts_local = to_local_str(ts_utc)
                if t is None and h is None:
                    print(f"[{ts_local}] Không có field hợp lệ trong bản ghi mới nhất: {latest['raw']}")
                else:
                    # In linh hoạt nếu một trong hai trường chưa có
                    msg_parts = []
                    if t is not None:
                        msg_parts.append(f"Temperature: {t:.1f} °C")
                    if h is not None:
                        msg_parts.append(f"Humidity: {h:.1f} %")
                    print(f"[{ts_local}] " + ", ".join(msg_parts))
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu từ ThingSpeak: {e}")

        time.sleep(20)


if __name__ == "__main__":
    main()                                                                                                                                                                                                            