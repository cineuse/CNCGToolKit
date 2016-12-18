# -*- coding: utf-8 -*-
import hou
import toolutils

def setfit(oldCam, resx, resy):
        oldCam.setDisplayFlag(False)

        oldCam.parm(oldCam.path() + "/resx").set(resx)
        oldCam.parm(oldCam.path() + "/resy").set(resy)

        camups = oldCam.inputAncestors()
        if camups == ():
                camup = oldCam
        else:
                camup = camups = oldCam.inputAncestors()[-1]

        null = hou.node('obj').createNode('null', 'ScaleWorld')
        blend = hou.node('obj').createNode('blend', 'Blend_position')
        fetch = hou.node('obj').createNode('fetch', 'Fetch_NewCam')
        newCam = hou.node('obj').createNode('cam', 'Render_Camera')

        null.move(camup.position() + hou.Vector2(0, 1))
        blend.move(oldCam.position() + hou.Vector2(0, -1))
        fetch.move(oldCam.position() + hou.Vector2(0, -2))
        newCam.move(oldCam.position() + hou.Vector2(0, -3))

        camup.setNextInput(null)
        blend.setNextInput(oldCam)
        fetch.setNextInput(blend)
        newCam.setNextInput(fetch)

        null.setDisplayFlag(False)
        blend.setDisplayFlag(False)
        fetch.setDisplayFlag(False)

        blend.parm(blend.path() + "/blendm1").set(63)
        fetch.parm(fetch.path() + "/useinputoffetched").set(1)

        oldCamPath = oldCam.path()
        relativePath = newCam.relativePathTo(oldCam)
        resx = " ch(\"" + relativePath + "/resx\")"
        resy = " ch(\"" + relativePath + "/resy\")"
        focal = " ch(\"" + relativePath + "/focal\")"
        aperture = " ch(\"" + relativePath + "/aperture\")"
        vm_background = " ch(\"" + relativePath + "/vm_background\")"

        newCam.setParmExpressions(dict(resx=resx, resy=resy, focal=focal,
									   aperture=aperture, vm_background=vm_background))

        newCam.parm("vm_bgenable").set(0)
        newCam.parm("vm_bgenable").set(0)
        newCam.parm("vm_bgenable").lock(True)

def main():
        view = toolutils.sceneViewer()
        sel = view.selectObjects('请选择一个相机')
        if len(sel) > 0:
            if sel[0].type().name()=='cam':
                resolution = hou.ui.readInput('set Resolution',buttons = ('Set','close'),title = 'set Resolution',initial_contents = '1920-1080',close_choice = 1,default_choice = 0)
                resx = resolution[1].split('-')[0]
                resy = resolution[1].split('-')[1]
                oldCam = sel[0]
                if resolution[0] == 0:
                    setfit(oldCam, resx, resy)