import random

from sqlalchemy import *
from conf import DATABASE

class Repository:
    '''
    Database contains a project table
    '''

    def __init__(self, showLog = False):
        """
        Initialize database structure
        """

        self.__showLog = showLog
        self.__engine = create_engine('postgres://{}:{}@localhost:{}/{}'.format(DATABASE['USER'], DATABASE['PASSWORD'], DATABASE['PORT'], DATABASE['DB_NAME']) , echo=self.__showLog, pool_size=20, pool_recycle=3600)
        self.__metadata = MetaData()

        self.__project = Table('project', self.__metadata,
                               Column('id', Integer, primary_key=True),
                               Column('name', String(255), nullable=False),
                               Column('budget', Float, nullable=False),
                               Column('location', String(255), nullable=False)
        )
        
        
    def create_schema(self):
        """
        Create schema in database.
        """
        self.__metadata.drop_all(self.__engine)
        self.__metadata.create_all(self.__engine)
        

    def get_engine(self):
        return self.__engine
    
    def get_meta_data(self):
        return self.__metadata
    
    def populate_data(self):
        locations = ['Addis Ababa', 'Awassa', 'Bahir Dar', 'Mekelle']
        for i in range(100):
            result = self.__engine.connect().execute(
                self.__project.insert()
                .values(name = 'PROJ ' + str(i),
                        budget = random.randint(10000, 40000),
                        location = locations[random.randint(0, len(locations) -1)]
                       )
            )
            
    def get_projects(self, location=None, budget=None):
        result = self.__engine.connect().execute(
            select([self.__project.c.id, 
                    self.__project.c.name, 
                    self.__project.c.location, 
                    self.__project.c.budget]
                  )
        )
        
        return result.fetchall()
    
    def fragment(self, relation, predicate):
        result = self.__engine.connect().execute(
            text("select * from " + relation + " where " + predicate.attribute + predicate.operation + "'" + str(predicate.value) +"'")
        )
        
        return result.fetchall()
    
    
repo = Repository()
meta = repo.get_meta_data()
repo.create_schema()
repo.populate_data()



