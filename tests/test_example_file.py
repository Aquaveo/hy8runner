"""Provides an example for how to use the HY8Runner Class."""
# 1. Standard python modules
import os

# 2. Third party modules

# 3. Aquaveo modules

# 4. Local modules
from hy8runner.hy8_runner import Hy8Runner

__copyright__ = "(C) Copyright Aquaveo 2024"
__license__ = "All rights reserved"

# This is not a FHWA product nor is it endorsed by FHWA.
# FHWA will not be providing any technical supporting, funding or maintenance.


class TestHy8Runner:
    """A class that will provide an example of how to create an HY-8 file and run HY-8."""

    # Here I am setting the directories for my HY-8 executable and where to find the HY-8 files.
    test_dir = os.path.dirname(__file__)
    hy8_exe_dir = os.path.join(test_dir, 'HY8')
    hy8_dir = os.path.join(test_dir, 'files', 'hy8_test_files')

    def set_crossing_data(self, hy8_runner):
        """Create the crossing data for the test."""
        # Set min, max, and increment flow values
        hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
        # Set the tailwater channel invert elevation and the tailwater elevation
        hy8_runner.set_tw_constant(98, 100)
        # or set the tailwater rating curve
        tw_i = 98.0
        # The rating curve is a list of lists where each list is a flow, tailwater elevation, and tw velocity
        rating_curve = [[0, tw_i, 0], [100, tw_i + 2, 3], [200, tw_i + 4, 5], [300, tw_i + 6, 7], [400, tw_i + 8, 9]]
        hy8_runner.set_tw_rating_curve(tw_i, rating_curve)

        # Set the roadway width
        hy8_runner.set_roadway_width(25)
        # Set the irregular roadway data (alternatively you can set a constant roadway elevation)
        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        # Set the culvert barrel shape: 'circle' or 'box'
        hy8_runner.set_culvert_barrel_shape('circle')
        # Set the culvert barrel material: 'concrete', 'corrugated steel'
        hy8_runner.set_culvert_barrel_material('concrete')
        # Set the culvert barrel span and rise (only span is required for circle)
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        # Set the culvert barrel site data
        hy8_runner.set_culvert_barrel_site_data(0, 100, 40, 98)

        # You can set crossing and culvert name and notes. project title, designer name, and a few other things.

    def test_run_build_full_report(self):
        """Validate the data for all culvert crossings."""
        # Setup the hy8 filename
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'build_full_report.hy8')
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)

        # Uses my function to setup the culvert crossing
        self.set_crossing_data(hy8_runner)

        # Create the hy8 file; if it fails, it will return False and a list of error messages
        result, messages = hy8_runner.create_hy8_file()
        if result:
            # Call HY-8 to generate the full report
            hy8_runner.run_build_full_report()
        # docx report file is created at the location of the hy8 file, same file name with .docx extension


    def test_run_open_save(self):
        """Validate the data for all culvert crossings."""
        # Setup the hy8 filename
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'open_run_save.hy8')
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)

        # Uses my function to setup the culvert crossing
        self.set_crossing_data(hy8_runner)

        # Create the hy8 file; if it fails, it will return False and a list of error messages
        result, messages = hy8_runner.create_hy8_file()
        if result:
            # Call HY-8 to generate the result file (rst), the result sql file (rsql), and the plot file (plt)
            hy8_runner.run_open_save()


    def test_run_open_save_plots(self):
        """Validate the data for all culvert crossings."""
        # Setup the hy8 filename
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'open_run_save_plots.hy8')
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)

        # Uses my function to setup the culvert crossing
        self.set_crossing_data(hy8_runner)

        # Create the hy8 file; if it fails, it will return False and a list of error messages
        result, messages = hy8_runner.create_hy8_file()
        if result:
            # Call HY-8 to generate the result file (rst), the result sql file (rsql), the plot file (plt), and bmp
            # files for each flow
            hy8_runner.run_open_save_plots()


    def test_run_build_flow_tw_table(self):
        """Validate the data for all culvert crossings."""
        # Setup the hy8 filename
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'build_flow_tw_table.hy8')
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)

        # Uses my function to setup the culvert crossing
        self.set_crossing_data(hy8_runner)

        # Create the hy8 file; if it fails, it will return False and a list of error messages
        result, messages = hy8_runner.create_hy8_file()
        if result:
            # Call HY-8 to generate the flow-tailwater table
            hy8_runner.run_build_flow_tw_table()


    # def test_run_build_hw_tw_table(self):
    #     """Validate the data for all culvert crossings."""
    #     # Setup the hy8 filename
    #     hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'build_hw_tw_table.hy8')
    #     hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)

    #     # Uses my function to setup the culvert crossing
    #     self.set_crossing_data(hy8_runner)
    #     # You will want to assign a UUID to the crossing to know the filename of the table that will be created.
    #     hy8_runner.crossings[0].guid = '38fb71e5-255b-451c-b616-2e219d9f82ad'

    #     # Create the hy8 file; if it fails, it will return False and a list of error messages
    #     result, messages = hy8_runner.create_hy8_file()
    #     if result:
    #         # Call HY-8 to generate the hw-tailwater table
    #         hy8_runner.run_build_hw_tw_table()
