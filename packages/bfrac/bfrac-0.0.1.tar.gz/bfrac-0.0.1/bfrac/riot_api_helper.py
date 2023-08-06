class RiotAPIHelper:
    """
    Helper class containing static methods for calling common riot api endpoints.
    """
    lol_servers = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "ph2", "ru", "sg2", "th2", "tr1",
                   "tw2", "vn2"]
    lol_continents = ["americas", "asia", "europe", "sea"]

    """
    The AMERICAS routing value serves NA, BR, LAN and LAS.
    The ASIA routing value serves KR and JP.
    The EUROPE routing value serves EUNE, EUW, TR and RU.
    The SEA routing value serves OCE, PH2, SG2, TH2, TW2 and VN2.
    """

    @staticmethod
    def url_summoner_by_name(in_region_server, in_summoner_name):
        return f"https://{in_region_server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{in_summoner_name}"

    @staticmethod
    def url_summoner_by_puuid(in_region_server, in_encrypted_puuid):
        return f"https://{in_region_server}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{in_encrypted_puuid}"

    @staticmethod
    def url_match_list_by_summoner_puuid(in_region_continent, in_puuid):
        return f"https://{in_region_continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{in_puuid}/ids"

    @staticmethod
    def url_match_info(in_region_continent, in_match_id):
        return f"https://{in_region_continent}.api.riotgames.com/lol/match/v5/matches/{in_match_id}"

    @staticmethod
    def url_match_timeline(in_region_continent, in_match_id):
        return f"https://{in_region_continent}.api.riotgames.com/lol/match/v5/matches/{in_match_id}/timeline"

    @staticmethod
    def get_summoner_by_name(in_riot_api_caller, in_region, in_summoner_name):
        url = RiotAPIHelper.url_summoner_by_name(in_region, in_summoner_name)
        return in_riot_api_caller.call_riotapi(url, {})

    @staticmethod
    def get_matches_list(in_riot_api_caller, in_region_continent, in_summoner_puuid, in_params={}):
        url = RiotAPIHelper.url_match_list_by_summoner_puuid(in_region_continent, in_summoner_puuid)
        return in_riot_api_caller.call_riotapi(url, in_params)

    @staticmethod
    def get_match_info(in_riot_api_caller, in_region_continent, in_match_id):
        url = RiotAPIHelper.url_match_info(in_region_continent, in_match_id)
        return in_riot_api_caller.call_riotapi(url, {})

    @staticmethod
    def get_match_timeline(in_riot_api_caller, in_region_continent, in_match_id):
        url = f"https://{in_region_continent}.api.riotgames.com/lol/match/v5/matches/{in_match_id}/timeline"
        return in_riot_api_caller.call_riotapi(url, {})
