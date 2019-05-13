from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os.path as osp
from PIL import ImageTk,Image
from fossilseg.segment.thresholding import segment

HERE = osp.dirname(osp.abspath(__file__))
IMAGE_PATH = osp.join(HERE, 'fossil.bmp')

#
# Main Window
#
class FossilSegmentApp(Frame):
	def __init__(self, master=None, title="Fossil Segmentation"):
		Frame.__init__(self, master)
		self.master = master
		self.pack(fill=BOTH, expand=1)
		# changing the title of our master widget
		self.master.title(title)
		self.initWidgets()
		self.original_image = None
		self.render_image = None
		self.result_image = None

	def initWidgets(self):
		# create a toplevel menu
		menubar = Menu(self)
		# create a pulldown menu, and add it to the menu bar
		filemenu = Menu(menubar, tearoff=0)
		# TODO: implement the
		filemenu.add_command(label="Open", command=self.open_file)
		filemenu.add_command(label="Save", command=self.hello)
		filemenu.add_command(label="Exit", command=self.master.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		# create more pulldown menus
		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label="Cut", command=self.hello)
		editmenu.add_command(label="Copy", command=self.hello)
		editmenu.add_command(label="Paste", command=self.hello)
		menubar.add_cascade(label="Edit", menu=editmenu)
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="About", command=self.hello)
		menubar.add_cascade(label="Help", menu=helpmenu)
		# display the menu
		self.master.config(menu=menubar)


		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)
		configframe = Frame(self)
		configframe.grid(row=0, column=0, sticky=N+S+E+W)
		imageframe = Frame(self)
		imageframe.grid(row=0, column=1, sticky=N+S+E+W)

		Label(configframe, text="Gaussian filter sigma").grid(row=0, sticky=W, padx=20)
		self.e_gaussian_sigma = Entry(configframe)
		self.e_gaussian_sigma.grid(row=1, sticky="nsew", padx=20)
		Label(configframe, text="Minimal object size").grid(row=2, sticky=W, padx=20)
		self.e_minimal_object_size = Entry(configframe)
		self.e_minimal_object_size.grid(row=3, sticky="nsew", padx=20)

		btn_thresholding = Button(configframe, text="Segment", command=self.thresholding)
		btn_thresholding.grid(row=4, sticky="nsew", padx=20, pady = 20)
		btn_superpixels = Button(configframe, text="SLIC", command=self.slic)
		btn_superpixels.grid(row=5, sticky="nsew", padx=20, pady = 20)

		# load = Image.open(IMAGE_PATH)
		# render = ImageTk.PhotoImage(load)
		self.canvas = Canvas(imageframe, bg='blue',  width=800, height=600)
		# canvas = Canvas(imageframe, bg='blue')
		self.canvas.grid(row=0, column=1, sticky="nsew")
		# canvas.create_image(20, 20, anchor=NW, image=render)
		# canvas.image = render

	def hello(self):
		print("hello!")

	def open_file(self):
		image_filename = filedialog.askopenfilename(initialdir="D:\\Code\\Python\\fossil-segmentation", title="Select file", filetypes=(("all files", "*.*")))
		self.original_image = Image.open(image_filename)
		self.render_image = self.fit_canvas_size(self.original_image)
		render = ImageTk.PhotoImage(self.render_image)
		self.canvas.create_image(0, 0, anchor=NW, image=render)
		self.canvas.image = render

	def thresholding(self):
		try:
			sigma = self.e_gaussian_sigma.get()
			messagebox.showinfo("Input Error", "a ")
		c
		self.result_image = segment(self.original_image)
		self.render_image = self.fit_canvas_size(self.result_image)
		render = ImageTk.PhotoImage(self.render_image)
		self.canvas.create_image(0, 0, anchor=NW, image=render)
		self.canvas.image = render

	def slic(self):
		print(self.e_gaussian_sigma.get())

	def fit_canvas_size(self, pil_image, canvas_size=(800,600)):
		width, height = canvas_size[0], canvas_size[1]
		img_width, img_height = pil_image.size
		if height/width > img_height/img_width:
			new_width = width
			new_height = int(img_height * (width/img_width))
		else:
			new_height = height
			new_width = int(img_width * (height/img_height))
		return pil_image.resize((new_width,new_height), Image.BILINEAR)

if __name__ == '__main__':
	win = Tk()
	# win.geometry("600x800")
	app = FossilSegmentApp(win, title="Fossil Segmentation")
	win.mainloop()
