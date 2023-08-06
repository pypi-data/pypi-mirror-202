from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class SparkReportLinksDw(PrimaryBase):
    __tablename__ = 'spark_report_links_dw'
    __table_args__ = {'schema': 'predictions'}
    
    project_id = Column(INTEGER, primary_key=True, autoincrement=False)
    simulation_id = Column(INTEGER, primary_key=True, autoincrement=False)
    order = Column(INTEGER, primary_key=True, autoincrement=False)
    name = Column(TEXT, primary_key=True, autoincrement=False)
    datetime = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    layer = Column(TEXT, autoincrement=False)
    state = Column(TEXT, autoincrement=False)
    date = Column(DATE, nullable=False, autoincrement=False)
    time = Column(TIME, nullable=False, autoincrement=False)
    flow = Column(NUMERIC, autoincrement=False)
    velocity = Column(NUMERIC, autoincrement=False)
    headloss = Column(NUMERIC, autoincrement=False)
    setting = Column(NUMERIC, autoincrement=False)
    reaction = Column(NUMERIC, autoincrement=False)
    f_factor = Column(NUMERIC, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    is_forecasted = Column(BOOLEAN, primary_key=True, autoincrement=False)
