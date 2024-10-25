import requests

class TelegramBot:
    def __init__(self, token):
        self.base_url = f'https://api.telegram.org/bot{token}'
        self.commands = {}

    def komut_ekle(self, komut, cevap):
        if isinstance(cevap, tuple) and len(cevap) == 2:
            self.commands[komut] = lambda chat_id: (self.mesaj_gonder(chat_id, cevap[0]),
                                                    self.dosya_gonder(chat_id, cevap[1]))
        elif isinstance(cevap, str):
            if cevap.endswith(".txt") or cevap.endswith(".pdf") or cevap.endswith(".png"):
                self.commands[komut] = lambda chat_id: self.dosya_gonder(chat_id, cevap)
            else:
                self.commands[komut] = lambda chat_id: self.mesaj_gonder(chat_id, cevap)
        elif callable(cevap):
            self.commands[komut] = cevap

    def mesaj_gonder(self, chat_id, metin):
        url = f'{self.base_url}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': metin
        }
        response = requests.post(url, data=payload)
        return response.json()

    def dosya_gonder(self, chat_id, dosya_yolu):
        url = f'{self.base_url}/sendDocument'
        try:
            with open(dosya_yolu, 'rb') as dosya:
                payload = {
                    'chat_id': chat_id
                }
                files = {
                    'document': dosya
                }
                response = requests.post(url, data=payload, files=files)
            return response.json()
        except Exception as e:
            self.mesaj_gonder(chat_id, f"Hata: {str(e)}")

    def komutlara_cevap_ver(self, chat_id, komut):
        if komut in self.commands:
            self.commands[komut](chat_id)

    def get_updates(self):
        url = f'{self.base_url}/getUpdates'
        response = requests.get(url)
        return response.json()

    def process_updates(self):
        """
        Alınan güncellemeleri işleyerek geçerli mesajları komutlara yönlendirir.
        """
        updates = self.get_updates()
        for update in updates['result']:
            if 'message' in update and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                text = update['message']['text']
                self.komutlara_cevap_ver(chat_id, text)
            else:
                print("Geçersiz güncelleme:", update)
