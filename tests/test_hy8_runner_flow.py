"""Performs testing for hy8 runner class."""
# 1. Standard python modules

# 2. Third party modules

# 3. Aquaveo modules

# 4. Local modules
from hy8runner.hy8_runner_flow import Hy8RunnerFlow

__copyright__ = "(C) Copyright Aquaveo 2024"
__license__ = "All rights reserved"

# This is not a FHWA product nor is it endorsed by FHWA.
# FHWA will not be providing any technical supporting, funding or maintenance.


class TestHy8RunnerFlow:
    """A class that will create an HY-8 file and run HY-8."""
    def test_init(self):
        """Initializes the HY-8 Runner class."""
        hy8_runner_flow = Hy8RunnerFlow()
        assert hy8_runner_flow.method == 'min-design-max'
        assert hy8_runner_flow.flow_min == 0.0
        assert hy8_runner_flow.flow_design == 0.0
        assert hy8_runner_flow.flow_max == 0.0
        assert hy8_runner_flow.flow_increment == 0.0
        assert hy8_runner_flow.flow_list == []

    def test_compute_list(self):
        """Compute the list of flows."""
        hy8_runner_flow = Hy8RunnerFlow()
        hy8_runner_flow.method = 'min-design-max'
        hy8_runner_flow.flow_min = 0.0
        hy8_runner_flow.flow_design = 100.0
        hy8_runner_flow.flow_max = 200.0
        hy8_runner_flow.compute_list()
        assert hy8_runner_flow.flow_list == [0.0, 100.0, 200.0]

        hy8_runner_flow.method = 'min-max-increment'
        hy8_runner_flow.flow_min = 0.0
        hy8_runner_flow.flow_max = 200.0
        hy8_runner_flow.flow_increment = 50.0
        hy8_runner_flow.compute_list()
        assert hy8_runner_flow.flow_list == [0.0, 50.0, 100.0, 150.0, 200.0]

        hy8_runner_flow.method = 'min-max-increment'
        hy8_runner_flow.flow_min = 0.0
        hy8_runner_flow.flow_max = 200.0
        hy8_runner_flow.flow_increment = 100.0
        hy8_runner_flow.compute_list()
        assert hy8_runner_flow.flow_list == [0.0, 100.0, 200.0]

        hy8_runner_flow.method = 'min-max-increment'
        hy8_runner_flow.flow_min = 0.0
        hy8_runner_flow.flow_max = 200.0
        hy8_runner_flow.flow_increment = 200.0
        hy8_runner_flow.compute_list()
        assert hy8_runner_flow.flow_list == [0.0, 200.0]

    def test_validate_flows(self):
        """Validate the data."""
        hy8_runner_flow = Hy8RunnerFlow()
        hy8_runner_flow.method = 'min-design-max'
        hy8_runner_flow.flow_min = 150.0
        hy8_runner_flow.flow_design = 100.0
        hy8_runner_flow.flow_max = 200.0
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is False
        assert messages == 'Crossing 1: Minimum flow must be less than or equal to design flow.\n'

        hy8_runner_flow.flow_min = 100.0
        hy8_runner_flow.flow_design = 300.0
        hy8_runner_flow.flow_max = 200.0
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is False
        assert messages == 'Crossing 1: Design flow must be less than or equal to maximum flow.\n'

        hy8_runner_flow.flow_min = -100.0
        hy8_runner_flow.flow_design = 100.0
        hy8_runner_flow.flow_max = 200.0
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is False
        assert messages == 'Crossing 1: Minimum flow must be zero or greater.\n'

        hy8_runner_flow.flow_min = 0.0
        hy8_runner_flow.flow_design = 100.0
        hy8_runner_flow.flow_max = 200.0
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is True
        assert messages == ''

        hy8_runner_flow.method = 'min-max-increment'
        hy8_runner_flow.flow_min = 300.0
        hy8_runner_flow.flow_max = 200.0
        hy8_runner_flow.flow_increment = 50.0
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is False
        assert messages == 'Crossing 1: Minimum flow must be less than maximum flow.\n'

        hy8_runner_flow.method = 'min-max-increment'
        hy8_runner_flow.flow_min = -300.0
        hy8_runner_flow.flow_max = 200.0
        hy8_runner_flow.flow_increment = 50.0
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is False
        assert messages == 'Crossing 1: Minimum flow must be zero or greater.\n'

        hy8_runner_flow.method = 'min-max-increment'
        hy8_runner_flow.flow_min = 0.0
        hy8_runner_flow.flow_max = 200.0
        hy8_runner_flow.flow_increment = 0.0
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is False
        assert messages == 'Crossing 1: Flow increment must be greater than zero.\n'

        hy8_runner_flow.method = 'min-max-increment'
        hy8_runner_flow.flow_min = 0.0
        hy8_runner_flow.flow_max = 200.0
        hy8_runner_flow.flow_increment = 50.0
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is True
        assert messages == ''

        hy8_runner_flow.method = 'user-defined'
        hy8_runner_flow.flow_list = [100]
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is False
        assert messages == 'Crossing 1: User-defined flow list must have at least two values.\n'

        hy8_runner_flow.method = 'user-defined'
        hy8_runner_flow.flow_list = [150, 100, 200]
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is False
        assert messages == 'Crossing 1: Flow list values must increase in value.\n'

        hy8_runner_flow.method = 'user-defined'
        hy8_runner_flow.flow_list = [50, 100, 200]
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is True
        assert messages == ''

        hy8_runner_flow.method = 'not supported'
        result, messages = hy8_runner_flow.validate_crossings_data('Crossing 1: ')
        assert result is False
        assert messages == 'Crossing 1: Flow method must be min-design-max, user-defined, or min-max-increment.\n'
