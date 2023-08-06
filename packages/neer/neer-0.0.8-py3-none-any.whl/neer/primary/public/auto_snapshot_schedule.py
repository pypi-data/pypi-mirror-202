from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class AutoSnapshotSchedule(PrimaryBase):
    __tablename__ = 'auto_snapshot_schedule'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    project_id = Column(VARCHAR(191), autoincrement=False)
    repetition = Column(VARCHAR(191), autoincrement=False)
    time = Column(VARCHAR(191), autoincrement=False)
    start_date = Column(VARCHAR(191), autoincrement=False)
    end_date = Column(VARCHAR(191), autoincrement=False)
    run_simulation = Column(BOOLEAN, autoincrement=False)
    created_at = Column(TIMESTAMP(timezone=False), autoincrement=False)
    updated_at = Column(TIMESTAMP(timezone=False), autoincrement=False)
    group = Column(VARCHAR(20), autoincrement=False)