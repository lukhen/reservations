from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


class Db:
    Base = declarative_base()

    def __init__(self, db_uri):
        # SMELL
        if db_uri == "sqlite:///:memory:":
            self.engine = create_engine(
                db_uri, connect_args={"check_same_thread": False}, poolclass=StaticPool
            )
        else:
            self.engine = create_engine(db_uri)
        Db.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    class Reservation(Base):
        __tablename__ = "Rezerwacje"

        RezerwacjaID = Column(Integer, primary_key=True)
        PokojID = Column(Integer)


def count_all_reservations(session):
    return len(session.query(Db.Reservation).all())


def count_all_reservations_sql(conn):
    res = conn.execute('SELECT COUNT(*) FROM "Rezerwacje"')
    return next(res)[0]
