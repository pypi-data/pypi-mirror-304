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
