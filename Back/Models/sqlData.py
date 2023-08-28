from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
Base = declarative_base()


class Users(Base):
    __tablename__ = "signin"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String)
    hash_password = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True, index=True)
    is_admin = sa.Column(sa.Boolean, default=False)
