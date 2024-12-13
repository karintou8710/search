from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('gradeinfo/', views.GradeInfoList.as_view()),
    path('gradeinfo/<int:pk>/', views.GradeInfoDetail.as_view()),
    path('bookmark/', views.BookMarkList.as_view()),
    path('bookmark/<int:pk>/', views.BookMarkDetail.as_view()),
]

# 拡張子(html, jsonなど)を指定して処理を切り替えできるようにする
urlpatterns = format_suffix_patterns(urlpatterns)
