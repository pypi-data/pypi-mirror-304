import sys

from . import vtk_utils
import pyvista as pv


def show_model(file_path: str, color: str = None, show_edges: bool = False):
    if 'ipykernel' in sys.modules:
        # 在 Jupyter 环境中
        pv.global_theme.trame.jupyter_extension_enabled = True
        pv.set_jupyter_backend("client")
    vtk_utils.show_model(file_path, color, show_edges)
