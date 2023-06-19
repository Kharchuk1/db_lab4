import mongoengine as me
import uuid

class SexType(me.Document):
    id = me.IntField(primary_key=True)
    name = me.StringField()
    
    def __str__(self):
        return self.name

class Location(me.Document):
    id = me.IntField(primary_key=True)
    name = me.StringField()
    
    def __str__(self):
        return self.name

class Subject(me.Document):
    id = me.IntField(primary_key=True)
    name = me.StringField()
    
    def __str__(self):
        return self.name

class TestStatus(me.Document):
    id = me.IntField(primary_key=True)
    name = me.StringField()
    
    def __str__(self):
        return self.name

class Test(me.Document):
    outid = me.UUIDField(binary=False)
    year = me.IntField()
    subject = me.ReferenceField(Subject)
    status = me.ReferenceField(TestStatus) 
    zno_grade = me.IntField()
    dpa_grade = me.IntField()
    test_grade = me.IntField()
    ptname = me.StringField()
    location = me.ReferenceField(Location)
    ptareaname = me.StringField()
    pttername = me.StringField()

class Student(me.Document):
    outid = me.UUIDField(primary_key=True, binary=False, default=uuid.uuid4)
    birth = me.IntField()
    sextype = me.ReferenceField(SexType)
    location = me.ReferenceField(Location)
    areaname = me.StringField()
    tername  = me.StringField()
    regtypename  = me.StringField()
    tertypename  = me.StringField()
    profile  = me.StringField()
    language  = me.StringField()
    eoname  = me.StringField()
    eotypename  = me.StringField()
    eoregname  = me.StringField()
    eoareaname  = me.StringField()
    eotername  = me.StringField()
    eoparent  = me.StringField()

    tests = me.ListField(me.ReferenceField(Test))