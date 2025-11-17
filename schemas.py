from pydantic import BaseModel
from typing import List,Optional


class CourseCreate(BaseModel):
    title: str

class CourseRead(BaseModel):
    id: int
    title: str
    class Config:
        orm_mode = True

class StudentCreate(BaseModel):
    name: str
    age: int
    course_id: int

class StudentBatchCreate(BaseModel):
    name: List[str]
    age: List[int]
    course_id: List[int]

class StudentRead(BaseModel):
    id: int
    name: str
    age: int
    course: CourseRead   # nested course details
    class Config:
        orm_mode = True

class CourseWithStudents(BaseModel):
    id: int
    title: str
    students: List[StudentRead] = []
    class Config:
        orm_mode = True



class StudentUpdate(BaseModel):
    name: str
    age: int
    course_id: int
    
    
    



class ContactCreate(BaseModel):
    
    name :str
    email:str
    message:str
    
    