from datetime import datetime
from sqlalchemy import create_engine


from sqlalchemy.orm import sessionmaker

from models import Person, Phones
   
engine = create_engine('sqlite:///test_new.db')  
DBSession = sessionmaker(bind=engine)
session = DBSession()
COMMANDS_LIST = ["hello", "exit", "close", "good bye", "show_all", "phone", "add", "add_phone",
                 "del_phone", "edit_phone", "del_contact", "add_birthday", "find"]

def handling(user_command_normalized):
    if "add" == str(user_command_normalized[0]):
        excist = 0
        for person in session.query(Person).all():
            if f"{user_command_normalized[1]}" == person.name:
                print(f"Contact name {user_command_normalized[1]} exists. Please use another name")     
                excist=1
        
        if excist == 0: 
            new_person = Person(name=f"{user_command_normalized[1]}")           
            session.add(new_person)            
            session.commit()
            print(f'Person {user_command_normalized[1]} added')

    elif "add_phone" == str(user_command_normalized[0]):
        excist = 0
        for person in session.query(Person).all():
            if f"{user_command_normalized[1]}" == person.name:
                excist=1
                if person.phones:
                    person.phones.append(Phones(phone=f"{user_command_normalized[2]}"))
                else:
                    person.phones =[Phones(phone=f"{user_command_normalized[2]}")]     
                session.add(person)                      
        if excist == 0:
            new_person = Person(name=f"{user_command_normalized[1]}")
            new_person.phones = [Phones(phone=f"{user_command_normalized[2]}")]
            session.add(new_person)            
        session.commit()
        
    elif "phone" == str(user_command_normalized[0]):
        excist = 0
        for person in session.query(Person).all():
            if f"{user_command_normalized[1]}" == person.name:
                for phone in person.phones:
                    print(phone.phone)
       

    elif "add_birthday" == str(user_command_normalized[0]):
        raw_birtday = f"{user_command_normalized[2]}"
        dt_birthday = datetime(year=int(raw_birtday[0:4]), month=int(raw_birtday[4:6]), day=int(raw_birtday[6:]))
        excist = 0
        for person in session.query(Person).all():
            if f"{user_command_normalized[1]}" == person.name:
                excist=1
                person.birthday=dt_birthday 
                session.add(person)
                print(f'Birthaday of {user_command_normalized[1]} is added')
                session.commit()          
        if excist == 0:            
            new_person = Person(name=f"{user_command_normalized[1]}")
            new_person.birthday=dt_birthday 
            session.add(new_person) 
            print(f'Person {user_command_normalized[1]} added')  
            session.commit()

    elif "edit_phone" == str(user_command_normalized[0]):        
        exist = 0
        for person in session.query(Person).all():
            if f"{user_command_normalized[1]}" == person.name:
                for phone in person.phones:                              
                    if phone.phone == int(user_command_normalized[2]):
                        phone.phone = int(user_command_normalized[3])
                        phone.person_id=person.id
                        print(f"Phone {user_command_normalized[2]} changet at {user_command_normalized[3]}")
                        exist = 1                                             
                        session.add(phone) 
                        session.commit()
        if exist == 0:
            print(f"There are no Person or phone") 

    elif "del_phone" == str(user_command_normalized[0]):        
        exist = 0
        for person in session.query(Person).all():
            if f"{user_command_normalized[1]}" == person.name:
                for phone in person.phones:                              
                    if phone.phone == int(user_command_normalized[2]):                        
                        print(f"Phone {user_command_normalized[2]} deleted")
                        exist = 1                                             
                        session.delete(phone) 
                        session.commit()
        if exist == 0:
            print(f"There are no Person or phone")                                             

    elif "del_contact" == str(user_command_normalized[0]):        
        exist = 0
        print("aaa")
        session.query(Person).filter(Person.name == f"{user_command_normalized[1]}").delete(synchronize_session='fetch')
        session.commit()

    elif "find" == str(user_command_normalized[0]):       
        for person in session.query(Person).all():
            if user_command_normalized[1] in person.name:
                print (person.name)
            for phone in person.phones:
                print(phone.phone)
    
    elif "show_all" == str(user_command_normalized[0]):       
        contact =[] 
        for person in session.query(Person).all():
            contact.append(person.name)
            if person.birthday != None:
                contact.append(person.birthday)    
            for phone in person.phones:
                contact.append(phone.phone)                                    
            print (contact)
            contact.clear()

def input_():
    while True:
        raw_user_command = input("Please, give me a command:")
        raw_user_command = raw_user_command.split(" ")        
        if raw_user_command[0] in COMMANDS_LIST:  
            return raw_user_command
        continue

while True:
    raw_user_command = input_()
    if raw_user_command[0] in ["close", "good bye", "exit"]:
        print("By")    
        break
    elif raw_user_command[0] == "hello":
        print(f"I know follow coomands{COMMANDS_LIST}")

    a= handling(raw_user_command) 
    try:
        a() 
    except   TypeError:
        pass                         