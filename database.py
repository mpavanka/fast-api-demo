from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://postgres:420638@localhost:5432/fast-api-demo')
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
