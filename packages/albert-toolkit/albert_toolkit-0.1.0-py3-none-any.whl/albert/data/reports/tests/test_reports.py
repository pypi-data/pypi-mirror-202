import os

import pandas as pd
import pytest
from albert.session import AlbertSession


@pytest.mark.usefixtures("ci_tokenset")
def test_report_gather_different_batch_size():
    """
    Test function to verify that the `ReportGather` transformer retrieves the same number of records regardless of batch size.

    The function creates an `AlbertSession` object and uses it to retrieve a report object. It then calls the `get()` method
    of the report object with two sets of report parameters, one with the default batch size and one with a custom batch size.
    The function asserts that the number of records retrieved in both cases is the same.

    Returns:
        None
    """

    session = AlbertSession(AlbertSession.default_dev_host)
    report = session.get_report_obj("RET27")
    report_parameters = {"dataColumnId": "DAC768", "dataTemplateId": "DAT44"}

    # Get the data with the default batch size.
    res = report.get(**report_parameters)

    # Get the data with a custom batch size.
    res2 = report.get(batch_size=60000, **report_parameters)

    # Get the data with a custom batch size.
    res3 = report.get(batch_size=1000, **report_parameters)

    # Assert that the number of records retrieved in both cases is the same.
    assert len(res) == len(res2)
    assert len(res) == len(res3)
