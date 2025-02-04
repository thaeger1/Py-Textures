import cv2
import base64
import numpy as np

def arr_to_b64 (arr_in):
    is_success, im_buf_arr = cv2.imencode(".png", arr_in)
    img_data = base64.b64encode(im_buf_arr.tobytes())
    return img_data

def b64_to_arr (b64_str):
    nparr = np.frombuffer(base64.b64decode(b64_str), np.uint8)
    img_out= cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_out
