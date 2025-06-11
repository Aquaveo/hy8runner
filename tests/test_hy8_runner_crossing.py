"""Performs testing for hy8 runner class."""
# 1. Standard python modules

# 2. Third party modules

# 3. Aquaveo modules

# 4. Local modules
from hy8runner.hy8_runner_crossing import Hy8RunnerCulvertCrossing

__copyright__ = "(C) Copyright Aquaveo 2024"
__license__ = "All rights reserved"

# This is not a FHWA product nor is it endorsed by FHWA.
# FHWA will not be providing any technical supporting, funding or maintenance.


class TestHy8RunnerCrossing:
    """A class that will create an HY-8 file and run HY-8."""
    def test_init(self):
        """Initializes the HY-8 Runner class."""
        hy8_runner_crossing = Hy8RunnerCulvertCrossing(0)
        assert hy8_runner_crossing.name == 'Crossing 1'
        assert hy8_runner_crossing.tw_type == 1
        assert hy8_runner_crossing.tw_constant_elevation == 0.0
        assert hy8_runner_crossing.tw_invert_elevation == 0.0
        assert hy8_runner_crossing.roadway_shape == 1
        assert hy8_runner_crossing.roadway_width == 0.0
        assert hy8_runner_crossing.roadway_stations == []
        assert hy8_runner_crossing.roadway_elevations == []
        assert hy8_runner_crossing.roadway_surface == 'paved'
        assert 1 == len(hy8_runner_crossing.culverts)

    def test_write_crossing_to_file(self):
        """Write the crossing data to the file."""
        hy8_runner_crossing = Hy8RunnerCulvertCrossing(0)
        hy8_runner_crossing.notes = 'This is a test note.'
        hy8_runner_crossing.tw_type = 6
        hy8_runner_crossing.culverts[0].shape = 'box'
        hy8_runner_crossing.culverts[0].material = 'corrugated steel'
        hy8_runner_crossing.culverts[0].span = 10.0
        hy8_runner_crossing.culverts[0].rise = 2.0
        hy8_runner_crossing.culverts[0].inlet_invert_elevation = 100.0
        hy8_runner_crossing.culverts[0].inlet_invert_station = 0.0
        hy8_runner_crossing.culverts[0].outlet_invert_elevation = 98.0
        hy8_runner_crossing.culverts[0].outlet_invert_station = 100.0
        hy8_runner_crossing.culverts[0].number_of_barrels = 1

        with open('tests/files/test_hy8_runner_crossing.txt', 'w') as f:
            hy8_runner_crossing.write_crossing_to_file(f)

        with open('tests/files/test_hy8_runner_crossing.txt', 'r') as f:
            lines = f.readlines()
            assert lines[0] == 'STARTCROSSING   "Crossing 1"\n'
            assert lines[1] == 'STARTCROSSNOTES    "This is a test note."\n'
            assert lines[2] == 'DISCHARGERANGE 0.0 0.0 0.0\n'
            assert lines[3] == 'DISCHARGEMETHOD 0\n'
            assert lines[4] == 'DISCHARGEXYUSER 3\n'
            assert lines[5] == 'DISCHARGEXYUSER_Y 0.0\n'
            assert lines[6] == 'DISCHARGEXYUSER_Y 0.0\n'
            assert lines[7] == 'DISCHARGEXYUSER_Y 0.0\n'
            assert lines[8] == 'TAILWATERTYPE 6\n'
            assert lines[9] == 'CHANNELGEOMETRY 0.0 1.0 0.0 0.0 0.0\n'
            assert lines[10] == 'NUMRATINGCURVE 6\n'
            assert lines[11] == 'TWRATINGCURVE 0.0 0.0 0.0 0.0\n'
            assert lines[12] == '              0.0 0.0 0.0 0.0\n'
            assert lines[13] == '              0.0 0.0 0.0 0.0\n'
            assert lines[14] == '              0.0 0.0 0.0 0.0\n'
            assert lines[15] == '              0.0 0.0 0.0 0.0\n'
            assert lines[16] == '              0.0 0.0 0.0 0.0\n'
            assert lines[17] == '              0.0 0.0 0.0 0.0\n'
            assert lines[18] == 'ROADWAYSHAPE 1\n'
            assert lines[19] == 'ROADWIDTH 0.0\n'
            assert lines[20] == 'SURFACE 1\n'
            assert lines[21] == 'NUMSTATIONS 0\n'
            assert lines[22] == 'NUMCULVERTS  1\n'
            assert lines[23] == 'STARTCULVERT    "Culvert 1"\n'
            assert lines[24] == 'CULVERTSHAPE    2\n'
            assert lines[25] == 'CULVERTMATERIAL 1\n'
            assert lines[26] == 'BARRELDATA  10.0 2.0 0.012 0.012\n'
            assert lines[27] == 'EMBANKMENTTYPE 2\n'
            assert lines[28] == 'NUMBEROFBARRELS 1\n'
            assert lines[29] == 'INVERTDATA 0.0 100.0 100.0 98.0\n'
            assert lines[30] == 'ROADCULVSTATION 0.0\n'
            assert lines[31] == 'BARRELSPACING 15.0\n'
            assert lines[32] == 'STARTCULVNOTES ""\n'
            assert lines[33] == 'ENDCULVNOTES\n'
            assert lines[34] == 'ENDCULVERT\n'
            assert lines[35] == 'ENDCROSSING\n'
