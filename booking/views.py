from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "index.html",{})   


def booking(request):
    #calling 'validWeekday' function to loop days we want in the next 21 days
    weekdays=validWeekday(22)

    #only show the days which are not full
    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        professors = request.POST.get('professors')
        day = request.POST.get('day')
        if professors == None:
            messages.success(request, "Pease Select A Professor!")
            return redirect('booking')
        
        #store day an professors in django section
        request.session['day'] = day
        request.session['professors'] = professors

        return redirect('bookingSubmit')


    return render(request, 'booking.html', {
        'weekdays' :weekdays,
        'validateWeekdays' :validateWeekdays,
    }) 



def bookingSubmit(request):
    user = request.user
    times = [
        "10 AM", "10:30 AM", "11 AM", "11:30 AM", "12 NOON", "12:30 PM", "1 PM", "1:30 PM", "2 PM", "2:30 PM", "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    #get sorted data from django session
    day = request.session.get('day')
    professors = request.session.get('professors')

    #only show the time of the day that has not been selected before
    hour = checkTime(times, day)
    if request.method =='POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if professors != None:
            if day <= maxDate and day >=minDate:
                if date == 'Monday' or date =='Tuesday' or date =='Wednesday' or date =='Thursday' or date == 'Friday':
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1:
                            AppointmentForm = Appointment.objects.get_or_create(
                                user = user,
                                professors = professors,
                                day = day,
                                time =time,
                            )
                            messages.success(request, "Appointment Saved!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect!")
            else:
                messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Professor!")

    return render(request, 'bookingSubmit.html', {
        'times' :hour,
    })


#userPanel() function displays the user’s booked appointments and allows the user to edit his appointments.
def userPanel(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user' :user,
        'appointments' :appointments,
    })


#The userUpdate() function takes the id argument from the appointment selected to edit (update) and in addition to the booking() function it has a “delta24” variable which is to determine if the selected date is 24hrs before the day user’s in using datetime.today() function.
def userUpdate(request, id):
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    #copy  booking
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    #24h if statement in template
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    #calling 'validWeekday, function to loop days you want in the next 21 days
    weekdays = validWeekday(22)

    #only show the days that are not full
    validateWeekdays = isWeekdayValid(weekdays)


    if request.method == 'POST':
        professors = request.POST.get('professors')
        day = request.POST.get('day')

        #store day and professors in django session
        request.session['day'] = day
        request.session['professors'] = professors

        return redirect('userUpdateSubmit', id=id)
    

    return render(request, 'userUpdate.html', {
        'weekdays' :weekdays,
        'validateWeekdays' :validateWeekdays,
        'delta24' :delta24,
        'id' :id,
    })


#The userUpdateSubmit() function just like the bookingSubmit() function saves or in this case updates the appointment data. This function check’s its times slightly differently by using the checkEditTime() function instead of the checkTime() function. hese changes are so the user can pick his own selected time (the time he booked before) in case he just wants to change the service or the day of the appointment.
def userUpdateSubmit(request, id):
    user = request.user
    times = [
        "10 AM", "10:30 AM", "11 AM", "11:30 AM", "12 NOON", "12:30 PM", "1 PM", "1:30 PM", "2 PM", "2:30 PM", "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    professors = request.session.get('professors')

    #only show the time of the day that has not been selected before and the time the user is editing
    hour = checkEditTime(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    userSelectedTime = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if professors !=None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date =='Tuesday' or date =='Wednesday' or date =='Thursday' or date == 'Friday':
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            AppointmentForm = Appointment.objects.filter(pk=id).update(
                                user = user,
                                professors = professors,
                                day = day,
                                time = time,
                            )
                            messages.success(request, "Appointment Edited!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect!")
            else:
                messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Professor!")
        return redirect('userPanel')
    
    return render(request, 'userUpdateSubmit.html', {
        'times' :hour,
        'id' :id,
    })

#The adminPanel() function shows the bookings in the next 21 days in the template.
#only admin members can access the admin page.
def adminPanel(request):
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    #only show the appointments 21 days from today
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    if request.method == "POST":
        id_list = request.POST.getlist('boxes')
        
        #uncheck all
        items.update(approved=False)
        #update approval
        for x in id_list:
            Appointment.objects.filter(pk=int(x)).update(approved=True)

        messages.success(request, ("Approvals are Updated!"))
        

    return render(request, 'adminPanel.html', {
        'items' :items,
    })

#def admin_approval(request):
#   return render(request, 'bookAppointments/admin_approval.html')
#The dayToWeekday() function takes an argument “x” (day) and converts it to a string so the Django template can show it to the user.
def dayToWeekday(x):
    z = datetime.strptime(x, '%Y-%m-%d')
    y = z.strftime('%A')
    return y

#The validWeekday() function takes an argument “days” (the period we want to check the weekdays) and checks if each day in the period is Monday or Wednesday or Wednesday or Thursday or Friday, then returns a list of “weekdays” of valid days.
def validWeekday(days):
    #loop days we want in the next 21 days
    today = datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y =='Tuesday' or y =='Wednesday' or y =='Thursday' or y == 'Friday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays


def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays


#The checkTime() function takes two arguments “times” and “day” so it can check which times of that day are free to be booked by the user.
def checkTime(times, day):
    #only show the time of the day that has not been selected before
    x=[]
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x


#The checkEditTime() function is exactly like checkTime() but takes an additional argument “id” (the appointment’s id that the user is trying to edit) so the time of that appointment the user is editing would be shown to the user.
def checkEditTime(times, day, id):
    #only show the time of the day that has not been selected before
    x = []
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x
                    
