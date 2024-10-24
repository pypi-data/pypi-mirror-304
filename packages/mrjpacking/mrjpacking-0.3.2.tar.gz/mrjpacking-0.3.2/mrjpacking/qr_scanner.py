import cv2
from .constants import frame_width, frame_height

def capture_label(frame):
    detector = cv2.QRCodeDetector()
    
    # Kiểm tra xem khung hình có hợp lệ không
    if frame is None or frame.size == 0:
        # Nếu khung hình trống, tiếp tục mà không quét
        return None
    
    try:
        # Thực hiện quét mã QR
        data, vertices, _ = detector.detectAndDecode(frame)
        
        # Kiểm tra nếu phát hiện mã QR
        if vertices is not None and data:
            vertices = vertices.astype(int)
            (x, y, w, h) = cv2.boundingRect(vertices)
            
            # Kiểm tra xem mã QR có nằm trong khung hình không
            if check_within_frame((x, y, w, h)):
                return data

        # Nếu không phát hiện mã QR, tiếp tục quét mà không báo lỗi
        return None

    except cv2.error:
        # Lặng lẽ bỏ qua lỗi mà không in ra bất cứ điều gì
        return None

def check_within_frame(box):
    (x, y, w, h) = box
    return x >= 0 and y >= 0 and (x + w) <= frame_width and (y + h) <= frame_height

def draw_green_frame_around_qr(frame):
    # Khởi tạo QRCodeDetector để phát hiện mã QR
    qr_detector = cv2.QRCodeDetector()
    
    # Phát hiện mã QR trong frame
    data, points, _ = qr_detector.detectAndDecode(frame)
    
    # Nếu tìm thấy mã QR
    if points is not None:
        points = points[0]  # Tọa độ các đỉnh của khung QR
        
        # Chuyển đổi các điểm sang số nguyên để có thể sử dụng vẽ hình
        points = points.astype(int)
        
        # Vẽ khung hình bao quanh mã QR
        for i in range(4):
            # Vẽ đường viền từ điểm hiện tại đến điểm kế tiếp (cạnh của mã QR)
            pt1 = tuple(points[i])
            pt2 = tuple(points[(i + 1) % 4])  # Modulo 4 để quay lại điểm đầu tiên
            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)  # Màu xanh lá và độ dày là 3px
        
        # Hiển thị nội dung giải mã được từ mã QR nếu có
        # if data:
        #     print(f"QR Code data: {data}")
    
    return frame