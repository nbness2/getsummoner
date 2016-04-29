from os.path import isdir
from os import makedirs as makedir
from time import sleep
import Watcher

w = Watcher.w

DIR = 'NBWatch'

regions = '''
    North America = 1
    Latin America North = 2
    Latin America South = 3
    Europe West = 4
    Europe East = 5
    Oceania = 6
    Korea = 7
    Russia = 8
    Turkey = 9
    Brazil = 10
    '''

regionlist  = {
    1:'na',
    2:'lan',
    3:'las',
    4:'euw',
    5:'eune',
    6:'oce',
    7:'kr',
    8:'ru',
    9:'tr',
    10:'br'
    }


def wait_for_request(delay=1):
    while not w.can_make_request():
        sleep(delay)

def updateSummoner(summonername, rg, summonerid = None):
    if rg == '':
        rg = 1
    try:
        rg = regionlist[int(rg)]
        DIR = 'NBWatch\\'+rg
    except Exception as e:
        print('Region {0} error: {1}'.format(rg, e))
    if not isdir(DIR):
        makedir(DIR)
    wait_for_request()
    # Get summoner info
    try:
        summoner = w.get_summoner(name=summonername, region = rg)
    except Exception:
        print(summonername, rg)
    SID = str(summoner['id'])
    if not isdir(DIR+'\\'+SID):
        makedir(DIR+'\\'+SID)
    wait_for_request()
    with open(DIR+'\\'+SID+'\\summonername.txt', 'w') as f:
        f.write(str(summonername))
    # Get summoner's mastery pages
    mastery_pages = w.get_mastery_pages(SID, region = rg)
    with open(DIR+'\\'+SID+'\\masteries.txt', 'w') as f:
        f.write(str(mastery_pages))
    wait_for_request()

    # Get summoner's rune pages
    rune_pages = w.get_rune_pages(SID, rg)
    with open(DIR+'\\'+SID+'\\runes.txt', 'w') as f:
        f.write(str(rune_pages))
    wait_for_request()

    # Get summoner's current ranked stats
    try:
        ranked = w.get_ranked_stats(SID, region =  rg)
        with open(DIR+'\\'+SID+'\\ranked.txt', 'w') as f:
            f.write(str(ranked))
    except Exception as e:
        print('{0}, {2} current season: {1}'.format(summonername, e, rg))
    wait_for_request()

    # Get summoner's season x ranked stats
    for x in range(1,5):
        try:
            ranked_season_x = w.get_ranked_stats(SID, season = x, region =  rg)
            with open(DIR+'\\'+SID+'\\ranked_s'+str(x)+'.txt', 'w') as f:
                f.write(str(ranked_season_x))
        except Exception as e:
            print('{0} Season {1}: {2}'.format(summonername, x, e))
#sn = input('Summoner Name: ')
#print(regions)
#rn = input('Input a region number:')
#updateSummoner(sn, rn, True)
def update_all_sums(rg=10, debug=False, delay=2):
    a=0
    while True:
        try:
            sl=[]
            for x in range(30):
                sl.append(str(a))
                a+=1
            summonernames = w.get_summoner_name(sl,region=regionlist[int(rg)])
            for x,y in summonernames.items():
                summonername=y
                rgn = regionlist[int(rg)]
                DIR = 'NBWatch\\'+rgn
                if not isdir(DIR):
                    makedir(DIR)
                wait_for_request()
                # Get summoner info
                try:
                    summoner = w.get_summoner(name=summonername, region = rgn)
                except Exception:
                    print(rgn, summonername)
                SID = str(summoner['id'])
                if not isdir(DIR+'\\'+SID):
                    makedir(DIR+'\\'+SID)
                wait_for_request()
                with open(DIR+'\\'+SID+'\\summonername.txt', 'w') as f:
                    f.write(str(summonername))
                # Get summoner's mastery pages
                sleep(1)
                mastery_pages = w.get_mastery_pages(SID, region = rgn)
                with open(DIR+'\\'+SID+'\\masteries.txt', 'w') as f:
                    f.write(str(mastery_pages))
                wait_for_request()
                # Get summoner's rune pages
                sleep(1)
                rune_pages = w.get_rune_pages(SID, rgn)
                with open(DIR+'\\'+SID+'\\runes.txt', 'w') as f:
                    f.write(str(rune_pages))
                if debug == True:
                    print('{2}, {0}, {1} runes: Pass'.format(summonername, rgn, SID))
                wait_for_request()

                # Get summoner's current ranked stats
                sleep(1)
                try:
                    ranked = w.get_ranked_stats(SID, region =  rgn)
                    with open(DIR+'\\'+SID+'\\ranked.txt', 'w') as f:
                        f.write(str(ranked))
                except Exception as e:
                    print('{3}, {0}, {2} current season: {1}'.format(summonername, e, rgn, SID))

                # Get summoner's season x ranked stats
                for x in range(1,5):
                    sleep(1)
                    wait_for_request()
                    try:
                        ranked_season_x = w.get_ranked_stats(SID, season = x, region =  rgn)
                        with open(DIR+'\\'+SID+'\\ranked_s'+str(x)+'.txt', 'w') as f:
                            f.write(str(ranked_season_x))
                    except Exception as e:
                        print('{3}, {0} Season {1}: {2}'.format(summonername, x, e, SID))
        except Exception as e:
            with open('errors.txt', 'a') as f:
                f.write('NA, error:')
                f.write(str(e))
                f.write('\n')
update_all_sums(rg=1)
