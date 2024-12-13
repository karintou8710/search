def InitBookMarkSessionDeco(callback):
    """BookMarkViewでsessionのbookmarkを初期化する

    ・セッションの初期化
    ・型チェック
    """
    def isValidTypeOfBookmrkIDs(bookMarkIDs):
        return isinstance(bookMarkIDs, list) and all(isinstance(d, int) for d in bookMarkIDs)

    def wrapper(self, request, *args, **kwargs):

        if request.session.get('bookMarkIDs'):
            bookMarkIDs = request.session['bookMarkIDs']
        else:
            bookMarkIDs = []
            request.session['bookMarkIDs'] = bookMarkIDs

        # sessionデータの型チェック(list[int])
        if not isValidTypeOfBookmrkIDs(bookMarkIDs):
            request.session['bookMarkIDs'] = []  # 不正なデータを消去
        return callback(self, request, *args, **kwargs)

    return wrapper
