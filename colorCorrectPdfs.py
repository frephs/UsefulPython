# import module
import os
from pdf2image import convert_from_path
import numpy as np
from PIL import Image

# listing pdfs

def getPDFs():
    list_pdf = os.listdir()
    for item in list_pdf:
        if ".pdf" in item:
            pass
        else:
            list_pdf.remove(item)
    return list_pdf

def pdfToImg():
    list_pdf = getPDFs()
    for pdf in list_pdf:
        images = convert_from_path(pdf)
        for i in range(len(images)):
            images[i].save('prov/'+str(pdf)+'page'+ str(i) +'.png', 'PNG')
            print( 'OK prov/'+str(pdf)+'page'+ str(i) +'.png')

def changeColor(image_file):
    print(image_file)
    im = Image.open(image_file)
    data = np.array(im)

    r1, g1, b1 = 170, 170, 170 # Original value
    r2, g2, b2 = 41, 51, 45 # Value that we want to replace it with
    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    mask = (red > r1) & (green > g1) & (blue > b1 )
    data[:,:,:3][mask] = [r2, g2, b2]

    r1, g1, b1 = 51, 51, 51 # Original value
    r2, g2, b2 = 255, 255, 255 # Value that we want to replace it with
    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:,:,:3][mask] = [r2, g2, b2]

    image_file = image_file.replace(".png","").replace("prov/","")
    im = Image.fromarray(data)
    im.save(f'final/{image_file}.png')
    print("Done")
    return f"Done {image_file}"

def modifyPages():
    list_png = os.listdir("prov")
    for item in list_png:
        if ".png" in item:
            pass
        else:
            list_png.remove(item)

    for image in list_png:
        changeColor("prov/"+image)


if __name__ == '__main__':
    try:
        pdfToImg()
    except Exception as e:
        pass
    modifyPages()
