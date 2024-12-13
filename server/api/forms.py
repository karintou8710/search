from django import forms


class BookMarkForm(forms.Form):
    """bookmarkIDのバリデーションをする
    """
    bookMarkID = forms.IntegerField()
