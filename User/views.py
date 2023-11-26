#view.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Server, Like, Tag
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer, ServerSerializer, CreateServerSerializer, PutServerSerializer, LikeSerializer, CreateLikeSerializer, TagSerializer, CreateTagSerializer, RegisterSerializer, MyTokenObtainPairSerializer
from rest_framework import status
from django.http import Http404, HttpResponseServerError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics

import json

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([])
    serializer_class = RegisterSerializer
class UserListAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        queryset = User.objects.all()
        print(queryset)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # def post(self, request):
    #     # request.data는 사용자의 입력 데이터
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid(): #유효성 검사
    #         serializer.save() # 저장
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ServerListAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        queryset=Server.objects.all()
        server_serializer=ServerSerializer(queryset,many=True)
        for server in server_serializer.data:
            # print(f"server_id: {server['server_id']}")
            likes=Like.objects.filter(server_id=server['server_id'])
            like_serializer = LikeSerializer(likes, many=True).data
            server['like'] = []
            for like in like_serializer:
                # print(f"like information: {like}")
                server['like'].append(like)

            tags=Tag.objects.filter(server_id=server['server_id'])
            tag_serializer = TagSerializer(tags, many=True).data
            server['tag'] = []
            for tag in tag_serializer:
                # print(f"tag information: {tag}")
                server['tag'].append(tag)
        
        return Response(server_serializer.data)
    
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = CreateServerSerializer(data=request.data)

        if serializer.is_valid(): #유효성 검사
            serializer.validated_data['user_id'] = request.user # user 추가
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServerDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_object(self, pk):
        try:
            return Server.objects.get(pk=pk)
        except Server.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        server = self.get_object(pk)
        serializer = ServerSerializer(server)
        object_serializer_data = serializer.data

        object_serializer_data['user_liked'] = 'n'
        likes=Like.objects.filter(server_id=pk)
        like_serializer = LikeSerializer(likes, many=True).data
        object_serializer_data['like'] = []
        for like in like_serializer:
            if(request.user.id == like['user_id']):
                object_serializer_data['user_liked'] = 'y'
            object_serializer_data['like'].append(like)

        tags=Tag.objects.filter(server_id=pk)
        tag_serializer = TagSerializer(tags, many=True).data
        object_serializer_data['tag'] = []
        for tag in tag_serializer:
            object_serializer_data['tag'].append(tag)

        if(request.user.id == object_serializer_data['user_id']):
            object_serializer_data['is_owner'] = 'y'
        else:
            object_serializer_data['is_owner'] = 'n'

        return Response(object_serializer_data)

    def put(self, request, pk, format=None):
        server = self.get_object(pk)
        serializer = PutServerSerializer(server, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user_id'] = request.user # user 추가
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        server = self.get_object(pk)
        server.delete()  
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagListAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        queryset = Tag.objects.all()
        print(queryset)
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = CreateTagSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.validated_data["user_id"] = request.user
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    # def get_object(self, pk):
    #     try:
    #         return Tag.objects.get(pk=pk)
    #     except Tag.DoesNotExist:
    #         raise Http404
    
    def get(self, request, server_id, format=None):
        tag = Tag.objects.filter(server_id=server_id)
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     tag = self.get_object(pk)
    #     serializer = TagSerializer(tag, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, server_id, format=None):
        tag_name = request.data["tag_name"]
        tag = Tag.objects.filter(server_id=server_id, tag_name=tag_name)
        if len(tag) != 0: #존재하지 않음
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class LikeListAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        queryset = Like.objects.all()
        print(queryset)
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = CreateLikeSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.validated_data['user_id'] = request.user
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = request.user
        server_id = request.data['server_id']
        like = Like.objects.filter(user_id=user_id, server_id=server_id)
        # like = Like.objects.get(data=request.data)
        if len(like) != 0:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
class LikeDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_object(self, pk):
        try:
            return Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            raise Http404
    
    # pk의 like 리스트를 넘겨줌
    def get(self, request, pk, format=None):
        like = Like.objects.filter(server_id=pk)
        serializer = LikeSerializer(like, many=True)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     like = self.get_object(pk)
    #     serializer = LikeSerializer(like, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServerSearchAPI(APIView):
    def get_object(self,pk):
        try:
            object = Server.objects.get(pk=pk)
            object_serializer = ServerSerializer(object)
            object_serializer_data = object_serializer.data
            # print(object_serializer.data)
            # print(type(object_serializer.data))
            likes=Like.objects.filter(server_id=pk)
            like_serializer = LikeSerializer(likes, many=True).data
            object_serializer_data['like'] = []
            for like in like_serializer:
                # print(f"like information: {like}")
                object_serializer_data['like'].append(like)

            tags=Tag.objects.filter(server_id=pk)
            tag_serializer = TagSerializer(tags, many=True).data
            object_serializer_data['tag'] = []
            for tag in tag_serializer:
                # print(f"tag information: {tag}")
                object_serializer_data['tag'].append(tag)
            # print(object_serializer_data)
            return object_serializer_data
        except Server.DoesNotExist:
            raise Http404
    
    def get(self, request, search_keyword, format=None):
        '''
        1. server_name에 search_keyword가 포함된 경우 server_id_map에 server_id 추가.
        2. tag_namep에 search_keyword가 포함된 경우 server_id_map에 server_id 추가.
        3. server_id_map은 중복 불가이기 때문에 자동 중복 제거
        4. server_id_map의 element인 각 server_id에 대해 server, tag, like 정보를 수집해 result에 append.
        5. result return.
        '''
        try:
            server_id_map = set()
            
            server_queryset = Server.objects.filter(server_name__contains=search_keyword)
            server_serializer = ServerSerializer(server_queryset, many=True)
            for server in server_serializer.data:
                # print(f"server id: {server['server_id']}, server name: {server['server_name']}") # type : 'int'
                server_id_map.add(server['server_id'])
            
            tag_queryset = Tag.objects.filter(tag_name__contains=search_keyword)
            tag_serializer = TagSerializer(tag_queryset, many=True)
            for tag in tag_serializer.data:
                # print(f"server id: {tag['server_id']}, tag name: {tag['tag_name']}") # type : 'int'
                server_id_map.add(tag['server_id'])

            print(server_id_map)

            result = []
            for server_id in server_id_map:
                server_info = ServerSearchAPI.get_object(self, pk=server_id)
                result.append(server_info)

            return Response(result)
        except:
            raise HttpResponseServerError
        

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer