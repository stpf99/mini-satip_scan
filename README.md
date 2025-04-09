Create the playlist spec for my location / replace with proper tune freq params:

./octoscan --use_nit --freq=650 --msys=dvbt2 --bw=8 --tmode=8k --gi=19/128 --mtype=256qam --create dvb.m3u 192.168.1.1

./octoscan --freq=586 --msys=dvbt2 --bw=8 --tmode=8k --gi=19/128 --mtype=256qam --append dvb.m3u 192.168.1.1

./octoscan --freq=562 --msys=dvbt2 --bw=8 --tmode=8k --gi=19/128 --mtype=256qam --create dvb.m3u 192.168.1.1

./octoscan --freq=538 --msys=dvbt2 --bw=8 --tmode=8k --gi=19/128 --mtype=256qam --append dvb.m3u 192.168.1.1

./octoscan --freq=184 --msys=dvbt --bw=7 --tmode=8k --mtype=64qam --append dvb.m3u 192.168.1.1

./octoscan --freq=554 --msys=dvbt2 --bw=8 --tmode=8k --gi=19/128 --mtype=256qam --append dvb.m3u 192.168.1.1

i modified code for adding dvb-t/2 


gcc -o octoscan octoscan.c -pthread
