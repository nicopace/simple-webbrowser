#!/usr/bin/python
import sys

from functools import partial
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


def _loadFinished(webview, url, alternativeurl, reply):
    print "loadfinished"
    requesturl = reply.request().url()
    if requesturl != url:
        if requesturl == alternativeurl:
            # Se supone que la url alternativa es local
            print "url alternativa cargada, reintentando con la primaria"
            QtCore.QTimer.singleShot(5000, partial(_pageTimeout, webview, url))
            print "in 5 seconds loading %s" % (url, )

        return

    error = reply.error()
    ok = error == QNetworkReply.NoError

    print "Load finished", ok
    if not ok:
        print "network error %i" % (error, )
        print "Reloading..."
        webview.load(alternativeurl)
    else:
        timeoutSeconds = 60
        QtCore.QTimer.singleShot(timeoutSeconds * 1000, partial(_pageTimeout, webview, url))
        print "in 60 seconds loading %s" % (url, )

def _pageTimeout(webview, url):
    webview.load(url)
    print "loading %s" % (url, )


def main():
    app = QtGui.QApplication(sys.argv)
    web = QtWebKit.QWebView()
    url = QtCore.QUrl(sys.argv[1])
    alternativeurl = QtCore.QUrl(sys.argv[2])

    nam = web.page().networkAccessManager()
    nam.finished.connect(partial(_loadFinished, web, url, alternativeurl))

    web.load(alternativeurl)
    web.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
