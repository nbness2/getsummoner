from threading import Thread
from queue import Queue
from os import makedirs
from os.path import isdir
import GetSummoners


class QueueWorker(Thread):
    def __init__(self, queue, funct):
        Thread.__init__(self)
        self.queue = queue
        self.funct = funct

    def run(self):
        while True:
            try:
                if not self.queue.empty():
                    parts = self.queue.get()
                    self.funct(parts)
                    del parts
                    print('solved')
            except:
                self.queue.put(parts)


def update_summoner(sumnames, region):
    namelist = []
    namelist.extend(sumnames)
    summoners = GetSummoners.get_summoners_info(namelist, region)
    ids = [sumid for sumid in summoners]
    for sumid in ids:
        info_queue.put((sumid, region, summoners[sumid]))

def write_info(suminfo):
    #sumid, region, sumname, sumlvl, sumicon, masteries, runes
    sumid, region, suminfo = suminfo
    basicinfo = suminfo['name'], suminfo['level'], suminfo['iconid']
    del suminfo['name'], suminfo['level'], suminfo['iconid']
    sumdir = '{0}\\{1}\\{2}\\'.format(defdir, GetSummoners.regions[region], sumid)
    confirm_directory(sumdir)
    del sumid, region

    with open(sumdir+'basicinfo.lsa', 'w+') as basicfile:
        basicfile.writelines([str(line)+'\n' for line in basicinfo])
    del basicinfo

    with open(sumdir+'masteries.lmf', 'w+') as masteryfile:
        masteryfile.write(str(suminfo['masteries']))
    del suminfo['masteries']

    with open(sumdir+'runes.lrf', 'w+') as runefile:
        runefile.write(str(suminfo['runes']))
    del suminfo


def confirm_directory(directory):
    if not isdir(directory):
        makedirs(directory)

defdir = 'watchdata'

info_queue = Queue()
info_worker = QueueWorker(info_queue, write_info)
info_worker.start()

update_summoner(['Meowpai', 'LtSmokerV2', 'Zalestus', 'LEPReconBen', 'Zachary Scuderi'], 1)