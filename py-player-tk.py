import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import os
import ctypes

# file must be in same directory as the script
FILEPATH =  os.path.join(os.path.dirname(os.path.realpath(__file__)), "canaletv.txt")
# lines from file with "channel name" -- "link"
channel_array = []

# split file by line and adding it to the array
with open(FILEPATH) as f:
    for line in f:
    	channel_array.append(line)

# dictionary with key = channel name and value = link
channel_dict = dict(ch.split(" -- ") for ch in channel_array)

# Remote window size, name, bring to front
root = tk.Tk()
root.title("Remote")
root.geometry("200x1370+%d+%d" % (-8, -3))
root.lift()
# always on top
# root.attributes("-topmost", True)

# create the placeholder for the channels and add it to the window
channel_box = tk.Listbox(root,height = 60, width = 40, bg = 'black', fg = 'green', font = ('Arial',20))
channel_box.pack()

# add channels to the placeholder
for channel in channel_dict.keys():
    channel_box.insert(0, channel)

#   keep focus on the remote window
set_to_foreground = ctypes.windll.user32.SetForegroundWindow
keybd_event = ctypes.windll.user32.keybd_event
alt_key = 0x12
extended_key = 0x0001
key_up = 0x0002

def steal_focus():
    keybd_event(alt_key, 0, extended_key | 0, 0)
    set_to_foreground(root.winfo_id())
    keybd_event(alt_key, 0, extended_key | key_up, 0)
    channel_box.focus_set()
# end of keeping focus

# ffplay configs
ffplayer = "ffplay -window_title tv_player "
ffplayer_kill = "taskkill /im ffplay.exe"

# mpv configs
mpv = "mpv --autofit=40%x40% --geometry=1565:840 --force-window "
mpv_kill = "taskkill /im mpv.exe"

# sellecting the channel from list
# opens the external player with the proper atributes from configs
def ffplay(event):
    if channel_box.curselection():
        # get channel name of the sellected item
        channel = channel_box.get(channel_box.curselection()[0])
        # get link from channel dict
        link = channel_dict[channel]
        # kill external player / open with new link
        os.system(mpv_kill)
        os.popen(mpv + link)
        # set focus on remote window
        root.after(500, steal_focus)

# call ffplay when channel selected
channel_box.bind('<<ListboxSelect>>',ffplay)

root.mainloop()