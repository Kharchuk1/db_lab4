import uuid
import pickle
import mmodels
from app import db, r, ACTIVE_DB
from sqlalchemy.sql import func
from models import Student, SexType, Location, Test, TestStatus, Subject, Location

# Student services
def serialize_student_all():
    match ACTIVE_DB:
        case "postgres":
            students = db.session.execute(db.select(Student).order_by(Student.birth.asc()).limit(40)).scalars()
            students = list(students)
        case "mongo":
            students = mmodels.Student.objects.order_by("birth")[:40]
    return students

def serialize_student(uuid):
    match ACTIVE_DB:
        case "postgres":
            student = db.one_or_404(db.select(Student).filter(Student.outid == uuid))
        case "mongo":
            student = mmodels.Student.objects.get(outid=uuid)
    return student

def serialize_student_options():
    match ACTIVE_DB:
        case "postgres":
            sextype = list(db.session.execute(db.select(SexType)).scalars())
            location = list(db.session.execute(db.select(Location)).scalars())
        case "mongo":
            sextype = mmodels.SexType.objects
            location = mmodels.Location.objects
    return {
        "sextype": sextype,
        "location": location,
    }

def create_student(form):
    data = dict(form)
    match ACTIVE_DB:
        case "postgres":
            data["outid"] = uuid.uuid4()
            db.session.add(Student(**data))
            db.session.commit()
        case "mongo":
            data = {"location" if k == "location_id" else k:v for k,v in data.items()}
            data = {"sextype" if k == "sextype_id" else k:v for k,v in data.items()}
            person = mmodels.Student(**data)
            person.save()

def update_student(uuid, form):
    data = dict(form)
    data = {k:v for k,v in data.items() if v}
    match ACTIVE_DB:
        case "postgres":
            db.session.execute(db.update(Student).filter(Student.outid == uuid).values(**data))
            db.session.commit()
        case "mongo":
            data = {"regname" if k == "regname_id" else k:v for k,v in data.items()}
            data = {"sextype" if k == "sextype_id" else k:v for k,v in data.items()}
            mmodels.Student.objects(outid=uuid).update(__raw__={
                "$set": data,
            })
            
def delete_student(uuid):
    match ACTIVE_DB:
        case "postgres":
            student = db.one_or_404(db.select(Student).filter(Student.outid == uuid))
            db.session.delete(student)
            db.session.commit()
        case "mongo":
            person = mmodels.Student.objects.get(outid=uuid)
            person.delete()

def serialize_student_columns(exclude=None):
    match ACTIVE_DB:
        case "postgres":
            cols = list(map(lambda c: c.name, Student.__table__.columns))
            cols = [i if i != "sextype_id" else "sextype" for i in cols]
            cols = [i if i != "location_id" else "location" for i in cols]
            if exclude is not None:
                cols = list(filter(lambda x: x not in exclude, cols))
        case "mongo":
            default_exclude = ["tests"]
            cols = mmodels.Student._fields
            cols = list(filter(lambda x: x not in default_exclude, cols))
            if exclude is not None:
                cols = list(filter(lambda x: x not in exclude, cols))
    return cols


# Test services
def serialize_test_all(student_uuid):
    match ACTIVE_DB:
        case "postgres":
            tests = db.session.execute(db.select(Test).filter(Test.outid == student_uuid)).scalars()
        case "mongo":
            tests = mmodels.Test.objects(outid=student_uuid)
    return tests

def serialize_test(id):
    match ACTIVE_DB:
        case "postgres":
            id = int(id)
            test = db.one_or_404(db.select(Test).filter(Test.id == id))
        case "mongo":
            test = mmodels.Test.objects.get(id=id)
    return test

def serialize_test_options():
    match ACTIVE_DB:
        case "postgres":
            status = list(db.session.execute(db.select(TestStatus)).scalars())
            subject = list(db.session.execute(db.select(Subject)).scalars())
            location = list(db.session.execute(db.select(Location)).scalars())
        case "mongo":
            status = mmodels.TestStatus.objects
            subject = mmodels.Subject.objects
            location = mmodels.Location.objects
    return {
        "status": status,
        "subject": subject,
        "location": location
    }

