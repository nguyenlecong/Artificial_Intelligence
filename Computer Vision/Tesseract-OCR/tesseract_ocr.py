from PIL import Image
import pytesseract
import cv2
import os

IMAGE_TO_PROCESS_PATH = 'sample/Roster1.jpg'

if __name__ == "__main__":

    img = cv2.imread(IMAGE_TO_PROCESS_PATH, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("no image")
    else:
        thresh, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) # Nhị phân hóa
        # img = cv2.medianBlur(img, 3) # Làm mờ, giảm noise

        # Ghi tạm ảnh xuống ổ cứng
        filename = "{}.jpg".format(os.getpid())
        cv2.imwrite(filename, img)

        # Tesseract OCR
        pytesseract.pytesseract.tesseract_cmd = r'D:\Tai Lieu\HUST-Study\20201\TTKT\tesseract\tesseract.exe'
        text = pytesseract.image_to_string(Image.open(filename), lang = 'jpn')
        print(text)

        # Xóa ảnh tạm
        os.remove(filename)

        # Ghi vào file
        with open('task2/output_task2.txt', "w", encoding="utf-8") as f:
            f.write(text)

        # # Thu nhỏ ảnh
        # scale_percent = 30
        # width = int(img.shape[1] * scale_percent / 100)
        # height = int(img.shape[0] * scale_percent / 100)
        # dim = (width, height)
        # img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        # cv2.imshow('Table Structure', img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
