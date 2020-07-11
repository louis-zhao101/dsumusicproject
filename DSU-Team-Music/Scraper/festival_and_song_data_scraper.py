from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

SPOTIFY_CLIENT_ID = input("Enter Spotify Client ID: ")
SPOTIFY_CLIENT_SECRET = input("Enter Spotify Client Secret: ")

credentials = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=credentials)

"""
@Input artists: list of names of artist
@Parameter concerts: bool of whether to scrape concerts as well as festivals
@Return: data frame with all festivals played by artist (cols: artist, event, festival or concert, date)

Scrapes festival names and dates by artist from Songkick
"""

# Louis & Sophie

# Use beautiful soup to scrape past concerts from Songkick
# Should check whether it was a festival or concert

def songkick_scraping(artists, concerts = False, verbose = False):
  ## verbose = True returns artists that are not found
  # Iterate through each artist
    # Search on Songkick for that artist
    # Add /gigography to url
    # Iterate through each page of past concerts
      # Checks if past concert or past festival
  

  template_URL = "https://www.songkick.com/search?utf8=%E2%9C%93&type=initial&query="
  total_data = pd.DataFrame(columns = ["Artist", "Event", "Festival or Concert", "Date"])

  for artist in artists:

    ############## locating gigography page #################
    artist = artist.replace(" ", "-")
    URL = template_URL + artist
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    artisturl = soup.find('li', class_ = 'artist')
    try:
      artisturl = artisturl.find('a')
    except:
      artisturl = None
      if verbose == True:
        print(artist + " Not Found")
      continue

    artist_id = artisturl.get("href")

    template_URL_2 = "https://www.songkick.com"

    try:
      correct_artist = artist_id.find(artist)
    except:
      correct_artist = -1
      if verbose == True:
        print(artist + " Not Found")
      continue

    artist_past_concerts = template_URL_2 + artist_id + "/gigography" 

    ############### finding total number of pages of events ################

    page2 = requests.get(artist_past_concerts)
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    num_pages = soup2.find('div', class_ = 'pagination')
    if num_pages != None:
      num_pages = num_pages.find_all('a')
      num_pages1 = num_pages[len(num_pages)-2].get_text()
      num_pages2 = range(1, int(num_pages1) + 1)
    else:
      num_pages2 = [1]
    
    ################ scraping actual data ####################

    performance_type = []
    concert_list = []
    total_events = []
    total_event_dates = []
    num_of_days = []

    for page in num_pages2:
      artist_past_concerts = template_URL_2 + artist_id + "/gigography" + "?page=" + str(page)
      page2 = requests.get(artist_past_concerts)
      soup2 = BeautifulSoup(page2.content, 'html.parser')
      main_soup2 = soup2.find('ul', class_ = 'event-listings artist-focus ')

      concert_dates = main_soup2.find_all(title = True) #find event date
      
      for val in concert_dates:       
        concert_dates = val["title"].split(" – ")
        total_event_dates.append(concert_dates[0])
        duration = 1
        if len(concert_dates) == 2:      #separate dates
          all_dates = pd.date_range(concert_dates[0], concert_dates[1], closed = 'right').strftime("%A %d %B %Y")
          for more_days in all_dates:
            total_event_dates.append(more_days)
            duration += 1
        num_of_days.append(duration)

      artist_page = main_soup2.find_all('p', class_ = 'artists summary') #get urls of all the concerts on page
      
      for info in artist_page:          #set up for festival_type and event name
        tempurl = info.find_all('a')
        
        for item in tempurl:
          event = item.get_text()
          event = " ".join(event.split())
          total_events.append(event)
          concert_url = item.get('href')
          concert_list.append(concert_url) #all the individual urls to concert/festival pages

    
    for concert in concert_list:       #determine type of event based on url
      key = concert.find('/festivals/')
      performance_type.append(key) #0 is for festival, -1 is for concert
   

    performance_type = [i * -1 for i in performance_type] #0 for festival, 1 for concert
    
    artist = artist.replace("-", " ")
    #artist_name= np.repeat(artist, len(performance_type)) #set up artist column
    artist_name = np.repeat(artist, len(total_event_dates))
    total_events = np.repeat(total_events, num_of_days)
    performance_type = np.repeat(performance_type, num_of_days)
    
    artist_data = pd.DataFrame(columns = ["Artist", "Event", "Festival or Concert", "Date"]) #combining all columns
    artist_data['Festival or Concert'] = performance_type
    artist_data['Artist'] = artist_name
    artist_data["Date"] = total_event_dates
    artist_data["Event"] = total_events
    
    total_data = total_data.append(artist_data) #append artist dataframe to final dataframe

  pd.set_option('display.max_columns', None)
  pd.set_option('display.max_rows', 20)

  for index,row in total_data.iterrows():
    if row['Festival or Concert'] == 0:
      row["Event"] = row['Event'][len(row['Artist']):]
    if row['Event'][0] == " ":
      row["Event"] = row["Event"][1:]

  if concerts == 0:
    return total_data[total_data['Festival or Concert'] == 0]
  else:
    return total_data

  # Path example for Audien:
  # https://www.songkick.com/search?page=1&per_page=10&query=audien&type=artists (search)
  # https://www.songkick.com/artists/4320841-audien (artist page)
  # https://www.songkick.com/artists/4320841-audien/gigography (artist past concerts)
  # https://www.songkick.com/festivals/1721184-crush-arizona/id/39340961-crush-arizona-2020 (specific event from gigography where we check if its a festival)

"""
@Input artists: list of names of artist
@Return: data frame with all songs each artist released on spotify (cols: artist, song, date)

Pulls song name and release date by artist from Spotify 
"""

# Should pull songs and dates from Spotify for each artist
# Probably wanna use artist_albums in spotipy documentation to pull all albums and info
# Then just get dates from there

def spotify_song_collection(artists, verbose = False):
    # Iterate through each artist
    # Search for artist and get their ID
    # Get all their songs and metadata (artist_albums)
    # Convert it to a data frame
  
  artists_ids = {}

  output_songs_df = None

  for artist in artists:
    result = sp.search(artist)

    try:
      first_result_artists = result['tracks']['items'][0]['artists']
    except:
      first_result_artists = None
      artists_ids[artist] = "no results"
      continue

    try:
      artist_search_info = [artist_results for artist_results in first_result_artists if artist_results["name"] == artist][0]
    except:
      artists_ids[artist] = "there was a problem finding"
      continue

    artists_ids[artist] = artist_search_info["id"]

    artists_albums_results = sp.artist_albums(artists_ids[artist], limit = 50)

    artists_albums_df = pd.DataFrame(artists_albums_results["items"])

    artists_albums_df.insert(loc = 0, column = "artist_name", value = artist)

    if output_songs_df is None:
      output_songs_df = artists_albums_df

    else:
      output_songs_df = output_songs_df.append(artists_albums_df, ignore_index = True)

  if verbose:
    print(artists_ids)
    print(output_songs_df)

  return output_songs_df

def main():    
    os.chdir("..")
    os.chdir("./Data")
    artists_to_scrape = pd.read_csv("selected_artists.csv")
    
    artists_names = artists_to_scrape["name"].tolist()
    
    input("There are " + str(len(artists_names)) + " artists inputed.\nPress enter to continue...")
    
    songkick_data = songkick_scraping(artists = artists_names)
    
    spotify_song_data = spotify_song_collection(artists = artists_names)
    
    songkick_data.to_csv('songkick_festival_data.csv')
    spotify_song_data.to_csv('spotify_song_data.csv')

if __name__ == "__main__":
    main()