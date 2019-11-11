import struct as st
from array import *
import os
import numpy as np
import matplotlib.pyplot as plt

# This code is partially based on
# the following GitHub repo:
# https://github.com/gskielian/JPG-PNG-to-MNIST-NN-Format
# and this well written Medium article:
# https://medium.com/@mannasiladittya/converting-mnist-data-in-idx-format-to-python-numpy-array-5cb9126f99f1
# which outlines the underlying concept of the IDX format in more detail.

class Idx:

    @staticmethod
    def save_idx(source_folder, output_folder=None):
        if output_folder is None:
            output_folder = source_folder

        categories = os.listdir(source_folder)
        ind_categories = [os.path.isdir(source_folder + i) for i in categories]
        categories = [categories[i] for i, x in enumerate(ind_categories) if x]

        data = array('B')
        header = array('B')
        label = array('B')
        num_files = 0
        num_cat = 0
        for cat in categories:

            cat_folder = source_folder + cat
            cat_files = os.listdir(cat_folder)

            for file in cat_files:
                num_files += 1

                file_path = cat_folder + "/" + file

                img = plt.imread(file_path)
                width, height = img.shape

                for x in range(0, width):
                    for y in range(0, height):
                        data.append(img[x, y])

                label.append(num_cat)

            num_cat += 1

        hexval = "{0:#0{1}x}".format(num_files, 6)  # number of files in HEX format

        header.extend([0, 0, 8, 1, 0, 0])
        header.append(int('0x' + hexval[2:][:2], 16))
        header.append(int('0x' + hexval[2:][2:], 16))

        label = header + label

        header.extend([0, 0, 0, width, 0, 0, 0, height])

        header[3] = 3
        data = header + data

        output_file = open(output_folder + 'images.idx3-ubyte', 'wb')
        data.tofile(output_file)
        output_file.close()

        output_file = open(output_folder + 'labels.idx3-ubyte', 'wb')
        label.tofile(output_file)
        output_file.close()

    @staticmethod
    def load_idx(filename):

        # Open the file
        file = open(filename, 'rb')

        # Extract the magic number
        file.seek(0)
        magic_number = st.unpack('>4B', file.read(4))
        print("Magic number: {}".format(magic_number))

        # Find size and number of images in the file
        n_img = st.unpack('>I', file.read(4))[0]
        n_rows = st.unpack('>I', file.read(4))[0]
        n_cols = st.unpack('>I', file.read(4))[0]

        # Calculate the number of bytes in the file
        n_bytes = n_img * n_rows * n_cols

        # Read the image data and reshape it to image number and size
        data = file.read(n_bytes)
        data = st.unpack('>' + 'B' * n_bytes, data)
        data = 255 - np.asarray(data).reshape((n_img, n_rows, n_cols))

        # Close the data file
        file.close()

        return data


    @staticmethod
    def load_labels(filename):

        # Open the file
        file = open(filename, 'rb')

        # Extract the magic number
        file.seek(0)
        magic_number = st.unpack('>4B', file.read(4))
        print("Magic number: {}".format(magic_number))

        # Find number of images in the file
        n_img = st.unpack('>I', file.read(4))[0]

        # Calculate the number of bytes in the file
        n_bytes = n_img

        # Read the image data and reshape it to image number and size
        data = file.read(n_bytes)
        data = st.unpack('>' + 'B' * n_bytes, data)
        data = np.asarray(data).reshape(n_bytes, 1)

        data = np.array([x[0] for x in data], dtype='uint8')

        # Close the data file
        file.close()

        return data
