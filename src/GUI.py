# This is the python source code for GUI bits of the Vision Egg package.
#
#
# Copyright (c) 2001, 2002 Andrew Straw.  Distributed under the terms of the
# GNU General Public License (GPL).

####################################################################
#
#        Import all the necessary packages
#
####################################################################

import string
__version__ = string.split('$Revision$')[1]
__date__ = string.join(string.split('$Date$')[1:3], ' ')
__author__ = 'Andrew Straw <astraw@users.sourceforge.net>'

import os
import Tkinter
import VisionEgg

####################################################################
#
#        StartGraphicsFrame
#
####################################################################

class OpenScreenFrame(Tkinter.Frame):
    """A GUI window to open an instance of Screen"""
    def __init__(self,master=None,set_screen_callback=lambda s: None,**cnf):
        apply(Tkinter.Frame.__init__,(self,master),cnf)
        self.winfo_toplevel().title('Vision Egg - Graphics configuration')
        self.pack()
        self.set_screen_callback = set_screen_callback

        # Fullscreen
        self.fullscreen = Tkinter.BooleanVar()
        self.fullscreen.set(VisionEgg.config.VISIONEGG_FULLSCREEN)
        Tkinter.Checkbutton(self,
                            text='Fullscreen - use only with multiple displays',
                            variable=self.fullscreen,
                            relief=Tkinter.FLAT).pack()

        # texture compression
        self.tex_compress = Tkinter.BooleanVar()
        self.tex_compress.set(VisionEgg.config.VISIONEGG_TEXTURE_COMPRESSION)
        Tkinter.Checkbutton(self,
                            text='Texture compression',
                            variable=self.tex_compress,
                            relief=Tkinter.FLAT).pack()

        # resolution
        Tkinter.Label(self,text="Window size (pixels):").pack()
        self.resolution = Tkinter.StringVar()
        default_res_string = "%dx%d"%(VisionEgg.config.VISIONEGG_SCREEN_W,VisionEgg.config.VISIONEGG_SCREEN_H)
        self.resolution.set(default_res_string)
        Tkinter.OptionMenu(self,self.resolution,default_res_string,"640x480","800x600","1024x768").pack()

        # color depth
        Tkinter.Label(self,text="Color depth (bits per pixel):").pack()
        self.color_depth = Tkinter.StringVar()
        default_bpp_string = "%d"%VisionEgg.config.VISIONEGG_PREFERRED_BPP
        self.color_depth.set(default_bpp_string)
        Tkinter.OptionMenu(self,self.color_depth,default_bpp_string,"0 (Any)","16","24","32").pack()

        # Start button
        Tkinter.Button(self,text="start",command=self.start).pack()
        
    def start(self):
        
        VisionEgg.config.VISIONEGG_FULLSCREEN = self.fullscreen.get()
        VisionEgg.config.VISIONEGG_TEXTURE_COMPRESSION = self.tex_compress.get()
        VisionEgg.config.VISIONEGG_SCREEN_W, VisionEgg.config.VISIONEGG_SCREEN_H = map(int,string.split(self.resolution.get(),'x'))
        VisionEgg.config.VISIONEGG_PREFERRED_BPP = int(string.split(self.color_depth.get(),' ')[0])

        screen = VisionEgg.Core.Screen(size=(VisionEgg.config.VISIONEGG_SCREEN_W,
                                             VisionEgg.config.VISIONEGG_SCREEN_H),
                                       fullscreen=VisionEgg.config.VISIONEGG_FULLSCREEN,
                                       preferred_bpp=VisionEgg.config.VISIONEGG_PREFERRED_BPP,
                                       bgcolor=VisionEgg.config.VISIONEGG_SCREEN_BGCOLOR)

        for child in self.children.values():
            child.destroy()

        self.set_screen_callback(screen)
        Tkinter.Tk.destroy(self.master) # OK, now close myself

class VideoInfoFrame(Tkinter.Frame):
    def __init__(self,master=None,**cnf):
        apply(Tkinter.Frame.__init__,(self,master),cnf)
        self.pack()

        Tkinter.Label(self,text="Video information:").pack()
        self.sub_frame = Tkinter.Frame(self,relief=Tkinter.GROOVE)
        self.sub_frame.pack()
        self.update()

    def update(self):
        for child in self.sub_frame.children.values():
            child.destroy()
        if VisionEgg.video_info.initialized:
            if VisionEgg.video_info.fullscreen:
                Tkinter.Label(self.sub_frame,text="fullscreen: %d x %d, %d bpp"%(VisionEgg.video_info.width,VisionEgg.video_info.height,VisionEgg.video_info.bpp)).pack()
            else:
                Tkinter.Label(self.sub_frame,text="window: %d x %d, %d bpp"%(VisionEgg.video_info.width,VisionEgg.video_info.height,VisionEgg.video_info.bpp)).pack()
            if VisionEgg.video_info.tex_compress:
                Tkinter.Label(self.sub_frame,text="Texture compression: On").pack()
            else:
                Tkinter.Label(self.sub_frame,text="Texture compression: Off").pack()
        else:
            Tkinter.Label(self.sub_frame,text="Video system not initialized").pack()

#        Tkinter.Button(self.sub_frame,text="Update video info",command=self.update).pack()

def get_screen_via_GUI():
    def callback(screen):
        global opened_screen # Python doesn't support nested namespace, so this is a trick
        opened_screen = screen
    global opened_screen
    window = OpenScreenFrame(set_screen_callback=callback)
    window.mainloop()
    local_screen = opened_screen
    del opened_screen # Get rid of evil global variables!
    return local_screen
