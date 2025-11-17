from database import Base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__="students"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100))
    age=Column(Integer)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    # relationship to Course
    course = relationship("Course", back_populates="students")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)

    # back-populates students relationship
    students = relationship("Student", back_populates="course", cascade="all, delete-orphan")

# class Student(Base):
#     __tablename__ = "students"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     age = Column(Integer, nullable=False)


class Books(Base):
    __tablename__="books"
    
    id=Column(Integer,primary_key=True,index=True)
    book_name=Column(String(200),nullable=False)
    
    
    
    
    
    
    

class Contact(Base):
    __tablename__="contactform"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=True)
    email=Column(String(100),nullable=True)
    message=Column(String(100),nullable=True)
    