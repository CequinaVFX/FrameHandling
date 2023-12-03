"""
FrameHandling Tool for Nuke
This tool provides functions to manipulate frame-related operations in Nuke's Viewer, and navigate to timeline's frames.
- set the reference frame where this knob exists in node, either from the current needle point, or for a given frame
- navigate to the reference frame
- mark in-out in your current Viewer if a frame-range pattern is found

Note:
    - Supported knobs for reference frame manipulation:
        reference_frame, referenceFrame, first_frame, ref_frame, fframe, tr_reference_frame.
    - Supported Nodes for frame-range manipulation
        TimeClip, FrameRange, Retime, Read, StickyNote, BackdropNode

menu.py Script:
    - This script sets up menu commands for easy access to the FrameHandling tool in the Nodes menu.
"""

__title__ = 'FrameHandling'
__author__ = 'Luciano Cequinel'
__website__ = 'https://www.cequinavfx.com'
__website_blog__ = 'https://www.cequinavfx.com/post/simplify-frame-operations-with-framehandling-in-nuke'
__version__ = '2.4.1'
__release_date__ = 'January, 10 2025'
__license__ = 'MIT'


import nuke
import re


SUPPORTED_KNOBS = ['reference_frame', 'referenceFrame', 'first_frame', 'ref_frame', 'fframe', 'tr_reference_frame']
FRAMERANGE_NODES = ['TimeClip', 'FrameRange', 'Retime', 'Read', 'StickyNote', 'BackdropNode']

def change_reference_frame(from_user=False):
    """
        Set the reference frame for selected nodes.
        Parameters:
            - from_user (bool): If True, prompts the user to input a frame. Defaults to False.
    """

    nodes = get_selection(True)
    if nodes:
        frame_value = get_frame(from_user=from_user)
        if frame_value:
            for node in nodes:
                for reference_knob in node.knobs():
                    if reference_knob in SUPPORTED_KNOBS:
                        node[reference_knob].setValue(frame_value)

    else:
        create_sticky_reference(from_user=from_user)


def clear_viewer_range():
    viewer_node = nuke.activeViewer().node()
    viewer_node.knob("frame_range_lock").setValue(False)


def set_viewer_range(node, viewer_node):
    """
        Set the in and out to the current viewer
    """
    frame_range = '{}-{}'.format(int(nuke.Root()['first_frame'].value()),
                                 int(nuke.Root()['last_frame'].value()))
    clear_range = False

    if node.Class() == 'FrameRange':
        frame_range = '{}-{}'.format(int(node['first_frame'].value()),
                                     int(node['last_frame'].value()))

    elif node.Class() in ('TimeClip', 'Read'):
        frame_range = '{}-{}'.format(int(node['first'].value()),
                                     int(node['last'].value()))

    elif node.Class() == 'Retime':
        frame_range = '{}-{}'.format(int(node['output.first'].value()),
                                     int(node['output.last'].value()))

    elif node.Class() in ('StickyNote', 'BackdropNode'):
        # search for the first group frame-range format (0000-0000 [at least 3 numbers for each value])
        # and use it as frame
        # search for the first group handle format (+0 / +00 [with or without space])
        node_label = node['label'].value()

        find_range = re.findall(r"(\d{3,6}\s?-\s?\d{3,6})", node_label)
        find_handle = re.findall(r"(\+\s?\d{3,})", node_label)
        find_frame = re.findall(r"(\d{3,})", node_label)

        if find_range:
            frame_range = find_range[0]
            if find_handle:
                handle_value = int(find_handle[0].replace('+', ''))
                in_value = int(frame_range.split('-')[0]) - handle_value
                out_value = int(frame_range.split('-')[1]) + handle_value

                frame_range = '{}-{}'.format(in_value, out_value)

            nuke.frame(int(frame_range.split('-')[0]))

        elif find_frame:
            nuke.frame(int(find_frame[0]))
            clear_range = True

        else :
            nuke.warning(" >>> This StickyNote does not provide any useful range!")

    if clear_range:
        clear_viewer_range()
    else:
        viewer_node['frame_range_lock'].setValue(True)
        viewer_node['frame_range'].setValue(frame_range)
        nuke.frame(int(frame_range.split('-')[0]))


def check_frame_range(viewer_node=None):
    if not viewer_node:
        viewer_node = nuke.activeViewer().node()
    viewer_range = viewer_node['frame_range'].value()

    root_range = '{}-{}'.format(int(nuke.Root()['first_frame'].value()),
                                int(nuke.Root()['last_frame'].value()))

    if root_range == viewer_range:
        return False

    return viewer_range


def go_to_reference_frame():
    """
        Navigate to the reference frame of a selected node.
    """
    node = get_selection(False)

    if node:
        viewer_node = nuke.activeViewer().node()

        if node.Class() in FRAMERANGE_NODES:
            set_viewer_range(node=node, viewer_node=viewer_node)

        else:
            if node.Class() in ('StickyNote', 'BackdropNode'):
                # search for the first group of numbers and use it as frame (at least 3 numbers)
                find_frame = re.findall("(\d{3,})", node['label'].value())
                if find_frame:
                    set_frame = int(find_frame[0])
                    nuke.frame(set_frame)
                else:
                    nuke.warning('\t >>> This StickyNote does not provide any reference frame!')

            else:
                clear_viewer_range()
                for knob in node.knobs():
                    if knob in SUPPORTED_KNOBS:
                        set_frame = node[knob].value()
                        nuke.frame(set_frame)


def create_sticky_reference(from_user=False):
    """
        When nothing is selected, it creates a StickyNote with the current frame as the label
    """
    frame_value = get_frame(from_user=from_user)
    sticky_reference = nuke.createNode('StickyNote', inpanel=False)
    sticky_reference['label'].setValue('{}'.format(frame_value))
    sticky_reference['note_font'].setValue('Verdana Bold')
    sticky_reference['note_font_size'].setValue(50)

    viewer_range = check_frame_range()
    if viewer_range:
        sticky_reference = nuke.createNode('StickyNote', inpanel=False)
        sticky_reference['label'].setValue('{}'.format(viewer_range))
        sticky_reference['note_font'].setValue('Verdana Bold')
        sticky_reference['note_font_size'].setValue(50)


def get_frame(from_user):
    """
        Get the frame value either from user input or the current frame.
        Parameters:
            - from_user (bool): If True, prompts the user to input a frame. Defaults to False.
    """

    if from_user:
        user_frame = nuke.getInput('> Set frame to ', '{}'.format(str(nuke.frame())))
        if user_frame:
            try:
                frame_value = int(user_frame)
                return frame_value
            except ValueError as error:
                nuke.message('You must write an integer value! (e.g., 1055)\n{}'.format(error))
                get_frame(from_user=True)

    else:
        return nuke.frame()


def get_selection(multiple_nodes=True):
    """
        Get the selected nodes in the Nuke script.
        Parameters:
            - multiple_nodes (bool): If True, returns a list of selected nodes;
                                     returns a single selected node otherwise.
    """

    try:
        nuke.activeViewer().node()
    except AttributeError as error:
        nuke.message('No active viewer\n{}'.format(error))
        return

    nodes = nuke.selectedNodes()

    if multiple_nodes:
        return nodes

    else:
        if len(nodes) == 1:
            return nuke.selectedNode()

        else :
            if len(nodes) > 1:
                nuke.warning('Select only one node')
            else:
                nuke.warning('Select something!')

            return None


if __name__ == '__main__':
    go_to_reference_frame()
    nuke.message('FrameHandling v{} loaded!'.format(__version__))
