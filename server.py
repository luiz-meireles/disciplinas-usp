from collections import defaultdict
import re
from typing import List, Optional
from fastapi import FastAPI
from fastapi.params import Query
import pydantic
from starlette.responses import JSONResponse
from models import (
    get_deep_subject_requirements,
    add_unit,
    update_department as _update_department,
)
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Unit(BaseModel):
    code: str
    name: str


class Department(BaseModel):
    code: str
    name: str
    unit_code: str


@app.get(
    "/requirements/",
)
async def read_root(subject: List[str] = Query([])):

    requirements_by_subject = defaultdict(list)
    get_deep_subject_requirements(
        subject, max_level=10, requirements_by_subject=requirements_by_subject
    )

    return JSONResponse(requirements_by_subject)


@app.post("/unit")
async def add_unidade(unidade: Unit):
    add_unit({"code": unidade.code, "name": unidade.name})
    return JSONResponse({})


@app.post("/department")
async def update_department(department: Department):
    print(department)
    _update_department(
        department.code,
        department.name,
        department.unit_code,
    )
    return JSONResponse({})
