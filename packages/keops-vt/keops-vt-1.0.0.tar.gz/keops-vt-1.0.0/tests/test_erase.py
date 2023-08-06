import shutil
import os

from keops.src.mvt_eraser import MVTEraser


def test_mvt_eraser_tiles():
    """

    :return:
    """
    src_mbtiles, tmp_mbtiles = 'tests/fixtures/sample.mbtiles', 'tests/fixtures/sample-temp.mbtiles'
    # Create a temporal copied version of the sample MBTiles files, to avoid deleting
    # real data
    shutil.copyfile(src_mbtiles, tmp_mbtiles) if not os.path.isfile(tmp_mbtiles) else None

    mvt_eraser = MVTEraser(tmp_mbtiles)
    mvt_eraser.erase_tile('8/128/160')
    tile_exists = mvt_eraser._check_tile_exists('8', '128', '160')

    # Remove the temporal MBTiles file
    os.remove(tmp_mbtiles)

    assert tile_exists is False


def test_mvt_eraser_map_images():
    """

    :return:
    """
    src_mbtiles, tmp_mbtiles = 'tests/fixtures/trails.mbtiles', 'tests/fixtures/sample-temp.mbtiles'
    # Create a temporal copied version of the sample MBTiles files, to avoid deleting
    # real data
    shutil.copyfile(src_mbtiles, tmp_mbtiles) if not os.path.isfile(tmp_mbtiles) else None

    mvt_eraser = MVTEraser(tmp_mbtiles)
    mvt_eraser.erase_tile('8/128/160')
    tile_exists = mvt_eraser._check_tile_exists('8', '46', '168')

    # Remove the temporal MBTiles file
    os.remove(tmp_mbtiles)

    assert tile_exists is False


def test_get_tiles_table():
    """

    :return:
    """
    mbtiles = 'tests/fixtures/sample.mbtiles'

    mvt_eraser = MVTEraser(mbtiles)
    result = mvt_eraser._get_tiles_table()
    expected = 'tiles'

    assert expected == result
