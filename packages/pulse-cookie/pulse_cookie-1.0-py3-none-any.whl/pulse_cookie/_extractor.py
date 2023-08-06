import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PyQt6.QtNetwork import QNetworkCookie


class CookieExtractor(QMainWindow):
    def __init__(self, *, url: str, cookie_name: str):
        super().__init__()

        self.cookie = None

        self._webview = QWebEngineView()
        self._cookie_name = cookie_name

        profile = QWebEngineProfile(parent=self._webview)
        cookie_store = profile.cookieStore()
        cookie_store.cookieAdded.connect(self.on_cookie_added)

        self._page = QWebEnginePage(profile, self._webview)
        self._webview.setPage(self._page)
        self._webview.load(QUrl(url))
        self.setCentralWidget(self._webview)

    def on_cookie_added(self, cookie) -> None:
        c = QNetworkCookie(cookie)
        if bytearray(c.name()).decode() == self._cookie_name:
            self.cookie = bytearray(c.value()).decode()
            self.close()


def extract_cookie(*, url: str, cookie_name: str) -> str:
    app = QApplication(sys.argv)
    window = CookieExtractor(url=url, cookie_name=cookie_name)
    window.show()
    app.exec()
    return window.cookie
