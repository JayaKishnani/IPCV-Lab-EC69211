# -*- coding: utf-8 -*-
"""Expt-1.ipynb
"""

class Image():
  def __init__(self, filename):
    self.read_bmp_image(filename)

  def read_bmp_image(self, filename):
    with open(filename, "rb") as f:

      #Reading file header
      #To check whether it is bitmap image file or not
      self.signature = f.read(2).decode("ascii")
      if(self.signature !="BM"):
        return None

      self.file_size = int.from_bytes(f.read(4), "little")
      self.reserved = int.from_bytes(f.read(4), "little")
      self.data_offset = int.from_bytes(f.read(4), "little")

      # Reading BMP Header
      self.info_header_size = int.from_bytes(f.read(4), "little")
      self.width = int.from_bytes(f.read(4), "little")
      self.height = int.from_bytes(f.read(4), "little")
      self.planes = int.from_bytes(f.read(2), "little")
      self.bits_per_pixel = int.from_bytes(f.read(2), "little")
      self.compression = int.from_bytes(f.read(4), "little")
      self.image_size = int.from_bytes(f.read(4), "little")
      self.XpixelsperM = int.from_bytes(f.read(4), "little")
      self.YpixelsperM = int.from_bytes(f.read(4), "little")
      self.colors_used = int.from_bytes(f.read(4), "little")
      self.imp_colors = int.from_bytes(f.read(4), "little")

      #Reading color Table
      #Present only if bits per pixel is less than 8 colors and should be ordered
      #by importance

      if self.bits_per_pixel <= 8:
        self.color_table = []
        red = []
        green = []
        blue = []
        reserved = []
        for x in range(self.colors_used):
          red.append(int.from_bytes(f.read(1), "little"))
          green.append(int.from_bytes(f.read(1), "little"))
          blue.append(int.from_bytes(f.read(1), "little"))
          reserved.append(int.from_bytes(f.read(1), "little"))
        self.color_table.append(red)
        self.color_table.append(green)
        self.color_table.append(blue)
        self.color_table.append(reserved)

      # reading bitmap image into an array
      self.image_array = []

      for x in range(self.height):
        row = []
        for y in range(self.width):
          row.append(int.from_bytes(f.read(self.bits_per_pixel//8), "little"))
        self.image_array.append(row)

      #Printing necessary information
      print("-------------------------------------------------\n")
      print("File name : ", filename)
      print("Height of the given Image : ", self.height)
      print("Width of the given Image : ", self.width)
      print("Bit Width of the given Image : ", self.bits_per_pixel)
      print("File Size of the given Image : ", self.file_size)
      print("Size of the given image image : ", self.image_size)
      print("Offset Size of the given image : ", self.data_offset)
      print("Pixel array of the given image : ", self.image_array)
      print("\n--------------------------------------------------")

  def writeBMP(self, filename):
    with open(filename, "wb") as f:
      signature = 'BM'
      data_offset = 14 + 40 + (4*self.colors_used if self.bits_per_pixel <= 8 else 0)
      file_size = data_offset + self.height*self.width*self.bits_per_pixel//8
      reserved = 0

      # File header
      f.write(signature.encode("ascii"))
      f.write(file_size.to_bytes(4, "little"))
      f.write(reserved.to_bytes(4, "little"))
      f.write(data_offset.to_bytes(4, "little"))

      # Info header
      f.write(self.info_header_size.to_bytes(4, "little"))
      f.write(self.width.to_bytes(4, "little"))
      f.write(self.height.to_bytes(4, "little"))
      f.write(self.planes.to_bytes(2, "little"))
      f.write(self.bits_per_pixel.to_bytes(2, "little"))
      f.write(self.compression.to_bytes(4, "little"))
      f.write(self.image_size.to_bytes(4, "little"))
      f.write(self.XpixelsperM.to_bytes(4, "little"))
      f.write(self.YpixelsperM.to_bytes(4, "little"))
      f.write(self.colors_used.to_bytes(4, "little"))
      f.write(self.imp_colors.to_bytes(4, "little"))

      #Color table
      if self.bits_per_pixel <= 8:
        for x in range(self.colors_used):
          f.write(self.color_table[0][x].to_bytes(1, "little"))
          f.write(self.color_table[1][x].to_bytes(1, "little"))
          f.write(self.color_table[2][x].to_bytes(1, "little"))
          f.write(self.color_table[3][x].to_bytes(1, "little"))

       #Pixel data
        for i in range(self.height):
          for j in range(self.width):
            tmp = self.image_array[i][j]
            f.write(tmp.to_bytes(self.bits_per_pixel//8, "little"))

  def remove_red(self, filename):
    copy_color_table = self.color_table.copy()
    self.color_table[2] = [0 for x in range(len(self.color_table[2]))]
    self.writeBMP(filename)
    self.color_table = copy_color_table

  def remove_green(self, filename):
    copy_color_table = self.color_table.copy()
    self.color_table[1] = [0 for x in range(len(self.color_table[1]))]
    self.writeBMP(filename)
    self.color_table = copy_color_table

  def remove_blue(self, filename):
    copy_color_table = self.color_table.copy()
    self.color_table[0] = [0 for x in range(len(self.color_table[0]))]
    self.writeBMP(filename)
    self.color_table = copy_color_table

if __name__ == "__main__":

  #Image paths
  img1 = "cameraman.bmp"
  img2 = "corn.bmp"
  img3 = "lena_colored_256.bmp"

  #read files
  Image_1 = Image(img1)
  Image_2 = Image(img2)
  Image_3 = Image(img3)

  #write image
  Image_1.writeBMP("cameraman_output.bmp")
  Image_2.writeBMP("corn_output.bmp")
  Image_3.writeBMP("lena_colored_256_output.bmp")

  #color channel manipulation
  Image_2.remove_red("corn_filter_red_channel.bmp")
  Image_2.remove_blue("corn_filter_blue_channel.bmp")
  Image_2.remove_green("corn_filer_green_channel.bmp")
