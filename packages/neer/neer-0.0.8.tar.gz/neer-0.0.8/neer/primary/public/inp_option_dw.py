from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class InpOptionDw(PrimaryBase):
    __tablename__ = 'inp_option_dw'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    option_name = Column(VARCHAR(25), autoincrement=False)
    option_value = Column(VARCHAR(250), autoincrement=False)
    description = Column(TEXT, autoincrement=False)
