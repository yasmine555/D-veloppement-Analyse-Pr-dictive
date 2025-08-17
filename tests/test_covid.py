import pytest
from unittest.mock import patch
from covid_app import get_covid_data

@patch('covid_app.requests.get')
def test_get_covid_data(mock_get):
    mock_response = {
        "timeline": {
            "cases": {"2020-01-01": 10, "2020-01-02": 15},
            "deaths": {"2020-01-01": 1, "2020-01-02": 2}
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    df = get_covid_data("France")
    assert not df.empty
    assert 'date' in df.columns
    assert 'cases' in df.columns
