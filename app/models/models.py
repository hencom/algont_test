from datetime import datetime
import databases
import sqlalchemy

import ormar

database = databases.Database(
    "postgresql://algontuser:algont2022@db_algont/algontdb")
engine = sqlalchemy.create_engine(
    "postgresql://algontuser:algont2022@db_algont/algontdb")

# database = databases.Database("sqlite:///./database.db")
metadata = sqlalchemy.MetaData()


class CpuPerformance(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    performance: float = ormar.Float()
    date_time: datetime = ormar.DateTime(server_default=sqlalchemy.func.now())
