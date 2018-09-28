from rest_framework import serializers

from .models import PayrollFile, TimeSheet, Employee, JobGroup, TimeReport


class TimeReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TimeReport
        fields = (
            'id',
            )


class JobGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JobGroup
        fields = (
            'id',
            'compensation',
            )


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
            )


class PayrollFileSerializer(serializers.ModelSerializer):
    class Meta():
        model = PayrollFile
        fields = ('file', 'id', 'timestamp')


class TimeSheetSerializer(serializers.HyperlinkedModelSerializer):
    job_group = JobGroupSerializer()
    employee = EmployeeSerializer()
    report = TimeReportSerializer()

    class Meta:
        model = TimeSheet
        fields = (
            'pay_date',
            'hours_worked',
            'job_group',
            'employee',
            'report'
            )
        read_only_fields = ('__all__',)
