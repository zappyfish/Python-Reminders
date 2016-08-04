import shelve

class shelveWith(object):
    def __enter__(self,filey):
        self.open(filey)
    def __exit__(self, type, value, traceback):
        self.close()
class assignment(object):
    def __init__(self, name, due_date):
        self.name = name
        self.due_date = due_date
        # date should be a tuple in format (MM, DD, YYYY)

class appointment(object):
    def __init__(self, appointment_type, date, time, location):
        self.type = appointment_type
        self.time = time
        # time should be a tuple in format(HH, MM, Bool)
        self.date = date
        # date should be a tuple in format (MM, DD, YYYY)
        self.location = location

#save assignments based on their due_date. same handling method as appointments
def save_assignment(assignment):
    f = shelve.open('assignment_db')
    try:  
        f[assignment.due_date].append(assignment)
    except KeyError:
        f[assignment.due_date] = [assignment]
    f.close()
            
# save appoiments based on their date 
def save_appointment(appointment):
    f = shelve.open('appointment_db')
    try:
         f[str(appointment.date)].append(appointment)
        #if other appointments exist on this day, add it to that list
        #otherwise, create a list for that date
    except KeyError:
        f[str(appointment.date)] = [appointment]
    f.close()

# get tuple of assignment objects for a given due date
def get_assignment(date):
    f = shelve.open('assignment_db')
    try:
        assignments = f[str(date)]
        return assignments
    except KeyError:
        pass
    f.close()
# get tuple of appointment objects for a given appointment date
def get_appointment(date):
    f = shelve.open('appointment_db')
    try:
        appointments = f[str(date)]
        return appointments
    except KeyError:
        pass
    f.close()

            
    
