import pytest
from werkzeug.exceptions import NotFound

from app.utils import non_production_environment_required
from tests.utils import configuration_with_production_environment_testing_route_policy, configuration_with_staging_environment_testing_route_policy


class TestNonProductionEnvironmentRequired:

    @pytest.mark.usefixtures("configuration_with_production_environment_testing_route_policy")
    def test_if_production_environment_set_then_raise_404(self):
        @non_production_environment_required
        def mock_route_function():
            return "OK", 200

        with pytest.raises(NotFound):
            mock_route_function()

    @pytest.mark.usefixtures("configuration_with_staging_environment_testing_route_policy")
    def test_if_not_production_environment_set_then_do_return_function(self):
        @non_production_environment_required
        def mock_route_function():
            return "OK", 200

        result = mock_route_function()
        assert result == ('OK', 200)
