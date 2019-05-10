#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import time
import logging
import watchdog
import shutil
import os
import subprocess
import commands
import astropy
from astropy.io import fits
from astropy.visualization import make_lupton_rgb

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import matplotlib.pyplot as pl

www = os.path.expanduser('~/sirilive/www')
wrk = os.path.expanduser('~/sirilive/work')
log = os.path.expanduser('~/sirilive/log')
scan = os.path.expanduser('~/sirilive/scan')
ind = 0
sirilpath = os.path.expanduser('')
wrkconv  = os.path.expanduser(wrk+"/conv")
wrkreg   = os.path.expanduser(wrk+"/reg")
wrkstack = os.path.expanduser(wrk+"/stack")



def conversion(fichier):
    if os.path.exists(wrkconv):
        shutil.rmtree(wrkconv)
    os.mkdir(wrkconv)
    shutil.copy(fichier,wrkconv+"/current001.fits")  
    shutil.copy(fichier,wrkconv+"/current002.fits") #dummy pour forcer à faire une sequence            
    subprocess.call(sirilpath+'siril -s ~/sirilive/live10.ssf -d '+wrkconv + ' >> ' + wrkconv + '/log.txt',  shell=True)
    return wrkconv+"/pp_current001.fits"
    #shutil.copy(fichier,wrkconv+"/current001.fits")  
    #return wrkconv+"/current001.fits"          

def register(f1,f2):
    if os.path.exists(wrkreg):
        shutil.rmtree(wrkreg)
    os.mkdir(wrkreg)
    shutil.copy(f1,wrkreg+"/current001.fits")  
    shutil.copy(f2,wrkreg+"/current002.fits")
    subprocess.call(sirilpath+'siril -s ~/sirilive/live50.ssf -d '+wrkreg + ' >> ' + wrkreg + '/log.txt',  shell=True)
    subprocess.call('cat ' + wrkreg + '/log.txt | grep FWHMx | tail -1 >> ' + log + '/log.txt',  shell=True)
    retour = commands.getoutput('cat ' + wrkreg + '/log.txt | grep FWHMx | tail -1')
    retour = retour[18:24]
    retour = retour.replace(" ","0")
    return float(retour)

def stack(f1,f2,s):
    if os.path.exists(wrkstack):
        shutil.rmtree(wrkstack)
    os.mkdir(wrkstack)
    shutil.copy(f1,wrkstack+"/current001.fits")  
    shutil.copy(f2,wrkstack+"/current002.fits")
    #shutil.copy(s ,wrkstack+"/r_current.seq")
    #subprocess.call(sirilpath+'siril -s ~/sirilive/live55.ssf -d '+wrkstack + ' >> ' + wrkstack + '/log.txt',  shell=True)
    stacked = fits.getdata(f1) + fits.getdata(f2)
    hdu = fits.PrimaryHDU(stacked)
    hdu.writeto(wrkstack+"/current_stacked.fits")

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            #print (event.src_path)
            
            shutil.move(conversion(event.src_path),wrk+"/converted.fits")
            subprocess.call('echo ' + event.src_path + ' >> ' + log + '/log.txt',  shell=True)

            if os.path.exists(wrk+"/master.fits"):

                if register(wrk+"/converted.fits",wrk+"/master.fits") < 999:
                    stack   (wrkreg+"/r_current001.fits",wrkreg+"/r_current002.fits",wrkreg+"/r_current.seq")
                    #stack   (wrk+"/converted.fits",wrk+"/master.fits","")  

                    os.remove(wrk+"/master.fits")
                    shutil.copy(wrkstack+"/current_stacked.fits",wrk+"/master.fits")
                    
                    #imgdata = fits.getdata(wrk+"/master.fits")
                    #R = imgdata[0]
                    #G = imgdata[1]
                    #B = imgdata[2]
                    #rgb_default = make_lupton_rgb(B, R, G, filename=wrk+"/result.jpeg")
                    #pl.imshow(rgb_default, origin='lower')
                    
                    subprocess.call(sirilpath+'siril -s ~/sirilive/live60.ssf -d '+wrk + ' >> ' + log + '/log.txt',  shell=True)
                    #ind=ind + 1
                    print ("----------------------- " + ind)                    
                    shutil.copy(wrk+'/public.jpg',www+"/public"+ind+".jpeg")
                    os.remove(www+"/master.fits")
                    shutil.copy(wrk+"/master.fits",www)
            else:
                shutil.move(wrk+"/converted.fits",wrk+"/master.fits")
                
        else:
            # Take any action here when a file is first created.
            print (event.src_path)
            


# on fait du ménage 


if os.path.exists(wrk):
    shutil.rmtree(wrk)
os.mkdir(wrk)        

if os.path.exists(log):
    shutil.rmtree(log)
os.mkdir(log)        

event_handler = Handler()



observer = Observer()
watch = observer.schedule(event_handler,scan, recursive=False)            
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
        observer.stop()
