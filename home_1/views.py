from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status 
from .models import users_collection, test_collection
from . import models
from . import serializer
from django.http import HttpResponse
from bson import ObjectId

# User Views
class getUsers(APIView):
   def get(self, request):
        try:
            user_data_list = list(users_collection.find({}))
            for user_data in user_data_list:
                user_data['_id'] = str(user_data['_id'])  # Convert ObjectId to string

            return Response(user_data_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class createUsers(APIView):
    def post(self, request):
        user_data = request.data
        user_regNo = request.regNo
        user_userId =request.userId

        if all(key in user_data for key in ['name', 'email', 'password', 'userId', 'isStudent', 'department', 'regNo']):
            try:
                existing_user = users_collection.find_one({"$or" : [{"regNo" : user_regNo}, {"userId": user_userId}]})
                if existing_user:
                    return Response({'message' :'User ID and Register Number already taken'}, status= status.HTTP_400_BAD_REQUEST)
                else:
                    result = users_collection.insert_one(user_data)
                    if result.acknowledged:
                        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'error': 'User creation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Incomplete or invalid user data'}, status=status.HTTP_400_BAD_REQUEST)

class EditUser(APIView):
    def put(self, request, user_id):
        try:
            user_id_str = str(user_id)
            _id = request.data.pop('_id', None)
            users_collection.update_one({'_id': ObjectId(user_id_str)}, {'$set': request.data})

            return Response({'message': 'User data updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteUser(APIView):
    def delete(self, request, user_id):
        try:
            user_id_str = str(user_id)
            result = users_collection.delete_one({'_id': ObjectId(user_id_str)})

            if result.deleted_count > 0:
                return Response({'message': 'User data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Test views
class createTest(APIView):
    def post(self, request):
        test_data = request.data
        if all(key in test_data for key in ['testName', 'subject', 'test', 'userId', 'isStudent', 'createdBy', 'answeredBy', 'regNo', 'score', 'reviewedBy']):
            try:
                result = test_collection.insert_one(test_data)
                if result.acknowledged:
                    return Response({'message': 'Test created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Test creation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Incomplete or invalid test data'}, status=status.HTTP_400_BAD_REQUEST)
        
class getTests(APIView):
   def get(self, request):
        try:
            test_data_list = list(test_collection.find({}))
            for test_data in test_data_list:
                test_data['_id'] = str(test_data['_id'])  # Convert ObjectId to string

            return Response(test_data_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class EditTest(APIView):
    def put(self, request, test_id):
        try:
            test_id_str = str(test_id)
            _id = request.data.pop('_id', None)
            test_collection.update_one({'_id': ObjectId(test_id_str)}, {'$set': request.data})

            return Response({'message': 'Test data updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteTest(APIView):
    def delete(self, request, test_id):
        try:
            test_id_str = str(test_id)
            result = test_collection.delete_one({'_id': ObjectId(test_id_str)})
            print(result.deleted_count)
            if result.deleted_count > 0:
                return Response({'message': 'Test deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class getStudentSummary(APIView):
#     def post(self, request, regNo):
#         try:
#             user_regNo = regNo
#             test_data = list(test_collection.find({"regNo": user_regNo}))
#             # print(test_data)
#             if not test_data:
#                 return Response({'error': 'No user found for the given Register number'})
#             else:
#                 overall_score = 0
#                 score_data=[]
#                 completed_test = []
#                 uncompleted_test=[]
#                 for user in test_data:
#                     if "score" in user and user['score']:
#                         score_data.extend(user.get('score', []))
#                         overall_score +=sum(user.score)
#                     if "answeredBy" in user and user['answeredBy']:
#                         completed_test.append(user)
#                     else:
#                         uncompleted_test.append(user)
#                 print(overall_score)
#             avg_score = overall_score / len(test_data)
#             response_data ={
#                 "test_attended" : test_data,
#                 "scores" : score_data,
#                 "overall_score" : overall_score,
#                 "overall_test_attended" : len(test_data),
#                 "avg_score"  : avg_score,
#                 "completed_tests" : completed_test,
#                 "uncompleted_test": uncompleted_test
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


            
