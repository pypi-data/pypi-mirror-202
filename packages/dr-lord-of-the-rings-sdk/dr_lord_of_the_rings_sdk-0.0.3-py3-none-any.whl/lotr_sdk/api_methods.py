import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from lotr_sdk.conf import BASE_URL, API_KEY

# Create session and add authorization header
session = requests.Session()
session.headers.update({"Accept": "application/json", "Authorization": f"Bearer {API_KEY}"})

# Create Retry object with desired settings
retries = Retry(
    total=5,
    backoff_factor=0.1,
    status_forcelist=[500, 501, 502, 504],
)

# Mount Retry to the session for all requests
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))


class ApiMethods:
    """Class containing methods for making API calls"""

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._id}>"

    @property
    def endpoint(self):
        return f"{BASE_URL}/{self.__class__.__name__.lower()}"

    @classmethod
    def get(cls, id=None, _id=None, movie=None):
        """
        Retrieves data from the API and returns the result of the query
        :param id (str): the unique identifier to query
        :param _id (str): the unique identifier to query
        :param movie (str): the unique identifier of the movie to get quotes from
        """
        url = f"{BASE_URL}/{cls.__name__.lower()}"
        if id is not None:
            url = f"{url}/{id}"
        elif _id is not None:
            url = f"{url}/{_id}"
        elif movie is not None:
            url = f"{url}?movie={movie}"
        resp = session.get(url)
        results = resp.json()["docs"] if "docs" in resp.json() else [resp.json()]
        result = results[0] if len(results) == 1 else results
        return cls(**result) if isinstance(result, dict) else result
