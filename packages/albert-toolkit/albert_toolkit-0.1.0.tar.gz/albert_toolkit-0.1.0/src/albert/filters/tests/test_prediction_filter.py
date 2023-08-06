import pytest
from albert.filters import PredictionFilter, exact


def test_prediction_filter_basic():
    """
    Tests that the prediction filter returns the expected fields when they are set
    """

    p1 = PredictionFilter(id="1234", taskId="abcd")
    p2 = PredictionFilter(
        id=exact("fghj"), dataColumnId=exact("ffff"), variable="INVA1234"
    )

    assert len(p1.get_filter_params()) == 2
    for name, is_exact, value in p1.get_filter_params():
        assert is_exact is False
        assert name in ["id", "taskId"]
        if name == "id":
            assert value == "1234"
        elif name == "taskId":
            assert value == "abcd"

    assert len(p2.get_filter_params()) == 3
    for name, is_exact, value in p2.get_filter_params():
        if name in ["id", "dataColumnId"]:
            assert is_exact is True
        else:
            assert is_exact is False

        if name == "id":
            assert value == "fghj"
        elif name == "dataColumnId":
            assert value == "ffff"
        elif name == "variable":
            assert value == "INVA1234"
