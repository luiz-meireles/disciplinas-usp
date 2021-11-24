from models import *


def get_all_departments_from_subject():
    query = Subject.select(Subject.department).group_by(Subject.department)
    return query


def populate_department(departments_list):
    with db.atomic():
        try:
            Department.insert_many(
                [{"name": department.department} for department in departments_list]
            ).execute()
        except IntegrityError:
            print(f"Some departments Already present")


# populate_department(get_all_departments_from_subject())


def associate_subject_departments():
    subjects = Subject.select()
    departments = Department.select()
    departments_by_name = {department.name: department for department in departments}
    with db.atomic():
        for subject in subjects:
            department = departments_by_name.get(subject.department_name)
            print(
                f"Associating subject {subject.name} with department {department.name}"
            )
            print(subject.department_name, subject.department_id)
            if department:
                Subject.update(department=department).where(
                    Subject.department_name == department.name
                ).execute()


def associate_unit_departments():
    units = Unit.select()
    deparments = Department.select()
    units_by_code = {unit.code: unit for unit in units}
    with db.atomic():
        for department in deparments:
            unit = units_by_code.get(department.unit_code)
            print(f"Associating subject {department.name} with department {unit.name}")
            print(department.name, department.id)
            if unit:
                Department.update(unit=unit).where(
                    Department.unit_code == unit.code
                ).execute()


associate_unit_departments()
