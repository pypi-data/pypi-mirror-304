import os
import sys

from . import vtk_utils
import pyvista as pv


def show_model(file_path: str, color: str = None, show_edges: bool = False):
    """显示3D模型。

    Args:
        file_path (str): 3D模型文件的路径。
        color (str, optional): 模型的颜色。默认为None。
        show_edges (bool, optional): 是否显示边缘。默认为False。

    Returns:
        None
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension not in ['.stl', '.obj']:
        raise ValueError(f"不支持的文件格式: {file_extension}。目前仅支持 .stl 和 .obj 格式")
    if 'ipykernel' in sys.modules:
        # 在 Jupyter 环境中
        pv.global_theme.trame.jupyter_extension_enabled = True
        pv.set_jupyter_backend("client")
    vtk_utils.show_obj_stl(file_path, color, show_edges)
