# from django.http import Http404
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import generics, filters
from .models import Profile 
from .serializers import ProfileSerializers
from django_drf_api.permissions import IsOwnerOrReadOnly

# -----------------------------------------------------------------views without generics
# class ProfileList(APIView):
    
#     def get(self, request):
#         # takes the model profile and get all
#         profiles = Profile.objects.all()

#         # specify serializer to be used
#         serializer = ProfileSerializers(
#             profiles, many=True, context={'request': request}
#             )
#         return Response(serializer.data)

# class ProfileDetail(APIView):
#     # this takes the profileserializer and make it a form, try remove this line to check
#     serializer_class = ProfileSerializers
#     # is ownerreadonly is living in permissions.py
#     permission_classes = [IsOwnerOrReadOnly]

# # return profile with id, and http404 error if id dont exist

#     def get_object(self, pk):
#         try:
#             profile = Profile.objects.get(pk=pk)
#             return profile
#         except Profile.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk):
#         profile = self.get_object(pk)
#         self.check_object_permissions(self.request, profile)
#         serializer = ProfileSerializers(
#             profile, context={'request': request}
#         )
#         return Response(serializer.data)

#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializers(
#             profile, data=request.data, context={'request': request}
#             )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#------------------------------------------------------------------------simplyfy the views with generic views
# Adding extra fields to Posts and Profiles part 2

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializers
    
    #----------------------------------------------------------------------the filter button
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering__fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializers