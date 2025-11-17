from fastapi import FastAPI,Depends,HTTPException
from typing import Union
from database import Base,SessionLocal
from models import Student,Course
from sqlalchemy.orm import Session,selectinload
import models, schemas

app = FastAPI()


def get_db():
    db=SessionLocal()
    try:

     return db
    
    finally:
       db.close()



@app.post("/student_add")
def create_student(name:str,age:int,db:Session=Depends(get_db)):
   student=Student(name=name,age=age)
   db.add(student)
   db.commit()
   db.refresh(student)
   return student


@app.post("/students/", response_model=schemas.StudentRead)
def create_student(student_in: schemas.StudentCreate, db: Session = Depends(get_db)):
    # ensure course exists
    course = db.get(models.Course, student_in.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    student = models.Student(name=student_in.name, age=student_in.age, course_id=student_in.course_id)
    existing=db.query(models.Student).filter(models.Student.name==student_in.name)
    if existing :
       raise HTTPException(status_code=422,detail="name already exists")
    db.add(student)
    db.commit()
    db.refresh(student)
    # refresh relationship
    db.refresh(student)
    return student

#array datas insert 

@app.post("/students/batch-insert")
def batch_insert_students(data: schemas.StudentBatchCreate, db: Session = Depends(get_db)):

    # Ensure lengths match
    if not (len(data.name) == len(data.age) == len(data.course_id)):
        return {
            "success": False,
            "message": "All lists must have same length",
            "data": None
        }

    inserted_students = []

    for i in range(len(data.name)):
        
        # check course exists
        course = db.get(models.Course, data.course_id[i])
        if not course:
            return {
                "success": False,
                "message": f"Course {data.course_id[i]} not found for student {data.name[i]}",
                "data": None
            }
        
        student = models.Student(
            name=data.name[i],
            age=data.age[i],
            course_id=data.course_id[i]
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        inserted_students.append({
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "course_id": student.course_id
        })

    return {
        "success": True,
        "message": "Students inserted successfully",
        "data": inserted_students
    }


@app.get("/listofStudents",response_model=list[schemas.StudentRead])
def listOfstudents(db:Session=Depends(get_db)):
    Student=db.query(models.Student).options(selectinload(models.Student.course)).all()
    return Student

@app.get("/getstudent/{student_id}")
def getOneStudent(student_id:int,db:Session=Depends(get_db)):
    print("student_id",student_id)
    student=db.query(models.Student).options(selectinload(models.Course)).filter(models.Student.id==student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student



@app.put("/updatestudent/{student_id}")
def updatestudent(student_id:int,studentData:schemas.StudentUpdate,db:Session=Depends(get_db)):
    student=db.get(models.Student,student_id)
    if not student:
        return{
            "success":False,
            "message":"student not found",
            "data":None
        }
    
    student.name=studentData.name
    student.age=studentData.age
    student.course_id=student.course_id

    db.commit()
    db.refresh(student)

    return {
        "success": True,
        "message": "Student updated successfully",
        "data": {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "course_id": student.course_id
        }
    }



@app.post("/courses/", response_model=schemas.CourseRead)
def create_course(course_in: schemas.CourseCreate, db: Session = Depends(get_db)):
    course = models.Course(title=course_in.title)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@app.get("/studentlist")
def listOfStudents(db:Session=Depends(get_db)):
   student=db.query(Student).all()
   return student




@app.get("/")
def read_root():
    return {"hello": "world"}







# test code

@app.post("/createform")
def createForm(contact:schemas.ContactCreate,db:Session=Depends(get_db)):
    newcontact=models.Contact(name=contact.name,email=contact.email,message=contact.message)
    db.add(newcontact)
    db.commit()
    db.refresh(newcontact)
    return newcontact


@app.get("/listofform")
def listofData(db:Session=Depends(get_db)):
    data=db.query(models.Contact).all()
    return data
    






    
    