def serialize_test_columns(exclude=None):
    match ACTIVE_DB:
        case "postgres":
            cols = list(map(lambda c: c.name, Test.__table__.columns))
            cols = [i if i != "subject_id" else "subject" for i in cols]
            cols = [i if i != "status_id" else "status" for i in cols]
            cols = [i if i != "location_id" else "location" for i in cols]
            if exclude:
                cols = list(filter(lambda x: x not in exclude, cols))
        case "mongo":
            cols = mmodels.Test._fields
            if exclude is not None:
                cols = list(filter(lambda x: x not in exclude, cols))
    return cols

def create_test(student_uuid, form):
    data = dict(form)
    match ACTIVE_DB:
        case "postgres":
            test = Test(**data)
            student = serialize_student(student_uuid)
            student.tests.append(test)
            db.session.add(student)
            db.session.commit()
        case "mongo":
            data = {"status" if k == "status_id" else k:v for k,v in data.items()}
            data = {"subject" if k == "subject_id" else k:v for k,v in data.items()}
            data = {"location" if k == "location_id" else k:v for k,v in data.items()}
            test = mmodels.Test(**{"outid": student_uuid, **data})
            test.save()
            person = serialize_student(student_uuid)
            person.tests.append(test)
            person.save()
        
def update_test(id, form):
    data = dict(form)
    data = {k:v for k,v in data.items() if v}
    match ACTIVE_DB:
        case "postgres":
            db.session.execute(db.update(Test).filter(Test.id == id).values(**data))
            db.session.commit()
        case "mongo":
            data = {"status" if k == "status_id" else k:v for k,v in data.items()}
            data = {"subject" if k == "subject_id" else k:v for k,v in data.items()}
            data = {"location" if k == "location_id" else k:v for k,v in data.items()}
            mmodels.Test.objects(id=id).update(__raw__={
                "$set": data,
            })
    
def delete_test(id):
    match ACTIVE_DB:
        case "postgres":
            id = int(id)
            test = db.one_or_404(db.select(Test).filter(Test.id == id))
            db.session.delete(test)
            db.session.commit()
        case "mongo":
            test = mmodels.Test.objects.get(id=id)
            test.delete()
    
def query(form):
    data = dict(form)
    
    
    match ACTIVE_DB:
        case "postgres":
            if res := r.get(str(data) + "postgres"):
                res = pickle.loads(res)
                return res
            
            res = db.session.execute(
                db.select(Test.year, Location.name.label("location"), func.avg(Test.ball100).label("bavg"))
                .join(Location)
                .where(
                    (Test.ball100 >= 100),
                    (Test.location_id == int(data.get("location_id")) if data.get("location_id") else True),
                    (Test.subject_id == int(data.get("subject_id")) if data.get("subject_id") else True),
                    (Test.year == int(data.get("year")) if data.get("year") else True),
                ).group_by(Test.year, Location.name)
            ).mappings()
            res = list(res)
            r.set(str(data) + "postgres", pickle.dumps(res))
        
        case "mongo":
            if res := r.get(str(data) + "mongo"):
                res = pickle.loads(res)
                return res
            
            conditions = {
                "ball100__gte":100,
                "ptregname": data.get("ptregname_id"),
                "subject": data.get("subject_id"),
                "year": data.get("year"),
            }

            conditions = {k:v for k,v in conditions.items() if v}
            
            res = mmodels.Test.objects(**conditions).aggregate([
                {
                    "$group": {
                        "_id": {"year": "$year", "location": "$location"},
                        "bavg": {"$avg": "$ball100"},
                    }
                }, 
                {
                    "$replaceRoot": {
                        "newRoot": {
                            "$mergeObjects": ["$_id", "$$ROOT"]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    }
                },
                {
                    "$lookup": {
                        "from": "location",
                        "localField": "location",
                        "foreignField": "_id",
                        "as": "location",
                    }
                }
            ])
            res = [{**item, "location": item["location"][0]["name"]} for item in res] #TODO improve aggregation + remove this
            r.set(str(data) + "mongo", pickle.dumps(res))
        
    return res