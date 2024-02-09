from djoser.serializers import UserCreateSerializer

class CustomUserCreateSerializer(UserCreateSerializer):
    
    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + ('first_name', 'last_name')
        extra_kwargs = {
            'first_name':{'required':True},
            'last_name':{'required':True},
        }
