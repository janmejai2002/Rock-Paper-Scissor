import os
import cv2


root_dir = os.getcwd()
rock_path = os.path.join(root_dir, 'imgs', 'Rock.png')
paper_path = os.path.join(root_dir, 'imgs', 'Paper.png')
scissor_path = os.path.join(root_dir, 'imgs', 'Scissor.png')
none_path = os.path.join(root_dir, 'imgs', 'None_Image.png')


img = cv2.imread(rock_path)
print(img)
while True:
    cv2.imshow('Image', img)
    key = cv2.waitKey(10) & 0xFF

    if key == ord('q'):
        break
