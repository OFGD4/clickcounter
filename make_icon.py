from PIL import Image

img = Image.open("mkwa.png")
img.save("mkwa.ico", sizes=[(16, 16), (32, 32),(48,48),(256,256)])