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
    index = 0
    available_cameras = []
    camera_names = get_camera_names()

    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        # Kiểm tra xem index có nằm trong phạm vi camera_names không
        cam_name = camera_names[index] if index < len(camera_names) else f"Unknown Camera {index}"
        available_cameras.append((index, cam_name))
        cap.release()
        index += 1

    if len(available_cameras) == 1:
        # print("\nChỉ có một camera khả dụng:", available_cameras[0][1])
        return available_cameras[0][0], available_cameras[0][1]
    elif len(available_cameras) > 1:
        print(f"\nĐã tìm thấy {len(available_cameras)} camera:")
        for i, (cam_index, cam_name) in enumerate(available_cameras):
            print(f"{i + 1}. {cam_name}")
        choice = int(input("Chọn camera (nhập số): ")) - 1
        return available_cameras[choice][0], available_cameras[choice][1]
    else:
        print("\nKhông tìm thấy camera nào khả dụng.")
        return None, None
        return None, None

def init_camera():
    selected_camera_index, selected_camera_name = list_available_cameras()
    if selected_camera_index is None:
        # print("\nKhông thể khởi tạo camera.")
        return None
    
    try:
        cap = cv2.VideoCapture(selected_camera_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            raise Exception("\nKhông thể mở camera, kiểm tra lại kết nối hoặc thiết bị.")
        
        print(f"Camera đã được chọn: {selected_camera_name}")
        return cap
    except Exception as e:
        # print(f"\nLỗi: {e}")
        pass
        return None

def release_camera(cap):
    if cap:
        cap.release()

def read_frame(cap):
    ret, frame = cap.read()
    return ret, frame

# def list_available_cameras():
#     index = 0
#     available_cameras = []
#     camera_names = get_camera_names()

#     # Redirect stdout để ẩn cảnh báo
#     class DummyFile(object):
#         def write(self, x): pass

#     original_stdout = sys.stdout
#     sys.stdout = DummyFile()

#     try:
#         while True:
#             cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
#             if not cap.isOpened():
#                 break
#             cam_name = camera_names[index] if index < len(camera_names) else f"Unknown Camera {index}"
#             available_cameras.append((index, cam_name))
#             cap.release()
#             index += 1

#         if len(available_cameras) == 1:
#             # print("\nChỉ có một camera khả dụng:", available_cameras[0][1])
#             return available_cameras[0][0], available_cameras[0][1]
#         elif len(available_cameras) > 1:
#             print("\nĐã tìm thấy {} camera:".format(len(available_cameras)))
#             for i, (cam_index, cam_name) in enumerate(available_cameras):
#                 print(f"{i + 1}. {cam_name}")
#             choice = int(input("Chọn camera (nhập số): ")) - 1
#             return available_cameras[choice][0], available_cameras[choice][1]
#         else:
#             print("\nKhông tìm thấy camera nào khả dụng.")
#             return None, None
#     finally:
#         # Trả lại stdout về trạng thái ban đầu
#         sys.stdout = original_stdout

# def init_camera():
#     selected_camera_index, selected_camera_name = list_available_cameras()
#     if selected_camera_index is None:
#         return None  # Không thể khởi tạo camera

#     try:
#         cap = cv2.VideoCapture(selected_camera_index)  # Bỏ qua CAP_DSHOW
#         if not cap.isOpened():
#             raise Exception("Không thể mở camera, kiểm tra lại kết nối hoặc thiết bị.")

#         print(f"\nCamera đã được chọn: {selected_camera_name}")
#         return cap
#     except Exception:
#         return None  # Bỏ qua lỗi mà không in ra thông báo

