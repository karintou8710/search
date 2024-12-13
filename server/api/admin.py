from django.contrib import admin

from .models import GradeInfo


@admin.register(GradeInfo)
class GradeInfoAdmin(admin.ModelAdmin):
    """成績データを管理画面から見れるようにする
    """
    pass
