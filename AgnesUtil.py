# builtin Python modules
import random
import json
import urllib
from os import path

# Agnes library imports
from Authenticator import Authenticator
import config


class AgnesUtil(Authenticator):
    """Contains various utility functions used across various Agnes objects.
    Is inherited (composition) by Agnes.
    """
    def __init__(self):
        super().__init__()
        self.last_quote_read = None

    def write_to_file(self, file, _input):
        try:
            if '�' in _input:
                _input.replace('�', "\'")   # sometimes apostrophes get encoded as '�' and I don't know why.
            with open(file, 'a') as outfile:
                outfile.write(f'\n{_input}')
        except FileNotFoundError:
            print(f'Error accessing {file}. Please try again later.')
            return

    def random_from_file(self, file):
        """
        Takes a txt file as a parameter and creates a list of each line,
        then chooses and returns a single line.
        """
        ltemp = []
        try:
            with open(file, 'r') as infile:
                line = infile.readline()
                while line:
                    ltemp.append(line)
                    line = infile.readline()
                choice = random.choice(ltemp)
            return choice
        except FileNotFoundError:
            print(f'{file} could not be opened. Please check the directory and try again.')
            return

    def getquote(self):
        dir_path = path.dirname(path.realpath(__file__))
        quote_path = path.join(dir_path, '.\\txt_files\\quotes.json')
        with open(quote_path, 'r') as quote_file:
            quotes_data = json.load(quote_file)
            quote = random.choice(quotes_data)
        self.last_quote_read = quote
        return quote["quote"]


    def get_quote_by_id(self, id):
        dir_path = path.dirname(path.realpath(__file__))
        quote_path = path.join(dir_path, '.\\txt_files\\quotes.json')
        with open(quote_path, 'r') as quote_file:
            quotes_data = json.load(quote_file)
            my_quote = 'I searched far and wide, but I couldn\'t find a quote with that ID.'
            for quote in quotes_data:
                if quote['id'] == id:
                    self.last_quote_read = quote
                    my_quote = quote['quote']
                    break
        return my_quote


    def get_quote_info(self, quote_text):
        dir_path = path.dirname(path.realpath(__file__))
        quote_path = path.join(dir_path, '.\\txt_files\\quotes.json')
        with open(quote_path, 'r') as quote_file:
            quotes_data = json.load(quote_file)
            my_quote = 'I searched far and wide but I couldn\'t find anything.'
            for quote in quotes_data:
                if quote['quote'] == quote_text:
                    self.last_quote_read = quote
                    my_quote = quote
                    break
        return f"Quote: {my_quote['quote']}\ntimestamp: {my_quote['timestamp']}\nauthor: {my_quote['author']}\nid: {my_quote['id']}"


    def search_quote(self, search_string):
        dir_path = path.dirname(path.realpath(__file__))
        quote_path = path.join(dir_path, '.\\txt_files\\quotes.json')
        with open(quote_path, 'r') as quote_file:
            quotes_data = json.load(quote_file)
            matches = [quote['quote'] for quote in quotes_data if search_string in quote['quote'].lower()]
        length = sum(len(q) for q in matches)
        if length >= 2000:
            matches = ['I found way too many quotes matching your search. Try to be more specific.']
        if not matches:
            matches.append('I searched far and wide, but I couldn\'t find anything.')
        return matches


    def edit_quote(self, quote_id, new_quote):
        dir_path = path.dirname(path.realpath(__file__))
        quote_path = path.join(dir_path, '.\\txt_files\\quotes.json')
        okay = False
        with open(quote_path, 'r') as quote_file:
            quotes_data = json.load(quote_file)
            for quote in quotes_data:
                if quote['id'] == quote_id:
                    quote['quote'] = new_quote
                    okay = True
                    break
        if okay:
            self.write_to_json(quotes_data, quote_path)
        return okay


    def generate_insult(self):
        """
        Chooses a random adjective, swear word, and noun from their respective files
        and returns them as a single string.
        """
        try:
            with open(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\adjectives curated.txt', 'r') as adjfile:
                ladj = []
                line = adjfile.readline()
                while line:
                    ladj.append(line)
                    line = adjfile.readline()
            with open(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\swear words.txt', 'r') as swearfile:
                lswear = []
                line = swearfile.readline()
                while line:
                    lswear.append(line)
                    line = swearfile.readline()
            with open(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\nouns curated.txt', 'r') as nounfile:
                lnoun = []
                line = nounfile.readline()
                while line:
                    lnoun.append(line)
                    line = nounfile.readline()
        except FileNotFoundError:
            print(f'A file could not be opened. Please check the directory and try again.')
            return config.error_message
        adjchoice = random.choice(ladj).strip('\n').capitalize()
        swearchoice = random.choice(lswear).strip('\n')
        nounchoice = random.choice(lnoun).strip('\n')
        if nounchoice[0] == '-':
            # hyphenates the last two words if nounchoice starts with a '-'.
            return f'{adjchoice} {swearchoice}{nounchoice}'
        else:
            return f'{adjchoice} {swearchoice} {nounchoice}'

    def add_song(self, url):
        """Refreshes Spotify token, then adds songs to the "Hey Dude Check Out This
        Song" playlist.
        """
        self.spotify_refresh(self.sp_oauth)
        uri = f'spotify:track:{url}'
        # track_id has to be a list in order to be an acceptable arg to user_playlist_add_tracks()
        track_id = [uri]
        results = self.sp.user_playlist_add_tracks(config.USER, config.PLAY_LIST, track_id)    # pylint: disable=unused-variable
        with open(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\spotify_uri_log.txt', 'a') as uri_log_file:
            uri_log_file.write(f'{uri}\n')
        track_info = self.sp.track(uri)
        name = track_info['name']
        artist = track_info['artists'][0]['name']
        print(f'Added {name} by {artist} to hey-dude-check-out-this-song.')

    def dice_roll(self, msg):
        """
        Rolls inputted dice. Syntax is '!roll qdn + x',
        where q is the quantity of dice, n is the number of sides on the die, and x is the modifier.
        Examples of valid syntax are '!roll d20', '!roll 4d6', '!roll 2d8 + 2'.
        """
        if '+' in msg:
            try:
                # takes the quantity of dice to be rolled by finding the number before 'd'
                quantity = msg[6:msg.find('d')]
                if not quantity.isdigit():
                    quantity = 1
                else:
                    quantity = int(quantity)

                # takes number of sides as parameter by looking for the number between '!roll d' and '+'
                size = int(msg[msg.find('d') + 1:msg.find('+')])
                if size == 0:
                    return 'Ha, good one. Zero-sided die. Hilarious.'
                # takes the modifier as a parameter by finding the number after the '+'
                modifier = int(msg[msg.find('+') + 1:].strip())

                if quantity == 1:
                    raw_roll = random.randint(1, size)
                    end_roll = raw_roll + modifier
                    return f'{raw_roll} + {modifier} = **{end_roll}**'
                elif quantity > 1:
                    if quantity > 100000:
                        return 'wtf that\'s too many dude.'
                    rolls_list = []
                    for i in range(quantity):   # pylint: disable=unused-variable
                        rolls_list.append(random.randint(1, size))
                    raw_roll = sum(rolls_list)
                    print_message = ' + '.join(str(x) for x in rolls_list)
                    if quantity > 495:
                        return f'{raw_roll + modifier}'
                    return f'{print_message} + {modifier} = **{raw_roll + modifier}**'

            except ValueError:
                return 'Invalid syntax. Please try again.'
        else:   # '+' not in msg
            try:
                quantity = msg[6:msg.find('d')]
                if not quantity.isdigit():
                    quantity = 1
                else:
                    quantity = int(quantity)

                if quantity > 100000:
                    return 'Wtf that\'s too many dude.'

                size = int(msg[msg.find('d') + 1:])

                if size == 0:
                    return 'Ha, good one. Zero-sided die. Hilarious.'
                if quantity == 1:
                    roll = random.randint(1, size)
                    return f'{roll}'
                elif quantity > 1:
                    rolls_list = []
                    for i in range(quantity):
                        rolls_list.append(random.randint(1, size))
                    raw_roll = sum(rolls_list)
                    print_message = ' + '.join(str(x) for x in rolls_list)

                    if quantity > 497:
                        return f'{raw_roll}'

                    return f'{print_message} = **{raw_roll}**'
            except ValueError:
                return 'Invalid syntax. Please try again.'

    def roll_char(self):
        rolls = []
        for i in range(6):                         # pylint: disable=unused-variable
            temp = []
            for j in range(4):                     # pylint: disable=unused-variable
                temp.append(random.randint(1, 6))
            temp = sorted(temp)
            lowest = temp[0]
            temp.remove(lowest)
            rolls.append(sum(temp))
        return str(rolls).strip('[]')

    def tweet(self, text):
        """Returns True and tweets if the message is OK, else returns false.

        Specifically, checks the length of the message and if it contains any
        forbidden words.
        """
        """
        # deprecated:
        words = text.split()
        for word in words:
            if word.lower() in FORBIDDEN_WORDS:
                return False
        """
        if any(word in text.lower() for word in config.FORBIDDEN_WORDS):
            return False
        if len(text) <= 280:
            self.twitter_api.update_status(text)
            return True
        return False

    def mock_str(self, msg):
        """rEtUrNs mSg iN sPoNgEcAsE"""
        new_msg = ''
        i = 1
        for char in msg:
            if i > 0:
                new_msg += char.lower()
            else:
                new_msg += char.upper()
            i = i * -1
        return new_msg

    """
    # Obsolete version of gif scraper. Scrapped in favor of Giphy, which has an API.
    def scrape_gifs(self):
        #Scrapes top 25 gifs from tenor and returns them in a list.S
        headers = {
            # gives browser headers for requests to pass to the site to prevent blocking
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
            }

        url = 'https://tenor.com/search/reaction-gifs'
        try:
            req = requests.get(url, headers)
            soup = BeautifulSoup(req.content, 'html.parser')
        except Exception as e:
            print(f'Error while scraping gifs: {e}')
            gifs = ['Gif source seems to be down at the moment. Please contact your supreme leader for maintenance.']
            return gifs
        chunk = soup.find(class_='homepage')
        if not chunk:
            chunk = soup.find(class_='search')
        images = chunk.find_all('img', limit=25)
        gifs = []
        for image in images:
            url = str(image['src'])
            if url.startswith('/assets'):
                # sometimes chunk.find_all() picks up directories instead of gif URLs
                pass
            else:
                gifs.append(url)
        return gifs
    """
    def scrape_gifs(self, n_gifs=5):
        """Scrapes the top n_gifs gifs from giphy's trending page."""
        url = f"http://api.giphy.com/v1/gifs/search?q=reaction&api_key=0aklWITv0o79rS6a3GjkCKbNG5jekF3r&limit={n_gifs}"
        with urllib.request.urlopen(url) as response:
            response_data = json.loads(response.read())
        gif_data = response_data['data']
        gifs = [gif['url'] for gif in gif_data]
        return gifs

    def write_to_json(self, data, filename):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4, default=str)
