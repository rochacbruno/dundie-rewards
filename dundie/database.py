import warnings

from sqlalchemy.exc import SAWarning
from sqlmodel import Session, create_engine

# We have to monkey patch this attributes
# https://github.com/tiangolo/sqlmodel/issues/189
from sqlmodel.sql.expression import Select, SelectOfScalar

from dundie import models
from dundie.settings import SQL_CON_STRING

# ^ IMPORTANTE importar todos os models para este contexto

warnings.filterwarnings("ignore", category=SAWarning)

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

engine = create_engine(SQL_CON_STRING, echo=False)
models.SQLModel.metadata.create_all(bind=engine)


def get_session() -> Session:
    return Session(engine)
