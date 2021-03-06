import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from selenium import webdriver
import os

# {data} ∪ {science}
# Using Selenium to load & scrape data from dynamic elements generated by JavaScript on Jambase's Analytics website

""" DEFINE SCRAPING FUNCTIONS """

def scrape_artist_data(festivals):
    # Scrape artist name data using the Firefox webdriver via selenium
    url = "https://www.jambase.com/festival/"
    performances = pd.DataFrame()
    
    for festival in festivals:
        driver = webdriver.Firefox()
        driver.get(url + festival)
                
        # Execute js cmd to scroll to the bottom of the webpage and make sure data is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        
        # Find artist names with xpath
        content = driver.find_elements_by_xpath("//*[contains(@class, 'h3 text-primary')]")
        
        # Put the names in a dataframe with the festival and date
        year = int(festival.split('-')[-1])
        festival = festival.replace('-',' ')[:-5]
        names = [i.text for i in content]
        
        df = pd.DataFrame({'Name':names, 'Year':year, 'Festival':festival})
        performances = performances.append(df)

        # Close the driver/web browser
        driver.quit()
    
    # Call get_spotify_artist_following to add follower metrics to the df    
    stats = get_spotify_artist_following(performances['Name'].drop_duplicates())
    return(stats)


def get_spotify_artist_following(artists, verbose = False):
    # Get follower & popularity metrics from Spotify's API
    print("This program utilizes Spotify's API to get popularity metrics on the artists.")
    SPOTIFY_CLIENT_ID = input("Enter Spotify Client ID: ")
    SPOTIFY_CLIENT_SECRET = input("Enter Spotify Client Secret: ")

    credentials = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=credentials)
    
    artists_info = []
    for artist in artists:
        result = sp.search(artist)
        
        try:
            first_result_artists = result['tracks']['items'][0]['artists']
        except:
            first_result_artists = None
            artists_info.append(artist + " no results")
            continue
        
        try:
            artist_search_info = [artist_results for artist_results in first_result_artists if artist_results["name"] == artist][0]
        except:
            artists_info.append(artist + " there was a problem finding")
            # if we want to include names of artists that dont have spotify stats, use the below
            # artists_info.append({'name':artist, 'followers':None,'popularity':None})
            continue

        artist_info = sp.artist(artist_search_info["id"])
        artists_info.append(artist_info)
  
    success_artists_info = [artist_info for artist_info in artists_info if isinstance(artist_info, dict)]
    
    artists_following = pd.DataFrame(success_artists_info)[["name", "followers", "popularity"]]
    artists_following["followers"] = artists_following["followers"].apply(pd.Series)["total"]
    artists_following.set_index("name", inplace = True)

    return(artists_following)


def main():
    festivals = ['edc-las-vegas-2019',
                 'ultra-music-festival-2019',
                 'escape-psycho-circus-2019',
                 'beyond-wonderland-socal-2019',
                 'nocturnal-wonderland-2019',
                 'paradiso-festival-2019',
                 'dreamstate-socal-2019',
                 'project-z-2019',
                 'lost-lands-music-festival-2019']
    
    data = scrape_artist_data(festivals)
    
    os.chdir("..")
    os.chdir("./Data")
    data.to_csv("artist_selection_data.csv")
    
if __name__ == "__main__":
    main()