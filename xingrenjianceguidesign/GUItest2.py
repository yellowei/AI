#Author:Huangliang   
#Time:2018/5/27
from tkinter import *
from tkinter.filedialog import *

def selectPath1():
    # path_ = askopenfilename(title='请打开一个.lst文件', filetypes=[('lst', '.lst')],initialdir=r'C:\Users\Timor\Desktop\xingrenjiance',defaultextension='.lst')
    # path.set(path_)
    fd = LoadFileDialog(root)  # 创建打开文件对话框
    filename = fd.go()  # 显示打开文件对话框，并获取选择的文件名称
    path1.set(filename) # 全局变量
    print(filename)

def selectPath2():
    # path_ = askopenfilename(title='请打开一个.lst文件', filetypes=[('lst', '.lst')],initialdir=r'C:\Users\Timor\Desktop\xingrenjiance',defaultextension='.lst')
    # path.set(path_)
    fd = LoadFileDialog(root)  # 创建打开文件对话框
    filename = fd.go()  # 显示打开文件对话框，并获取选择的文件名称
    path2.set(filename)  # 全局变量
    print(filename)

root = Tk()
path1 = StringVar()
path2 = StringVar()

Label(root,text = "目标路径:").grid(row = 0, column = 0)
Label(root,text = "目标路径:").grid(row = 1, column = 0)
et1 = Entry(root, textvariable = path1, state='readonly').grid(row = 0, column = 1)
et2 = Entry(root, textvariable = path2, state='readonly').grid(row = 1, column = 1)


Button(root, text = "路径选择", command = selectPath1).grid(row = 0, column = 2)
Button(root, text = "路径选择", command = selectPath2).grid(row = 1, column = 2)

root.mainloop()