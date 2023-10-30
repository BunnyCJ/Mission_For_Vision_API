from django.urls import path
from . import views

urlpatterns = [
    # users
    path('getUser/', views.getUsers.as_view()),
    path('createUser/', views.createUsers.as_view()),
    path('updateUser/<str:user_id>/', views.EditUser.as_view()),
    path('deleteUser/<str:user_id>/', views.DeleteUser.as_view()),

    # tests
    path('getTests/', views.getTests.as_view()),
    path('createTest/', views.createTest.as_view()),
    path('updateTest/<str:test_id>/', views.EditTest.as_view()),
    path('deleteTest/<str:test_id>/', views.DeleteTest.as_view()),

    # student details
    #  path('getStudentSummary/<str:regNo>/', views.getStudentSummary.as_view()),


]