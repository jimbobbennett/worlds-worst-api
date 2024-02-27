from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy_serializer import SerializerMixin
from database import Base


class User(Base, SerializerMixin):
    """
    This class is used to represent a users ID
    A user is broken into 2 records - a user_id record and a user record,
    and this class/table wraps the user's unique id along with their email.

    Each user needs a unique email
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    email = Column(String, unique=True, index=True)


class UserDetails(Base, SerializerMixin):
    """
    The second half of the user record, containing additional user details.

    The salary is a string to allow flexibility with adding currency symbols.
    """

    __tablename__ = "user_details"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, index=True)
    user_name = Column(String)
    department = Column(String)
    salary = Column(String)


class Ticket(Base, SerializerMixin):
    """
    This class is for the tickets stored in the database.
    """

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String)
    body = Column(String)
    status = Column(String)
