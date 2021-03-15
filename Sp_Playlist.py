import json
import spotipy
import spotipy.util as util
import os

from spotipy.oauth2 import SpotifyClientCredentials

from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

from itertools import chain

username = 


cid = 
secret = 

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)
sp = spotipy.Spotify(auth_manager=client_credentials_manager)

class SpPlaylist:
    def __init__(self, playlist_id, offset=0, name=None,):
        self.playlist_id = playlist_id
        self.offset_ini = offset
        self.offset = self.offset_ini
        self.name = name
        pass

    def wholeplaylist(self):
        return sp.user_playlist_tracks(username, playlist_id=self.playlist_id, offset=self.offset)

    def tracks(self):
        output = self.wholeplaylist()['items']
        if self.wholeplaylist()['next'] == None:
            return self.wholeplaylist()['items']
        else:  # bc limit = 100, so offset to get more
            while True:
                self.offset += 100
                output.extend(self.wholeplaylist()['items'])
                if self.wholeplaylist()['next'] == None:
                    break
            self.offset = self.offset_ini  # back to initial value
            return output

    def tracknameartistdate(self):
        """[[title,artist,added date],......] for the moment"""
        track_num = self.tracknum()
        track_names = self.tracknames()
        track_artists = self.trackartists()
        track_dates = self.trackdates()
        output = []
        for i in range(track_num):
            output.append([track_names[i],track_artists[i],track_dates[i]])
        return output      

    def tracknameartistdate_log(self):
        """tracknameartistdate for everyday"""
        track_nameartistdate = self.tracknameartistdate()
        log_file = f"{self.name}_tracknameartistdate_logs.txt"
        try:
            with open(log_file, "r", encoding='utf-8') as logs:
                logsdict = json.load(logs)
            with open(log_file, "w", encoding='utf-8') as logs:
                logsdict[str(date.today())] = track_nameartistdate
                json.dump(logsdict, logs)
        except:
            with open(log_file, 'w', encoding='utf-8') as logs:
                json.dump({}, logs)
            with open(log_file, "r", encoding='utf-8') as logs:
                logsdict = json.load(logs)
            with open(log_file, "w", encoding='utf-8') as logs:
                logsdict[str(date.today())] = track_nameartistdate
                json.dump(logsdict, logs)
        # add the result to self.tracknum_logs for future reference
        self.tracknameartistdate_logs = logsdict
        return logsdict


    def tracknameartistdate_log_flatten(self):
        """log flattened, unit=['title','artist']"""
        """no use for now"""
        log = eval(open(f'{self.name}_tracknameartistdate_logs.txt','r').read())
        log_flattened = list(chain.from_iterable(list(log.values())))
        for item in list(log.values())[-1]:
            print(item,log_flattened.count(item))


    def tracknum(self):
        track_num = len(self.tracks())
        return track_num

    def tracknum_log(self):
        track_num = self.tracknum()
        log_file = f"{self.name}_tracknum_logs.txt"
        try:
            with open(log_file, "r", encoding='utf-8') as logs:
                logsdict = json.load(logs)
            with open(log_file, "w", encoding='utf-8') as logs:
                logsdict[str(date.today())] = track_num
                json.dump(logsdict, logs)
        except:
            with open(log_file, 'w', encoding='utf-8') as logs:
                json.dump({}, logs)
            with open(log_file, "r", encoding='utf-8') as logs:
                logsdict = json.load(logs)
            with open(log_file, "w", encoding='utf-8') as logs:
                logsdict[str(date.today())] = track_num
                json.dump(logsdict, logs)
        # add the result to self.tracknum_logs for future reference
        self.tracknum_logs = logsdict
        return logsdict

    def tracknum_line(self):
        """line gragh of playlist tracks number history"""
        self.tracknum_log()  # create log
        plt.plot(list(self.tracknum_logs.keys()),
                 list(self.tracknum_logs.values()))
        plt.gca().axes.xaxis.set_ticklabels([]) #hide x label (dates)
        # plt.gca().axes.get_xaxis().set_visible(False) #hide x label (dates) and the dots on x axis
        plt.ylim(bottom=0)
        plt.show()

    def trackdates(self):
        output = []
        track_num = self.tracknum()
        tracks=self.tracks()
        for i in range(track_num):
            output.append(tracks[i]['added_at'][:10])
        return output

    def tracknames(self):
        """all tracks' name in the playlist"""
        output = []
        track_num = self.tracknum()
        tracks=self.tracks()
        for i in range(track_num):
            output.append(tracks[i]['track']['name'])
        return output

    def trackartists(self):
        """all tracks' (leading) artist in the playlist"""
        output = []
        track_num = self.tracknum()
        tracks = self.tracks()  # reduce computation
        for i in range(track_num):
            output.append(json.dumps(tracks[i]['track']['artists'][0]['name'],
                                     sort_keys=True, indent=4, ensure_ascii=False).encode('utf-8').decode())
            # output.append(tracks[i]['track']['artists'][0]['name'])
        return output

    def artistcounts(self):
        """return the dict of each artist with how many tracks in the playlist"""
        temp = self.trackartists()

        log = []
        artist_counts = {}
        for artist in temp:
            if artist not in log:
                artist_counts[artist.strip('"')] = temp.count(artist) #add artist:number to dict
                log.append(artist)
            else:
                pass
        artist_counts = dict(sorted(artist_counts.items(),
                                    key=lambda item: item[1], reverse=True)) #order the dictionary by vlaues
        return artist_counts

    def artistcounts_log(self):
        artist_counts = self.artistcounts()
        log_file = f"{self.name}_artistdistribution_logs.txt"
        try:
            with open(log_file, "r", encoding='utf-8') as logs:
                logsdict = json.load(logs)
            with open(log_file, "w", encoding='utf-8') as logs:
                logsdict[str(date.today())] = artist_counts
                json.dump(logsdict, logs)
        except:
            with open(log_file, 'w', encoding='utf-8') as logs:
                json.dump({}, logs)
            with open(log_file, "r", encoding='utf-8') as logs:
                logsdict = json.load(logs)
            with open(log_file, "w", encoding='utf-8') as logs:
                logsdict[str(date.today())] = artist_counts
                json.dump(logsdict, logs)
        # add the result to self.artistcounts_logs for future reference
        self.artistcounts_logs = logsdict
        return logsdict

    def artistcounts_piechart(self,date=str(date.today())):
        """draw piechart of artist account"""
        try:
            artist_counts = self.artistcounts_logs[date]
        except: #if no self.log → generate
            artist_counts = self.artistcounts_log()
            artist_counts = self.artistcounts_logs[date]
        plt.pie(artist_counts.values(), labels=artist_counts.keys())
        # plt.axis('equal')
        plt.show()
        # bruh

    def track_info(self,name):
        """return dates of existence of a track in the playlist (doesn't avoid title name collision)"""
        """need exact title match"""
        try:
            log = eval(open(f'{self.name}_tracknameartistdate_logs.txt','r').read())
            trks = list(log.values())
            dates = list(log.keys())
            date_start, date_end = 0,0
            for i in range(len(trks)-1,-1,-1):
                c = np.where(np.array(trks[i])[:,0] == name) #find
                if len(c[0]) != 0: #found
                    date_end = dates[i]
                    date_start = trks[i][c[0][0]][2]
                    break

            if date_start == 0:
                return 'no result\npossible reasons:\n1.really no match\n2.not the exact title name\n3.was deleted before 2021-03-07'
            else:
                a = datetime.strptime(date_start,'%Y-%m-%d')
                b = datetime.strptime(date_end,'%Y-%m-%d')
                return f'dates of existence: {date_start} ~ {date_end}, {(b-a).days} days'

        except: # before added dates in logs (before 2021-03-07)
        #every days of existence goes into hist
            hist = []
            for i in range(len(trks)): #check every day's log
                c = np.where(np.array(trks[i])[:,0] == name) #find
                if len(c[0]) != 0: #found
                    hist.append(list(log.keys())[i])

            if len(hist) == 0:
                return 'no result\npossible reasons:\n1.really no match\n2.not the exact title name\n3.was deleted before 2020-12-26'
            else:
                a=datetime.strptime(hist[0],'%Y-%m-%d')
                b=datetime.strptime(hist[-1],'%Y-%m-%d')
                return f'dates of existence: {hist[0]} ~ {hist[-1]}, {(b-a).days} days\n(only count 2020-12-26 and after)'

