from django.db import models


# Models to support the spec
class Employee(models.Model):
    id = models.CharField(max_length=64, blank=False, primary_key=True)
    employee_id = models.CharField(max_length=64, blank=True)

class JobGroup(models.Model):
    id = models.CharField(max_length=128, blank=False, unique=True, primary_key=True)
    compensation = models.DecimalField(max_digits=12, decimal_places=2, blank=False)

class TimeReport(models.Model):
    id = models.CharField(max_length=128, blank=False, unique=True, primary_key=True)

class TimeSheet(models.Model):
    id = models.BigAutoField(primary_key=True)
    pay_date = models.DateTimeField(blank=False)
    pay_period = models.CharField(max_length=64, blank=True, null=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    job_group = models.ForeignKey(JobGroup, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    report = models.ForeignKey(TimeReport, on_delete=models.PROTECT, null=True)

class PayrollFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
