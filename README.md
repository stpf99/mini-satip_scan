# octoscan

This is how it works : 

Create the playlist:

  ./octoscan --freq=122 --msys=dvbc --sr=6900 --mtype=64qam  --create Scanned_DVB-C.m3u <IP of the SAT>IP Server>

Add another Transponder to the Playlist:

  ./octoscan --freq=330 --msys=dvbc --sr=6900 --mtype=256qam --append Scanned_DVB-C.m3u <IP of the SAT>IP Server>

FYI The Binary provided is compiled on Ubuntu 19.10 / X86
