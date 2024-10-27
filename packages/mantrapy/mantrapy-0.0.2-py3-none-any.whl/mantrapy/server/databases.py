from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///./webhooks.db'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models
Base = declarative_base()


class Webhook(Base):
    __tablename__ = 'webhooks'

    id = Column(String, primary_key=True, index=True)
    url = Column(String, index=True)
    query = Column(String, index=True)


# Create the database tables
Base.metadata.create_all(bind=engine)
