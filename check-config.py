#!/usr/bin/env python
"""check-config.py -- VisionEgg configuration check

Run this program first to check the installation status or version
number of the Vision Egg.

"""

import sys, string, os, traceback

# Mac OS X weirdness:

gui_ok = 1

if sys.platform == 'darwin':

    try:
        if not os.path.isabs(sys.argv[0]):
            
            print """Mac OS X - It appears you are running this script
            from the commandline -- turning off GUIs."""
            
            gui_ok = 0
    except Exception, x:
        raise
    print

# sys.stdout and sys.stderr hard to see:

if sys.platform in ['darwin','mac','win32'] and gui_ok:
    try:
        import Tkinter
        class showwarning(Tkinter.Frame):
            def format_string(self,in_str):
                min_line_length = 65
                in_list = string.split(in_str)
                out_str = ""
                cur_line = ""
                for word in in_list:
                    cur_line = cur_line + word + " "
                    if len(cur_line) > min_line_length:
                        out_str = out_str + cur_line[:-1] + "\n"
                        cur_line = ""
                out_str = out_str + cur_line
                return out_str
            def close_window(self,dummy_arg=None):
                #self.destroy()
                self.winfo_toplevel().destroy()
            def __init__(self,title="Vision Egg Warning",message=None):
                Tkinter.Frame.__init__(self,borderwidth=20)
                #self.focus_force()
                self.pack()
                self.winfo_toplevel().title(title)
                Tkinter.Label(self,text=self.format_string(message)).pack()
                b = Tkinter.Button(self,text="OK",command=self.close_window)
                b.pack()
                b.focus_force()
                b.bind('<Return>',self.close_window)
                self.mainloop()
        if sys.platform == 'darwin':
            
            add_str = """ To see this information, run the utility
            'Console' in the 'Applications/Utilities' Folder."""
            
        elif sys.platform == 'win32':
            
            add_str = """ After this script has finished, second GUI
            window will appear.  Until this window is closed, it keeps
            the console available for viewing."""

        else:
            
            add_str = """ Information specific to your platform has
            not been written yet."""
            
        showwarning(title="Conole location warning",
                    message=
                    
            """This script displays information on the console, which
            is not readily visible on this platform."""+add_str)
        
    except:
        print "(Failed to open dialog box-- is Tkinter installed?)"

# Import
unknown_import_fail = 0

try:
    import VisionEgg
except ImportError:
    print """Could not import the VisionEgg module.
    
    This is probably because it is not yet installed.
    
    Try installing by running 'python setup.py install' from the
    command line (as root if necessary).

    The exception raised was:"""
    traceback.print_exc()
except AttributeError, x:
    try:
        def my_import(name):
            mod = __import__(name)
            components = string.split(name, '.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
                return mod
        mod = my_import("VisionEgg.VisionEgg")
        if mod.__name__ == "VisionEgg.VisionEgg":
            print """            **********************************************************
            YOU APPEAR TO HAVE AN OLD COPY OF THE VISION EGG INSTALLED

            Please remove the old installation directory and re-install.

            The old installation directory is %s
            **********************************************************"""%(os.path.abspath(os.path.dirname(mod.__file__)),)
        else:
            unknown_import_fail = 1
    except:
        unknown_import_fail = 1
except:
    unknown_import_fail = 1

if unknown_import_fail:
    print """Could not import the VisionEgg module for an unknown reason.
    
    The exception raised was:"""
    traceback.print_exc()

# Finally, do it!

if 'VisionEgg' in globals().keys():
    print "VisionEgg version %s"%(VisionEgg.release_name,)
    print
    if VisionEgg.config.VISIONEGG_CONFIG_FILE:
        print "Config file found at %s"%(VisionEgg.config.VISIONEGG_CONFIG_FILE,)
    else:
        configuration_src = '<unable to find>'
        try:
            import VisionEgg.Configuration
            configuration_src = VisionEgg.Configuration.__file__
        except:
            pass
        print "No config file found, using defaults from file %s"%(configuration_src,)

    print
    for configname in dir(VisionEgg.config):
        if configname[:2] != '__':
            print configname + " = " + str(getattr(VisionEgg.config,configname))
    print

    print "The demo files should be in %s"%(os.path.join(VisionEgg.config.VISIONEGG_SYSTEM_DIR,'demos'),)

    print

    # These things have been removed from the installed library directory.
    # Print error if it's still around
    ancient_VisionEgg_files = ['AppHelper.py', # old module
                               'demo', # old install location
                               'test', # old install location
                               ]
    files_installed = os.listdir(os.path.dirname(VisionEgg.__file__))
    ancient_files = []
    for filename in ancient_VisionEgg_files:
        if filename in files_installed:
            ancient_files.append(filename)
    if len(ancient_files):
        print """        ************************************************************
        
        WARNING: The following files were found in your VisionEgg
        library directory:

        %s

        The library directory is %s

        These files are from old installations of the Vision
        Egg. Although they will not cause problems unless your scripts
        import them, they may lead to confusion.
        
        ************************************************************
        
        """%(string.join(ancient_files),os.path.abspath(os.path.dirname(VisionEgg.__file__)))
else:
    print "VisionEgg not installed (or other VisionEgg import problems)"
    print
    print "Continuing with prerequisites check."
    print

print "Version checklist:"

print

print "Python version %s"%(sys.version,)

try:
    import Numeric
    print "Numeric version %s"%(Numeric.__version__,),
    if Numeric.__version__ >= '20.':
        print "(OK)"
    else:
        print "(Untested)"
except:
    print "Numeric <failed>"

try:
    import OpenGL
    print 'PyOpenGL (package "OpenGL") version %s'%(OpenGL.__version__,),
    if OpenGL.__version__ >= '2.0': 
        print "(OK)"
    else:
        print "(Untested)"
except:
    print 'PyOpenGL (package "OpenGL") failed'

try:
    import pygame.version
    print "pygame version %s"%(pygame.version.ver,),
    if pygame.version.ver >= '1.5':
        print "(OK)"
    elif pygame.version.ver >= '1.3.3':
        print "(Some VisionEgg features unsupported)"
    else:
        print "(Untested)"
except:
    print "pygame failed"

try:
    import Image # PIL
    print 'Python Imaging Library (package "Image") version %s'%(Image.VERSION,),
    if Image.VERSION >= '1.1.2':
        print "(OK)"
    else:
        print "(Untested)"
except:
    print 'Python Imaging Library (package "Image") failed'
    
print

print "Optional module(s):"

print

try:
    import Pyro.core
    print "Pyro version %s"%(Pyro.core.constants.VERSION,),
    if Pyro.core.constants.VERSION >= '2.7':
        print "(OK)"
    else:
        print "(Untested)"
except:
    print "Pyro failed"

if sys.platform == 'win32':
    try:
        import winioport
        print "winioport",
        try:
            winioport.out(0x378,0)
            print "(appears to work)"
        except:
            print "(not working)"
    except:
        print "winioport failed"

if gui_ok and sys.platform == 'win32':
    showwarning(title="View the console",
                             message=
        
        """This dialog keeps the console open until you close
        it. However, this feature is not provided by other Vision Egg
        scripts.  Although the Vision Egg does not print by default to the console,
        all python errors

        , so an error occursif anything (such as errors) is printed to the console
        you have to run from the command line to see the
        console -- sorry!""")
