import pytest
from adaptivecard.actions import Submit, ShowCard, Execute, OpenUrl
from adaptivecard.exceptions import *


class Test:
    def test_submit(self):
        with pytest.raises(TypeError):
            Submit((1,2,3), None)
        submit_action = Submit({}, None)
        with pytest.raises(ValueError):
            submit_action.style = "dstructve"
        with pytest.raises(TypeError):
            submit_action.data = []
        assert submit_action.to_dict()["associatedInputs"] == "none"
    def test_show_card(self):
        with pytest.raises(TypeError):
            ShowCard([])