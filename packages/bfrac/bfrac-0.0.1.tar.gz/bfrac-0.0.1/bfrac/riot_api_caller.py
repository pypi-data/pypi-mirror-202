"""
RiotAPICaller
Manages the waiting times and calls any given endpoint url.
"""

import time
from collections import deque
import requests


class RequestError(Exception):
    """
    RequestError is an Exception
    Raised when the RiotAPI sends an error code instead of 200
    """

    def __init__(self, in_status_code, in_text):
        msg = f"Request returned an error: {in_status_code} -> {in_text}."
        super().__init__(msg)


class RiotAPICaller:
    """
    RiotAPICaller is the main class of this package.
    Keeps track of requests timers.
    """

    def __init__(self, in_app_config, in_last_use=120):
        """
        in_app_config : AppConfig object
        in_last_use : Float the number of seconds the API was used before the creation of this object
        """
        self.config = in_app_config
        #
        # burst : 20 requests per 1 second
        self._burst_queue = deque(maxlen=20)
        self._burst_queue.extend(
            (time.time() - in_last_use for i in range(20)))
        #
        # long : 100 requests per 2 minutes (120 seconds)
        self._long_queue = deque(maxlen=100)
        self._long_queue.extend(
            (time.time() - in_last_use for i in range(100)))

    def _connect_to_endpoint(self, url, params):
        response = requests.request("GET", url, headers={
                                    "X-Riot-Token": self.config.get_key()}, 
                                    params=params, timeout=3600)
        print(response.status_code)
        if response.status_code != 200:
            print(response)
            print(response.json())
            raise RequestError(response.status_code, response.text)
        return response.json()

    def _wait_rate_limit(self):
        # check long queue 1st
        current_time = time.time()
        long_elapsed_time = current_time - self._long_queue[0]
        burst_elapsed_time = current_time - self._burst_queue[0]
        max_wait = max(0, 120.0001 - long_elapsed_time, 1.0001 - burst_elapsed_time)
        if max_wait != 0:
            print(f"Waiting for : {max_wait}")
            time.sleep(max_wait)
            current_time = time.time()
        self._burst_queue.append(current_time)
        self._long_queue.append(current_time)

    def call_riotapi(self, in_url, in_params):
        """
        Calls the end point given in the url with the given params.
        Waits for the appropriate amount of time.
        """
        self._wait_rate_limit()
        json_response = self._connect_to_endpoint(in_url, in_params)
        return json_response
