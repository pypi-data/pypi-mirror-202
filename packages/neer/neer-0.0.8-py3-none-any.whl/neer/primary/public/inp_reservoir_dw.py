from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class InpReservoirDw(PrimaryBase):
    __tablename__ = 'inp_reservoir_dw'
    __table_args__ = {'schema': 'public'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(250), autoincrement=False)
    descript = Column(VARCHAR(1024), autoincrement=False)
    total_head = Column(VARCHAR(25), autoincrement=False)
    head_pat = Column(VARCHAR(25), autoincrement=False)
    init_qual = Column(VARCHAR(25), autoincrement=False)
    src_qual = Column(VARCHAR(25), autoincrement=False)
    src_pattern = Column(VARCHAR(25), autoincrement=False)
    src_type = Column(VARCHAR(25), autoincrement=False)
    project_id = Column(INTEGER, autoincrement=False)
    site_id = Column(VARCHAR(191), autoincrement=False)
    a_type = Column(VARCHAR(191), autoincrement=False)
    a_status = Column(VARCHAR(191), autoincrement=False)
    a_pressure_zone = Column(VARCHAR(191), autoincrement=False)
    a_dma = Column(VARCHAR(191), autoincrement=False)
