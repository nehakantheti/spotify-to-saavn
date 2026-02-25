import pytest
from src.spotify_to_saavn.transfer import TransferManager

def test_transfer_playlist_workflow(mocker):
    mock_spotify = mocker.MagicMock()
    mock_saavn = mocker.MagicMock()

    # making mock spotify return 2 tracks
    mock_spotify.get_playlist_tracks.return_value = [
        {'name': 'Shape of You', 'artist': 'Ed Sheeran'},
        {'name': 'Obscure Indie Song', 'artist':'Local Band'}
    ]

    # making saavn mock the first search result successfully, but 2nd one to return None
    mock_saavn.search_song.side_effect = [
        {'id': 'S123', 'title': 'Shape of You', 'singers': 'Ed Sheeran'},
        None
    ]

    manager = TransferManager(spotify_client=mock_spotify, saavn_client=mock_saavn)

    matched_ids, missing_tracks = manager.get_jiosaavn_track_ids('fake_playlist_id_123')

    assert len(matched_ids) == 1
    assert matched_ids[0] == 'S123'

    # mocked only one missing track
    assert len(missing_tracks) == 1
    assert missing_tracks[0]['name'] == 'Obscure Indie Song'

    mock_spotify.get_playlist_tracks.assert_called_once_with('fake_playlist_id_123')
    assert mock_saavn.search_song.call_count == 2
