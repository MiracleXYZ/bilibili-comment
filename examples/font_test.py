from PIL import Image, ImageDraw, ImageFont

Font = ImageFont.truetype('C://Windows/Fonts/msyh.ttc',21)
Img = Image.new("RGBA", (200,200),(255,255,255))
Draw = ImageDraw.ImageDraw(Img, "RGBA")
Draw.setfont(Font)
Draw.text((10, 10), 'Love', fill='black')
Img.show()