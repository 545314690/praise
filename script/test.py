from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class Puzzle:
    def __init__(self, master):
        self.master = master
        self.master.title("图片拼图程序")
        self.master.resizable(False, False)
        self.images = []
        self.photo_images = []
        self.pieces = []
        self.rows = 0
        self.cols = 0
        self.rotation = 0
        self.scale = 1.0
        self.current_piece = None
        self.canvas_width = 600
        self.canvas_height = 600
        self.canvas = Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label="文件", menu=self.file_menu)
        self.file_menu.add_command(label="导入图片", command=self.import_image)
        self.file_menu.add_command(label="导出拼图", command=self.export_image)
        self.piece_menu = Menu(self.menu)
        self.menu.add_cascade(label="拼图", menu=self.piece_menu)
        self.piece_menu.add_command(label="旋转90度", command=self.rotate_right)
        self.piece_menu.add_command(label="旋转-90度", command=self.rotate_left)
        self.piece_menu.add_command(label="放大", command=self.zoom_in)
        self.piece_menu.add_command(label="缩小", command=self.zoom_out)
        self.canvas.bind("<Button-1>", self.select_piece)
        self.canvas.bind("<ButtonRelease-1>", self.release_piece)
        self.canvas.bind("<B1-Motion>", self.move_piece)

    def import_image(self):
        filenames = filedialog.askopenfilenames(title="选择图片")
        if not filenames:
            return
        for filename in filenames:
            try:
                image = Image.open(filename)
                self.images.append(image)
                photo_image = ImageTk.PhotoImage(image)
                self.photo_images.append(photo_image)
            except:
                messagebox.showerror("错误", "无法打开文件: " + filename)
                continue
        self.update_pieces()

    def update_pieces(self):
        self.pieces = []
        if not self.images:
            return
        for i, image in enumerate(self.images):
            piece_width = int(image.width * self.scale)
            piece_height = int(image.height * self.scale)
            rows = int(self.canvas_height / piece_height)
            cols = int(self.canvas_width / piece_width)
            for row in range(rows):
                for col in range(cols):
                    x = col * piece_width
                    y = row * piece_height
                    piece = image.crop((0, 0, image.width, image.height)).resize((piece_width, piece_height), Image.ANTIALIAS)
                    self.pieces.append((piece, x, y, i))
        self.rows = rows
        self.cols = cols
        self.draw_pieces()

    def draw_pieces(self):
        self.canvas.delete("all")
        for piece, x, y, i in self.pieces:
            photo_image = Image
            photo_image = Tk.PhotoImage(piece)
            self.canvas.create_image(x, y, anchor=NW, image=photo_image)
            self.canvas.create_rectangle(x, y, x + piece.width(), y + piece.height(), width=1, outline="black")
    def rotate_right(self):
        self.rotation += 90
        self.update_pieces()

    def rotate_left(self):
        self.rotation -= 90
        self.update_pieces()

    def zoom_in(self):
        self.scale += 0.1
        self.update_pieces()

    def zoom_out(self):
        if self.scale > 0.1:
            self.scale -= 0.1
            self.update_pieces()

    def select_piece(self, event):
        x = event.x
        y = event.y
        for piece, px, py, i in self.pieces:
            if px <= x < px + piece.width() and py <= y < py + piece.height():
                self.current_piece = (piece, px, py, i)
                break

    def release_piece(self, event):
        self.current_piece = None

    def move_piece(self, event):
        if self.current_piece:
            piece, px, py, i = self.current_piece
            dx = event.x - px
            dy = event.y - py
            px += dx
            py += dy
            self.current_piece = (piece, px, py, i)
            self.draw_pieces()

    def export_image(self):
        if not self.pieces:
            return
        image_width = self.cols * self.pieces[0][0].width()
        image_height = self.rows * self.pieces[0][0].height()
        image = Image.new("RGB", (image_width, image_height), "white")
        for piece, x, y, i in self.pieces:
            x += int((self.canvas_width - self.cols * piece.width()) / 2)
            y += int((self.canvas_height - self.rows * piece.height()) / 2)
            piece = piece.rotate(self.rotation, expand=True)
            piece = piece.resize((int(piece.width() * self.scale), int(piece.height() * self.scale)), Image.ANTIALIAS)
            image.paste(piece, (x, y))
        filename = filedialog.asksaveasfilename(title="保存拼图", filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.bmp")])
        if filename:
            try:
                image.save(filename)
                messagebox.showinfo("成功", "拼图已保存到文件: " + filename)
            except:
                messagebox.showerror("错误", "无法保存文件: " + filename)

root = Tk()
app = Puzzle(root)
root.mainloop()