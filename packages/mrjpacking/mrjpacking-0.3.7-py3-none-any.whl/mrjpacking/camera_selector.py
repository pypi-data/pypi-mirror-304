# camera_selector.py
import cv2

def list_cameras():
    # Tìm danh sách các camera có sẵn
    cameras = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        cameras.append(index)
        cap.release()
        index += 1
    return cameras

def select_camera(cameras):
    # Hiển thị danh sách camera và yêu cầu người dùng chọn
    print("Chọn camera để sử dụng:")
    for i in cameras:
        print(f"{i}: Camera {i}")

    # Yêu cầu người dùng chọn camera
    camera_index = -1
    while camera_index not in cameras:
        try:
            camera_index = int(input("Nhập số camera bạn muốn sử dụng: "))
        except ValueError:
            print("Lựa chọn không hợp lệ. Vui lòng nhập số hợp lệ.")
    print(f"Sử dụng Camera {camera_index}")
    return camera_index
