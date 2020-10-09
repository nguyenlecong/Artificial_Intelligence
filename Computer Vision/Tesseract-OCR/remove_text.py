import cv2
import numpy as np

IMAGE_TO_PROCESS_PATH = 'sample/Roster1.jpg'

if __name__ == "__main__":

    img = cv2.imread(IMAGE_TO_PROCESS_PATH, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("no image")
    else:
        thresh, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) # Nhị phân hóa
        img_bin = 255-img_bin # Đảo ngược ảnh

        # Xác định đường kẻ ngang và kẻ dọc
        kernel_len = np.array(img).shape[1]//100
        ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len)) # Ma trận kích thước 1xkernel_len, các phần tử có giá trị = 1
        hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
        vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3) # Giãn ảnh

        image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
        horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)

        # Cấu trúc bảng không có văn bản
        img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
        img_vh = cv2.erode(~img_vh, kernel, iterations=2)
        thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        bitor = cv2.bitwise_or(img,img_vh)

        # Thu nhỏ ảnh
        scale_percent = 30
        width = int(bitor.shape[1] * scale_percent / 100)
        height = int(bitor.shape[0] * scale_percent / 100)
        dim = (width, height)
        bitor = cv2.resize(bitor, dim, interpolation = cv2.INTER_AREA)

        cv2.imshow('Table Structure', bitor)
        # cv2.imwrite('output_task1.jpg', bitor)

        cv2.waitKey(0)
        cv2.destroyAllWindows()