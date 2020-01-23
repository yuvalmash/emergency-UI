# from .sqlite_conf import *
from . import sqlite_handler

sqlite_handler.create_tables(sqlite_handler.DATABASE)