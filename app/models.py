from app import db

class Location(db.Model):
    __table__ = db.metadata.tables["location"]
    
    def __str__(self):
        return self.name

class SexType(db.Model):
    __table__ = db.metadata.tables["sex_type"]
    
    def __str__(self):
        return self.name

class Student(db.Model):
    __table__ = db.metadata.tables["student"]
    
    tests = db.relationship(
        "Test", cascade="all,delete-orphan", lazy="selectin", back_populates="student"
    )
    
    sextype = db.relationship(
        "SexType", lazy=True
    )
    
    location = db.relationship(
        "Location", lazy=True
    )

class TestStatus(db.Model):
    __table__ = db.metadata.tables["test_status"]
    
    def __str__(self):
        return self.name
    
class Subject(db.Model):
    __table__ = db.metadata.tables["subject"]
    
    def __str__(self):
        return self.name

class Test(db.Model):
    __table__ = db.metadata.tables["test"]
    
    student = db.relationship(
        "Student", single_parent=True, back_populates="tests"
    )
    
    subject = db.relationship(
        "Subject", lazy=True
    )
    
    status = db.relationship(
        "TestStatus", lazy=True
    )
    
    location = db.relationship(
        "Location", lazy=True
    )