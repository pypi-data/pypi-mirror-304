import cv2
import subprocess

def get_camera_names():
    camera_names = []
    try:
        # Lấy danh sách các thiết bị camera từ Powershell
        command = "powershell -Command \"Get-PnpDevice -Class Camera | Select-Object -ExpandProperty FriendlyName\""
        result = subprocess.check_output(command, shell=True, text=True)
        camera_names = [name.strip() for name in result.splitlines() if name.strip()]
    except subprocess.CalledProcessError:
        pass
        # print("\nKhông thể lấy tên camera từ PowerShell.")
    return camera_names

def list_available_cameras():
    available_cameras = []
    camera_names = get_camera_names()
    
    # Liệt kê các camera khả dụng
    index = 0
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            break
        cam_name = camera_names[index] if index < len(camera_names) else f"Unknown Camera {index}"
        available_cameras.append((index, cam_name))
        cap.release()
        index += 1

    # Xử lý trường hợp số lượng camera tìm được
    if len(available_cameras) == 1:
        return available_cameras[0]
    elif len(available_cameras) > 1:
        print(f"\nĐã tìm thấy {len(available_cameras)} camera:")
        for i, (_, cam_name) in enumerate(available_cameras):
            print(f"{i + 1}. {cam_name}")
        
        # Yêu cầu người dùng chọn camera và kiểm tra tính hợp lệ
        while True:
            try:
                choice = int(input("Chọn camera (nhập số): ")) - 1
                if 0 <= choice < len(available_cameras):
                    return available_cameras[choice]
                else:
                    print("\nLựa chọn không hợp lệ. Vui lòng chọn lại.")
            except ValueError:
                print("Vui lòng nhập một số hợp lệ.")
    else:
        print("\nKhông tìm thấy camera nào khả dụng.")
        return None, None

def init_camera():
    selected_camera_index, selected_camera_name = list_available_cameras()
    if selected_camera_index is None:
        return None  # Không thể khởi tạo camera

    try:
        cap = cv2.VideoCapture(selected_camera_index, cv2.CAP_DSHOW)  # Bỏ qua CAP_DSHOW
        if not cap.isOpened():
            raise Exception("Không thể mở camera, kiểm tra lại kết nối hoặc thiết bị.")

        print(f"\nĐã chọn: {selected_camera_name}")
        return cap
    except Exception:
        return None  # Bỏ qua lỗi mà không in ra thông báo

def release_camera(cap):
    if cap:
        cap.release()

def read_frame(cap):
    ret, frame = cap.read()
    return ret, frame