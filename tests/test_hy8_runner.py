"""Performs testing for hy8 runner class."""
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
    """A class that will create an HY-8 file and run HY-8."""

    test_dir = os.path.dirname(__file__)
    hy8_exe_dir = os.path.join(test_dir, 'HY8')
    hy8_dir = os.path.join(test_dir, 'files', 'hy8_test_files')

    def test_init(self):
        """Initializes the HY-8 Runner class."""
        hy8_runner = Hy8Runner()

        assert Hy8Runner.hy8_exe_path == ''
        assert Hy8Runner.hy8_basename_exe == 'HY864.exe'
        assert Hy8Runner.version == 80.0
        assert Hy8Runner.si_units is False
        assert Hy8Runner.exit_loss_option == 0

        assert hy8_runner.project_title == ''
        assert hy8_runner.designer_name == ''
        assert hy8_runner.project_notes == ''

        assert 1 == len(hy8_runner.crossings)

    def test_set_hy8_exe_path(self):
        """Set the path to the HY-8 executable."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_hy8_exe_path('/tests/files/HY8/')
        assert hy8_runner.hy8_exe_path == '/tests/files/HY8/'

    def test_set_hy8_file(self):
        """Set the path to the HY-8 file."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_hy8_file('/tests/files/test')
        assert hy8_runner.hy8_file == '/tests/files/test.hy8'

    def test_add_crossing(self):
        """Add a new culvert crossing to the HY-8 Runner."""
        hy8_runner = Hy8Runner()
        index = hy8_runner.add_crossing()
        assert 2 == len(hy8_runner.crossings)
        assert 1 == index

    def test_delete_crossing(self):
        """Delete a culvert crossing from the HY-8 Runner (and make sure we never have 0)."""
        hy8_runner = Hy8Runner()
        hy8_runner.add_crossing()
        assert 2 == len(hy8_runner.crossings)
        hy8_runner.delete_crossing(1)
        assert 1 == len(hy8_runner.crossings)
        hy8_runner.delete_crossing(1)
        assert 1 == len(hy8_runner.crossings)

    def test_add_culvert_barrel(self):
        """Add a new culvert barrel to the HY-8 Runner."""
        hy8_runner = Hy8Runner()
        hy8_runner.add_culvert_barrel(0)
        assert 2 == len(hy8_runner.crossings[0].culverts)
        hy8_runner.add_culvert_barrel(2)  # Should not add a culvert because of bad index
        assert 2 == len(hy8_runner.crossings[0].culverts)
        hy8_runner.add_culvert_barrel()
        assert 3 == len(hy8_runner.crossings[0].culverts)

    def test_delete_culvert_barrel(self):
        """Delete a culvert barrel to the HY-8 Runner (and ensure that it is never zero)."""
        hy8_runner = Hy8Runner()
        hy8_runner.add_culvert_barrel(0)
        assert 2 == len(hy8_runner.crossings[0].culverts)
        hy8_runner.delete_culvert_barrel(2, 1)  # Should not add a culvert because of bad index
        assert 2 == len(hy8_runner.crossings[0].culverts)
        hy8_runner.delete_culvert_barrel(0, 2)  # Should not add a culvert because of bad index
        assert 2 == len(hy8_runner.crossings[0].culverts)
        hy8_runner.add_culvert_barrel(0)
        hy8_runner.delete_culvert_barrel()
        assert 2 == len(hy8_runner.crossings[0].culverts)
        hy8_runner.delete_culvert_barrel(0, 1)
        assert 1 == len(hy8_runner.crossings[0].culverts)
        hy8_runner.delete_culvert_barrel(0, 0)
        assert 1 == len(hy8_runner.crossings[0].culverts)

    def test_set_crossing_name(self):
        """Set the project title for the HY-8 file."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_culvert_crossing_name('My Crossing')
        assert hy8_runner.crossings[0].name == 'My Crossing'

    def test_set_min_design_max_flow(self):
        """Set the minimum, design, and max flow for a culvert crossing."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_discharge_min_design_max_flow(0.0, 100.0, 200.0)
        assert hy8_runner.crossings[0].flow.method == 'min-design-max'
        assert hy8_runner.crossings[0].flow.flow_min == 0.0
        assert hy8_runner.crossings[0].flow.flow_design == 100.0
        assert hy8_runner.crossings[0].flow.flow_max == 200.0

    def test_set_user_list_flow(self):
        """Set the list of user-defined flows for a culvert crossing."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_discharge_user_list_flow([0.0, 100.0, 200.0])
        assert hy8_runner.crossings[0].flow.method == 'user-defined'
        assert hy8_runner.crossings[0].flow.flow_list == [0.0, 100.0, 200.0]

    def test_set_min_max_inc_flow(self):
        """Set the list of user-defined flows using a min, max, and incremental flows for a culvert crossing."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_discharge_min_max_inc_flow(0.0, 200.0, 50.0)
        assert hy8_runner.crossings[0].flow.method == 'min-max-increment'
        assert hy8_runner.crossings[0].flow.flow_min == 0.0
        assert hy8_runner.crossings[0].flow.flow_max == 200.0
        assert hy8_runner.crossings[0].flow.flow_increment == 50.0

    def test_set_tw_rectangular(self):
        """Set the tailwater information for a culvert crossing."""
        hy8_runner = Hy8Runner()
        bottom_width = 100.0
        channel_slope = 0.001
        manning_n = 0.04
        channel_invert_elevation = 11.35
        hy8_runner.set_tw_rectangular(bottom_width, channel_slope, manning_n, channel_invert_elevation)
        assert hy8_runner.crossings[0].tw_bottom_width == bottom_width
        assert hy8_runner.crossings[0].tw_channel_slope == channel_slope
        assert hy8_runner.crossings[0].tw_manning_n == manning_n
        assert hy8_runner.crossings[0].tw_invert_elevation == channel_invert_elevation

    def test_set_tw_constant(self):
        """Set the tailwater information for a culvert crossing."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_tw_constant(0, 100.0)
        assert hy8_runner.crossings[0].tw_constant_elevation == 100.0

    def test_set_tw_rating_curve(self):
        """Set the tailwater information for a culvert crossing."""
        hy8_runner = Hy8Runner()

        invert_elevation = 100.0
        rating_curve = [[0, invert_elevation, 0], [100, 102, 3], [200, 104, 5], [300, 106, 7], [400, 108, 9]]
        hy8_runner.set_tw_rating_curve(invert_elevation, rating_curve)

        assert hy8_runner.crossings[0].tw_invert_elevation == invert_elevation
        assert hy8_runner.crossings[0].tw_rating_curve == rating_curve

    def test_set_roadway_width(self):
        """Set the roadway width for a culvert crossing."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_roadway_width(10.0)
        assert hy8_runner.crossings[0].roadway_width == 10.0

    def test_set_roadway_surface(self):
        """Set the roadway surface for a culvert crossing."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_roadway_surface('paved')
        assert hy8_runner.crossings[0].roadway_surface == 'paved'

    def test_set_roadway_stations_and_elevations(self):
        """Set the roadway stations and elevations for a culvert crossing."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_roadway_stations_and_elevations([0.0, 100.0], [100.0, 98.0])
        assert hy8_runner.crossings[0].roadway_stations == [0.0, 100.0]
        assert hy8_runner.crossings[0].roadway_elevations == [100.0, 98.0]

    def test_set_constant_roadway(self):
        """Set the roadway as constant for a culvert crossing."""
        hy8_runner = Hy8Runner()
        roadway_length = 100.0
        elevation = 50.0
        hy8_runner.set_constant_roadway(roadway_length, elevation)
        assert hy8_runner.crossings[0].roadway_shape == 1
        assert hy8_runner.crossings[0].roadway_stations == [0.0, roadway_length]
        assert hy8_runner.crossings[0].roadway_elevations == [elevation, elevation]

    def test_set_culvert_barrel_name(self):
        """Set the name for a culvert barrel."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_culvert_barrel_name('barrel1')
        assert hy8_runner.crossings[0].culverts[0].name == 'barrel1'

    def test_set_culvert_barrel_shape(self):
        """Set the shape for a culvert barrel."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_culvert_barrel_shape('box')
        assert hy8_runner.crossings[0].culverts[0].shape == 'box'

    def test_set_culvert_barrel_material(self):
        """Set the material for a culvert barrel."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_culvert_barrel_material('corrugated steel')
        assert hy8_runner.crossings[0].culverts[0].material == 'corrugated steel'

    def test_set_culvert_barrel_span_and_rise(self):
        """Set the span and rise for a culvert barrel."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_culvert_barrel_span_and_rise(10.0, 2.0)
        assert hy8_runner.crossings[0].culverts[0].span == 10.0

    def test_set_culvert_barrel_site_data(self):
        """Set the site data for a culvert barrel."""
        hy8_runner = Hy8Runner()
        inlet_invert_station = 0.0
        inlet_invert_elevation = 100
        outlet_invert_station = 40
        outlet_invert_elevation = 98
        hy8_runner.set_culvert_barrel_site_data(inlet_invert_station, inlet_invert_elevation, outlet_invert_station,
                                                outlet_invert_elevation)
        assert hy8_runner.crossings[0].culverts[0].inlet_invert_station == inlet_invert_station
        assert hy8_runner.crossings[0].culverts[0].inlet_invert_elevation == inlet_invert_elevation
        assert hy8_runner.crossings[0].culverts[0].outlet_invert_station == outlet_invert_station
        assert hy8_runner.crossings[0].culverts[0].outlet_invert_elevation == outlet_invert_elevation

    def test_set_culvert_barrel_number_of_culverts(self):
        """Set the number of culvert barrels for a culvert crossing."""
        hy8_runner = Hy8Runner()
        hy8_runner.set_culvert_barrel_number_of_barrels(2)
        assert hy8_runner.crossings[0].culverts[0].number_of_barrels == 2

    def test_validate_crossings_data(self):
        """Validate the data for all culvert crossings."""
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_build_full_report.hy8')
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)
        hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
        hy8_runner.set_tw_constant(98, 100)
        hy8_runner.set_roadway_width(25)
        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        hy8_runner.set_culvert_barrel_shape('circle')
        hy8_runner.set_culvert_barrel_material('concrete')
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        hy8_runner.set_culvert_barrel_site_data(0, 100, 100, 98)
        result, messages = hy8_runner.validate_crossings_data()
        assert result is True
        assert messages == ''

        hy8_runner.set_tw_constant(102, 100)
        result, messages = hy8_runner.validate_crossings_data()
        assert result is False
        assert messages == 'Crossing: Crossing 1 with index: 0 Tailwater constant elevation must be greater than '\
            'tailwater invert elevation.\n'

        hy8_runner.crossings[0].name = 'my crossing'
        hy8_runner.set_tw_constant(98, 100)
        hy8_runner.set_roadway_width(-25)
        result, messages = hy8_runner.validate_crossings_data()
        assert result is False
        assert messages == 'Crossing: my crossing with index: 0 Roadway width must be greater than zero.\n'

        hy8_runner.set_roadway_width(25)
        hy8_runner.set_roadway_stations_and_elevations([0], [110, 112])
        result, messages = hy8_runner.validate_crossings_data()
        assert result is False
        assert messages == 'Crossing: my crossing with index: 0 Roadway stations & elevations must have at least two'\
            ' values.\nCrossing: my crossing with index: 0 Roadway stations and elevations must have the same number '\
            'of values.\n'

        hy8_runner.set_roadway_stations_and_elevations([0], [110])
        result, messages = hy8_runner.validate_crossings_data()
        assert result is False
        assert messages == \
            'Crossing: my crossing with index: 0 Roadway stations & elevations must have at least two values.\n'

        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111, 113])
        result, messages = hy8_runner.validate_crossings_data()
        assert result is False
        assert messages == 'Crossing: my crossing with index: 0 Roadway stations and elevations must have the same '\
            'number of values.\n'

        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        hy8_runner.crossings[0].culverts[0].span = 0.0
        result, messages = hy8_runner.validate_crossings_data()
        assert result is False
        assert messages == \
            'Crossing: my crossing with index: 0 Culvert barrel: Culvert 1\tspan of the culvert must be specified.\n'

        hy8_runner.set_culvert_barrel_shape('box')
        hy8_runner.crossings[0].culverts[0].rise = 0.0
        result, messages = hy8_runner.validate_crossings_data()
        assert result is False
        assert messages == 'Crossing: my crossing with index: 0 Culvert barrel: Culvert 1\tspan of the culvert must '\
            'be specified.\nCrossing: my crossing with index: 0 Culvert barrel: Culvert 1\trise of the box culvert'\
            ' must be specified.\n'

        hy8_runner.crossings[0].culverts[0].name = 'my culvert'
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        hy8_runner.set_culvert_barrel_number_of_barrels(0)
        result, messages = hy8_runner.validate_crossings_data()
        assert result is False
        assert messages == 'Crossing: my crossing with index: 0 Culvert barrel: my culvert\t'\
            'Number of barrels must be greater than zero.\n'

        hy8_runner.crossings[0].culverts = []
        result, messages = hy8_runner.validate_crossings_data()
        assert result is False
        assert messages == 'Crossing: my crossing with index: 0 Crossing must have at least one culvert barrel.\n'

    def test_write_hy8_file(self):
        """Write the HY-8 file to disk."""
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_write_hy8_file.hy8')
        if os.path.exists(hy8_file):
            os.remove(hy8_file)
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)
        hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
        hy8_runner.set_tw_constant(98, 100)
        hy8_runner.set_roadway_width(25)
        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        hy8_runner.set_culvert_barrel_shape('circle')
        hy8_runner.set_culvert_barrel_material('concrete')
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        hy8_runner.set_culvert_barrel_site_data(0, 100, 40, 98)

        hy8_runner.create_hy8_file()
        assert os.path.exists(hy8_file)

    def test_write_second_hy8_file(self):
        """Write the HY-8 file to disk."""
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_write_hy8_file.hy8')
        if os.path.exists(hy8_file):
            os.remove(hy8_file)
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)
        hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
        hy8_runner.set_tw_constant(98, 100)
        hy8_runner.set_roadway_width(25)
        hy8_runner.crossings[0].roadway_surface = 'gravel'
        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        hy8_runner.set_culvert_barrel_shape('circle')
        hy8_runner.set_culvert_barrel_material('corrugated steel')
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        hy8_runner.set_culvert_barrel_site_data(0, 100, 40, 98)

        hy8_runner.create_hy8_file()
        assert os.path.exists(hy8_file)

    def test_write_third_hy8_file(self):
        """Write the HY-8 file to disk."""
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_write_hy8_file.hy8')
        if os.path.exists(hy8_file):
            os.remove(hy8_file)
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)
        hy8_runner.si_units = True
        hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
        hy8_runner.set_tw_constant(98, 100)
        hy8_runner.set_roadway_width(25)
        hy8_runner.crossings[0].roadway_surface = 'user-defined'
        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        hy8_runner.set_culvert_barrel_shape('circle')
        hy8_runner.set_culvert_barrel_material('corrugated steel')
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        hy8_runner.set_culvert_barrel_site_data(0, 100, 40, 98)

        hy8_runner.create_hy8_file()
        assert os.path.exists(hy8_file)

    # def test_run_hy8(self):
    #     """Run the HY-8 file and return the results as a string."""
    #     hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_hy8.hy8')
    #     hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)

    #     hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
    #     hy8_runner.set_tw_constant(98, 100)
    #     hy8_runner.set_roadway_width(25)
    #     hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
    #     hy8_runner.set_culvert_barrel_shape('circle')
    #     hy8_runner.set_culvert_barrel_material('concrete')
    #     hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
    #     hy8_runner.set_culvert_barrel_site_data(0, 100, 40, 98)

    #     hy8_runner.create_hy8_file()
    #     hy8_runner._run_hy8_executable('')

    def test_run_hy8_exe_with_no_exe(self):
        """Run the HY-8 executable and return the error message."""
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_hy8_exe_with_no_exe.hy8')
        hy8_runner = Hy8Runner()
        hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
        hy8_runner.set_tw_constant(98, 100)
        hy8_runner.set_roadway_width(25)
        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        hy8_runner.set_culvert_barrel_shape('circle')
        hy8_runner.set_culvert_barrel_material('concrete')
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        hy8_runner.set_culvert_barrel_site_data(0, 100, 40, 98)

        hy8_runner.set_hy8_file(hy8_file)
        hy8_runner.set_hy8_exe_path('tests/files/HY8/')
        hy8_runner.create_hy8_file()
        results, messages = hy8_runner.validate_crossings_data()
        assert results is False
        assert messages == 'HY-8 executable does not exist: tests/files/HY8/HY864.exe\n'

    def test_run_hy8_exe_with_no_file(self):
        """Run the HY-8 executable and return the error message."""
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, '')
        hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
        hy8_runner.set_tw_constant(98, 100)
        hy8_runner.set_roadway_width(25)
        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        hy8_runner.set_culvert_barrel_shape('circle')
        hy8_runner.set_culvert_barrel_material('concrete')
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        hy8_runner.set_culvert_barrel_site_data(0, 100, 40, 98)

        hy8_runner.create_hy8_file()
        results, messages = hy8_runner.validate_crossings_data()
        assert results is False
        assert messages == 'HY-8 file must be specified.\n'

    def test_run_build_full_report(self):
        """Validate the data for all culvert crossings."""
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_build_full_report.hy8')
        report_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_build_full_report.docx')
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)
        hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
        hy8_runner.set_tw_constant(98, 100)
        hy8_runner.set_roadway_width(25)
        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        hy8_runner.set_culvert_barrel_shape('circle')
        hy8_runner.set_culvert_barrel_material('concrete')
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        hy8_runner.set_culvert_barrel_site_data(0, 100, 40, 98)

        if os.path.exists(report_file):
            os.remove(report_file)

        result, messages = hy8_runner.create_hy8_file()
        hy8_runner.run_build_full_report()
        assert os.path.exists(report_file)

    def test_run_open_save(self):
        """Validate the data for all culvert crossings."""
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_open_save.hy8')
        rst_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_open_save.rst')
        rsql_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_open_save.rsql')
        plt_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_open_save.plt')
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)
        hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
        hy8_runner.set_tw_constant(98, 100)
        hy8_runner.set_roadway_width(25)
        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        hy8_runner.set_culvert_barrel_shape('circle')
        hy8_runner.set_culvert_barrel_material('concrete')
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        hy8_runner.set_culvert_barrel_site_data(0, 100, 100, 98)

        if os.path.exists(rst_file):
            os.remove(rst_file)
        if os.path.exists(rsql_file):
            os.remove(rsql_file)
        if os.path.exists(plt_file):
            os.remove(plt_file)

        result, messages = hy8_runner.create_hy8_file()
        hy8_runner.run_open_save()

        assert os.path.exists(rst_file)
        assert os.path.exists(rsql_file)
        assert os.path.exists(plt_file)

    def test_run_open_save_plots(self):
        """Validate the data for all culvert crossings."""
        hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_open_save_plots.hy8')
        bmp0_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_open_save_plots--Culvert0--WaterProfile0.bmp')
        bmp1_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_open_save_plots--Culvert0--WaterProfile1.bmp')
        bmp2_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_open_save_plots--Culvert0--WaterProfile2.bmp')
        bmp3_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_open_save_plots--Culvert0--WaterProfile3.bmp')
        bmp4_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_open_save_plots--Culvert0--WaterProfile4.bmp')
        hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)
        hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
        hy8_runner.set_tw_constant(98, 100)
        hy8_runner.set_roadway_width(25)
        hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
        hy8_runner.set_culvert_barrel_shape('circle')
        hy8_runner.set_culvert_barrel_material('concrete')
        hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
        hy8_runner.set_culvert_barrel_site_data(0, 100, 100, 98)

        if os.path.exists(bmp0_file):
            os.remove(bmp0_file)
        if os.path.exists(bmp1_file):
            os.remove(bmp1_file)
        if os.path.exists(bmp2_file):
            os.remove(bmp2_file)
        if os.path.exists(bmp3_file):
            os.remove(bmp3_file)
        if os.path.exists(bmp4_file):
            os.remove(bmp4_file)

        _, _ = hy8_runner.create_hy8_file()
        hy8_runner.run_open_save_plots()

        assert os.path.exists(bmp0_file)
        assert os.path.exists(bmp1_file)
        assert os.path.exists(bmp2_file)
        assert os.path.exists(bmp3_file)
        assert os.path.exists(bmp4_file)

    # def test_run_build_flow_tw_table(self):
    #     """Validate the data for all culvert crossings."""
    #     hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_build_flow_tw_table.hy8')
    #     table_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_build_flow_tw_table.table')
    #     hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)
    #     hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
    #     hy8_runner.set_tw_constant(98, 100)
    #     hy8_runner.set_roadway_width(25)
    #     hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
    #     hy8_runner.set_culvert_barrel_shape('circle')
    #     hy8_runner.set_culvert_barrel_material('concrete')
    #     hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
    #     hy8_runner.set_culvert_barrel_site_data(0, 100, 100, 98)

    #     if os.path.exists(table_file):
    #         os.remove(table_file)

    #     result, messages = hy8_runner.create_hy8_file()
    #     hy8_runner.run_build_flow_tw_table()

    #     assert os.path.exists(table_file)

    # def test_run_build_hw_tw_table(self):
    #     """Validate the data for all culvert crossings."""
    #     hy8_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_build_hw_tw_table.hy8')
    #     table_file = os.path.join(TestHy8Runner.hy8_dir, 'test_run_build_hw_tw_table.table')
    #     hy8_runner = Hy8Runner(TestHy8Runner.hy8_exe_dir, hy8_file)
    #     hy8_runner.set_discharge_min_max_inc_flow(0, 200, 50)
    #     hy8_runner.set_tw_constant(98, 100)
    #     hy8_runner.set_roadway_width(25)
    #     hy8_runner.set_roadway_stations_and_elevations([0, 100, 200], [110, 112, 111])
    #     hy8_runner.set_culvert_barrel_shape('circle')
    #     hy8_runner.set_culvert_barrel_material('concrete')
    #     hy8_runner.set_culvert_barrel_span_and_rise(5, 4)
    #     hy8_runner.set_culvert_barrel_site_data(0, 100, 100, 98)
    #     hy8_runner.crossings[0].uuid = 'test_run_build_hw_tw_table'

    #     if os.path.exists(table_file):
    #         os.remove(table_file)

    #     result, messages = hy8_runner.create_hy8_file()
    #     hy8_runner.run_build_hw_tw_table()

    #     assert os.path.exists(table_file)
