# flex_telegram_bot/__init__.py
import requests

class TelegramBot:
    def __init__(self, token):
        self.base_url = f'https://api.telegram.org/bot{token}'
        self.commands = {}

    def komut_ekle(self, komut, cevap):
        self.commands[komut] = cevap

    def mesaj_gonder(self, chat_id, metin):
        url = f'{self.base_url}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': metin
        }
        response = requests.post(url, data=payload)
        return response.json()

    def komutlara_cevap_ver(self, chat_id, komut):
        if komut in self.commands:
            cevap = self.commands[komut]
            self.mesaj_gonder(chat_id, cevap)

    def get_updates(self):
        url = f'{self.base_url}/getUpdates'
        response = requests.get(url)
        return response.json()
