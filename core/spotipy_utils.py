from spotipy import CacheHandler

class DjangoCacheHandler(CacheHandler):

    def get_cached_token(self):
        current_user = None # Fill me in
        token_info = {
            'expires_at': current_user.expires_at,
            'access_token': current_user.access_token,
            'expires_in': current_user.expires_in,
            'scope': current_user.scope,
            'refresh_token': current_user.refresh_token,
        }

        return token_info

    def save_token_to_cache(self, token_info):
        # This should only run for refreshes

        current_user = None # fill me in
        current_user(**token_info)
        current_user.save()

        return None
