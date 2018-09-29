from django.db import models

# Models to support the provided

class Employee(models.Model):
    id = models.CharField(max_length=64, blank=False, unique=True, primary_key=True) # Assuming any user entered string

class JobGroup(models.Model):
    id = models.CharField(max_length=128, blank=False, unique=True, primary_key=True) # Assuming any user entered string
    compensation = models.DecimalField(max_digits=12, decimal_places=2, blank=False) # Monetary values, save max value of 9,999,999,999.99

class TimeReport(models.Model):
    id = models.CharField(max_length=128, blank=False, unique=True, primary_key=True) # Assuming any user entered string

class TimeSheet(models.Model):
    id = models.BigAutoField(primary_key=True) # internal ID, all time sheets are unique
    pay_date = models.DateTimeField(blank=False) # date field
    pay_period = models.CharField(max_length=64, blank=True, null=True) # generated on csv POST. Stored as plain text.
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    job_group = models.ForeignKey(JobGroup, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    report = models.ForeignKey(TimeReport, on_delete=models.PROTECT, null=True)

# Django needed this to allow for file upload
# Data not used in application
# Could be useful to retain down the road
class PayrollFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
