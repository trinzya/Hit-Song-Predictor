from django.shortcuts import render
from django.shortcuts import render,redirect
from django.template import loader
from django.contrib.auth.models import User,auth
from django.contrib import auth
from .models import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import time
# Create your views here.
from django.http import HttpResponse
total_artist = pd.read_csv('artist.csv')
print(type(total_artist['Artist'].iloc[0]))
client_id = '63f9b9b485954d2ba277f7bc5234c071'
client_secret = '975060eb928a488f92f0a70ac73ff87f'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
def sigmoid(z):
    return 1/(1+np.exp((-1)*z))
def hy(x,weights):
    z=np.dot(x,weights)
    #print(z.shape)
    return sigmoid(z)
weights=[[-1.99028495e-01],
  [ 3.34033628e-01],
 [ 1.09006219e-01],
 [ 2.06455554e-02],
 [-1.06333522e-04],
 [ 1.34400044e-02],
 [ 1.34712175e-02],
 [-3.64847462e-02],
 [-8.76188964e-02],
 [-1.80284075e-01],
 [-3.37334163e-02],
 [-4.24991954e-02],
 [ 1.11017161e-04]]
weights=np.array(weights)
def predict(x,weights):
    m=len(x)
    pred=np.zeros((m,1))
    temp=hy(x,weights)
    pred = np.where(temp > 0.5, 1, 0)
    return pred
song=None
def home(request):
    print(1)
    if request.method=="POST":
        song=request.POST['song']
        artist=request.POST['Artist']
        print("hello")
        print(song,artist)
        song=str(song).lower()
        artist=str(artist).lower()
        results = sp.search(q='artist:' + artist + ' track:' + song, type='track')
        if len(results['tracks']['items'] ) ==0:
            print("invalid")
        trackId = results['tracks']['items'][0]['id']
        print(trackId)
        features = sp.audio_features(trackId)
        test_case=list(features[0].values())[:11]
        if len(total_artist[total_artist['Artist']==artist])==0:
            test_case.insert(0,0)
        else:
            test_case.insert(0,1)
        test_case.insert(0,1)
        print(test_case)
        test_case=np.array(test_case)
        print(predict(test_case,weights))
        pred=predict(test_case,weights)
        context={'ans':pred[0],'song':song}
        song=None
        return render(request, 'index.html',context)
    return render(request, 'index.html')

# Create your views here.
