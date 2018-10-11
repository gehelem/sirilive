#!/usr/bin/python3
# -*- coding: utf-8 -*-
wrk = '/home/gilles/projects/sirilive/WORK'
scan = '/home/gilles/projects/sirilive/SCAN'

import sys
import time
import logging
import watchdog
import shutil
import os
import subprocess

from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            print (event.src_path)
            if os.listdir(wrk) == []: 
                shutil.copy(event.src_path,wrk+"/current001.fits")
                shutil.copy(event.src_path,wrk+"/current002.fits") #dummy pour forcer à faire une sequence
                subprocess.call('siril -s /home/gilles/projects/sirilive/live10.ssf -d '+wrk, shell=True)
                shutil.move(wrk+"/pp_current001.fits",wrk+"/master001.fits")
                os.remove(wrk+"/current001.fits")
                os.remove(wrk+"/current002.fits")                
                #os.remove(wrk+"/current00001.fits")
                #os.remove(wrk+"/current00002.fits") 
                #os.remove(wrk+"/pp_current00001.fits")
                os.remove(wrk+"/pp_current002.fits")                 
                os.remove(wrk+"/current.seq") 
            else: 
                shutil.copy(event.src_path,wrk+"/current001.fits")  
                shutil.copy(event.src_path,wrk+"/current002.fits") #dummy pour forcer à faire une sequence            
                subprocess.call('siril -s /home/gilles/projects/sirilive/live10.ssf -d '+wrk, shell=True) 
                shutil.move(wrk+"/pp_current001.fits",wrk+"/master002.fits")
                subprocess.call('siril -s /home/gilles/projects/sirilive/live50.ssf -d '+wrk, shell=True) 
                os.remove(wrk+"/current001.fits")
                os.remove(wrk+"/current002.fits")                
                #os.remove(wrk+"/current00001.fits")
                #os.remove(wrk+"/current00002.fits") 
                #os.remove(wrk+"/pp_current00001.fits")
                os.remove(wrk+"/pp_current002.fits")                 
                os.remove(wrk+"/r_master001.fits")
                os.remove(wrk+"/r_master002.fits")
                os.remove(wrk+"/master001.fits")
                os.remove(wrk+"/master002.fits")                
                os.remove(wrk+"/current.seq") 
                os.remove(wrk+"/master.seq")
                os.remove(wrk+"/r_master.seq")                
                shutil.move(wrk+"/r_master_stacked.fits",wrk+"/master001.fits")
                subprocess.call('convert -flatten -normalize '+wrk+'/master001.fits '+wrk+'/master001.jpeg', shell=True) 
                
        else:
            # Take any action here when a file is first created.
            print (event.src_path)
            


# on fait du ménage 
shutil.rmtree(wrk)
os.makedirs(wrk)
        
event_handler = Handler()
observer = Observer()
watch = observer.schedule(event_handler,scan, recursive=False)            
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
        observer.stop()
