import sqlalchemy as sa
import mmodels
from app import db
from models import SexType, TestStatus, Subject, Location, Student, Test

def migrate():
    if mmodels.SexType.objects.count() > 0:
        return None
    
    print("Migrating to MongoDB")
    
    #SexType
    print("Migrating SexType")
    items = db.session.execute(db.select(SexType.__table__)).mappings()
    for item in items:
        mmodels.SexType(**item).save()

    #TestSubject
    print("Migrating Subject")
    items = db.session.execute(db.select(Subject.__table__)).mappings()
    for item in items:
        mmodels.Subject(**item).save()

    #TestStatus
    print("Migrating TestStatus")
    items = db.session.execute(db.select(TestStatus.__table__)).mappings()
    for item in items:
        mmodels.TestStatus(**item).save()
    
    #Location
    print("Migrating Location")
    items = db.session.execute(db.select(Location.__table__)).mappings()
    for item in items:
        mmodels.Location(**item).save()
    
    #Test
    print("Migrating Tests")
    tcolumns = ["outid", "year", "zno_grade", "dpa_grade", "test_grade", "ptname", "ptareaname", "pttername"]
    subjects = {i.name:i for i in mmodels.Subject.objects.all()}
    statuses = {i.name:i for i in mmodels.TestStatus.objects.all()}
    locations = {i.name:i for i in mmodels.Location.objects.all()}
    tests = db.session.execute(db.select(Test)).scalars()
    for i, partition in enumerate(tests.partitions(10000)):
        print(f"Migrating Test [~ {i*10000}]")
        ntests = []
        for t in partition:
            subject = subjects.get(t.subject.name)
            status = statuses.get(t.status.name)
            location = locations.get(t.location.name)
            rst = {attr:getattr(t, attr) for attr in tcolumns}
            ntest = mmodels.Test(**{
                "subject":subject.id,
                "status":status.id,
                "location":location.id,
                **rst
            })
            ntests.append(ntest)
        mmodels.Test.objects.insert(ntests)

    #Student
    print("Migrating Student")
    pcolumns = ["birth", "areaname", "tername", "regtypename",
               "tertypename", "profile", "language",
               "eoname", "eotypename", "eoregname", "eoareaname",
               "eotername", "eoparent"]
    persons = db.session.execute(db.select(Student).options(sa.orm.selectinload(Student.tests))).scalars()
    sextypes = {i.name:i for i in mmodels.SexType.objects.all()}
    locations = {i.name:i for i in mmodels.Location.objects.all()}
    for i, partition in enumerate(persons.partitions(10000)):
        print(f"Migrating Student [~ {i*10000}]")
        npersons = []
        for person in partition:
            sextype = sextypes.get(person.sextype.name)
            location = locations.get(person.location.name)
            rst = {attr:getattr(person, attr) for attr in pcolumns}
            tests = [test.id for test in person.tests]
            nperson = mmodels.Student(**{
                "outid":str(person.outid),
                "sextype":sextype.id,
                "location":location.id,
                "tests":tests,
                **rst
            })
            npersons.append(nperson)
        mmodels.Student.objects.insert(npersons)
    