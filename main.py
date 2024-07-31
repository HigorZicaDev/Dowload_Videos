import tkinter
from tkinter import *
from tkinter import ttk

import os
from pathlib import Path

import datetime
import calendar

from PIL import ImageTk, Image,ImageOps , ImageDraw

import requests

from pytubefix import YouTube
from pytubefix.cli import on_progress
from tkinter.ttk import Progressbar

################# cores ###############
co0 = "#444466"  # Preta
co1 = "#feffff"  # branca
co2 = "#6f9fbd"  # azul
co3 = "#38576b"  # valor
co4 = "#403d3d"   # letra

fundo = "#3b3b3b"
btn_fundo = "#ccc"


janela = Tk()
janela.title('')
janela.geometry('500x300')
janela.configure(bg=fundo)

################# Frames ####################

ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=250)

frame_principal = Frame(janela, width=500, height=110,bg=fundo, pady=5, padx=0, relief="flat",)
frame_principal.grid(row=1, column=0)

frame_quadros = Frame(janela, width=500, height=300,bg=fundo, pady=12, padx=0, relief="flat",)
frame_quadros.grid(row=2, column=0, sticky=NW)

logo = Image.open('images/youtube.png')
logo = logo.resize((50, 50))
logo = ImageTk.PhotoImage(logo)
l_logo = Label(frame_principal,image=logo, compound=LEFT,  bg=fundo, fg="white",font=('Ivy 10 bold'), anchor="nw", relief=FLAT)
l_logo.place(x=5, y=10)

app_nome = Label(frame_principal, text="YouTube Downloader app", width=32, height=1, padx=0, relief="flat", anchor="nw", font=('Ivy 15 bold'), bg=fundo, fg=co1)
app_nome.place(x=65, y=15)

#style = ttk.Style(frame_principal)
#style.theme_use("clam")


def search():
	global img
	url=e_url.get()
	yt=YouTube(url)

	#Title of video
	title=yt.title
	#Number of views of video
	view= yt.views

	#Length of the video
	duration= str(datetime.timedelta(seconds=yt.length)) 

	#Description of video
	Description=yt.description

	#cover of the video
	cover=yt.thumbnail_url



	print(cover)


	img_ = Image.open(requests.get(cover, stream=True).raw)
	img_ = img_.resize((230, 150))
	img_ = ImageTk.PhotoImage(img_)

	img=img_
	l_image['image']=img

	l_title['text']="Titlo : " + str(title)
	l_view['text']="Views : " + str('{:,}'.format(view))
	l_time['text']="Duracao : " + str(duration)



previousprogress = 0
concluido= "Feito download com sucesso!"

def on_progress(stream, chunk, bytes_remaining):
    global previousprogress
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining 

    liveprogress = (int)(bytes_downloaded / total_size * 100)
    if liveprogress > previousprogress:
        previousprogress = liveprogress
        print(liveprogress)
        bar.place(x=250, y=120)
        bar['value'] = liveprogress
        janela.update_idletasks()

def download():
	url=e_url.get()
	yt = YouTube(url)
	
	yt.on_progress_callback = on_progress
	ys = yt.streams.get_highest_resolution()
	ys.download(Path.home()/'Downloads')

	l_success['text'] = str(concluido)

def dowload_audio():
	url=e_url.get()
	yt = YouTube(url)
	
	yt.on_progress_callback = on_progress
	ys = yt.streams.get_audio_only()
	ys.download(mp3=True, output_path=Path.home()/'Downloads')

	l_success['text'] = str(concluido)
    



l_url = Label(frame_principal, text="Enter URL", height=1,pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 10 bold'), bg=fundo, fg=co1)
l_url.place(x=10, y=80)

e_url = Entry(frame_principal, width=50, justify='left',relief=SOLID)
e_url.place(x=100, y=80)

b_search = Button(frame_principal, text="Search", width=10, height=1, bg=co2, fg=co1,font=('Ivy 7 bold'), relief=RAISED, overrelief=RIDGE,command = lambda:search())
b_search.place(x=404, y=80)


################ Operations ####################

l_image = Label(frame_quadros, compound=LEFT,  bg=fundo, fg="white",font=('Ivy 10 bold'), anchor="nw", relief=FLAT)
l_image.place(x=10, y=10)

l_title = Label(frame_quadros,  height=2,pady=0, padx=0, relief="flat",wraplength=225,compound=LEFT,justify='left', anchor=NW, font=('Ivy 10 bold'), bg=fundo, fg=co1)
l_title.place(x=250, y=15)

l_view = Label(frame_quadros, height=1,pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 8 bold'), bg=fundo, fg=co1)
l_view.place(x=250, y=60)

l_time = Label(frame_quadros, height=1,pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 8 bold'), bg=fundo, fg=co1)
l_time.place(x=250, y=85)

l_success = Label(frame_quadros, height=1,pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 8 bold'), bg=fundo, fg=co1)
l_success.place(x=250, y=85)



down = Image.open('images/download_2.png')
down = down.resize((30, 30))
down = ImageTk.PhotoImage(down)
b_download = Button(frame_quadros, image=down, bg=btn_fundo, fg=co1,font=('Ivy 10 bold'), relief=FLAT, overrelief=RIDGE, command=download)
b_download.place(x=444, y=75)

audio = Image.open('images/music.png')
audio = audio.resize((30, 30))
audio = ImageTk.PhotoImage(audio)
b_audio = Button(frame_quadros, image=audio, bg=btn_fundo, fg=co1,font=('Ivy 10 bold'), relief=FLAT, overrelief=RIDGE, command=dowload_audio)
b_audio.place(x=444, y=125)

style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='#00E676')
style.configure("TProgressbar", thickness=6)

bar = Progressbar(frame_quadros, length=190,style='black.Horizontal.TProgressbar')


janela.mainloop()