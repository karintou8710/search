from rest_framework import serializers

from .models import GradeInfo


class GradeInfoSerializer(serializers.ModelSerializer):
    """成績データのシリアライザー。フォームのような役割をする。
    """

    class Meta:
        model = GradeInfo
        fields = '__all__'
