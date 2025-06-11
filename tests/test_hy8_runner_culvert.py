"""Performs testing for hy8 runner class."""
# 1. Standard python modules

# 2. Third party modules

# 3. Aquaveo modules

# 4. Local modules
from hy8runner.hy8_runner_culvert import Hy8RunnerCulvertBarrel

__copyright__ = "(C) Copyright Aquaveo 2024"
__license__ = "All rights reserved"

# This is not a FHWA product nor is it endorsed by FHWA.
# FHWA will not be providing any technical supporting, funding or maintenance.


class TestHy8RunnerCulvert:
    """A class that will create an HY-8 file and run HY-8."""
    def test_init(self):
        """Initializes the HY-8 Runner class."""
        hy8_runner_culvert = Hy8RunnerCulvertBarrel(0)
        assert hy8_runner_culvert.name == 'Culvert 1'
        assert hy8_runner_culvert.shape == 'circle'
        assert hy8_runner_culvert.material == 'concrete'
        assert hy8_runner_culvert.span == 0.0
        assert hy8_runner_culvert.rise == 0.0
        assert hy8_runner_culvert.inlet_invert_elevation == 0.0
        assert hy8_runner_culvert.inlet_invert_station == 0.0
        assert hy8_runner_culvert.outlet_invert_elevation == 0.0
        assert hy8_runner_culvert.outlet_invert_station == 0.0
        assert hy8_runner_culvert.number_of_barrels == 1

    def test_write_culvert_to_file(self):
        """Write the culvert data to the file."""
        hy8_runner_culvert = Hy8RunnerCulvertBarrel(0)
        hy8_runner_culvert.shape = 'box'
        hy8_runner_culvert.material = 'concrete'
        hy8_runner_culvert.span = 10.0
        hy8_runner_culvert.rise = 5.0
        hy8_runner_culvert.inlet_invert_elevation = 100.0
        hy8_runner_culvert.inlet_invert_station = 0.0
        hy8_runner_culvert.outlet_invert_elevation = 98.0
        hy8_runner_culvert.outlet_invert_station = 100.0
        hy8_runner_culvert.number_of_barrels = 1

        with open('tests/files/test_hy8_runner_culvert.txt', 'w') as f:
            hy8_runner_culvert.write_culvert_to_file(f)

        with open('tests/files/test_hy8_runner_culvert.txt', 'r') as f:
            lines = f.readlines()
            assert lines[0] == 'STARTCULVERT    "Culvert 1"\n'
            assert lines[1] == 'CULVERTSHAPE    2\n'
            assert lines[2] == 'CULVERTMATERIAL 1\n'
            assert lines[3] == 'BARRELDATA  10.0 5.0 0.012 0.012\n'
            assert lines[4] == 'EMBANKMENTTYPE 2\n'
            assert lines[5] == 'NUMBEROFBARRELS 1\n'
            assert lines[6] == 'INVERTDATA 0.0 100.0 100.0 98.0\n'
            assert lines[7] == 'ROADCULVSTATION 0.0\n'
            assert lines[8] == 'BARRELSPACING 15.0\n'
            assert lines[9] == 'STARTCULVNOTES ""\n'
            assert lines[10] == 'ENDCULVNOTES\n'
            assert lines[11] == 'ENDCULVERT\n'
