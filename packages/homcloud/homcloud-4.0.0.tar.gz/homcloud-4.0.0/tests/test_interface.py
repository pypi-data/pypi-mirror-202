import os

import numpy as np
import pytest

import homcloud.interface as hc
import homcloud.paraview_interface as pv
from homcloud.compat import imageio


class TestOptimal1CycleForBitmap(object):
    @pytest.mark.integration
    def test_construction_from_pair(self):
        bitmap = np.array([[0, 0, 0, 4], [0, 4, 2, 1], [3, 5, 6, -1], [0, -1, 0, 0]])
        pd = hc.PDList.from_bitmap_levelset(bitmap, "sublevel").dth_diagram(1)
        pair = pd.nearest_pair_to(3, 6)
        assert pair.degree == 1
        opt1cyc = pair.optimal_1_cycle()
        assert opt1cyc.birth_time() == 3
        assert opt1cyc.death_time() == 6
        assert opt1cyc.birth_position() == (2, 0)
        assert opt1cyc.path() == [
            (2, 0),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (2, 3),
            (1, 3),
            (1, 2),
            (0, 2),
            (0, 1),
            (0, 0),
            (1, 0),
            (2, 0),
        ]
        assert sorted(opt1cyc.boundary_points()) == sorted(
            [(2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 2), (0, 2), (0, 1), (0, 0), (1, 0)]
        )
        assert isinstance(opt1cyc.to_pvnode(), pv.VTK)


class TestOptimal1Cycle(object):
    class TestForAlphaFiltration(object):
        @pytest.fixture
        def optimal_1_cycle(self, tetragon):
            pd1 = hc.PDList.from_alpha_filtration(tetragon, save_boundary_map=True)[1]
            return pd1.nearest_pair_to(8.5, 11.56).optimal_1_cycle()

        def test_birth_time(self, optimal_1_cycle):
            assert optimal_1_cycle.birth_time() == pytest.approx(8.5)

        def test_death_time(self, optimal_1_cycle):
            assert optimal_1_cycle.death_time() == pytest.approx(11.56)

        def test_birth_position(self, optimal_1_cycle):
            assert optimal_1_cycle.birth_position() == [[3.0, 5.0], [6.0, 0.0]]

        def test_path(self, optimal_1_cycle):
            assert sorted(optimal_1_cycle.path()) == sorted(
                [[[0, 0], [3, 5]], [[0, 0], [2, -4]], [[6, 0], [2, -4]], [[3, 5], [6, 0]]]
            )

        def test_path_symbols(self, optimal_1_cycle):
            assert sorted(optimal_1_cycle.path_symbols()) == sorted([["0", "1"], ["0", "3"], ["2", "3"], ["1", "2"]])

        def test_boundary_points_symbols(self, optimal_1_cycle):
            assert sorted(optimal_1_cycle.boundary_points_symbols()) == ["0", "1", "2", "3"]

        def test_boundary_points(self, optimal_1_cycle):
            assert sorted(optimal_1_cycle.boundary_points()) == [
                [0, 0],
                [2, -4],
                [3, 5],
                [6, 0],
            ]

    class TestForCubicalFiltration(object):
        @pytest.fixture
        def optimal_1_cycle(self):
            bitmap = np.array(
                [
                    [9, 8, 7, 12],
                    [5, 13, 1, 2],
                    [-1, 2, 10, 4],
                ]
            )
            pd1 = hc.PDList.from_bitmap_levelset(bitmap, type="cubical", save_boundary_map=True)[1]
            return pd1.nearest_pair_to(10, 13).optimal_1_cycle()

        def test_boundary_points(self, optimal_1_cycle):
            assert sorted(optimal_1_cycle.boundary_points()) == sorted(
                [
                    (0, 0),
                    (0, 1),
                    (0, 2),
                    (1, 0),
                    (1, 2),
                    (2, 0),
                    (2, 1),
                    (2, 2),
                ]
            )


class TestPDMask(object):
    PARAMETERS = (
        "mask_bitmap,expected",
        [
            (np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=bool), []),
            (np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0]], dtype=bool), [(-1, 1), (-1, 1)]),
        ],
    )

    @pytest.mark.parametrize(*PARAMETERS)
    def test_filter_pairs(self, binary3d, mask_bitmap, expected):
        pd = hc.PDList.from_bitmap_levelset(hc.distance_transform(binary3d, True))[1]
        mask = hc.HistoSpec((-2.5, 1.5), 4).mask_from_2darray(mask_bitmap)
        assert [(p.birth, p.death) for p in mask.filter_pairs(pd.pairs())] == expected

    @pytest.mark.parametrize(*PARAMETERS)
    def test_filter_pd(self, binary3d, mask_bitmap, expected):
        pd = hc.PDList.from_bitmap_levelset(hc.distance_transform(binary3d, True))[1]
        mask = hc.HistoSpec((-2.5, 1.5), 4).mask_from_2darray(mask_bitmap)
        assert [(p.birth, p.death) for p in mask.filter_pd(pd)] == expected


