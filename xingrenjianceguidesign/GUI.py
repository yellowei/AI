#Author:Huangliang   
#Time:2018/5/25
import tkinter as tk
from tkinter.filedialog import *
import tkinter.messagebox
import Final_Fantasy_Driver as FFD
import demo_training as DT
import threading

window = tk.Tk()
window.title('Pedestrians Detector')
window.geometry('300x210')

def tick():
    import winsound
    winsound.PlaySound('./prompt_tone/3.wav', winsound.SND_ASYNC)
def tick1():
    import winsound
    winsound.PlaySound('./prompt_tone/1.wav', winsound.SND_ASYNC)
def Choose():
    tick()
    choose = var.get()
    if choose == 1:
        DEMOTRAINING()
    elif choose == 2:
        VIDEODETECTION()

def DEMOTRAINING():
    window1 = tk.Toplevel()
    window1.title('设置路径')
    window1.geometry('400x150')
    path1 = tk.StringVar()
    path2 = tk.StringVar()

    def selectPath1():
        tick1()
        fd = LoadFileDialog(window1)  # 创建打开文件对话框
        filename = fd.go()  # 显示打开文件对话框，并获取选择的文件名称
        print(filename)
        path1.set(filename)  # 全局变量
        print(path1.get())

    def selectPath2():
        tick1()
        fd = LoadFileDialog(window1)  # 创建打开文件对话框
        filename = fd.go()  # 显示打开文件对话框，并获取选择的文件名称
        print(filename)
        path2.set(filename)  # 全局变量
        print(path2.get())

    def training():
        tick()
        newfilename1 = path1.get()
        newfilename2 = path2.get()
        newfilename1 = newfilename1.replace('\\','/')
        newfilename2 = newfilename2.replace('\\','/')
        print(newfilename1)
        print(newfilename2)
        window1.destroy()

        # 显示训练日志
        window2 = tk.Toplevel()
        window2.title('训练中...')
        window2.geometry('400x600')


        try:
            # 创建子线程进行训练，不卡主线程去刷新UI
            new_thread_1 = threading.Thread(target=DT.main, args=(newfilename1, newfilename2, window2,))
            new_thread_1.setDaemon(True)
            new_thread_1.start()

        except:
            print("Error: unable to start training")

        window2.mainloop()

    l0 = Label(window1, text="请保证样本集文件夹中存在.lst图片名列表文件\n").grid(row=0, column=1)
    l1 = Label(window1, text="POS目标路径:").grid(row=1, column=0)
    et1 = Entry(window1, textvariable=path1).grid(row=1, column=1)
    bt1 = Button(window1, text="路径选择", command=selectPath1).grid(row=1, column=2)
    l1 = Label(window1, text="NEG目标路径:").grid(row=2, column=0)
    et2 = Entry(window1, textvariable = path2).grid(row = 2, column = 1)
    bt2 = Button(window1, text="路径选择", command=selectPath2).grid(row=2, column=2)
    bt3 = Button(window1, text="   确定   ", command=training).grid(row=3, column=2)

    window1.mainloop()

def VIDEODETECTION():
    window2 = tk.Toplevel()
    window2.title('设置路径')
    window2.geometry('290x105')
    path3 = tk.StringVar()
    def selectPath1():
        tick1()
        fd = LoadFileDialog(window2)  # 创建打开文件对话框
        filename = fd.go()  # 显示打开文件对话框，并获取选择的文件名称
        path3.set(filename)  # 全局变量

    def detection():
        tick()
        filename = path3.get()
        newfilename = filename.replace('\\', '/')
        print(newfilename)
        FFD.main(newfilename)
        tick()
        tk.messagebox.showinfo('提示', '视频处理完成')

    l0 = Label(window2, text="请选择视频文件的路径\n").grid(row=0, column=1)
    l1 = Label(window2, text="原始视频路径:").grid(row=1, column=0)
    et1 = Entry(window2, textvariable=path3).grid(row=1, column=1)
    bt1 = Button(window2, text="路径选择", command=selectPath1).grid(row=1, column=2)
    bt3 = Button(window2, text="   确定   ", command=detection).grid(row=2, column=2)
    window2.mainloop()

var = tk.IntVar()
l1 = Label(window,text='\n欢迎使用视频行人检测系统\n\n请选择您需要的功能\n').pack()
r1 = tk.Radiobutton(window, text='训练样本',variable=var, value=1)
r1.pack()
r2 = tk.Radiobutton(window, text='检测视频',variable=var, value=2)
r2.pack()
bt = tk.Button(window, text='确定', width=15, height=2, command=Choose)
bt.pack()

window.mainloop()
