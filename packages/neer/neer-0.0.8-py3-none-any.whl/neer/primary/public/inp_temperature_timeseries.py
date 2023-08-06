from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class InpTemperatureTimeseries(PrimaryBase):
    __tablename__ = 'inp_temperature_timeseries'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    temperature_id = Column(INTEGER, nullable=False, autoincrement=False)
    timeseries_name = Column(VARCHAR(250), autoincrement=False)
    created_at = Column(TIMESTAMP, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
