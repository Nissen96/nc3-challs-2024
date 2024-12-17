from io import BytesIO
from random import randint

from flask import Flask, Response, render_template
from PIL import Image


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/skift-kanal')
def generate_image():
    im = Image.open("flag.png")
    
    # Randomize white pixels
    for y in range(im.height):
        for x in range(im.width):
            if im.getpixel((x, y)) == (255, 255, 255, 255):
                im.putpixel((x, y), (randint(0, 255), randint(0, 255), randint(0, 255), 255))

    # Save the image to an in-memory file
    buffer = BytesIO()
    im.save(buffer, format="PNG")
    buffer.seek(0)

    # Return the image as a response
    return Response(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
