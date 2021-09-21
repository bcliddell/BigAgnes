# spotipy
import spotipy
from spotipy import oauth2

# selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# BeautifulSoup
from bs4 import BeautifulSoup

# tweepy
import tweepy

# Agnes library imports
import config

class Authenticator:
    def __init__(self):
        self.sp = None
        self.sp_oauth, self.token_info = self.spot_auth()
        # self.twitter_api is the object that handles actual interfacing with twitter
        self.twitter_api = self.twitter_auth()

    def spot_auth(self):
        """Authenticates with Spotify's API and returns sp_oauth, which is an
        SpotifyOAuth object used to refresh the token.
        """
        sp_oauth = oauth2.SpotifyOAuth(client_id=config.CLIENT_ID,
                                client_secret=config.CLIENT_SECRET,
                                redirect_uri=config.REDIRECT_URI,
                                scope=config.SCOPE)
        token_info = sp_oauth.get_cached_token()    # fetches cached token info from .cache
        if not token_info:                          # if cache not found, logs into spotify with selenium
            auth_url = sp_oauth.get_authorize_url()
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            driver = webdriver.Firefox(options=options, service_log_path=None)
            driver.get(auth_url)
            driver.find_element_by_id('login-username').send_keys(config.SPOT_USERNAME)
            driver.find_element_by_id('login-password').send_keys(config.SPOT_PASSWORD)
            driver.find_element_by_id('login-button').click()
            WebDriverWait(driver, 10).until(expected_conditions.title_is('Problem loading page'))
            response = driver.current_url
            driver.quit()

            code = sp_oauth.parse_response_code(response)
            token_info = sp_oauth.get_access_token(code)
            token = token_info['access_token']
        else:
            token = token_info['access_token']

        self.sp = spotipy.Spotify(auth=token)    # pylint: disable=unused-variable
        print('Authenticated with Spotify.')
        return sp_oauth, token_info

    def twitter_auth(self):
        """Authenticates on Twitter."""
        auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(config.TW_ACCESS_TOKEN, config.TW_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        print('Authenticated with Twitter.')
        return api

    def spotify_refresh(self, sp_oauth):
        """Refreshes the Spotify access token, since it expires every hour."""
        if sp_oauth.is_token_expired(self.token_info):
            print('Attempting to refresh access token...')
            self.token_info = sp_oauth.refresh_access_token(self.token_info['refresh_token'])
            token = self.token_info['access_token']
            self.sp = spotipy.Spotify(auth=token)
