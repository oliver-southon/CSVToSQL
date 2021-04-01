import sqlite3
import csv
import os

db_name = 'school.db'
sql_name = 'dump.sql'

def makeDB(f):
    # -- SETUP -- #

    # database name
  

    # remove existing db and sql
    if os.path.exists(db_name):
        os.remove(db_name)

    if os.path.exists(sql_name):
        os.remove(sql_name)

    # make db
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # read csv
    f = open(f, 'r')
    csv_data = csv.reader(f)

    # make table containing everything in csv. will be used to insert into the split tables
    c.execute("""
        CREATE TABLE IF NOT EXISTS ImportTable (
            teacher_id INTEGER NOT NULL,
            teacher_title TEXT,
            teacher_surname TEXT,
            subject_id TEXT NOT NULL,
            subject_name TEXT,
            student_id INTEGER NOT NULL,
            student_first_name TEXT,
            student_surname TEXT,
            student_year TEXT,
            parent_id INTEGER NOT NULL,
            parent_first_name TEXT,
            parent_surname TEXT,
            parent_email TEXT
        )
    """)

    for row in csv_data:
        c.execute ("""
            INSERT INTO ImportTable (
                teacher_id, teacher_title, teacher_surname, subject_id, subject_name, student_id, student_first_name, student_surname, student_year, parent_id, parent_first_name, parent_surname, parent_email
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (row)
        )

    # >1. MAKE TABLES
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS Parent (
            parent_id INTEGER NOT NULL,
            parent_first_name TEXT,
            parent_surname TEXT,
            parent_email TEXT,
            PRIMARY KEY (parent_id)
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS Student (
            student_id INTEGER NOT NULL,
            student_first_name TEXT,
            student_surname TEXT,
            student_year TEXT,
            parent_id INTEGER NOT NULL,
            PRIMARY KEY (student_id),
            FOREIGN KEY (parent_id) REFERENCES Parent(parent_id)
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS Teacher (
            teacher_id INTEGER NOT NULL,
            teacher_title TEXT,
            teacher_surname TEXT,
            PRIMARY KEY (teacher_id)
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS Subject (
            subject_id TEXT NOT NULL,
            subject_name TEXT,
            PRIMARY KEY (subject_id)
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS Class (
            class_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            PRIMARY KEY (class_id),
            FOREIGN KEY (subject_id) REFERENCES Subject(subject_id),
            FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS Student_Class (
            student_id_fk INTEGER NOT NULL,
            class_id_fk INTEGER NOT NULL,
            PRIMARY KEY (student_id_fk, class_id_fk),
            FOREIGN KEY (student_id_fk) REFERENCES Student(student_id),
            FOREIGN KEY (class_id_fk) REFERENCES Class(class_id)
        )
        """
    )

    # >2 .INSERT DATA
    c.execute(
        """
        INSERT INTO Parent (
            parent_id, parent_first_name, parent_surname, parent_email
        ) SELECT DISTINCT parent_id, parent_first_name, parent_surname, parent_email FROM ImportTable
        """
    )

    c.execute(
        """
        INSERT INTO Student (
            student_id, student_first_name, student_surname, student_year, parent_id
        ) SELECT DISTINCT student_id, student_first_name, student_surname, student_year, parent_id FROM ImportTable
        """
        )

    c.execute(
        """
        INSERT INTO Subject (
            subject_id, subject_name
        ) SELECT DISTINCT subject_id, subject_name FROM ImportTable
        """
        )

    c.execute(
        """
        INSERT INTO Teacher (
            teacher_id, teacher_title, teacher_surname
        ) SELECT DISTINCT teacher_id, teacher_title, teacher_surname FROM ImportTable
        """
        )
        
    c.execute(
        """
        INSERT INTO Class (
            subject_id, teacher_id
        ) SELECT DISTINCT subject_id, teacher_id FROM ImportTable
        """
        )
        
    c.execute(
        """
        INSERT INTO Student_Class (
            student_id_fk, class_id_fk
        ) SELECT DISTINCT S.student_id, C.class_id FROM Student S, Class C
        """
        )

    conn.commit()

    out = open(sql_name, 'w')
    for line in conn.iterdump():
        out.write('%s\n' % line)
    out.close()
    return out
    
