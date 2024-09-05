from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# con = psycopg2.connect(
#     dbname = "postgres",
#     user = self.user_name,
#     password = self.password, 
#     host = '',
# )

# con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# cur = con.cursor()

# cur.execute(sql.SQL())
             # postgresql://username:password@host:port/database_name
DATABASE_URL = "postgresql://TimeTracker:test@localhost:5432/timetracker"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()