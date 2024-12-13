from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .decorators import InitBookMarkSessionDeco
from .filters import OrderingFilter, SearchFilter
from .forms import BookMarkForm
from .models import GradeInfo
from .permissions import ReadOnly
from .serializers import GradeInfoSerializer


class GradeInfoList(generics.ListCreateAPIView):

    queryset = GradeInfo.objects.all()
    serializer_class = GradeInfoSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAdminUser | ReadOnly]
    search_fields = [
        'subject', 'lecture', 'group', 'teacher', 'year', 'semester',
        'faculty',
    ]
    ordering_fields = [
        'f', 'failure', 'a_band', 'gpa', 'year', 'semester',
    ]
    ordering = ['-year', '-semester']


class GradeInfoDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = GradeInfo.objects.all()
    serializer_class = GradeInfoSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class BookMarkList(APIView):

    ordering_fields = [
        'f', 'failure', 'a_band', 'gpa', 'year', 'semester',
    ]
    ordering = ['-year', '-semester']

    @InitBookMarkSessionDeco
    def get(self, request, format=None):
        bookMarkIDs = request.session['bookMarkIDs']
        gradeInfoList = GradeInfo.objects.filter(pk__in=bookMarkIDs)
        gradeInfoList = OrderingFilter().filter_queryset(request, gradeInfoList, self)
        serializer = GradeInfoSerializer(gradeInfoList, many=True)
        return Response(serializer.data)

    @InitBookMarkSessionDeco
    def post(self, request, format=None):

        form = BookMarkForm(request.data)

        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        bookMarkID = form.cleaned_data['bookMarkID']
        bookMarkIDs = request.session['bookMarkIDs']

        if bookMarkID in bookMarkIDs:
            error = {
                'detail': 'このbookMarkIDは既に登録されています。'
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        request.session['bookMarkIDs'].append(bookMarkID)
        # sessionの変更を伝える
        request.session.modified = True
        context = {
            'bookMarkIDs': request.session['bookMarkIDs'],
        }
        return Response(context, status=status.HTTP_201_CREATED)

    # bookmark dataを全て削除
    @InitBookMarkSessionDeco
    def delete(self, request, format=None):
        request.session['bookMarkIDs'] = []
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookMarkDetail(APIView):

    @InitBookMarkSessionDeco
    def delete(self, request, pk, format=None):
        try:
            request.session['bookMarkIDs'].remove(pk)
            # sessionの変更を伝える
            request.session.modified = True
        except ValueError:
            raise Http404

        return Response(status=status.HTTP_204_NO_CONTENT)
