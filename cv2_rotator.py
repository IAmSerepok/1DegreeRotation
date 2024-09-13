import cv2
import numpy as np


def rotate_image(image, angle):
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_image


def extend_to_square(image):
    height, width = image.shape[:2]
    max_dim = max(height, width)
    
    square_image = np.zeros((max_dim, max_dim, 3), np.uint8)
    start_y = (max_dim - height) // 2
    start_x = (max_dim - width) // 2
    square_image[start_y:start_y+height, start_x:start_x+width] = image
    
    return square_image


image_path = "2.jpg"  # <-- image path
angle = 1  # <-- angle


original_image = cv2.imread(image_path)
original_image = extend_to_square(original_image)

height, width, _ = original_image.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 60  # <-- fps

out = cv2.VideoWriter('output/video/output_video_cv2.mp4', fourcc, fps, (width, height))

rotated_image = original_image


for _ in range(1000):
    out.write(rotated_image)

    cv2.imshow("Rotated Image", rotated_image)
    cv2.waitKey(1)

    rotated_image = rotate_image(rotated_image, angle)


out.release()
cv2.destroyAllWindows()
