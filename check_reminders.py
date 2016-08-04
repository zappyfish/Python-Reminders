import shelve
import datetime
import reminder_setup
from Tkinter import *
from tkMessageBox import showinfo
import sys

#get the value of a month. not perfect b/c leap years but w/e
def month_value(month):
    monthDict = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:30}
    month_value = 0
    for i in range(1, month):
        month_value+=monthDict[i]
    return month_value
#take difference between two dates 
def date_difference(check_date, current_date):
    current_date_value = (365 * current_date[2]) + current_date[1] + month_value(current_date[0])
    date_value = (365 * check_date[2]) + check_date[1] + month_value(check_date[0])
    difference = current_date_value - date_value
    return difference

def clearOld(current_date):
    f = shelve.open('assignment_db')
    for date in f:
        my_date_tuple = (int(date[1:3]), int(date[5:7]), int(date[9:13])) 
        if date_difference(my_date_tuple, current_date) > 0:
            del f[date]
    f.close()
    f = shelve.open('appointment_db')
    for date in f:
        print date
        my_date_tuple = (int(date[1:3]), int(date[5:7]), int(date[9:13]))
        print my_date_tuple
        if date_difference(my_date_tuple, current_date) > 0:
            del f[date]
    f.close()
# whenever script is called, delete old assignments/appointments            


#start tkinter interface over here
#start by reminding the user of everything in the upcoming week
today = datetime.date.today()
my_day = today.strftime('%d%m%Y')
my_date_tuple = (int(my_day[:2]), int(my_day[2:4]), int(my_day[4:6]))

#start with all the dates we need to deal with

dates = []
for i in range(1, 7):
    delta = datetime.timedelta(i)
    new_day = today + delta
    my_day = new_day.strftime('(%m, %d, %Y)') 
    dates.append(my_day)
    

#now we can create the tkinter userface and cycle through all assignments
#and appointments for each given date!
def format_date(my_date_string):
    #in format (MM, DD, YYYY)
    formatted_date = my_date_string[1:3] + '-' + my_date_string[5:7] + '-' + my_date_string[9:13]
    return formatted_date

def show_upcoming_assignment(assignment):
    due_date = format_date(assignment.due_date)
    showinfo(title=due_date, message='Assignment: %s\nDue Date: %s' % (assignment.name, due_date))
    
def show_upcoming_appointments(appointment):
    date = format_date(appointment.date)
    time = appointment.time
    showinfo(title=date, message='Appointment: %s\nDate: %s\nTime: %s\nLocation: %s' %(appointment.type, date, time, appointment.location))
   

  
#then ask if the user has any new things to add

def anything_else():
    mainwin = Tk()
    Label(mainwin, text="Anything to Remind Yourself of?").pack()
    Button(mainwin, text='Yes, appointment', command=addAppointment).pack(side=LEFT)
    Button(mainwin, text='Yes, assignment', command=addAssignment).pack(side=LEFT)
    Button(mainwin, text='Nope', command=sys.exit).pack(side=RIGHT)
    return mainwin
    
appointment_fields = ('Date', 'Time', 'Type', 'Location')

def addAppointment():
    global appoint_entries
    window = Tk()
    window.title('Add Appointment')
    form = Frame(window)
    form.pack()
    appoint_entries = {}
    for (ix, label) in enumerate(appointment_fields):
        lab = Label(form, text=label)
        ent = Entry(form)
        lab.grid(row=ix, column=0)
        ent.grid(row=ix, column=1)
        appoint_entries[label] = ent
    Button(window, text='Save', command=save_appoint).pack(side=LEFT)
    Button(window, text='Add Assignments', command=addAssignment).pack(side=LEFT)
    Button(window, text='Close', command=sys.exit).pack(side=RIGHT)
    return window

assignment_fields = ('Date', 'Description')

def addAssignment():
    global assign_entries
    window = Tk()
    window.title('Add Assignment')
    form = Frame(window)
    form.pack()
    assign_entries = {}
    for (ix, label) in enumerate(assignment_fields):
        lab = Label(form, text=label)
        ent = Entry(form)
        lab.grid(row=ix, column=0)
        ent.grid(row=ix, column=1)
        assign_entries[label] = ent
    Button(window, text='Save', command=save_assign).pack(side=LEFT)
    Button(window, text='Add Appointments', command=addAppointment).pack(side=LEFT)
    Button(window, text='Close', command=sys.exit).pack(side=RIGHT)
    return window

def save_appoint():
    appt_type = appoint_entries['Type'].get()
    time = appoint_entries['Time'].get()
    date = appoint_entries['Date'].get()
    location = appoint_entries['Location'].get()
    current_appointment = reminder_setup.appointment(appt_type, date, time, location)
    reminder_setup.save_appointment(current_appointment)
def save_assign():
    description = assign_entries['Description'].get()
    date = assign_entries['Date'].get()
    current_assignment = reminder_setup.assignment(description, date)
    reminder_setup.save_assignment(current_assignment)

if __name__ == '__main__':
    today = datetime.date.today()
    my_day = today.strftime('%m%d%Y')
    my_date_tuple = (int(my_day[:2]), int(my_day[2:4]), int(my_day[4:6]))
    clearOld(my_date_tuple)
    #list of all upcoming assignment lists

    upcoming_assignments = []

    for date in dates:
        try:
            upcoming_assignments.append(reminder_setup.get_assignment(str(date)))
        except KeyError:
            pass
            print "keyerror appending"
    print upcoming_assignments

    upcoming_appointments = []
    for date in dates:
        try:
            upcoming_appointments.append(reminder_setup.get_appointment(str(date)))
            print "you have appointments"
            print date
        except KeyError:
            print "keyerror apptment"
    for lists in upcoming_assignments:
        try:
            for asgnment in lists:
                show_upcoming_assignment(asgnment)
                print(repr(asgnment))
        except:
            pass

    for lists in upcoming_appointments:
        try:
            for aptment in lists:
                show_upcoming_appointments(aptment)
        except:
            pass
    additional = anything_else()
    additional.mainloop()





# things to do:
# 1. in line 88, fix NoneType object thing
# 2. in general, fix execution order (i.e. if __name__ = '__main__' to execute
# the script
# 3. fix date entry to save by user (convert all tuples to string as key)
# 4. AM vs. PM
