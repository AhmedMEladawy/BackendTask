
from datetime import datetime, timezone
from rest_framework import serializers
from .models import User, Company, Department, Employee

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'number_of_departments', 'number_of_employees']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'company', 'name', 'number_of_employees']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'company', 'department', 'status', 'name', 'email', 'mobile_number', 'address', 'designation', 'hired_on', 'days_employed']
        read_only_fields = ['days_employed']

    def validate(self, data):
        status = data.get('status', self.instance.status if self.instance else 'onboarding')
        hired_on = data.get('hired_on', self.instance.hired_on if self.instance else None)
        days_employed = data.get('days_employed', self.instance.days_employed if self.instance else None)

        print(f"Validation - Status: {status}, Hired On: {hired_on}, Days Employed: {days_employed}")

        if status == 'active':
            if not hired_on:
                raise serializers.ValidationError({'hired_on': 'This field is required when status is active.'})
            if days_employed is None:
                data['days_employed'] = (datetime.utcnow().date() - hired_on).days
        elif status in ['onboarding', 'inactive']:
            data['hired_on'] = None
            data['days_employed'] = None

        print(f"Validation After Adjustment - Status: {status}, Hired On: {data.get('hired_on')}, Days Employed: {data.get('days_employed')}")
        return data

    def update(self, instance, validated_data):
        instance.company = validated_data.get('company', instance.company)
        instance.department = validated_data.get('department', instance.department)
        instance.status = validated_data.get('status', instance.status)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.address = validated_data.get('address', instance.address)
        instance.designation = validated_data.get('designation', instance.designation)

        status = validated_data.get('status', instance.status)
        hired_on = validated_data.get('hired_on', instance.hired_on)

        print(f"Update - Status: {status}, Hired On: {hired_on}")

        if status == 'active' and hired_on:
            instance.hired_on = hired_on
            instance.days_employed = (datetime.utcnow().date() - hired_on).days
        else:
            instance.hired_on = None
            instance.days_employed = None

        print(f"Update After Adjustment - Status: {status}, Hired On: {instance.hired_on}, Days Employed: {instance.days_employed}")

        instance.save()
        return instance

    def create(self, validated_data):
        status = validated_data.get('status', 'onboarding')
        hired_on = validated_data.get('hired_on', None)

        print(f"Create - Status: {status}, Hired On: {hired_on}")

        if status == 'active' and hired_on:
            validated_data['days_employed'] = (datetime.utcnow().date() - hired_on).days
        else:
            validated_data['hired_on'] = None
            validated_data['days_employed'] = None

        print(f"Create After Adjustment - Status: {status}, Hired On: {validated_data.get('hired_on')}, Days Employed: {validated_data.get('days_employed')}")
        
        return super().create(validated_data)