
from rest_framework import serializers #type: ignore


from .models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    full_name = serializers.ReadOnlyField(source="user.get_full_name")
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "country",
            "city",
            "date_joined",
            "phone_number",
            "address",
        ]



# class UpdateProfileSerializer(serializers.ModelSerializer):
#     first_name = serializers.CharField(source="user.first_name")
#     last_name = serializers.CharField(source="user.last_name")
#     country_of_origin = CountryField(name_only=True)

#     class Meta:
#         model = Profile
#         fields = [
#             "first_name",
#             "last_name",
#             "gender",
#             "country_of_origin",
#             "city_of_origin",
#             "occupation",
#             "phone_number",
#         ]


# class AvatarUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ["avatar"]
