import cv2

def list_available_cameras():
    index = 0
    available_cameras = []
    
    # Thử duyệt qua các chỉ số camera để kiểm tra thiết bị nào khả dụng
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            break
        available_cameras.append(index)
        cap.release()
        index += 1
    
    # Nếu chỉ có một camera, tự động chọn nó, nếu nhiều hơn thì hỏi người dùng
    if len(available_cameras) == 1:
        print("Chỉ có một camera khả dụng.")
        return available_cameras[0]
    elif len(available_cameras) > 1:
        print("Có nhiều camera khả dụng:")
        for i, cam_index in enumerate(available_cameras):
            print(f"{i + 1}. Camera {cam_index}")
        choice = int(input("Chọn camera (nhập số): ")) - 1
        return available_cameras[choice]
    else:
        print("Không tìm thấy camera nào khả dụng.")
        return None

def init_camera():
    selected_camera_index = list_available_cameras()
    if selected_camera_index is None:
        print("Không thể khởi tạo camera.")
        return None
    
    try:
        # Khởi tạo camera với chỉ số được chọn
        cap = cv2.VideoCapture(selected_camera_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            raise Exception("Không thể mở camera, kiểm tra lại kết nối hoặc thiết bị.")
        return cap
    except Exception as e:
        print(f"\nLỗi: {e}")  # In ra lỗi tùy chỉnh khi không tìm thấy camera
        return None  # Trả về None nếu không thể khởi tạo camera

def release_camera(cap):
    if cap:
        cap.release()

def read_frame(cap):
    ret, frame = cap.read()
    return ret, frame
