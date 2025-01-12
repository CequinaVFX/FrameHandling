import nuke
import FrameHandling

# Define the shortcut for the tool
# The shortcut is defined as a string, where the key is separated by a '+'
# The key can be any key on the keyboard, and the modifier keys are 'shift', 'ctrl', 'alt', 'meta'
# The shortcut is not case-sensitive
# e.g 'f', 'shift+f', 'ctrl+shift+f', 'f4'
# e.g macos 'cmd+f', 'cmd+shift+f'
# or use 'none' or None to disable shortcut
SHORTCUT_SET_FRAME = 'alt+shift+f'
SHORTCUT_USER_FRAME = 'alt+shift+g'
SHORTCUT_GO_TO_FRAME = 'shift+g'
SHORTCUT_CLEAR_INOUT = 'alt+c'

###################################################################################################
###################################################################################################
###################################################################################################

ICON_SET_FRAME = 'FrameHandling_set_frame.png'
ICON_USER_FRAME = 'FrameHandling_user_set_frame.png'
ICON_GO_TO_FRAME = 'FrameHandling_go_to_frame.png'
ICON_CLEAR_INOUT = 'FrameHandling_clear_inout.png'

# Add to Nodes menu
toolbar = nuke.menu('Nodes')
cqnTools = toolbar.addMenu('CQN Tools', icon='CQN_icon.png')

cqnTools.addCommand('Set to current frame',
                    'FrameHandling.change_reference_frame()',
                    SHORTCUT_SET_FRAME,
                    icon=ICON_SET_FRAME)

cqnTools.addCommand('Set to specific a frame',
                    'FrameHandling.change_reference_frame(True)',
                    SHORTCUT_USER_FRAME,
                    icon=ICON_USER_FRAME)

cqnTools.addCommand('Go to Frame | Set in-out',
                    'FrameHandling.go_to_reference_frame()',
                    SHORTCUT_GO_TO_FRAME,
                    icon=ICON_GO_TO_FRAME)

cqnTools.addCommand('Clear in-out',
                    'FrameHandling.clear_viewer_range()',
                    SHORTCUT_CLEAR_INOUT,
                    icon=ICON_CLEAR_INOUT)
