from policyengine_uk import Microsimulation
import pytest

YEARS = range(2024, 2026)
baseline = Microsimulation()


@pytest.mark.parametrize("year", YEARS)
def test_not_nan(year):
    for variable in baseline.tax_benefit_system.variables:
        requires_computation_after = baseline.tax_benefit_system.variables[
            variable
        ].requires_computation_after
        if requires_computation_after:
            continue
        if (
            baseline.tax_benefit_system.variables[variable].definition_period
            == "year"
        ):
            assert ~baseline.calc(variable, period=year).isna().any()
