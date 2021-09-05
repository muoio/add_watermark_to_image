from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 




import os


import tkinter as tk, os, PyPDF2, time
from tkinter import colorchooser
from tkinter import filedialog,ttk,messagebox, Entry, ttk
import fitz
from fitz import  PDF_ENCRYPT_AES_128, PDF_PERM_ACCESSIBILITY,PDF_ENCRYPT_AES_256,PDF_ENCRYPT_RC4_40,PDF_ENCRYPT_KEEP,PDF_PERM_PRINT

class scrollwindow:
    def __init__(self,parent,**kwargs):
        canvas = tk.Canvas(parent, **kwargs)
        scrollbar = tk.Scrollbar(parent, orient = "vertical", command = canvas.yview)
        self.scrollframe = tk.Frame(canvas, **kwargs)

        self.scrollframe.bind("<Configure>",lambda x: canvas.configure(scrollregion = canvas.bbox("all")))
        canvas.create_window((0,0), window = self.scrollframe, anchor = "nw")
        canvas.configure(yscrollcommand = scrollbar.set)
        
        canvas.pack(side = "left", fill = "both")
        scrollbar.pack(side = "right", fill = "y")



def add_text(img_path, text, font_path, color, fontsize, posision):
	img = Image.open(img_path)
	draw = ImageDraw.Draw(img)
	width, height = img.size
	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype(font_path, fontsize)
	# draw.text((x, y),"Sample Text",(r,g,b))
	pos_x, pos_y = posision
	
	pos_x *= width/100
	pos_y *= height/100
	
	draw.text((pos_x, pos_y),text,color ,font=font)
	img.save(img_path)
	
	
#add_text('image.jpg', 'toi yeu lap trinh', "fonts/sansserif italic.ttf", (255,255,0), 40, (100,100))

def merge():
    num = len(pdf_files)
    #try:
    bar["maximum"] = num
    #watermark_reader = PyPDF2.PdfFileReader(watermark_field.get()).getPage(0)
    for num,file in enumerate(pdf_files):
        add_text(file,watermark.get(),font_field.get(), get_color(), int(fontSize.get()), get_position())

        bar["value"] = num + 1
        bar.update()
        time.sleep(1)
    messagebox.showinfo("Completed", f"Process Completed!\nAdded watermarks on {num+1} files")
   # except:
    #    messagebox.showerror("Error", "OOPS! Something went wrong.")

def addwatermark():
    x = filedialog.askdirectory(title = "Select folder")
    if x != "":
        watermark_field.configure(state = "normal")
        watermark_field.delete(0, tk.END)
        watermark_field.insert(0, x)
        watermark_field.configure(state = "readonly")

def addFont():
    x = filedialog.askopenfilename(title = "Select font ttf", filetypes = (("Font fIle","*.ttf"), ("All Files","*.*")),initialdir=os.getcwd())

    if x != "":
        font_field.configure(state = "normal")
        font_field.delete(0, tk.END)
        font_field.insert(0, x)
        font_field.configure(state = "readonly")

def get_color():
	r = int(float(color_field_r.get()))
	g = int(float(color_field_g.get()))
	b = int(float(color_field_b.get()))
	return (r,g,b)

def get_position():
	return (int(posision_X.get()),int(posision_Y.get()))

def choose_color():
 
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title ="Choose color")
    rgb,code = color_code
    r,g,b = rgb
    color_field_r.configure(state = "normal")
    color_field_r.delete(0, tk.END)
    color_field_r.insert(0, r)
    color_field_r.configure(state = "readonly")
    
    color_field_g.configure(state = "normal")
    color_field_g.delete(0, tk.END)
    color_field_g.insert(0, g)
    color_field_g.configure(state = "readonly")
    
    color_field_b.configure(state = "normal")
    color_field_b.delete(0, tk.END)
    color_field_b.insert(0, b)
    color_field_b.configure(state = "readonly")
    print(color_code)

def addfile():
    x = filedialog.askdirectory(title = "Select folder",initialdir= os.getcwd())
    for parent, dirnames, filenames in os.walk(x):
        for fn in filenames:
            if fn.lower().endswith('.png') or fn.lower().endswith('.jpg') or fn.lower().endswith('.jpeg'):
                y = os.path.join(parent, fn)
                y =y.replace('\\','/')
                pdf_files.append(y)
                tk.Label(frame, text = y, bg = "white", anchor = "w", padx = 10).pack(fill = "both")

def resetfile():
    global pdf_files
    pdf_files = []
    for child in frame.winfo_children():
        child.destroy()
        

