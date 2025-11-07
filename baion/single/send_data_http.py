from urllib import request, parse
from time import sleep, time
from seeed_dht import DHT

# Channel ID: 3142608
# Author: mwa0000039454674
# API Key (Write): AHHO5UL59ZCYUYCV
# API Key (Read): N251PNZ5EG0MWI2Y

def make_param_thingspeak(temp, humi):
    params = parse.urlencode({'field1': temp, 'field2': humi}).encode()
    return params

def thingspeak_post(params):
    api_key_write = "AHHO5UL59ZCYUYCV"
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('X-THINGSPEAKAPIKEY', api_key_write)
    r = request.urlopen(req, data=params)
    response_data = r.read()
    return response_data

def main():
    # Grove - Temperature & Humidity Sensor connected to port D5
    sensor = DHT('11', 5)
    
    print("Bắt đầu gửi dữ liệu lên ThingSpeak qua HTTP...")
    print("Nhấn Ctrl+C để dừng chương trình")
    
    while True:
        temp_list = []
        humi_list = []
        
        # Thu thập dữ liệu trong 20 giây
        print("\n--- Thu thập dữ liệu trong 20 giây ---")
        collect_start = time()
        
        while time() - collect_start < 20:
            try:
                humi, temp = sensor.read()
                
                # Kiểm tra giá trị hợp lệ
                if temp is not None and humi is not None:
                    if 0 <= temp <= 50 and 0 <= humi <= 100:
                        temp_list.append(temp)
                        humi_list.append(humi)
                        print(f'Đọc: Nhiệt độ {temp}°C, Độ ẩm {humi}%')
                    else:
                        print(f'Giá trị không hợp lệ: Nhiệt độ {temp}°C, Độ ẩm {humi}%')
                else:
                    print('Lỗi đọc cảm biến')
                    
            except Exception as e:
                print(f'Lỗi: {e}')
            
            sleep(1)
        
        # Tính giá trị trung bình
        if len(temp_list) > 0 and len(humi_list) > 0:
            avg_temp = sum(temp_list) / len(temp_list)
            avg_humi = sum(humi_list) / len(humi_list)
            
            print(f'\n--- Giá trị trung bình ---')
            print(f'Nhiệt độ TB: {avg_temp:.2f}°C')
            print(f'Độ ẩm TB: {avg_humi:.2f}%')
            print(f'Số mẫu hợp lệ: {len(temp_list)}')
            
            # Gửi dữ liệu lên ThingSpeak
            params_thingspeak = make_param_thingspeak(avg_temp, avg_humi)
            response = thingspeak_post(params_thingspeak)
            print(f'Đã gửi dữ liệu qua HTTP. Response: {response.decode()}')
        else:
            print('\nKhông có dữ liệu hợp lệ để gửi')

if __name__ == '__main__':
    main()