import cv2
from matplotlib import pyplot as plt
import numpy as np


'''Image'''


'''Load và xử lý'''
img = cv2.imread('orange.jpg')
img = cv2.imread('orange.jpg',cv2.IMREAD_GRAYSCALE)
cv2.imshow("orange", img)

'''tách vật thể'''
# min = np.array([0, 50,240])
# max = np.array([150, 200, 260])
# mask = cv2.inRange(img, min, max)
# cv2.imshow('only orange', mask)
# final = cv2.bitwise_and(img, img, mask = mask)
# cv2.imshow('only orange', final)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''tách biên ảnh'''
# img = cv2.imread('widow.jpg', 0)
# img2 = cv2.Canny(img, 100, 200)
# cv2.imshow('widow', img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


'''kích thước của ảnh'''
# (h, w, d) = img.shape
# print("width={}, height={}, depth={}".format(w, h, d))

'''Xoay ảnh'''
# center = (w // 2, h // 2) 
# M = cv2.getRotationMatrix2D(center, 180, 1.0) 
# rotated = cv2.warpAffine(img, M, (w, h))
# cv2.imshow('wrap', rotated)

'''giá trị màu ở một điểm ảnh'''
# (B, G, R) = img[50, 50]
# print("R={}, G={}, B={}".format(R, G, B))

'''Cắt ảnh'''
# roi = img[50:350, 60:360]
# cv2.imshow('Region Of Interest', roi)
# cv2.waitKey(0)

# cv2.imshow('image output',img) # hiển thị hình ảnh
# cv2.waitKey(0)
# cv2.destroyAllWindows() # đóng tất cả
#cv2.imwrite('watchgray.png',img) # lưu lại sửa đổi

'''hiển thị hình ảnh bằng Matplotlib'''
# plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
# plt.plot([200,300,400],[100,200,300],'c', linewidth=5)
# plt.show()





'''Video'''


# cap = cv2.VideoCapture(0) # camera
# #cap = cv2.VideoCapture('cat.mp4') # video file

# while(cap.isOpened()):
#     # Capture frame-by-frame
#     ret, frame = cap.read() # Nếu khung được đọc đúng, nó sẽ là True.

#     # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Display the resulting frame
#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'): # "q" to quit
#         break
# #cv2.imwrite('video gray', gray)# save video

# # When everything done, release the capture
# # giải phóng webcam, sau đó đóng tất cả cửa sổ imshow ().
# cap.release()
# cv2.destroyAllWindows()