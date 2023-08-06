import os, sys
import time
import logging

from functools import wraps
from multiprocessing import Process, Lock
from .caller import call_txt2img, call_img2img, call_interrogate

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="PID %(process)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger('MPAPI')

class MPAPI():

    def spinlock(self, func):

        @wraps(func)
        def wrapped(*args):
            self.busy_waiting()
            url = self.find_idle_process()
            logger.info(f"{func.__name__} URL: {url}")
            # logger.info(args)

            self.pdict[url]={
                "api": func.__name__,
                # "payload": payload
            }
            self.pdict[url]["proc"] = Process(target=func, args=(
                url, *args
            ))
            self.pdict[url]["proc"].start()

        return wrapped


    def __init__(self, url_list, intv=0.1):
        self.url_list = url_list
        self.MAXP = len(url_list)
        self.intv = intv

        self.pdict = dict([])

        logger.info(f"Total urls : {self.MAXP}")

        # func
        self.call_txt2img = self.spinlock(call_txt2img)
        self.call_img2img = self.spinlock(call_img2img)
        self.call_interrogate = self.spinlock(call_interrogate)

    def busy_waiting(self):
        current_process = self.MAXP
        while(current_process>=self.MAXP):
            time.sleep(self.intv)
            current_process = self.emtpy_done_process()

    def emtpy_done_process(self):
        current_process = 0
        dead_url = []

        # count alive process
        for url, info in self.pdict.items():
            if info["proc"].is_alive():
                current_process+= 1
            else:
                info["proc"].join()
                dead_url.append(url)

        # pop dead process
        for url in dead_url:
            self.pdict.pop(url)
        
        return current_process
    
    def find_idle_process(self):
        for url in self.url_list:
            if url in self.pdict:
                continue
            else:
                return url
        else:
            return False
