import os
import json
import sys
from urllib.request import urlretrieve

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

def letoltes(cim,sorszam,src,konyvtar_video):
	cim=cim.replace("  ", " ")
	cim=cim.replace(" ", "_")
	cim=cim.replace("/", "")
	sorszam=str(sorszam)
	sorszamhossz=len(str(sorszam))
	if sorszamhossz==1:
		sorszam="00"+sorszam
	elif sorszamhossz==2:
		sorszam="0"+sorszam
	elif sorszamhossz==3:
		sorszam=sorszam
	hely=konyvtar_video+sorszam+"-"+cim+".mp4"
	print(sorszam+"-"+cim)
	urlretrieve(src, hely, reporthook)	
	print("ok")




konyvtar = input("Enter the videofiles absolute path: ")

konyvtar_video = input("Enter the destination folder absolute path: ")

downloaded_list=os.listdir(konyvtar_video)

downloaded_videos={}

for x in downloaded_list:
	if os.path.isfile(konyvtar_video+"/"+x):
		fileinfo=os.stat(konyvtar_video+"/"+x)
		filesize=fileinfo.st_size
		cim=x.replace("_", " ")
		cim=cim[4:-4]
		print ("Downloaded: "+cim+"-"+str(filesize)+" byte")
		downloaded_videos[cim] = filesize


listavideo=os.listdir(konyvtar)
for i in listavideo:
	if i!="tmp":
		if i[1]=="-":
			keresesi_cim=i[2:-4]
			sorszam=int(i[0])+1
		elif i[2]=="-":
			keresesi_cim=i[3:-4]
			sorszam=int(i[:2])+1
		elif i[3]=="-":
			keresesi_cim=i[4:-4]
			sorszam=int(i[:3])+1
		f = open(konyvtar+"tmp/"+keresesi_cim+".json", "r")
		adatok=json.loads(f.read())
		cim=adatok["name"]
		src=adatok["sources"][6]["src"]
		size=adatok["sources"][6]["size"]
		f.close()
		if cim in downloaded_videos:
			file_meret=downloaded_videos[cim]
			if file_meret != size:
				letoltes(cim, sorszam, src, konyvtar_video)
				
		else:
			letoltes(cim, sorszam, src, konyvtar_video)
			

print ("download complete!")
