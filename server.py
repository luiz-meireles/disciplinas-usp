from collections import defaultdict
import re
from typing import List, Optional
from fastapi import FastAPI
from fastapi.params import Query
from starlette.responses import JSONResponse
from models import get_deep_subject_requirements
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


@app.get(
    "/requirements/",
)
async def read_root(subject: List[str] = Query([])):

    requirements_by_subject = defaultdict(list)
    get_deep_subject_requirements(
        subject, max_level=10, requirements_by_subject=requirements_by_subject
    )

    return JSONResponse(requirements_by_subject)
