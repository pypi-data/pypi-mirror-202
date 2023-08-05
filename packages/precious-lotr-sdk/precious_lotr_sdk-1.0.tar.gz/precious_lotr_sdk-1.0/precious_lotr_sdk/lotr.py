import requests

class LOTRSDK:
    BASE_URL = 'https://the-one-api.dev/v2/movie'

    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(self, endpoint):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_movies(self):
        return self._make_request(LOTRSDK.BASE_URL)

    def get_movie(self, movie_id):
        return self._make_request(f'{LOTRSDK.BASE_URL}/{movie_id}')

    def get_movie_quotes(self, movie_id):
        return self._make_request(f'{LOTRSDK.BASE_URL}/{movie_id}/quote')
