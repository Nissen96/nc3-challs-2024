from PIL import Image
from random import randint

im = Image.open("flag-original.png")

for y in range(im.height):
    for x in range(im.width):
        r, g, b, a = im.getpixel((x, y))
        if r < 100 and g < 100 and b < 100:
            im.putpixel((x, y), (randint(0, 255), randint(0, 255), randint(0, 255), a))
        else:
            im.putpixel((x, y), (255, 255, 255, 255))

im.save("app/flag.png")
    
# Randomize white pixels
for y in range(im.height):
    for x in range(im.width):
        if im.getpixel((x, y)) == (255, 255, 255, 255):
            im.putpixel((x, y), (randint(0, 255), randint(0, 255), randint(0, 255), 255))

im.save("flimmer.png")
