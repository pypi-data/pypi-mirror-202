import tempfile

import numpy as np

from homcloud.visualize_3d import ParaViewCubeDrawer, ParaViewLinesDrawer, ParaViewSparseCubeDrawer


class Test_ParaViewCubeDrawer(object):
    def test_coord2index(self):
        drawer = ParaViewCubeDrawer(10, [20, 30, 40], {})
        assert drawer.coord2index([5, 12, 38]) == 38 + 12 * 40 + 5 * 40 * 30

    def test_index2coord(self):
        drawer = ParaViewCubeDrawer(10, [20, 30, 40], {})
        assert drawer.index2coord(38 + 12 * 40 + 5 * 40 * 30) == [5, 12, 38]

    def test_dvs(self):
        assert np.allclose(
            ParaViewCubeDrawer.dvs([0, 1, 1]),
            [
                [0, 0, 0],
                [0, 0, 1],
                [0, 1, 0],
                [0, 1, 1],
            ],
        )

    def test_dls(self):
        assert np.allclose(ParaViewCubeDrawer.dls([0, 1, 1]), [[0, 1, 0], [0, 0, 1]])
        assert np.allclose(ParaViewCubeDrawer.dls([1, 1, 1]), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])


class TestParaViewSparseCubeDrawer(object):
    def test_prepare_points(self):
        drawer = ParaViewSparseCubeDrawer(2, 3, {})
        drawer.points.append([0, 1, 2])
        indices, dvs = drawer.prepare_points([3, 4, 5], [0, 1, 1])
        assert len(drawer.points) == 5
        assert np.all(indices == [[[1, 2], [3, 4]], [[0, 0], [0, 0]]])
        assert np.all(np.array(dvs) == [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1]])


class TestParaViewLinesDrawer(object):
    def test_draw_loop(self):
        drawer = ParaViewLinesDrawer(1, {"value": None})
        drawer.draw_loop([(0, 1), (1, 1), (1, 0), (0, 1)], 0, value="12")
        with tempfile.NamedTemporaryFile("w") as f:
            drawer.write(f)
