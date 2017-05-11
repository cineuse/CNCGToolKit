# -*- coding: utf-8 -*-

import hou
import toolutils


def setfit(oldcam, resx, resy):
    # get parent node
    camups = oldcam.inputAncestors()
    if camups == ():
        camup = oldcam
    else:
        camup = camups = oldcam.inputAncestors()[-1]
    # create node
    null = hou.node('obj').createNode('null', 'ScaleWorld')
    blend = hou.node('obj').createNode('blend', 'Blend_position')
    fetch = hou.node('obj').createNode('fetch', 'Fetch_newcam')
    newcam = hou.node('obj').createNode('cam', 'Render_Camera')
    # move node
    null.move(camup.position() + hou.Vector2(0, 1))
    blend.move(oldcam.position() + hou.Vector2(0, -1))
    fetch.move(oldcam.position() + hou.Vector2(0, -2))
    newcam.move(oldcam.position() + hou.Vector2(0, -3))
    # set input
    camup.setNextInput(null)
    blend.setNextInput(oldcam)
    fetch.setNextInput(blend)
    newcam.setNextInput(fetch)
    # set flag
    oldcam.setDisplayFlag(False)
    null.setDisplayFlag(False)
    blend.setDisplayFlag(False)
    fetch.setDisplayFlag(False)
    # set attr
    blend.parm(blend.path() + "/blendm1").set(63)
    fetch.parm(fetch.path() + "/useinputoffetched").set(1)
    oldcam.parm(oldcam.path() + "/resx").set(resx)
    oldcam.parm(oldcam.path() + "/resy").set(resy)
    oldcampath = oldcam.path()
    relativepath = newcam.relativePathTo(oldcam)
    resx = " ch(\"" + relativepath + "/resx\")"
    resy = " ch(\"" + relativepath + "/resy\")"
    focal = " ch(\"" + relativepath + "/focal\")"
    aperture = " ch(\"" + relativepath + "/aperture\")"
    vm_background = " ch(\"" + relativepath + "/vm_background\")"
    newcam.setParmExpressions(dict(resx=resx, resy=resy,
                                   focal=focal,aperture=aperture,
                                   vm_background=vm_background))
    newcam.parm("vm_bgenable").set(0)
    newcam.parm("vm_bgenable").set(0)
    newcam.parm("vm_bgenable").lock(True)


# check nodetype and get resolution
def main():
    view = toolutils.sceneViewer()
    sel = view.selectObjects('请选择一个相机', allowed_types=('cam',))
    if len(sel) > 0:
        if sel[0].type().name() == 'cam':
            resolution = hou.ui.readInput('set Resolution',
                                          buttons=('Set', 'close'),
                                          title='set Resolution',
                                          initial_contents='1920-1080',
                                          close_choice=1, default_choice=0)
            resx = resolution[1].split('-')[0]
            resy = resolution[1].split('-')[1]
            oldcam = sel[0]
            if resolution[0] == 0:
                setfit(oldcam, resx, resy)
