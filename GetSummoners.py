from time import sleep
import Watcher

requester = Watcher.watcher

regions = {1: 'na', 2: 'lan', 3: 'las', 4: 'euw', 5: 'eune',
           6: 'oce', 7: 'kr', 8: 'ru', 9: 'tr', 10: 'br'}


def wait_for_request(delay=1):
    while not requester.can_make_request():
        sleep(delay)


def get_summoners_info(names, region):
    region = regions[int(region)]
    summoners = {}

    wait_for_request()
    suminfos = requester.get_summoners(names, region=region).values()
    del names
    for suminfo in suminfos:
        sumid = str(suminfo['id'])
        summoners[sumid] = {}
        summoners[sumid]['name'] = suminfo['name']
        summoners[sumid]['iconid'] = suminfo['profileIconId']
        summoners[sumid]['level'] = suminfo['summonerLevel']
    del suminfos

    wait_for_request()
    mpages = requester.get_mastery_pages(summoners.keys(), region=region)
    for sumid in summoners:
        summoners[sumid]['masteries'] = mpages[sumid]['pages']
        del mpages[sumid]
    del mpages

    wait_for_request()
    rpages = requester.get_rune_pages(summoners.keys(), region=region)
    for sumid in summoners:
        summoners[sumid]['runes'] = rpages[sumid]['pages']
        del rpages[sumid]
    del rpages, region

    return summoners
