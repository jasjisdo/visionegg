#!/usr/bin/env python

# Copyright (c) 2002-2003 Andrew Straw.  Distributed under the terms
# of the GNU Lesser General Public License (LGPL).

import VisionEgg, string
__version__ = VisionEgg.release_name
__cvs__ = string.split('$Revision$')[1]
__date__ = string.join(string.split('$Date$')[1:3], ' ')
__author__ = 'Andrew Straw <astraw@users.sourceforge.net>'

import sys, os, math
import VisionEgg.Core
import VisionEgg.Textures
import VisionEgg.SphereMap
import VisionEgg.PyroHelpers
import Pyro.core

from VisionEgg.PyroApps.ScreenPositionServer import ScreenPositionMetaController
from VisionEgg.PyroApps.ScreenPositionGUI import ScreenPositionParameters
from VisionEgg.PyroApps.GridGUI import GridMetaParameters

class GridMetaController( Pyro.core.ObjBase ):
    def __init__(self,screen,presentation,stimuli):

        # get the instance of Stimulus that was created
        assert( stimuli[0][0] == '3d_perspective' )
        grid = stimuli[0][1]
        
        Pyro.core.ObjBase.__init__(self)
        self.meta_params = GridMetaParameters()
        if not isinstance(screen,VisionEgg.Core.Screen):
            raise ValueError("Expecting instance of VisionEgg.Core.Screen")
        if not isinstance(presentation,VisionEgg.Core.Presentation):
            raise ValueError("Expecting instance of VisionEgg.Core.Presentation")
        if not isinstance(grid,VisionEgg.SphereMap.SphereMap):
            raise ValueError("Expecting instance of VisionEgg.SphereMap.SphereMap")
        self.p = presentation
        self.stim = grid

        screen.parameters.bgcolor = (0.5, 0.5, 0.5, 0.0)

    def get_parameters(self):
        return self.meta_params

    def set_parameters(self, new_parameters):
        if isinstance(new_parameters, GridMetaParameters):
            self.meta_params = new_parameters
        else:
            raise ValueError("Argument to set_parameters must be instance of GridMetaParameters")
        self.update()
        
    def update(self):
        self.p.parameters.go_duration = ( 0.0, 'seconds')

    def go(self):
        self.p.parameters.enter_go_loop = 1

    def quit_server(self):
        self.p.parameters.quit = 1

def get_meta_controller_class():
    return GridMetaController

def make_stimuli():
    filename = os.path.join(VisionEgg.config.VISIONEGG_SYSTEM_DIR,"data/mercator.png")
    texture = VisionEgg.Textures.Texture(filename)
    stimulus = VisionEgg.SphereMap.SphereMap(texture=texture,
                                             stacks=100,
                                             slices=100,
                                             shrink_texture_ok=1)
    return [('3d_perspective',stimulus)] # return ordered list of tuples

def get_meta_controller_stimkey():
    return "grid_server"

# Don't do anything unless this script is being run
if __name__ == '__main__':
    
    pyro_server = VisionEgg.PyroHelpers.PyroServer()

    screen = VisionEgg.Core.Screen.create_default()

    # get Vision Egg stimulus ready to go
    stimuli = make_stimuli()
    stimulus = stimuli[0][1]
    temp = ScreenPositionParameters()

    projection = VisionEgg.Core.PerspectiveProjection(temp.left,
                                                      temp.right,
                                                      temp.bottom,
                                                      temp.top,
                                                      temp.near,
                                                      temp.far)
    viewport = VisionEgg.Core.Viewport(screen=screen,stimuli=[stimulus],projection=projection)
    p = VisionEgg.Core.Presentation(viewports=[viewport])

    # now hand over control of projection to ScreenPositionMetaController
    projection_controller = ScreenPositionMetaController(p,projection)
    pyro_server.connect(projection_controller,"projection_controller")

    # now hand over control of drum to GridMetaController
    meta_controller = GridMetaController(screen,p,stimuli)
    pyro_server.connect(meta_controller,get_meta_controller_stimkey())

    # get listener controller and register it
    p.add_controller(None,None, pyro_server.create_listener_controller())

    # enter endless loop
    p.run_forever()
