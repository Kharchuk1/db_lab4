CREATE TABLE subject(
  id SERIAL PRIMARY KEY, 
  name VARCHAR(40)
);

CREATE TABLE test_status(
  id SERIAL PRIMARY KEY, 
  name VARCHAR(40)
);

CREATE TABLE location(
  id SERIAL PRIMARY KEY,
  name VARCHAR(80)
);

CREATE TABLE sex_type(
  id SERIAL PRIMARY KEY,
  name VARCHAR(40)
);

CREATE TABLE student(
  outid UUID PRIMARY KEY,
  birth INT2 NOT NULL,
  sextype_id INT,
  location_id INT,
  areaname VARCHAR(256),
  tername VARCHAR(256),
  regtypename VARCHAR(256),
  tertypename VARCHAR(256),
  profile VARCHAR(256),
  language VARCHAR(256),
  eoname VARCHAR(256),
  eotypename VARCHAR(256),
  eoregname VARCHAR(256),
  eoareaname VARCHAR(256),
  eotername VARCHAR(256),
  eoparent VARCHAR(256)
);

CREATE TABLE test(
  id SERIAL PRIMARY KEY,
  outid UUID,
  subject_id INT,
  status_id INT,
  location_id INT,
  zno_grade INT,
  dpa_grade INT,
  test_grade INT,
  ptname VARCHAR(256),
  ptareaname VARCHAR(256),
  pttername VARCHAR(256),
  year INT
);

ALTER TABLE student
ADD CONSTRAINT student_sextype_fk
FOREIGN KEY (sextype_id) 
REFERENCES sex_type(id);

ALTER TABLE student
ADD CONSTRAINT student_location_fk
FOREIGN KEY (location_id) 
REFERENCES location(id);

ALTER TABLE test
ADD CONSTRAINT subject_fk 
FOREIGN KEY (subject_id) 
REFERENCES subject(id);

ALTER TABLE test
ADD CONSTRAINT test_status_fk 
FOREIGN KEY (status_id) 
REFERENCES test_status(id);

ALTER TABLE test
ADD CONSTRAINT test_student_fk
FOREIGN KEY (outid) 
REFERENCES student(outid);

ALTER TABLE test
ADD CONSTRAINT test_location_fk
FOREIGN KEY (location_id) 
REFERENCES location(id);