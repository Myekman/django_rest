from rest_framework import serializers
from .models import Profile


class ProfileSerializers(serializers.ModelSerializer):
    # this line takes away owner for showing (readonly)
    owner = serializers.ReadOnlyField(source='owner.username')
    

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image'
        ]