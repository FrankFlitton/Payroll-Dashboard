from django.db import models


class Employee(models.Model):
    # Assuming any user entered string
    id = models.CharField(max_length=64, blank=False, unique=True, primary_key=True)


class JobGroup(models.Model):
    # Assuming any user entered string
    id = models.CharField(max_length=128, blank=False, unique=True, primary_key=True)
    # Monetary values, save max value of 99,999,999.99
    compensation = models.DecimalField(max_digits=8, decimal_places=2, blank=False)


class TimeReport(models.Model):
    # Assuming any user entered string
    id = models.CharField(max_length=128, blank=False, unique=True, primary_key=True)


class TimeSheet(models.Model):
    # internal ID, all time sheets are unique
    id = models.BigAutoField(primary_key=True)
    # date field
    pay_date = models.DateTimeField(blank=False)
    # generated on csv POST. Stored as plain text.
    pay_period = models.CharField(max_length=64, blank=True, null=True)
    # Decimal field to allow for 5 min resolution. 999.08333
    hours_worked = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    # ForeignKey models with delete protection
    job_group = models.ForeignKey(JobGroup, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    report = models.ForeignKey(TimeReport, on_delete=models.PROTECT, null=True)


# Django needed this to allow for file upload
# Data stored used in the application for security
# Could be useful to retain down the road
class PayrollFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
