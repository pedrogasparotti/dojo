from PIL import Image

imagem = Image.open("/Users/home/Documents/github/dojo/roger_waters.jpg")\

# Este código contém um bug
def limit_img_size(img:Image, limit=1024):
    width, height = img.size

    #  lado do quadrado será a menor valor entre as dimensões da imagem
    size = min(width, height, limit)

    # dimensões parametrizadas de acordo com o tamanho do quadrado
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size


    # Corta o centro da imagem
    img = img.crop((left, top, right, bottom))
    return img


if __name__ == '__main__':
    print(limit_img_size(imagem))

    limit_img_size(imagem).show()

    print("done")