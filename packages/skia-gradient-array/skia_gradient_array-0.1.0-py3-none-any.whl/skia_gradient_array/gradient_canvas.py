from typing import List, Tuple
from collections.abc import Iterable
import numpy as np
import skia

from .gradient_param import Point, RGB


class Stops:
    def __init__(self, offset_color_alpha_list: Iterable[Tuple[float, RGB, float]]):
        self._offset_color_alpha_list = list(offset_color_alpha_list)

    @classmethod
    def from_offsets_colors(cls, offsets: List[float] | np.ndarray[float],
                            colors: List[RGB | Tuple],
                            alphas: None | List[float]=None):
        assert len(offsets) == len(colors)
        if alphas is not None:
            assert len(offsets) == len(alphas)
        else:
            alphas = [1.] * len(offsets)

        return cls(zip(offsets, colors, alphas))

    def get_skia_offsets_colors(self) -> Tuple[List[float], List[skia.Color4f]]:
        offsets = []
        colors = []
        for o, c, a in self._offset_color_alpha_list:
            stop_color = skia.Color4f(*(c + (a,)))

            offsets.append(o)
            colors.append(stop_color)

        return offsets, colors


class GradientCanvas:
    def __init__(self, width: int, height: int):
        self.arr = np.zeros(shape=(height, width, 4), dtype="uint8")
        self.surface = skia.Surface(self.arr,
                                    colorType=skia.kRGBA_8888_ColorType,
                                    alphaType=skia.kUnpremul_AlphaType
                                    )
        self.canvas = self.surface.getCanvas()
        self.canvas.save()

    def clear(self):
        self.canvas.clear(0)

    def makeLinear(self, xy1: Point, xy2: Point, stops: Stops,
                   affine: None | np.ndarray[np.float32] = None):
        """
        affine: [a, b, c, d, e, f] - c & f for translation.
        """
        offsets, colors = stops.get_skia_offsets_colors()
        matrix = skia.Matrix()
        if affine is not None:
            matrix.setAffine(affine)

        shader = skia.GradientShader.MakeLinear(
            points=[xy1, xy2],
            colors=colors,
            positions=offsets,
            # mode=_extendModeMap[extendMode],
            localMatrix=matrix,
        )

        paint = skia.Paint(
            Shader=shader
        )

        # canvas.drawRect(rect, paint)
        self.canvas.drawPaint(paint)
        self.canvas.restore()

        return self

    def makeRadial(self,
                   startCenter: Point | Tuple, startRadius: float,
                   endCenter: Point | Tuple, endRadius: float,
                   stops: Stops,
                   affine: None | np.ndarray[np.float32] = None):
        offsets, colors = stops.get_skia_offsets_colors()
        matrix = skia.Matrix()
        if affine is not None:
            matrix.setAffine(affine)

        shader = skia.GradientShader.MakeTwoPointConical(
            start=startCenter,
            startRadius=startRadius,
            end=endCenter,
            endRadius=endRadius,
            colors=colors,
            positions=offsets,
            # mode=_extendModeMap[extendMode],
            localMatrix=matrix,
        )

        paint = skia.Paint(
            Shader=shader
        )

        # canvas.drawRect(rect, paint)
        self.canvas.drawPaint(paint)
        self.canvas.restore()

        return self

    def get_array(self):
        return self.arr
