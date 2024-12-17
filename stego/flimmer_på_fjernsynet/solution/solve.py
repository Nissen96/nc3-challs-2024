from PIL import Image

im1 = Image.open("kanal1.png")
im2 = Image.open("kanal2.png")

new_im = Image.new("RGB", im1.size, (255, 255, 255))

for y in range(im1.height):
    for x in range(im1.width):
        if im1.getpixel((x, y)) == im2.getpixel((x, y)):
            new_im.putpixel((x, y), (0, 0, 0))

new_im.save("result.png")
