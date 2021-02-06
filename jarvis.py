import sys
import time
import webbrowser
import yfinance as yf # to fetch financial data
from utils import text_to_speech, speech_to_text, is_keywords


class Jarvis:
    
    def __init__(self):
        self.user_name = ''
    
    def respond(self, voice_text):
        print(voice_text)
        if voice_text:
            # Name
            if is_keywords(  # check stop words
                text=voice_text.lower(), 
                key_words=['comment', 'quel', 'ton', 'tu', 'vous']
                ) and is_keywords(  # check important words
                    text=voice_text.lower(),
                    key_words=['appelle', 'prenom', 'prénom', 'nom']
                ):
                self.ask_my_name()
            # Search on Google
            if is_keywords(
                text=voice_text.lower(),
                key_words=['recherche']
            ) and is_keywords(
                text=voice_text.lower(),
                key_words=['google']
            ):
                voice_google_search = speech_to_text(question='Que voulez-vous que je recherche pour vous ?' + self.user_name)
                url = f"https://google.fr/search?q={voice_google_search}"
                webbrowser.get().open(url)
            # Go on Youtube
            if is_keywords(
                text=voice_text.lower(),
                key_words=['youtube']
            ):
                voice_youtube_search = speech_to_text(question='Que voulez-vous faire sur Youtube ?' + self.user_name)
                if is_keywords(
                    text=voice_youtube_search.lower(),
                    key_words=['tendance']):
                    webbrowser.get().open('https://www.youtube.com/feed/trending')
                elif is_keywords(
                    text=voice_youtube_search.lower(),
                    key_words=['abonnement']):
                    webbrowser.get().open('https://www.youtube.com/feed/subscriptions')
                else:
                    url = f"https://www.youtube.com/results?search_query={voice_youtube_search}"
                    webbrowser.get().open(url)
            # Stock Price
            if is_keywords(
                    text=voice_text.lower(),
                    key_words=['cour', 'prix', 'action', 'bourse']):
                stocks = {
                    "apple": "AAPL",
                    "microsoft": "MSFT",
                    "facebook": "FB",
                    "tesla": "TSLA",
                    "bitcoin": "BTC-USD",
                    #"dinar": "EUR-TND",
                    "dollar": "USD"
                }
                search_stock = None
                for s in stocks.keys():
                    if s in voice_text.lower():
                        search_stock = s
                        break
                try:
                    stock = stocks[search_stock]
                    stock = yf.Ticker(stock)
                    price = stock.info["regularMarketPrice"]
                    
                    text_to_speech(text=f'Le prix du {search_stock} est de {price} {stock.info["currency"]} {self.user_name}', filename="cour")
                    print(f'Le prix du {search_stock} est de {price} {stock.info["currency"]} {self.user_name}')
                except:
                    text_to_speech(text='Une erreur est survenu lors de la recherche du prix du cour' + self.user_name, filename="erreur")
            # Sayonara! Bye!
            if is_keywords(
                text=voice_text.lower(),
                key_words=['rien', 'fin', 'aurevoir', 'bye']
            ):
                text_to_speech(text='Aurevoir et à très vite ' + self.user_name, filename="sayonara")
                sys.exit(0)

                
    
    def get_user_name(self):
        question = 'Comment vous appelez vous ?'
        voice_text = speech_to_text(question=question)
        if voice_text is not None:
            self.user_name =  [x for x in voice_text.split() 
                            if x.lower() not in [
                                'je', 
                                'm\'appelle', 
                                'm\'',
                                'm', 
                                'appelle',
                                'mon',
                                'prenom',
                                'nom',
                                'est'
                                ]
                            ]
            self.user_name = ' '.join(self.user_name).strip()
        print(self.user_name)
        text_to_speech(text="Enchanté " + self.user_name + " Moi je m'appelle Jarviset", filename='vocal_assistant_name')
    
    def ask_my_name(self):
        text_to_speech(text="Alors, je m'appelle Jarviset", filename='vocal_assistant_name')
        
    def vocal_assistant(self):
        while True:
            voice_text = speech_to_text(question='Comment puis-je vous aider ?')
            self.respond(voice_text=voice_text)
            time.sleep(1)