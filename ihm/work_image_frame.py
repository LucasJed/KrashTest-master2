import tkinter as tk
import numpy
from PIL import Image, ImageTk

from controllers import work_manager

img_size = (700, 500)


class WorkImageFrame(tk.Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Work config frame
        self.pack(expand=True)

        self.label = tk.Label(self, text="Creating work matrix...")
        self.label.pack()

        self.color_matrix = None
        self.validated_pixels = 0

    def display_matrix(self, matrix):

        tmp = matrix.copy()

        color_mask = (100, 100, 100)

        for row in range(len(matrix)):
            for column in range(len(matrix[0])):
                val = matrix[row][column]/255
                tmp[row][column] = [val * color_mask[0], val * color_mask[1], val * color_mask[2]]

        self.color_matrix = numpy.array(matrix, dtype=numpy.uint8)

        img_data = Image.fromarray(self.color_matrix)
        img_data = img_data.transpose(Image.ROTATE_90)
        img = ImageTk.PhotoImage(image=img_data.resize(img_size))

        self.label.configure(image=img)
        self.label.image = img

        self.start()

    def start(self):
        work_manager.do_work(update_callback=self.update_progress, callback=self.complete)

    def complete(self):
        tk.Label(self, text="Finished !").pack()
        tk.Button(self, text='OK', command=self.close).pack()

    def close(self):
        self.master.display_form_frame()

    def update_progress(self, value):

        validation_color_mask = (0, 100, 0)

        row_size = len(self.color_matrix[0])

        delta = value - self.validated_pixels
        row = self.validated_pixels // row_size
        column = self.validated_pixels - row * row_size

        for _ in range(delta):
            self.color_matrix[row][column][0] = self.color_matrix[row][column][0] + validation_color_mask[0]
            self.color_matrix[row][column][1] = self.color_matrix[row][column][1] + validation_color_mask[1]
            self.color_matrix[row][column][2] = self.color_matrix[row][column][2] + validation_color_mask[2]

            if column < row_size-1:
                column += 1
            else:
                column = 0
                row += 1

        self.validated_pixels = value

        img_data = Image.fromarray(self.color_matrix)
        img_data = img_data.transpose(Image.ROTATE_90)
        img = ImageTk.PhotoImage(image=img_data.resize(img_size))

        self.label.configure(image=img)
        self.label.image = img