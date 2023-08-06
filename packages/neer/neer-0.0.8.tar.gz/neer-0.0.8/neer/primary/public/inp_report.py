from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class InpReport(PrimaryBase):
    __tablename__ = 'inp_report'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    option_name = Column(VARCHAR(25), autoincrement=False)
    option_value = Column(VARCHAR(255), autoincrement=False)
    description = Column(VARCHAR(1024), autoincrement=False)