class Test_draw_birthdeath_pixels:
    def test_for_image(self, bitmap, tmpdir, picture_dir):
        image_path = str(tmpdir.join("tmp.png"))
        pds = hc.PDList.from_bitmap_levelset(bitmap, mode="sublevel")
        imageio.imsave(image_path, bitmap)
        image = hc.draw_birthdeath_pixels_2d(
            pds[0].pairs(),
            image_path,
            draw_birth=True,
            draw_death=True,
            draw_line=True,
            scale=100,
            marker_size=6,
            with_label=True,
        )
        image.save(str(picture_dir.joinpath("test_interface_birthdeath1.png")))

    def test_for_ndarary(self, bitmap, picture_dir):
        pds = hc.PDList.from_bitmap_levelset(bitmap, mode="sublevel")
        image = hc.draw_birthdeath_pixels_2d(
            pds[0].pairs(),
            bitmap,
            draw_birth=True,
            draw_death=True,
            draw_line=True,
            scale=100,
            marker_size=6,
            with_label=True,
        )
        image.save(str(picture_dir.joinpath("test_interface_birthdeath2.png")))


class TestPH0Components(object):
    @pytest.mark.parametrize(
        "birth, death, epsilon, expected",
        [
            (0.0, 1.25, 0.0, [[1, 2, 0]]),
            (0.0, 2.0, 0.0, [[3, 0, 0]]),
            (0.0, 25.25, 0.0, [[0, 0, 0], [3, 0, 0], [1, 2, 0]]),
        ],
    )
    def test_birth_component(self, pd, birth, death, epsilon, expected):
        pair = pd.nearest_pair_to(birth, death)
        component = pair.ph0_components(epsilon).birth_component
        assert sorted(component.tolist()) == sorted(expected)

    @pytest.mark.parametrize(
        "birth, death, epsilon, expected",
        [
            (0.0, 1.25, 0.0, [[0, 0, 0]]),
            (0.0, 2.0, 0.0, [[0, 0, 0], [1, 2, 0]]),
            (0.0, 25.25, 0.0, [[1, 1, 10]]),
        ],
    )
    def test_elder_component(self, pd, birth, death, epsilon, expected):
        pair = pd.nearest_pair_to(birth, death)
        component = pair.ph0_components(epsilon).elder_component
        assert sorted(component.tolist()) == sorted(expected)

    @pytest.mark.parametrize(
        "birth, death, epsilon, expected",
        [
            (0.0, 1.25, 0.0, ["3"]),
            (0.0, 2.0, 0.0, ["2"]),
            (0.0, 25.25, 0.0, ["1", "2", "3"]),
        ],
    )
    def test_birth_component_symbols(self, pd, birth, death, epsilon, expected):
        pair = pd.nearest_pair_to(birth, death)
        component = pair.ph0_components(epsilon).birth_component_symbols
        assert sorted(component) == sorted(expected)

    @pytest.mark.parametrize(
        "birth, death, epsilon, expected",
        [
            (0.0, 1.25, 0.0, ["1"]),
            (0.0, 2.0, 0.0, ["1", "3"]),
            (0.0, 25.25, 0.0, ["0"]),
        ],
    )
    def test_elder_component_symbols(self, pd, birth, death, epsilon, expected):
        pair = pd.nearest_pair_to(birth, death)
        component = pair.ph0_components(epsilon).elder_component_symbols
        assert sorted(component) == sorted(expected)

    @pytest.fixture
    def pd(self):
        pointcloud = np.array(
            [
                [1, 1, 10, 0.003],
                [0, 0, 0, 0.002],
                [3, 0, 0, 0.001],
                [1, 2, 0, 0.000],
            ],
            dtype=float,
        )
        return hc.PDList.from_alpha_filtration(pointcloud, weight=True, save_boundary_map=True)[0]


def test_draw_volumes_on_2d_image(datadir, picture_dir):
    bitmap = imageio.imread(os.path.join(datadir, "bin.png"), as_gray=True)
    bmtrees = hc.BitmapPHTrees.for_bitmap_levelset(hc.distance_transform(bitmap >= 1, True)).bitmap_phtrees(0)

    node = bmtrees.nearest_pair_node(-2, 4)
    image = hc.draw_volumes_on_2d_image([node], bitmap, (255, 0, 0), 0.5)
    image.save(str(picture_dir.joinpath("test_interface_draw_volumes_on_2d_image.png")))
