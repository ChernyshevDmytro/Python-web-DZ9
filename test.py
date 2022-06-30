from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base() 

class Person(Base):
    __tablename__ = "person"    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)  

class Phones(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    phone = Column(Integer, unique=True)
    person_id = Column(Integer, ForeignKey('person.id'))  
    person = relationship(Person)

class Birthday(Base):
    __tablename__ = "birthdays"
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    birthday = Column(DateTime, nullable=True)
    person_id = Column(Integer, ForeignKey('person.id'))  
    person = relationship(Person)    

class Record(Base):
    __tablename__ = "all_data"
    id = Column(Integer, primary_key=True)
    person_id = Column(String(50), ForeignKey('person.id'))
    name = Column(String(50), ForeignKey('person.name'))
    phone = Column(Integer, ForeignKey('phones.phone'))      
    birthday = Column(DateTime, ForeignKey('birthdays.birthday'))
     
    
engine = create_engine('sqlite:///DZ9.db')
Base.metadata.create_all(engine)   
DBSession = sessionmaker(bind=engine)
COMMANDS_LIST = ["hello", "exit", "close", "good bye", "show all", "phone", "add", "add_phone",
                 "del_phone", "edit_phone", "del_contact", "add_birthday", "find"]

def handling(user_command_normalized):  
    session = DBSession()
    if "add" == str(user_command_normalized[0]):
        new_person = Person(name=f"{user_command_normalized[1]}")
        
        session.add(new_person)
        session.commit()
    elif "add_phone" == str(user_command_normalized[0]):
        new_person = Person(name=f"{user_command_normalized[1]}")
        new_phone = Phones(phone=f"{user_command_normalized[2]}", person=new_person)        
        session.add(new_phone)
        session.commit() 

def input_():
    while True:
        raw_user_command = input("Please, give me a command:")
        raw_user_command = raw_user_command.split(" ")
        print(raw_user_command)
        if raw_user_command[0] in COMMANDS_LIST:     
            
            return raw_user_command
        continue

raw_user_command = input_()
a= handling(raw_user_command) 
try:
    a() 
except   TypeError:
    pass                         