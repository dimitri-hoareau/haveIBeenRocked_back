import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Password
from .serializers import PasswordCheckSerializer

class PasswordCheckView(APIView):
    def post(self, request):
        serializer = PasswordCheckSerializer(data=request.data)
        
        if serializer.is_valid(): 
            password = serializer.validated_data['password'] 
            hash_value = hashlib.sha1(password.encode('utf-8')).hexdigest()

            is_compromised = Password.objects.filter(hash=hash_value).exists()

            recommendations = []
            if len(password) < 8:
                recommendations.append("Le mot de passe doit comporter au moins 8 caractères.")
            if not any(char.isdigit() for char in password):
                recommendations.append("Le mot de passe doit contenir des chiffres.")
            if not any(char.islower() for char in password):
                recommendations.append("Le mot de passe doit contenir des lettres minuscules.")
            if not any(char.isupper() for char in password):
                recommendations.append("Le mot de passe doit contenir des lettres majuscules.")
            if not any(char in "!@#$%^&*()-_+=<>?/.,:;" for char in password):
                recommendations.append("Le mot de passe doit contenir des caractères spéciaux.")

            return Response({
                "compromised": is_compromised,
                "recommendations": recommendations,
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
