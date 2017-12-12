import argparse
from time import sleep
from datetime import datetime

from vklancer import api

PHOTO_COUNT = 100
SLEEP_TIME = 0.34


def parse_arguments():
    parser = argparse.ArgumentParser(description='Программа для получения комментариев из альбома vkontakte')
    parser.add_argument('link', metavar='L', type=str, help='ссылка на альбом vk')
    album_link = parser.parse_args().link
    return album_link


def get_readable_date(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y.%m.%d %H:%M:%S')


def find_by_flag(data_list, flag):
    return next(filter(lambda x: x.startswith(flag), data_list), '').replace(flag, '')


def with_sleep(func):
    def decorated(*args, pause=SLEEP_TIME, **kwargs):
        sleep(pause)
        return func(*args, **kwargs)
    return decorated


class VKConnector(object):
    API_VERSION = '5.6'

    def __init__(self, token, version=API_VERSION):
        self.vk_api = api.API(token=token,
                              version=version)

    @with_sleep
    def get_comments(self, owner_id, album_id, offset=0, count=PHOTO_COUNT):
        return self.vk_api.photos.getAllComments(owner_id=owner_id,
                                                 album_id=album_id,
                                                 offset=offset,
                                                 count=count)['response']

    @with_sleep
    def get_user_data(self, ids):
        return self.vk_api.users.get(user_ids=ids)['response']

    @with_sleep
    def get_image_data_by_id(self, owner_id, pic_id):
        return self.vk_api.photos.getById(photos=f'{owner_id}_{pic_id}')['response'][0]

    def get_photo_text(self, owner_id, album_id, pause=SLEEP_TIME):
        count = self.vk_api.photos.get(owner_id=owner_id,
                                       album_id=album_id,
                                       count=1)['response']['count']
        out = {}
        for i in range(count//1000+1):
            sleep(pause)
            r = self.vk_api.photos.get(owner_id=owner_id,
                                       album_id=album_id,
                                       count=1000,
                                       offset=i*100)['response']['items']
            out.update({item['id']: item['text'] for item in r})
        return out

    def get_users_json(self, data):
        out = {}
        for user in self.get_user_data(data):
            user_dict = {user['id']: {'name': f"{user['last_name']} {user['first_name']}",
                                      'user_page': f"https://vk.com/id{user['id']}"}}
            out.update(user_dict)
        return out

    def get_images_comments(self, owner, album):
        images = self.vk_api.photos.get(owner_id=owner, album_id=album)['response']['items']
        return {i['id']: i['text'] for i in images}
