import os
from typing import List, Optional
from datetime import timedelta

from fastapi import FastAPI, HTTPException, status, Query, Body, Path, Depends
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from fastapi.middleware.cors import CORSMiddleware

import operations
import database


app = FastAPI(
    title="Mascotas",
    description="Una API básica para gestionar usuarios y mascotas.",
    version="1.0.0",
)