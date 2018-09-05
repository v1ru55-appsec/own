import design, sys
from PyQt5 import QtWidgets, QtCore
import urllib
import http.cookiejar
import json


class GUI(QtWidgets.QMainWindow, design.Ui_MainWindow):
    flag1 = False
    flag3 = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_url)
        self.pushButton_2.clicked.connect(self.browse_folder)
        self.pushButton_3.clicked.connect(self.download)
        self.pushButton_4.clicked.connect(self.stop)

    def browse_folder(self):
        self.lineEdit_2.clear()
        if 'https://www.twitch.tv/videos/' in self.url:
            TwitchGrabler.filename = \
            QtWidgets.QFileDialog.getSaveFileName(self, "Выберите папку", "stream", "Video Files (*.ts)")[0]
        else:
            TwitchGrabler.filename = \
            QtWidgets.QFileDialog.getSaveFileName(self, "Выберите папку", "clip", "Video Files (*.mp4)")[0]
        self.flag1 = True
        self.lineEdit_2.setText(TwitchGrabler.filename)

    def get_url(self):
        self.default()
        self.url = self.lineEdit.text()
        if 'www.twitch.tv/videos/' not in self.url and 'clips.twitch.tv/' not in self.url:
            QtWidgets.QMessageBox.about(self, "Внимание", "Неверный формат ссылки, проверьте правильность ссылки")
            return
        TwitchGrabler.video_id = self.url.rsplit('/', 1)[1]
        TwitchGrabler.info(TwitchGrabler, self.url)
        self.comboBox.addItems(TwitchGrabler.resolutions)
        TwitchGrabler.resolution = TwitchGrabler.resolutions[0]
        self.comboBox.activated[str].connect(self.is_res_choose)

    def is_res_choose(self, text):
        TwitchGrabler.resolution = text

    def download(self):
        if self.flag1:
            self.tw = TwitchGrabler()
            self.tw.pbar_signal.connect(self.pbar_change)
            self.tw.start()
        else:
            QtWidgets.QMessageBox.about(self, "Внимание", "Выберите место сохранения стрима!")

    def pbar_change(self, val):
        self.progress.setValue(val)

    def stop(self):
        if self.flag1:
            QtWidgets.QMessageBox.about(self, "Внимание", "Загрузка останавливается...")
            GUI.flag3 = True
        else:
            QtWidgets.QMessageBox.about(self, "Внимание", "Выберите место сохранения стрима!")

    def default(self):
        self.flag3 = False
        self.flag1 = False
        self.lineEdit_2.setText("Выберете место сохранения")
        self.comboBox.clear()
        self.progress.setValue(0)


class TwitchGrabler(QtCore.QThread):
    pbar_signal = QtCore.pyqtSignal(int)
    video_id = ''
    nauth = ''
    resolution = ''
    filename = ''

    def __init__(self):
        super().__init__()

    def auth(self, url):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        r = opener.open(url)
        for i in cj:
            cookie = i.value

        get_nauth = 'https://api.twitch.tv/api/vods/' + self.video_id + '/access_token?adblock=true&need_https=true&oauth_token&platform=web&player_backend=mediaplayer&player_type=site'
        info = urllib.request.Request(get_nauth, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Cookie': 'unique_id=' + cookie, 'client-id': 'jzkbprff40iqj646a697cyrvl0zt2m6'}, method="GET")
        self.nauth = urllib.request.urlopen(info).read().decode("utf-8").replace('{"token":"', 'nauth=').replace(
            '","sig":"',
            '&nauthsig=').replace(
            '\\', '')[:-2]

    def info(self, url):
        if 'https://clips.twitch.tv/' in url:
            get_info = 'https://clips.twitch.tv/api/v2/clips/' + self.video_id + '/status'
            info = urllib.request.Request(get_info, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
                'client-id': 'jzkbprff40iqj646a697cyrvl0zt2m6'}, method="GET")
            resp = urllib.request.urlopen(info).read().decode("utf-8")
            resp = resp[38: -1]
            resp = json.JSONDecoder().decode(resp)
            self.resolutions = []
            self.video_link = dict()
            for el in resp:
                self.resolutions.append(el['quality'])
                self.video_link[el['quality']] = el['source']
        else:
            get_info = 'https://api.twitch.tv/kraken/videos/v' + self.video_id
            info = urllib.request.Request(get_info, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
                'client-id': 'jzkbprff40iqj646a697cyrvl0zt2m6'}, method="GET")
            resp = urllib.request.urlopen(info).read().decode("utf-8")
            q = resp.index("\"resolutions\":{")
            self.resolutions = list(resp[q + 15: resp.index('}', q)].replace('"', '').split(','))
            for i in range(len(self.resolutions)):
                self.resolutions[i] = self.resolutions[i][:self.resolutions[i].index(':')]

    def run(self):
        self.download()
        GUI.flag3 = False
        GUI.flag1 = False

    def download(self):
        if self.video_id.isdigit():
            self.auth('https://www.twitch.tv/videos/' + self.video_id)
            get_video = 'https://usher.ttvnw.net/vod/' + self.video_id + '.m3u8?allow_source=true&' + self.nauth
            video = urllib.request.Request(get_video, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}, method="GET")
            resp = urllib.request.urlopen(video).read().decode("utf-8")

            video_link = resp[resp.index('https:'):resp.index('.m3u8') + 5]

            m3u = urllib.request.Request(video_link, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}, method="GET")
            resp = urllib.request.urlopen(m3u).read().decode("utf-8")

            pieces = list(resp.split('\n'))
            l = len(pieces)
            i = 0
            while i < l:
                if '#' in pieces[i]:
                    pieces.pop(i)
                    i -= 1
                    l -= 1
                i += 1

            # построение ссылки для скачивания
            video_link = video_link[:video_link.rindex('chunked')] + self.resolution + '/'

            # скачивание стрима
            l = len(pieces) - 1
            f = open(self.filename + '.ts', mode='wb')
            for i in range(l):
                if GUI.flag3:
                    break
                download = urllib.request.Request(video_link + pieces[i], headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'},
                                                  method="GET")
                resp = urllib.request.urlopen(download).read()
                f.write(resp)
                tmp = (i + 1) * 100 // l
                self.pbar_signal.emit(tmp)
        else:
            link = self.video_link[self.resolution]
            f = open(self.filename + '.mp4', mode='wb')
            self.pbar_signal.emit(13)
            download = urllib.request.Request(link, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'},
                                              method="GET")
            resp = urllib.request.urlopen(download).read()
            self.pbar_signal.emit(67)
            f.write(resp)
            self.pbar_signal.emit(100)
        f.close()
        QtWidgets.QMessageBox.about(GUI(), "Ура!", "Стрим успешно сохранен!")
        GUI.default(GUI())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
