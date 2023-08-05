import sys
import typing


def entry_add(list_path: str = "", active_index_path: str = ""):
    ''' Add an entry to the list after the current active item :File: startup/bl_ui/generic_ui_list.py\:208 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_ui/generic_ui_list.py#L208> __

    :param list_path: list_path
    :type list_path: str
    :param active_index_path: active_index_path
    :type active_index_path: str
    '''

    pass


def entry_move(list_path: str = "",
               active_index_path: str = "",
               direction: typing.Union[str, int] = 'UP'):
    ''' Move an entry in the list up or down :File: startup/bl_ui/generic_ui_list.py\:234 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_ui/generic_ui_list.py#L234> __

    :param list_path: list_path
    :type list_path: str
    :param active_index_path: active_index_path
    :type active_index_path: str
    :param direction: Direction * UP UP -- UP. * DOWN DOWN -- DOWN.
    :type direction: typing.Union[str, int]
    '''

    pass


def entry_remove(list_path: str = "", active_index_path: str = ""):
    ''' Remove the selected entry from the list :File: startup/bl_ui/generic_ui_list.py\:191 <https://projects.blender.org/blender/blender/src/branch/main/scripts/startup/bl_ui/generic_ui_list.py#L191> __

    :param list_path: list_path
    :type list_path: str
    :param active_index_path: active_index_path
    :type active_index_path: str
    '''

    pass
