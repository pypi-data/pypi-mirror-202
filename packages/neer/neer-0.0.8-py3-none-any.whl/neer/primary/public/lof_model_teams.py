from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT, SMALLINT
from neer.base import PrimaryBase

class LofModelTeams(PrimaryBase):
    __tablename__ = 'lof_model_teams'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    lof_model_id = Column(BIGINT, nullable=False, autoincrement=False)
    team_id = Column(INTEGER, autoincrement=False)
    user_id = Column(INTEGER, autoincrement=False)
    project_id = Column(INTEGER, autoincrement=False)
