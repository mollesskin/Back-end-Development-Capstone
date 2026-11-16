import os
from unittest.mock import Mock, patch
from django.test import TestCase, override_settings
from django.urls import reverse
import requests

@override_settings(ALLOWED_HOSTS=['testserver'])
class ServicePagesTests(TestCase):
    def test_missing_configuration_is_explicit(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertContains(self.client.get(reverse('songs')), 'not configured', status_code=503)
    @patch.dict(os.environ, {'SONGS_API_URL':'https://songs.example/'})
    @patch('concert.views.req.get')
    def test_songs_from_service(self, get):
        get.return_value=Mock(json=lambda:{'songs':[{'id':42,'title':'Live API song','lyrics':'Example lyrics'}]})
        self.assertContains(self.client.get(reverse('songs')), 'Live API song')
        get.assert_called_once_with('https://songs.example/song',timeout=10)
    @patch.dict(os.environ, {'PICTURES_API_URL':'https://pictures.example'})
    @patch('concert.views.req.get')
    def test_photos_from_service(self, get):
        get.return_value=Mock(json=lambda:[{'id':2,'pic_url':'https://example.org/photo.png','event_city':'Astana','event_state':'Akmola','event_date':'2026-11-16'}])
        self.assertContains(self.client.get(reverse('photos')), 'Astana')
        get.assert_called_once_with('https://pictures.example/picture',timeout=10)
    @patch.dict(os.environ, {'SONGS_API_URL':'https://songs.example'})
    @patch('concert.views.req.get',side_effect=requests.Timeout())
    def test_timeout_shows_error(self,get):
        self.assertContains(self.client.get(reverse('songs')), 'temporarily unavailable',status_code=503)
    @patch.dict(os.environ, {'SONGS_API_URL':'https://songs.example'})
    @patch('concert.views.req.get')
    def test_invalid_payload_shows_error(self,get):
        get.return_value=Mock(json=lambda:{'unexpected':'value'})
        self.assertContains(self.client.get(reverse('songs')), 'temporarily unavailable',status_code=503)
