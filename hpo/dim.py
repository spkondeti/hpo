import cv2

def get_image_info(filename):
    img = cv2.imread(filename,0)
    height, width = img.shape[:2]
    dim_dict = dict()
    dim_dict["w"] = width
    dim_dict["h"] = height
    print(dim_dict)
get_image_info("mike.jpeg")