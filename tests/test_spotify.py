import pytest
from src.spotify_to_saavn.spotify import SpotifyClient
from src.spotify_to_saavn.logger import setup_logger

logger = setup_logger(__name__)

def test_get_user_playlists(mocker):
    # Arrage a mock spotipy.Spotify client
    mock_spotify_instance = mocker.MagicMock()
    mock_spotify_instance.current_user_playlists.return_value = {
        'items': [
            {'name': 'Workout mix', 'id': '123'},
            {'name': 'Chill Vibes', 'id': '456'},
        ]
    }
    logger.info("Successfully mocked spotipy.Spotify client for get_user_playlists")

    mocker.patch('src.spotify_to_saavn.spotify.spotipy.Spotify', return_value=mock_spotify_instance)
    mocker.patch('src.spotify_to_saavn.spotify.SpotifyOAuth', return_value=mocker.MagicMock())
    client = SpotifyClient()
    playlists = client.get_user_playlists()

    assert len(playlists) == 2
    assert playlists[0]['name'] == 'Workout mix'
    assert playlists[1]['id'] == '456'
    mock_spotify_instance.current_user_playlists.assert_called_once()

def test_get_playlist_tracks(mocker):
    mock_spotify_instance = mocker.MagicMock()

    mock_spotify_instance.playlist_items.return_value = {
        'items': [
            {
                'track': {
                    'name': 'Shape of You',
                    'artists': [{'name': 'Ed Sheeran'}],
                    'external_ids': {'isrc': 'GB12345'}
                }
            },
            {
                'track': {
                    'name': 'Blinding Lights',
                    'artists': [{'name': 'The Weeknd'}],
                    'external_ids': {'isrc': 'US56789'}
                }
            }
        ]
    }

    mocker.patch('src.spotify_to_saavn.spotify.spotipy.Spotify', return_value=mock_spotify_instance)
    mocker.patch('src.spotify_to_saavn.spotify.SpotifyOAuth')

    client = SpotifyClient()
    tracks = client.get_playlist_tracks('fake_playlist_id_123')

    assert len(tracks)==2
    assert tracks[0]['name'] == 'Shape of You'
    assert tracks[0]['artist'] == 'Ed Sheeran'
    assert tracks[1]['name'] == 'Blinding Lights'

    mock_spotify_instance.playlist_items.assert_called_once_with('fake_playlist_id_123')

    def get_playlist_tracks_with_pagination(mocker):
        mock_spotify_instance = mocker.MagicMock()

        page_1 = {
            'items': [
                {
                    'track': {
                        'name': 'Song 1',
                        'artists': [{'name': 'Artist 1'}]}}
            ],
            'next': 'http://api.spotify.com/v1/playlists/.../tracks?offset=100'
        }

        page_2 = {
            'items': [
                {
                    'track': {
                        'name': 'Song2',
                        'artist': [{'name':'Artist 2'}]
                    }
                }
            ],
            'next': None
        }
            
        mock_spotify_instance.playlist_itesm.return_value = page_1
        mock_spotify_instance.next.return_value = page_2

        mocker.patch('src.spotify_to_saavn.spotify.spotipy.Spotify', return_value=mock_spotify_instance)
        mocker.patch('src.spotify_to_saavn.spotify.SpotifyOAuth')

        client = SpotifyClient()
        tracks = client.get_playlist_tracks('fake_playlist_id_123')

        assert len(tracks) == 2
        assert tracks[0]['name'] == 'Song 1'
        assert tracks[1]['name'] == 'Song 2'

        mock_spotify_instance.playlist_items.assert_called_once_with('fake_playlist_id_123')
        mock_spotify_instance.next.assert_called_once_with(page_1)

def test_get_playlist_tracks_with_pagination(mocker):
    """This is to test the usage of side_effect to test data without hardcoding the pagination data for every page"""
    mock_spotify_instance = mocker.MagicMock()
    
    page_1 = {
        'items': [
            {
                'track': {
                    'name': 'Song 1',
                    'artists': [{'name': 'Artist 1'}],
                }
            }
        ],
        'next': 'http://api.spotify.com/page2',
    }

    page_2 = {
        'items': [
            {
                'track': {
                    'name': 'Song 2',
                    'artists': [{'name': 'Artist 2'}],
                }
            }
        ],
        'next': 'http://api.spotify.com/page3',
    }

    page_3 = {
        'items': [
            {
                'track': {
                    'name': 'Song 3',
                    'artists': [{'name': 'Artist 3'}],
                }
            }
        ],
        # Last page with no next pointer
        'next': None
    }

    mock_spotify_instance.playlist_items.return_value = page_1

    # side_effect takes all the pages that shoudl be called for for next, (sequentially returns in the same order of list)
    mock_spotify_instance.next.side_effect = [page_2, page_3]

    # Mocking 2 required instances
    mocker.patch('src.spotify_to_saavn.spotify.spotipy.Spotify', return_value=mock_spotify_instance)
    mocker.patch('src.spotify_to_saavn.spotify.SpotifyOAuth')

    client = SpotifyClient()
    tracks = client.get_playlist_tracks('fake_playlist_id_123')

    assert len(tracks) == 3
    assert tracks[0]['name'] == 'Song 1'
    assert tracks[1]['name'] == 'Song 2'
    assert tracks[2]['name'] == 'Song 3'

    mock_spotify_instance.playlist_items.assert_called_once_with('fake_playlist_id_123')
    assert mock_spotify_instance.next.call_count == 2
    
