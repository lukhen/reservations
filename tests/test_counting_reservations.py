import pytest
from project.model import Db, count_all_reservations, count_all_reservations_sql


@pytest.fixture
def session():
    db = Db("sqlite:///:memory:")
    session = db.Session()
    yield session


def test_zero(session):
    assert count_all_reservations(session) == 0


def test_one(session):
    res = Db.Reservation(PokojID=1)
    session.add(res)
    session.commit()

    assert count_all_reservations(session) == 1


def test_many(session):
    count = 100
    for i in range(count):
        res = Db.Reservation(PokojID=i)
        session.add(res)
    session.commit()

    assert count_all_reservations(session) == count


def test_many_sql():
    db = Db("sqlite:///:memory:")
    session = db.Session()

    count = 100
    for i in range(count):
        res = Db.Reservation(PokojID=i)
        session.add(res)
    session.commit()

    with db.engine.connect() as conn:
        assert count_all_reservations_sql(conn) == count
