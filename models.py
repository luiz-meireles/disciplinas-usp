from collections import defaultdict
from playhouse.migrate import *
from peewee import *
import itertools
import pprint
from dataclasses import dataclass

pp = pprint.PrettyPrinter(indent=4)

db = SqliteDatabase("data.db")
migrator = SqliteMigrator(db)


class BaseModel(Model):
    class Meta:
        database = db


class Department(BaseModel):
    name = CharField()

    class Meta:
        indexes = ((("name",), True),)


class Subject(BaseModel):
    code = CharField()
    name = TextField()
    credits = TextField()
    wcredits = TextField()
    summary = TextField()
    department = ForeignKeyField(Department)


class SubjectRequirement(BaseModel):
    subject = ForeignKeyField(Subject)
    requirement = ForeignKeyField(Subject)
    requirement_type = TextField()

    class Meta:
        indexes = ((("subject", "requirement", "requirement_type"), True),)


class ErrorLogger(BaseModel):
    subject_code = TextField()
    error = TextField()


db.connect()
db.create_tables(
    [Subject, ErrorLogger, SubjectRequirement, Department],
)


def get_subject_requirements(subject_codes=[]):

    subject = Subject.alias()
    query = (
        SubjectRequirement.select(SubjectRequirement)
        .join(Subject, on=Subject.id == SubjectRequirement.requirement)
        .join(subject, on=subject.id == SubjectRequirement.subject)
    )

    if subject_codes:
        return query.where(Subject.code.in_(subject_codes))

    return query


def get_deep_subject_requirements(
    subject_codes=[], max_level=5, level=1, requirements_by_subject=defaultdict(list)
):
    print("level", level)
    print("subject_codes", subject_codes)

    if level == max_level or len(subject_codes) == 0:
        return

    requirements_codes = []
    for subject_code in subject_codes:
        if subject_code not in requirements_by_subject:
            requirements_by_subject[subject_code] = []

    for req in get_subject_requirements(subject_codes):
        if req.requirement.code not in requirements_by_subject:
            requirements_codes.append(req.requirement.code)
        requirements_by_subject[req.subject.code].append(req.requirement.code)
        # requirements_by_subject[req.subject.code]["level"] = level

    pp.pprint(requirements_by_subject)

    get_deep_subject_requirements(
        subject_codes=requirements_codes,
        max_level=max_level,
        level=level + 1,
        requirements_by_subject=requirements_by_subject,
    )
