import requests


class VKAPIHandler:
    def __init__(self, token):
        self.token = token
        self.api_version = '5.131'
        self.base_url = 'https://api.vk.com/method/'

    def _make_request(self, method, params):
        params.update({
            'access_token': self.token,
            'v': self.api_version
        })
        response = requests.get(f'{self.base_url}{method}', params=params)
        data = response.json()

        if 'error' in data:
            error_msg = data['error']['error_msg']
            raise Exception(f"API Error: {error_msg}")
        return data['response']

    def get_user_info(self, user_id):
        if user_id:
            params = {
                'user_ids': user_id,
                'fields': 'first_name,last_name,bdate,city,country'
            }
        else:
            params = {
                'fields': 'first_name,last_name,bdate,city,country'
            }
        response = self._make_request('users.get', params)
        return response[0] if response else None

    def resolve_screen_name(self, screen_name):
        """Преобразует короткое имя (screen_name) в числовой ID"""
        params = {
            'screen_name': screen_name
        }
        response = self._make_request('utils.resolveScreenName', params)
        return response.get('object_id') if response else None

    def get_friends(self, user_id):
        # Получаем числовой ID даже если введен screen_name
        if not str(user_id).isdigit():
            user_id = self.resolve_screen_name(user_id)
            if not user_id:
                raise ValueError("Пользователь не найден")

        params = {
            'user_id': user_id,
            'fields': 'first_name,last_name',
            'count': 5000
        }
        response = self._make_request('friends.get', params)
        return response['items']

    def get_albums(self, user_id):
        # Аналогично для альбомов
        if not str(user_id).isdigit():
            user_id = self.resolve_screen_name(user_id)
            if not user_id:
                raise ValueError("Пользователь не найден")

        params = {
            'owner_id': user_id,
            'need_system': 0
        }
        response = self._make_request('photos.getAlbums', params)
        return response['items']