import os
import random
import pathlib
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# ChatGPT API Key (with payed quota)
IMAGES_PATH = pathlib.Path('/home/pigs_images')

# Initializing client
imgs = os.listdir(IMAGES_PATH)
wisdoms = open('home/wisdoms.txt', encoding = 'utf-8').readlines( )

#
# Get random wisdom quote
#
def get_random_wisdom( ):
  return random.choice(wisdoms)

#
# Get random image from database
#
def get_random_image( ):
  return IMAGES_PATH / random.choice(imgs)

#
# Wraps a reply into given image width and returns wrapped text
#
def wrap_text(text, font, draw, max_width, stroke_width):
  words = text.split( )
  lines = [ ]
  line  = ''

  for word in words:
    nline  = f'{line}{word} '
    lwidth = draw.textlength(nline, font)
    if lwidth <= max_width:
      line = nline
    else:
      lines.append(line.strip( ))
      line = f'{word} '

  if line:
    lines.append(line.strip( ))

  return lines

#
# Wraps text to a given image width and adds text to the given image
#
def add_text_to_img(txt, img):
  img_src = Image.open(img)
  draw = ImageDraw.Draw(img_src)
  font = ImageFont.truetype('arial.ttf', 24)
  image_width, image_height = img_src.size
  stroke_width = 2
  wrapped_lines = wrap_text(txt, font, draw, image_width - 40, stroke_width)
  line_spacing = 10
  line_height = font.getbbox('Ay')[3] + stroke_width
  total_text_height = len(wrapped_lines) * (line_height + line_spacing)
  y = (image_height - total_text_height) / 2 + 150
  for line in wrapped_lines:
    bbox = draw.textbbox((0, 0), line, font=font, stroke_width = stroke_width)
    line_width = bbox[2] - bbox[0]
    x = (image_width - line_width) / 2  # центрируем по ширине
    draw.text((x, y), line, font=font, fill="white", stroke_width = stroke_width, stroke_fill="black")
    y += line_height + line_spacing

  bio = BytesIO( )
  bio.name = 'image.png'
  img_src.save(bio, 'PNG')
  bio.seek(0)
  return bio