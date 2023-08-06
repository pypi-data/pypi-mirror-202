import requests, eitaa
from bs4 import BeautifulSoup
from os.path import isfile

class Nany:
    def __init__(self, auth: str) -> str:
        self.auth = auth
    def getMe(self):
        url = f"https://eitaayar.ir/api/{self.auth}/getMe"
        return requests.get(url=url).json()
    def sendMessage(self, Chat_id: str, Message: str):
        url = f"https://eitaayar.ir/api/{self.auth}/sendMessage?chat_id={Chat_id}&text={Message}"
        return requests.get(url=url).json()
    def send_file(self, chat_id, caption, file, pin=False, view_to_delete=-1,
                disable_notification=False, reply_to_message_id=None):
        if not isfile(file):
            raise Exception(f"File `{file}` not found")

        r = requests.post(
            f"https://eitaayar.ir/api/{self.token}/sendFile",
            data={
                'chat_id': chat_id,
                'caption': caption,
                'pin': int(pin),
                'viewCountForDelete': view_to_delete,
                'disable_notification': int(disable_notification),
                'reply_to_message_id' : reply_to_message_id if reply_to_message_id != None else '',
            },
            files={
                'file': open(file, 'rb'),
            }
        )
        return r.json()
    
    @staticmethod
    def getChannelInfo(channel_id):
        r = requests.get(f"https://eitaa.com/{channel_id}")
        soup = BeautifulSoup(r.text, 'html.parser')
        result = {}
        if len(soup.find_all('div',attrs={'class':'etme_body_wrap'})) != 0:
            account_name = soup.find('div',attrs={'class':'etme_page_title'}).find('span').text

            image_url = soup.find('img',attrs={'class':'etme_page_photo_image'})['src']

            is_verified = bool(len(soup.find_all('i',attrs={'class' : 'verified-icon'})))

            result = {
                'name' : account_name,
                'image_url' : image_url,
                'is_verified' : is_verified,
                'is_channel' : False,
                'users' : None,
                'description' : None,
            }
        else :
            channel_name = soup.find('div', attrs = {'class':'etme_channel_info_header_title'}).find('span').text
            
            channel_image_url = soup.find('i', attrs = {'class':'etme_page_photo_image'}).find('img')['src']

            users_count = soup.find('span', attrs = {'class':'counter_value'}).text.replace('هزار','K')
            
            description = soup.find('div', attrs = {'class':'etme_channel_info_description'}).text.replace('\\u200c',' ')

            is_verified = bool(len(soup.find_all('i',attrs={'class' : 'verified-icon'})))

            result = {
                'name' : " ".join(channel_name.split()),
                'image_url' : channel_image_url,
                'users' : users_count,
                'description' : description,
                'is_verified' : is_verified,
                'is_channel' : True,
            }
        return result
    @staticmethod
    def Last_Message(channel_id):
        r = requests.get(f"https://eitaa.com/{channel_id}")
        soup = BeautifulSoup(r.text, 'html.parser')
        pure_messages = soup.find_all('div',attrs={'class':'etme_widget_message_bubble'})
        messages = []

        for message in pure_messages :
            image_link = soup.find('a',attrs={'class':'etme_widget_message_photo_wrap'})['style']
            image_link = image_link.split('url(\'')[1][:-2]
            
            message_text = soup.find('div',attrs={'class':'etme_widget_message_text'}).text
            views = soup.find('span',attrs={'class':'etme_widget_message_views'}).text.replace('میلیون','M')
            time = soup.find('span',attrs={'class':'etme_widget_message_meta'}).text

            messages.append({
                'image_link' : image_link,
                'text' : message_text,
                'views' : views,
                'time' : time
            })
        print(len(messages))
        return messages
    
    @staticmethod
    def getTrends():
        result = {
            "last_12_hours": [],
            "last_24_hours": [],
            "last_7_days": [],
            "last_30_days": [],
        }

        r = requests.get(
            f"https://trends.eitaa.com"
        )

        soup = BeautifulSoup(r.text, 'html.parser')

        last_12_hours = soup.find("div",{"class":"col-xl-3 col-lg-6 col-md-6 col-sm-12 animateIn animated zoomInLeft"})
        last_24_hours = soup.find("div",{"class":"col-xl-3 col-lg-6 col-md-6 col-sm-12 animateIn animated zoomInDown"})
        last_7_days = soup.find("div",{"class":"col-xl-3 col-lg-6 col-md-6 col-sm-12 animateIn animated zoomInRight"})
        last_30_days = soup.find("div",{"col-xl-3 col-lg-6 col-md-6 col-sm-12 animateIn animated zoomInUp"})

        for trend in last_12_hours.find_all("div",{"class":"row item"}):
            trend_name = trend.find("div",{"class":"col-9 text-right hashtag"})
            trend_count = trend.find("div",{"class":"col-3 text-left number"})

            result["last_12_hours"].append({
                "name": trend_name.text,
                "count": trend_count.text,
            })

        for trend in last_24_hours.find_all("div",{"class":"row item"}):
            trend_name = trend.find("div",{"class":"col-9 text-right hashtag"})
            trend_count = trend.find("div",{"class":"col-3 text-left number"})

            result["last_24_hours"].append({
                "name": trend_name.text,
                "count": trend_count.text,
            })
        
        for trend in last_7_days.find_all("div",{"class":"row item"}):
            trend_name = trend.find("div",{"class":"col-9 text-right hashtag"})
            trend_count = trend.find("div",{"class":"col-3 text-left number"})

            result["last_7_days"].append({
                "name": trend_name.text,
                "count": trend_count.text,
            })

        for trend in last_30_days.find_all("div",{"class":"row item"}):
            trend_name = trend.find("div",{"class":"col-9 text-right hashtag"})
            trend_count = trend.find("div",{"class":"col-3 text-left number"})

            result["last_30_days"].append({
                "name": trend_name.text,
                "count": trend_count.text,
            })
        return result
class Nany_Robot(Nany):
    ...