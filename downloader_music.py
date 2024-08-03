import eyed3,csv,os,yt_dlp
from mutagen.id3 import APIC, ID3
class Musique:
    def __init__(self, url, artist, album, title, image):
        self.url = url
        if(url == ""):
            if(artist!="" and title!=""):
                self.url = yt_dlp.YoutubeDL().extract_info("ytsearch:"+artist+" "+title, download=False)["entries"][0]["webpage_url"]
        self.artist = artist
        self.album = album
        self.title = title
        self.image = image
        self.filename = artist+" - "+title
    def download(self):
        if(self.artist!="" and self.title!=""):
            ydl_opts = {"audio-format": "mp3", "outtmpl": self.filename, "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "0"}], "quiet": "True"}
        else:
            if(self.url==""):
                return True
            self.filename = yt_dlp.YoutubeDL().extract_info(self.url, download=False)["title"]
            ydl_opts = {"audio-format": "mp3", "outtmpl": self.filename, "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "0"}], "quiet": "True"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
            self.filename = self.filename+".mp3"
    def set_metadata(self):
        audiofile = eyed3.load(self.filename)
        if(self.artist!=""):audiofile.tag.artist = self.artist
        if(self.album!=""):audiofile.tag.album = self.album
        if(self.title!=""):audiofile.tag.title = self.title
        audiofile.tag.save()
        find = True
        if self.image!="":
            try :
                file = ID3(self.filename)
                mime='image/jpeg'
                if(self.image.endswith(".png")):
                    mime = 'image/png'
                if ":/" not in self.image:
                    self.image = "./Pochettes/"+self.image
                with open(self.image, 'rb') as albumart:
                    file.add(APIC(encoding=3,mime=mime,type=3,data=albumart.read()))
                    albumart.close()
                file.save(v2_version=3)
            except Exception as e:
                find=False
        os.replace("./"+self.filename, "./Musiques/"+self.filename)
        return find
def load(file):
    with open(file, newline='',encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        metadata = []
        for row in spamreader:
            metadata.append(row)
        return metadata[1:]
def menage():
    for i in os.listdir():
        if i.endswith(".mp3") or i.endswith(".webm") or i.endswith(".part") or i.endswith(".mp4") or i.endswith(".ytdl"):
            os.remove(i)
def main(mode,tags):
    try:
        callbackMessage = "Téléchargement(s) terminé(s)"
        if mode == "link":
            musique = Musique(tags[0], tags[1], tags[2], tags[3], tags[4])
            retour = musique.download()
            if(retour):
                callbackMessage = "Manque de données pour le téléchargement"
            else:
                find = musique.set_metadata()
                if(not find):
                    callbackMessage = "Téléchargement(s) terminé(s) - Des pochettes n'ont pas pu être trouvées"
        elif mode == "csv":
            metadatas = load(tags[0])
            for i in metadatas:
                musique = Musique(i[3], i[0], i[2], i[1], i[4])
                retour = musique.download()
                if(retour):
                    callbackMessage = "Manque de données pour le téléchargement"
                else:
                    find = musique.set_metadata()
                    if(not find):
                        callbackMessage = "Téléchargement(s) terminé(s) - Des pochettes n'ont pas pu être trouvées"
        menage()
        return callbackMessage
    except Exception as e:
        return 'Erreur de téléchargement : '+str(e)