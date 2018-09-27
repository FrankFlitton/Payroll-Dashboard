from django.contrib import admin
from .models import Employee, JobGroup, TimeReport, TimeSheet


# Register your models here.
class JobGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'compensation', )
    list_filter = ('id', 'compensation', )
    ordering = ('id', )
    search_field = ('id', 'compensation', )

class TimeReportAdmin(admin.ModelAdmin):
    list_display = ('id', )
    list_filter = ('id', )
    ordering = ('id', )
    search_field = ('id', )

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_id', )
    list_filter = ('id', 'employee_id', )
    ordering = ('id', )
    search_field = ('id', 'employee_id', )

class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'pay_date', 'hours_worked', 'job_group', 'employee', 'report', )
    list_filter = ('id', 'pay_date', 'hours_worked', 'job_group', 'employee', 'report', )
    ordering = ('pay_date', )
    search_field = ('id', 'pay_date', 'hours_worked', 'job_group', 'employee', 'report', )

admin.site.register(JobGroup, JobGroupAdmin)
admin.site.register(TimeReport, TimeReportAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(TimeSheet, TimeSheetAdmin)