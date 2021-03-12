from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing our APIView"""
    #you define the serializer and then you specify the fields that you want to
    #accept in your serializer input
    name = serializers.CharField(max_length=10)
