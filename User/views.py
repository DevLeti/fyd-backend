#view.py
from django.shortcuts import render
from rest_framework.response import Response
from .models import User, Server, Like
from rest_framework.views import APIView
from .serializers import UserSerializer, ServerSerializer, LikeSerializer
from rest_framework import status
from django.http import Http404

class UserListAPI(APIView):
    def get(self, request):
        queryset = User.objects.all()
        print(queryset)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServerListAPI(APIView):
    def get(self, request):
        queryset = Server.objects.all()
        print(queryset)
        serializer = ServerSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = ServerSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServerDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return Server.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        server = self.get_object(pk)
        serializer = ServerSerializer(server)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        server = self.get_object(pk)
        serializer = ServerSerializer(server, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        server = self.get_object(pk)
        server.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class LikeListAPI(APIView):
    def get(self, request):
        queryset = Like.objects.all()
        print(queryset)
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)