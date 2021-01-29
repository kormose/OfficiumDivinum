from pathlib import Path

from .api import api

testpage = Path("./backend/api/test.html")


@api.route("/")
def test_api_page():
    with testpage.open() as f:
        data = testpage.read()
    return data
