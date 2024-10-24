import mpl_visual_context.patheffects as pe
from mpl_visual_context.image_box import ImageBox

def set_patch_background(patch, arr):
    patch.set_path_effects(
        [pe.FillImage(
            ImageBox(arr,
                     axes=patch.axes if patch.axes else patch.figure,
                     coords="figure fraction"))
         ]
    )
