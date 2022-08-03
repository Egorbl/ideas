import profile
from rest_framework import serializers

from authentication.models import Account


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'password',
                  'password2', 'profile_image', ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        account = Account(
            id=self.validated_data['id'],
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Password must match'})

        profile_image = self.validated_data.get("profile_image")
        print(profile_image)
        if profile_image:
            account.profile_image = profile_image

        account.set_password(password)
        account.save()
        return account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = (
            'id', 'email', 'username', 'date_joined', 'last_login', 'profile_image', 'hide_email',
        )

    # def save(self):
    #     # print(self.instance)
    #     return self.instance
