import project
from project import create_app
import pytest
from unittest.mock import Mock


@pytest.fixture
def client():
    class TestConfig:
        DB_URI = "sqlite:///:memory:"

    app = create_app(TestConfig)

    with app.test_client() as client:
        yield client


def test_getting_response(client):
    irrelevant_number = 5
    irrelevant_text_desc = "all_reservations"
    project.count_all_reservations = Mock(return_value=irrelevant_number)
    project.render_the_number_of_reservations = Mock(
        return_value={irrelevant_text_desc: "{}".format(irrelevant_number)}
    )

    r = client.get("/allrescount")

    print(r.data)
    assert bytes(irrelevant_text_desc, "utf-8") in r.data
    assert bytes(str(irrelevant_number), "utf-8") in r.data
