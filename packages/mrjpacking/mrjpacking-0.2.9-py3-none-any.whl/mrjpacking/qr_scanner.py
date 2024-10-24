# import cv2
# from .constants import frame_width, frame_height

# def capture_label(frame):
#     detector = cv2.QRCodeDetector()
#     data, vertices, _ = detector.detectAndDecode(frame)
#     if vertices is not None and data:
#         vertices = vertices.astype(int)
#         (x, y, w, h) = cv2.boundingRect(vertices)
#         if check_within_frame((x, y, w, h)):
#             return data
#     return None

# def check_within_frame(box):
#     (x, y, w, h) = box
#     return x >= 0 and y >= 0 and (x + w) <= frame_width and (y + h) <= frame_height


# Traceback (most recent call last):
#   File "<frozen runpy>", line 198, in _run_module_as_main
#   File "<frozen runpy>", line 88, in _run_code
#   File "C:\Users\Justin Nguyen\AppData\Local\Programs\Python\Python312\Scripts\mrjpacking.exe\__main__.py", line 7, in <module>
#   File "C:\Users\Justin Nguyen\AppData\Local\Programs\Python\Python312\Lib\site-packages\mrjpacking\main.py", line 54, in main
#     label_text = qr.capture_label(frame)
#                  ^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\Justin Nguyen\AppData\Local\Programs\Python\Python312\Lib\site-packages\mrjpacking\qr_scanner.py", line 6, in capture_label
#     data, vertices, _ = detector.detectAndDecode(frame)
#                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# cv2.error: OpenCV(4.10.0) D:\a\opencv-python\opencv-python\opencv\modules\objdetect\src\qrcode.cpp:2951: error: (-2:Unspecified error) in function 'class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > __cdecl cv::ImplContour::decode(const class cv::_InputArray &,const class cv::_InputArray &,const class cv::_OutputArray &) const'
# > Invalid QR code source points (expected: 'contourArea(src_points) > 0.0'), where
# >     'contourArea(src_points)' is 0
# > must be greater than
# >     '0.0' is 0

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
