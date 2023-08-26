#******************************************************
# content: simple script to quickly update reference frame on a selected list of nodes
# if the option to use current frame, or to write a specific one
#
# version: 2.2.1
# date: July 31 2022
#
# how to: getFrameUI()
# dependencies: nuke
# todos: --//--
#
# license: MIT
# author: Luciano Cequinel [lucianocequinel@gmail.com]
#******************************************************

import nuke

##################
# global variables

SUPPORTED_NODES = ['Tracker4', 'FrameHold', 'Roto', 'RotoPaint', 'Transform', 'CornerPin2D', 'VectorDistort']
SUPPORTED_KNOBS = ['reference_frame', 'referenceFrame', 'first_frame', 'ref_frame']


def changeFrame(newFrame, node):
   
    for knob in node.knobs():
        if knob in SUPPORTED_KNOBS:
            node[knob].setValue(int(newFrame))
            print ('{}.{} got the value: {}'.format (node.name(), (knob), newFrame))


def getCurrentFrame():
    '''
    use the current frame from current viewer
    '''
    newFrame = nuke.frame()
    selNodes = nuke.selectedNodes()

    if len (selNodes) > 0:
        for node in selNodes:
            if node.Class() in SUPPORTED_NODES:
                changeFrame(newFrame, node)

    else:
        nuke.message('Select some valid node\n{}!'.format (SUPPORTED_NODES))
        return


def getFrameUI():
    '''
    get a specific frame from user
    '''

    selNodes = nuke.selectedNodes()

    validNodes = []

    for node in selNodes:
        if node.Class() in SUPPORTED_NODES:
            validNodes.append(node)

    if len (validNodes) > 0:

        newFrame = (nuke.getInput('set frame to', '%s' % str(nuke.frame())))

        if newFrame == None:
            return 

        elif newFrame.isdigit():
            for node in validNodes:
                changeFrame(newFrame, node)
        else:
            nuke.message('You must write an integer value! (e.g 1055)')
            getFrameUI()

    else:
        nuke.message('Select some valid node\n{}!'.format (SUPPORTED_NODES))
        return


#################################
#Add to Nodes menu
toolbar = nuke.menu('Nodes')
cqnTools = toolbar.addMenu('CQNTools', 'Modify.png')
cqnTools.addCommand('Set to this frame', 'setReferenceFrame.getCurrentFrame()')
cqnTools.addCommand('Set to specific frame', 'setReferenceFrame.getFrameUI()')


##########################
# main function
if __name__ == '__main__':
    getFrameUI()
