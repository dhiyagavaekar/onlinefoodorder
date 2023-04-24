from models import department_models
from fastapi import HTTPException
from common import helper as common_helper
from . import helper as department_helper


def read_department(id: int, session):

    # get the department data with the given id
    department =\
        session.query(
            department_models.Department
        ).filter(
            department_models.Department.DepartmentID==id
        ).first()

    # check if department data with given id exists. If not, raise exception and return 404 not found response
    if not department:
        raise HTTPException(
            status_code=404, detail=f"department data with id {id} not found"
        )

    return department



def create_department(department,session):

    # create an instance of the Department database model
    department =\
        department_helper.transform_json_data_into_department_model(
            department_models.Department(), 
            dict(department)
        )
    # add it to the session and commit it
    session.add(department)
    session.commit()
    session.refresh(department)

    # return the department object
    return department


def update_department(id: int,update_department, session):
    update_department_json_data = dict(update_department)
    department =\
        session.query(
            department_models.Department
        ).filter(
            department_models.Department.DepartmentID==id
        ).first()
    # update department data with the given departments (if an data with the given id was found)
    if department:
        department=\
            department_helper.transform_json_data_into_department_model(
                department,update_department_json_data
            )
        session.commit()
    # check if department data with given id exists. If not, raise exception and return 404 not found response
    if not department:
        raise HTTPException(
            status_code=404, detail=f"department data with id {id} not found"
        )

    return department

def delete_department(id: int, session):

    # get the department data with the given id
    department = session.query(department_models.Department).get(id)

    # if department data with given id exists, delete it from the database. Otherwise raise 404 error
    if department:
        session.delete(department)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"department data with id {id} not found")

    return None

def read_department_list(session):

    # get all department data
    department_list =\
        session.query(
            department_models.Department
        ).first()

    return department_list