pdf_files = []
root = tk.Tk()
root.title("IMAGES WATERMARKER")
#root.iconphoto(True, tk.PhotoImage(file = "icon.png"))
info = tk.LabelFrame(root, text = "Info", padx = 0, pady = 5)
info.grid(row = 0, column = 0, pady = 0, padx = 0)


#watermark frame
watermark_fr = tk.LabelFrame(info, text = "Watermark to add", padx = 0, pady = 5)
watermark_fr.grid(row = 0, column = 0, pady = 1, padx = 1)

watermark = ttk.Entry(watermark_fr,text="Watermark to add")
watermark.grid(row = 0, column = 0,  pady = 10, padx = 0)
# font frame
font_fr = tk.LabelFrame(info, text = "Select font", padx = 0, pady = 5)
font_fr.grid(row = 0, column = 1, pady = 0, padx = 0)

select_font = tk.Button(font_fr, text = "Load", command = addFont)
select_font.grid(row = 0, column = 0,  pady = 10, padx = 0)

font_field = tk.Entry(font_fr, width = 10, state = "readonly")
font_field.grid(row = 1, column = 0)

##fontSize

fontSize_fr = tk.LabelFrame(info, text = "Font size", padx = 0, pady = 5)
fontSize_fr.grid(row = 0, column = 2, pady = 0, padx = 0)

var = tk.StringVar()
fontSize = tk.Spinbox(fontSize_fr, from_=10, to=1000, width = 5, textvariable=var)
fontSize.grid(row = 0, column = 1, pady = 0, padx = 0)
var.set(30)




###postision x,y

position_fr = tk.LabelFrame(info, text = "Position", padx = 0, pady = 5)
position_fr.grid(row = 0, column = 3, pady = 0, padx = 0)

varX = tk.StringVar()
posision_X = tk.Spinbox(position_fr, from_=0, to=100, width = 5, textvariable=varX)
posision_X.grid(row = 0, column = 1, pady = 0, padx = 0)
varX.set(80)


varY = tk.StringVar()
posision_Y = tk.Spinbox(position_fr, from_=0, to=100, width = 5, textvariable=varY)
posision_Y.grid(row = 1, column = 1, pady = 0, padx = 0)
varY.set(80)

# COLOR PICKER
color_fr = tk.LabelFrame(info, text = "Select Color", padx = 0, pady = 5)
color_fr.grid(row = 0, column = 4, pady = 0, padx = 0)

select_font = tk.Button(color_fr, text = "Select Color", command = choose_color)
select_font.grid(row = 0, column = 0,  pady = 10, padx = 0)

color_field = tk.Entry(color_fr, width = 5, state = "readonly")
color_field.grid(row = 1, column = 0)

color_field_r = tk.Entry(color_field, width = 5, state = "readonly")
color_field_r.grid(row = 0, column = 0)

color_field_g = tk.Entry(color_field, width = 5, state = "readonly")
color_field_g.grid(row = 0, column = 1)

color_field_b = tk.Entry(color_field, width = 5, state = "readonly")
color_field_b.grid(row = 0, column = 2)



#images frame
files = tk.LabelFrame(root, text = "Files to have watermark on", padx = 15, pady = 10)
files.grid(row = 1, column = 0, padx = 5, pady = 5)

file_add = tk.Button(files, text = "Load", command = addfile)
file_add.grid(row = 0, column = 1, padx = 10)

file_reset = tk.Button(files, text = "Reset", command = resetfile)
file_reset.grid(row = 1, column = 1, padx = 10)

loaded_files = tk.LabelFrame(files, text = "Loaded Files", padx = 5, pady = 5)
loaded_files.grid(row = 0, column = 0, rowspan = 2)

scroll = scrollwindow(loaded_files, bg = "grey")
frame = scroll.scrollframe
'''
watermark = tk.LabelFrame(root, text = "Add watermark PDF file", padx = 10, pady = 10)
watermark.grid(row = 0, column = 0, pady = 5, padx = 5)

watermark_field = tk.Entry(watermark, width = 53, state = "readonly")
watermark_field.grid(row = 0, column = 0)

watermark_add = tk.Button(watermark, text = "Load", command = addwatermark)
watermark_add.grid(row = 0, column = 1, padx = 2)'''

but = tk.Button(root, text = "EXECUTE", command = merge)
but.grid(row = 2, column = 0, pady = 5)

bar = ttk.Progressbar(root, length = 525)
bar.grid(row = 3, column = 0, pady = 5, padx = 10)

root.mainloop()
