#!/usr/bin/env python
# -*- coding: latin-1 -*-
#pip3 install libtorrent google.colab
import libtorrent as lt
import time
import datetime
from google.colab import drive

drive.mount('/content/drive')

#pip3 install --upgrade pip setuptools wheel
#pip3 install lbry-libtorrent google google.colab

link = input("Cole aqui o magnet link: \n") 

ses = lt.session()
ses.listen_on(6881, 6891) 
params = {
    'save_path': '/content/drive/My Drive/Torrent/',
    'storage_mode': lt.storage_mode_t(2)}
print(link)

handle = lt.add_magnet_uri(ses, link, params)
ses.start_dht()

begin = time.time()
print(datetime.datetime.now())

print ('Baixando Metadata...')
while (not handle.has_metadata()):
    time.sleep(1)
print ('Iniciando Torrent Download...')

print("Iniciando", handle.name())

while (handle.status().state != lt.torrent_status.seeding):
    s = handle.status()
    state_str = ['fila', 'checando', 'baixando metadata', \
            'baixando', 'terminado', 'semeando', 'alocando']
    print ('%.2f%% terminado (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
            s.num_peers, state_str[s.state]))
    time.sleep(5)

end = time.time()
print(handle.name(), "COMPLETO")

print("Elapsed Time: ",int((end-begin)//60),"min :", int((end-begin)%60), "seg")

print(datetime.datetime.now())


