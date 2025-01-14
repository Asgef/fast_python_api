from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse


app = FastAPI()


@app.get('/')
async def homepage():
    return JSONResponse({'Hello': 'World'})