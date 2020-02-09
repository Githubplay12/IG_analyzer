import json
import requests
import re

from bs4 import BeautifulSoup


# PhantomJs : "YourphantomJSlink"
# Chromedriver : "your Chromedriver link"

# Avg nb like / last 12 pictures
# Avg nb comments / last 12 pictures
# Nb followers
# Nb followings


class IGTracker():

    def __init__(self, username):
        profil_url = f'https://www.instagram.com/{username}/'

        # Solution 2 : with requests
        r = requests.get(profil_url)

        profil_soup2 = BeautifulSoup(r.text, 'html.parser')

        scripts = profil_soup2.find_all('script', type="text/javascript", text=re.compile('window._sharedData'))
        self.stringified_json = scripts[0].get_text().replace('window._sharedData = ', '')[:-1]



    def get_ig_data(self):

        global_json = json.loads(self.stringified_json)['entry_data']['ProfilePage'][0]['graphql']['user']

        #print(global_json)

        # global_json = (profil_soup2.find_all(type='text/javascript')[4].text.split('graphql":')[1].split('}]},"gatekeepers"')[0])
        list_nb_likes = []
        list_nb_comments = []

        for element in global_json['edge_owner_to_timeline_media']['edges'][1:]:
            nb_likes = element['node']['edge_liked_by']['count']
            nb_comments = element['node']['edge_media_to_comment']['count']
            list_nb_likes.append(nb_likes)
            list_nb_comments.append(nb_comments)

        nb_followers = global_json['edge_followed_by']['count']
        avg_likes = round(sum(list_nb_likes) / len(list_nb_likes))
        avg_comments = round(sum(list_nb_comments) / len(list_nb_comments))

        average_engagement_from_likes = f'{(avg_likes/nb_followers)*100:.2f} %'
        #average_engagement_from_comments = f'{(avg_comments/nb_followers)*100:.2f} %'

        ig_dict = {
            'full_name' : global_json['full_name'],
            'profil_pic' : global_json['profile_pic_url'],
            'followers' : nb_followers,
            'followings' : global_json['edge_follow']['count'],
            'posts' : global_json['edge_owner_to_timeline_media']['count'],
            'avg_likes' : avg_likes,
            'avg_comments' : avg_comments,
            'engagement' : average_engagement_from_likes
        }
        return json.dumps(ig_dict)


# Average likes and comments from html
"""
# Solution 1 : using selenium to extract data from html
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome("Chromedriverlinkhere", chrome_options=options)
        self.driver.get(profil_url)
        
        self.profil_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.nb_followers_driver = int(self.profil_soup.find(class_='g47SY', title=True)['title'].replace(',', ''))
        self.nb_following_driver = self.profil_soup.find_all(class_='g47SY')[2].text
        self.profil_pic_driver = self.profil_soup.find(class_='_6q-tv')['src']
        self.average_engagement_from_likes_driver = f'{(self.get_avg_likes_coms()[0]/self.nb_followers_driver)*100:.2f} %'

    def get_avg_likes_coms(self):
        
        list_nblikes = []
        list_nbcoms = []

        for picture in self.profil_soup.find_all(class_='v1Nh3', limit=12):
            link = picture.a['href']
            ig_post_url = f'https://www.instagram.com{link}'
            self.driver.get(ig_post_url)
            post_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            prettysoup_post = post_soup.prettify()

            # Getting the number of likes per post, little problem here : Posts under 12 are omitted
            # Works fine beside that
            nblikes_post = post_soup.find(class_='zV_Nj', role=True)
            if nblikes_post:
                # Appending each sum of comments to the likes list
                list_nblikes.append(int(nblikes_post.span.text.replace(',', '')))
            # If video
            else:
                nblikes_post = post_soup.find_all(content=True)[5]['content'].split(' ')[0].replace(',', '')
                # If superior than 10 K (not giving the exact value)
                try:
                    nblikes_post = int(nblikes_post)
                except ValueError:
                    nblikes_post = nblikes_post.split('k')[0]
                    bignum, littlenum = nblikes_post.split('.')
                    nblikes_post = int(bignum)*1000 + int(littlenum)*100

                # Appending each sum of comments to the likes list
                list_nblikes.append(nblikes_post)


            # Getting the number of commentaries excluding the owner of the page
            # The little problem here is that we are only getting 24 comments max (when big account, it matters)
            nbcoms_post = post_soup.find_all(class_='gElp9')
            i = 0
            for com in nbcoms_post:
                if com.a.text != self.username:
                    i += 1
            # Appending each sum of comments to the comments list
            list_nbcoms.append(i)

        # Calculating the average for comments and likes
        avg_likes = round(sum(list_nblikes)/len(list_nblikes))
        print(list_nbcoms)
        avg_coms = round(sum(list_nbcoms)/len(list_nbcoms))

        # Returning the values
        return avg_likes, avg_coms
"""

