# import tesserocr as ocr
import ddddocr
import time
import os
from PIL import Image

docr = ddddocr.DdddOcr()

# def get_code(img_pos):      # 驗證碼圖片的位置
#     image = Image.open('Vcode.jpg')
#     image= image.crop(img_pos) # 裁切

#     image = image.convert('L')
#     threshold = 110
#     table = []

#     for i in range(256):

#         if i < threshold:
#             table.append(0)
#         else:
#             table.append(1)

#     image = image.point(table,"1")
#     # OCR識別
#     result = ocr.image_to_text(image, lang="eng")

#     result = result.strip()
#     # image.show()
#     return result[0:6]      # 返回驗證碼結果 6位


def ddocr(img_pos):
    image = Image.open('Vcode.jpg')
    image= image.crop(img_pos) # 裁切

    image.save("Vcode.png")
    # # os.path.join(os.getcwd(), "logs/error_img/"+random.ranint(1,999)+".png")
    # path = os.path.join(os.getcwd(), "logs\\error_img\\"+int(time.time())+".png")
    # image.save(path)

    with open("Vcode.png", 'rb') as f:
        image = f.read()
    
    res = docr.classification(image)
    print('驗證碼:', res)
    return res


# ddocr(1)