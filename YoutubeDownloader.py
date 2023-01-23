from pytube import YouTube

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("Ocorreu um erro")
    print("Download completo")


link = input("Entre com a url do vídeo a ser baixado: ")
Download(link)