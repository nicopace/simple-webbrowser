#!/usr/bin/python
import sys

from functools import partial
from PyQt4 import QtCore, QtGui, QtWebKit


def _loadFinished(webview, url, ok):
    print "Load finished", ok
    if not ok:
        print "Reloading..."
        webview.load(url)


def main():
    app = QtGui.QApplication(sys.argv)
    web = QtWebKit.QWebView()
    url = QtCore.QUrl(sys.argv[1])

    web.loadFinished.connect(partial(_loadFinished, web, url))

    web.load(url)
    web.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
