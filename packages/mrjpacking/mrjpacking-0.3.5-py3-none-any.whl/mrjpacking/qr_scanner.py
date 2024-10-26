import cv2
from .constants import frame_width, frame_height, FRAME_COLOR

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
        return None

def check_within_frame(box):
    (x, y, w, h) = box
    return x >= 0 and y >= 0 and (x + w) <= frame_width and (y + h) <= frame_height

def draw_green_frame_around_qr(frame):
    qr_detector = cv2.QRCodeDetector()
    
    try:
        # Thực hiện quét mã QR
        data, points, _ = qr_detector.detectAndDecode(frame)

        # Bỏ qua nếu không tìm thấy mã QR
        if points is not None and data:  # Chỉ xử lý khi tìm thấy mã QR và dữ liệu không rỗng
            # Kiểm tra diện tích của các điểm mã QR để đảm bảo hợp lệ
            if cv2.contourArea(points) > 0:  
                points = points[0].astype(int)  # Lấy tọa độ các điểm bao quanh mã QR

                # Vẽ khung xanh quanh mã QR theo các điểm
                cv2.polylines(frame, [points], isClosed=True, color=FRAME_COLOR, thickness=2)

    except cv2.error as e:
        # Bỏ qua lỗi và tiếp tục tìm kiếm
        pass

    return frame
