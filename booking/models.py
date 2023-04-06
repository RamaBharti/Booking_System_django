from django.db import models

# Create your models here.
#we are creating a model named Appointment

from datetime import datetime
from django.contrib.auth.models import User

SELECT_PROFESSOR = (
    ("Biplab Basak", "Biplab Basak"),
    ("Niladri Chatterjee", "Niladri Chatterjee"),
    ("Aparajita Dasgupta", "Aparajita Dasgupta"),
    ("Minati De", "Minati De"),
    ("S. Dharmaraja", "S. Dharmaraja"),
    ("Debdip Ganguly", "Debdip Ganguly"),
    ("Surjeet Kaur", "Surjeet Kaur"),
    ("Harish Kumar", "Harish Kumar"),
    ("N. Shravan Kumar", "N. Shravan Kumar"),
    ("V.V.K. Srinivas Kumar", "V.V.K. Srinivas Kumar"),
    ("Ananta Kumar Majee", "Ananta Kumar Majee"),
    ("Aparna Mehra", "Aparna Mehra"),
    ("Mani Mehra", "Mani Mehra"),
    ("Vivek Mukundan", "Vivek Mukundan"),
    ("Anima Nagar", "Anima Nagar"),
    ("B.S. Panda", "B.S. Panda"),
    ("Shiv Prakash Patel", "Shiv Prakash Patel"),
    ("Kamana Porwal", "Kamana Porwal"),
    ("Amit Priyadarshi", "Amit Priyadarshi"),
    ("Ashutosh Rai", "Ashutosh Rai"),
    ("S.C.S. Rao", "S.C.S. Rao"),
    ("Biswajyoti Saha", "Biswajyoti Saha"),
    ("Ekata Saha", "Ekata Saha"),
    ("Sivananthan Sampath", "Sivanathan Sampath"),
    ("Ritumoni Sarma", "Ritumoni Sarma"),
    ("Punit Sharma", "Punit Sharma"),
    ("Rajendra Kumar Sharma", "Rajendra Kumar Sharma"),
    ("Vikas Vikram Singh", "Vikas Vikram Singh"),
    ("K. Sreenadh", "K. Sreenadh"),
    ("Amitabha Tripathi", "Amitabha Tripathi"),
    ("Viswanathan Puthan Veedu", "Viswanathan Puthan Veedu"),
)

TIME_CHOICES = (
    ("10 AM", "10 AM"),
    ("10:30 AM", "10:30 AM"),
    ("11 AM", "11 AM"),
    ("11:30 AM", "11:30 AM"),
    ("12 NOON", "12 NOON"),
    ("12:30 PM", "12:30 PM"),
    ("1 PM", "1 PM"),
    ("1:30 PM", "1:30 PM"),
    ("2 PM", "2 PM"),
    ("2:30 PM", "2:30 PM"),
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)

class Appointment(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    professors = models.CharField(max_length=50, choices=SELECT_PROFESSOR, default="Aparna Mehra") #Aparna Mehra is the HOD
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="10 AM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    approved=models.BooleanField('Approved', default=False)

    def __str__(self):
            return f"{self.user.username} | day: {self.day} | time: {self.time}"
    
    