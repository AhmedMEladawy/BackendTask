
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Company, Department, Employee
from .serializers import UserSerializer, CompanySerializer, DepartmentSerializer, EmployeeSerializer
from .permissions import IsAdminOrManager
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import get_object_or_404
from .decorators import role_required
from django.utils.decorators import method_decorator




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    @method_decorator(role_required(['admin']))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    @method_decorator(role_required(['admin']))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(role_required(['admin']))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(role_required(['admin']))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    @method_decorator(role_required(['admin', 'manager']))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(role_required(['admin', 'manager']))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(role_required(['admin', 'manager']))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Department.objects.all()
        company_id = self.request.query_params.get('company', None)
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    @method_decorator(role_required(['manager']))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(role_required(['admin', 'manager']))
    def partial_update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(role_required(['admin', 'manager']))
    def destroy(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(role_required(['admin']))
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'User created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    pass

class MyTokenRefreshView(TokenRefreshView):
    pass
