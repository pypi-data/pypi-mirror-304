import camera_module
import cv2

def test_camera_selection():
    # Kiểm tra danh sách camera và khởi tạo camera
    cap = camera_module.init_camera()
    
    # Nếu không có camera nào được khởi tạo, báo lỗi và thoát
    if cap is None:
        print("Không thể khởi tạo camera. Vui lòng kiểm tra kết nối.")
        return
    
    # Đọc và hiển thị khung hình để kiểm tra camera
    print("Camera đã được khởi tạo thành công. Nhấn 'q' để thoát.")
    while True:
        ret, frame = camera_module.read_frame(cap)
        if not ret:
            print("Không thể đọc khung hình từ camera.")
            break
        
        # Hiển thị khung hình từ camera
        cv2.imshow("Camera Feed", frame)
        
        # Nhấn 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Giải phóng camera sau khi kết thúc
    camera_module.release_camera(cap)
    cv2.destroyAllWindows()
    print("Đã dừng camera.")

# Thực thi hàm test
test_camera_selection()
