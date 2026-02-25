import pytest
from src.spotify_to_saavn.saavn import SaavnClient

def test_search_song_success(mocker):
    # making mock objects for responses
    mock_response = mocker.MagicMock()
    # setting to 200 for success test
    mock_response.status_code = 200

    # simulating a response from saavn search api
    mock_response.json.return_value = {
        'status': 'SUCCESS',
        'results': [
            {
                'id': 'S12345',
                'title': 'Shape of You',
                'singers': 'Ed Sheeran',
                'url': 'https://www.jiosaavn.com/song/shape-of-you/...'
            }
        ]
    }

    # mocking the request.get function to deliver above response
    mock_get = mocker.patch('src.spotify_to_saavn.saavn.requests.get', return_value=mock_response)

    client = SaavnClient()
    result = client.search_song("Shape of You Ed Sheeran")

    # asserting a valid response
    assert result is not None
    assert result['id'] == 'S12345'
    assert result['title'] == 'Shape of You'

    mock_get.assert_called_once()   # ensures the endpoint is called exactly once - not more, not less
    args, kwargs = mock_get.call_args      # args are the arguments and kwargs are keyword arguments
    # requests.get("https://api.example.com", params={"query": "something"})
    # in this, url is a tuple and is a positional argument, params is a dictionary and are keyword arguments

    assert "query" in kwargs['params']      # checks if query is in keyword arguments passed
    assert kwargs['params']['query'] == 'Shape of You Ed Sheeran'   # Checks the exact search query extracted from the mock response
