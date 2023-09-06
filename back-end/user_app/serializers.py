from rest_framework.serializers import ModelSerializer
from user_app.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'email', 'name', 'annual_salary', 'bank_balance', 'debt']
        fields = ['__all__']

