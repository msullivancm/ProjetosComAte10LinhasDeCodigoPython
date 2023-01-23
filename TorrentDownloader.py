# -*- coding: utf-8 -*-
#python -m pip install --upgrade pip setuptools wheel
#python -m pip install lbry-libtorrent google google.colab
#Instale os módulos acima para poder baixar.

from google.colab import drive
drive.mount('/content/drive')

link = input("Copie o magnet link e cole aqui: \n") 

import libtorrent as lt
import time
import datetime

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

print ('Fazendo Download...')
while (not handle.has_metadata()):
    time.sleep(1)
print ('Adquirindo Metadados, Iniciando Download do Torrent...')

print("Iniciando", handle.name())

while (handle.status().state != lt.torrent_status.seeding):
    s = handle.status()
    state_str = ['fila', 'checando', 'baixando metadata', \
            'baixando', 'concluído', 'semeando', 'alocando']
    print ('%.2f%% completo (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
            s.num_peers, state_str[s.state]))
    time.sleep(5)

end = time.time()
print(handle.name(), "COMPLETO")

print("Tempo Decorrido: ",int((end-begin)//60),"min :", int((end-begin)%60), "seg")

print(datetime.datetime.now())