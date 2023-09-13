# from django.http import Http404
# from rest_framework import status, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Post
# from .serializer import PostSerializer
from django.db.models import Count
from rest_framework import generics, permissions, filters
from .models import Post
from django_drf_api.permissions import IsOwnerOrReadOnly
from .serializer import PostSerializer

# -----------------------------------------------------------------views without generics
# class PostList(APIView):
#     # the import permission and code below is so that the form is only there when logedin
#     serializer_class = PostSerializer
#     permission_classes = [
#         permissions.IsAuthenticatedOrReadOnly
#     ]

#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(
#             posts, many=True, context = {'request': request}
#         )
#         return Response(serializer.data)

#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(
#             posts, many=True, context={'request': request}
#         )
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(
#             data=request.data, context={'request': request}
#         )
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(
#                 serializer.data, status=status.HTTP_201_CREATED
#             )
#         return Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST
#         )


# class PostDetail(APIView):
#     permissions_classes = [IsOwnerOrReadOnly]
#     serializer_class = PostSerializer

#     def get_object(self,pk):
#         try:
#             post = Post.objects.get(pk=pk)
#             self.check_object_permissions(self.request, post)
#             return post 
#         except Post.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#             post = self.get_object(pk)
#             serializer = PostSerializer(
#                 post, context={'request': request}
#             )
#             return Response(serializer.data)

# # update a post that you own in http : posts/id
#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(
#             post, data=request.data, context={'request': request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST
#         )

# # delete post
#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )

#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT)

class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True), 
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter
        ]
    ordering_fields = [
        'likes_count', 
        'comments_count',
        'likes__created_at',
    ]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
     serializer_class = PostSerializer
     permission_classes = [IsOwnerOrReadOnly]
     queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')