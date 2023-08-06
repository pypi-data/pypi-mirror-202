import pytest
from albert.filters import ReportFilter
from albert.data.reports import ReportBase


def report_list() -> list[ReportBase]:
    report1 = ReportBase(
        reportTypeId="RET00",
        reportType="Ds A parameter report",
        category="datascience",
        description="A report that contains data about parameters",
    )

    report2 = ReportBase(
        **{
            "reportTypeId": "RET1",
            "reportType": "Property Task Data by Trial",
            "category": "reports",
            "description": "Analyze all task data broken down to the individual trials.",
        }
    )

    report3 = ReportBase(
        **{
            "reportTypeId": "RET10",
            "reportType": "Inventory Movements",
            "category": "reports",
            "description": "See how inventory is being moved and consumed.",
        }
    )

    report4 = ReportBase(
        **{
            "reportTypeId": "RET12",
            "reportType": "Inventory Equipment Calibration",
            "category": "reports",
            "description": "View all equipment inventory to support in calibration planning",
        }
    )

    return [report1, report2, report3, report4]


def test_report_filter_basic():
    """
    Does a series of basic tests on a Report
    """

    report1 = ReportBase(
        reportTypeId="RET00",
        reportType="Ds A parameter report",
        category="datascience",
        description="A report that contains data about parameters",
    )
    assert ReportFilter(name="parameter").filter(report1) is True
    assert ReportFilter(name="property").filter(report1) is False

    assert ReportFilter(id="00").filter(report1) is True
    assert ReportFilter(id="01").filter(report1) is False

    assert ReportFilter(desc="contains data").filter(report1) is True
    assert ReportFilter(desc="parameter").filter(report1) is True

    # TODO: This test should maybe be true in the future??
    # though this would require a more sophisticated search feature
    assert ReportFilter(desc="contains parameters").filter(report1) is False

    assert ReportFilter(any="Ds").filter(report1) is True
    assert ReportFilter(any="parameters").filter(report1) is True
    assert ReportFilter(any="datascience").filter(report1) is True

    assert ReportFilter(any="analytics").filter(report1) is False


def test_report_filter_list():
    """
    Does some basic filtering on a list of reports
    """
    rlist = report_list()

    assert ReportFilter(id="10").filter(rlist) == [False, False, True, False]
    assert ReportFilter(name="inventory").filter(rlist) == [False, False, True, True]
    assert ReportFilter(any="calibration").filter(rlist) == [False, False, False, True]
