import nuke
import setReferenceFrame

#Add to Nodes menu
toolbar = nuke.menu('Nodes')
cqnTools = toolbar.addMenu('CQNTools', icon='Modify.png')
cqnTools.addCommand('Set to this frame', 'setReferenceFrame.getCurrentFrame()')
cqnTools.addCommand('Set to specific frame', 'setReferenceFrame.getFrameUI()')
