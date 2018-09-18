import feedparser
import subprocess
import datetime
import os

print("~ Showrss Scrape ~")

url = 'http://showrss.info/user/12000.rss?magnets=true&namespaces=false&name=null&quality=hd&re=yes'
test_magnet = 'magnet:?xt=urn:btih:7A1A06A198BF6AA75A85D1E0C2430F38B7D38C65&dn=Its+Always+Sunny+in+Philadelphia+S13E01+REPACK+720p+WEBRip+x264+TBS&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce'
feed = feedparser.parse(url)
dir = os.path.dirname(__file__)
auth = ""
error = 0

with open(os.path.join(dir, 'auth'), 'r') as f:
    auth = f.read()[:-1]

log = open(os.path.join(dir, 'log'), 'a+')
log.write("{0}: Starting showrss scrape\n".format(datetime.datetime.now()))

def start_download(magnet):
    output = subprocess.call(['transmission-remote', '-a', magnet, '--auth={0}'.format(auth)])
    if not output:
        log.write("{0}: Torrent added successfully\n".format(datetime.datetime.now()))
        print("Torrent added successfully")
    else:
        log.write("{0}: Failed to add torrent\n".format(datetime.datetime.now()))
        print("Failed to add torrent")
    return not output

last_guid = ""
latest_guid = ""

with open(os.path.join(dir, 'track'), 'r') as f:
    last_guid = f.read()

latest_guid = feed['entries'][0]['guid']

if latest_guid == last_guid:
    log.write("{0}: Initial GUID match ({1} == {2}) - Finishing.\n".format(datetime.datetime.now(), last_guid, latest_guid))
    log.close()
    exit()

for entry in feed['entries']:
    if entry['guid'] == last_guid:
        log.write("{0}: Finished adding new torrents\n".format(datetime.datetime.now()))
        break
    else:
        log.write("{0}: Adding Torrent - {1}\n".format(datetime.datetime.now(), entry['title']))
        if not start_download(entry['link']):
            error = 1


if not error:
    with open(os.path.join(dir, 'track'), 'w') as f:
        log.write("{0}: Writing latest GUID - {1}\n".format(datetime.datetime.now(), latest_guid))
        f.write(latest_guid)
else:
    log.write("{0}: An error occurred - Some torrents may not have been started\n".format(datetime.datetime.now(), latest_guid))


log.close()
