'''
Image transformation.
'''

import sys
import os
from tkinter import filedialog
from PIL import Image


def main() -> None:
  img_filepaths = get_image_filepaths('Select images')

  if not img_filepaths:
    sys.stdout.write('No image selected.')
    return

  pdf_filename = get_suggested_filename(img_filepaths)
  pdf_filepath = get_pdf_filepath('Save as PDF', pdf_filename)

  if not pdf_filepath:
    sys.stdout.write('No PDF document selected.')
    return

  img_filepaths.sort()
  img_list = [open_image(filepath) for filepath in img_filepaths]
  save_images_as_pdf(pdf_filepath, img_list)

  sys.stdout.write(f'Saved {len(img_list)} image(s) as PDF "{pdf_filepath}".')


def get_image_filepaths(title) -> list[str]:
  return list(filedialog.askopenfilenames(
    title=title,
    filetypes=[
      ('JPEG image', '*.jpg'),
      ('PNG image', '*.png'),
      ('GIF image', '*.gif'),
      ('WebP image', '*.webp'),
      ('BMP image', '*.bmp'),
      ('All files', '*.*'),
    ]
  ))


def get_pdf_filepath(title, initial_filepath) -> str:
  return filedialog.asksaveasfilename(
    title=title,
    initialfile=initial_filepath,
    defaultextension='.pdf',
    filetypes=[
      ('PDF document', '*.pdf'),
    ]
  )


def get_suggested_filename(filepaths, filename_ext=''):
  filename = os.path.basename(filepaths[0])
  return os.path.splitext(filename)[0].strip() + filename_ext


def open_image(img_filepath) -> Image:
  return Image.open(img_filepath)


def convert_image(img) -> Image:
  return img.convert('RGB')


def save_images_as_pdf(pdf_filepath, img_list) -> bool:
  conv_img_list = [convert_image(img) for img in img_list]

  if not conv_img_list:
    return False

  first_img = conv_img_list[0]

  if len(conv_img_list) == 1:
    first_img.save(pdf_filepath,
      format='PDF'
    )
  else:
    first_img.save(pdf_filepath,
      format='PDF',
      save_all=True,
      append_images=conv_img_list[1:]
    )

  return True


if __name__ == '__main__':
  main()
