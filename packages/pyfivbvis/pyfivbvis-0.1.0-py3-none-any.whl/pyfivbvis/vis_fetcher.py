import requests
from bs4 import BeautifulSoup

class FivbVis:

    def fetch_beach_tournament_list():
        """
        Fetch FIVB beach tournament list from VIS.

        Returns
        -------
        list of dicts:
            A list of ALL beach tournaments with fields such as No, Title, Type, etc.
            
        Notes
        ------
        Documentation:
            https://www.fivb.org/VisSDK/VisWebService/BeachTournament.html
        """
        # Create the XML request string
        xml_request = """
            <Requests>
                <Request Type='GetBeachTournamentList' 
                        Fields='No Title Type NoEvent Code Gender Name CountryCode 
                                StartDateQualification StartDateMainDraw 
                                EndDateQualification EndDateMainDraw 
                                NbTeamsQualification NbTeamsMainDraw 
                                NbTeamsFromQualification' />
            </Requests>
        """

        # Set the URL for the request
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"

        # Send the request
        try:
            res = requests.post(url, data=xml_request, headers={'Content-Type': 'text/xml'})
            res.raise_for_status()  # Raise an error for bad responses
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return []

        # Parse the XML response
        soup = BeautifulSoup(res.content, 'xml')
        tournaments = soup.find_all('BeachTournament')

        # Define the fields of interest
        fields = [
            "No", "Title", "Type", "NoEvent", "Code", 
            "Gender", "Name", "CountryCode", 
            "StartDateQualification", "StartDateMainDraw", 
            "EndDateQualification", "EndDateMainDraw", 
            "NbTeamsQualification", "NbTeamsMainDraw", 
            "NbTeamsFromQualification"
        ]

        # Extract tournament details using a list comprehension
        tourn_list = [
            {field: tournament.get(field) for field in fields}
            for tournament in tournaments
        ]

        return tourn_list

    def fetch_beach_match_list(tournament_id, ref_info=False, round_info=False):
        """
        Fetch FIVB beach match list for a specific tournament.

        Parameters
        ----------
        tournament_id : str
            The ID of the tournament to fetch matches for.
        ref_info : bool, optional
            Include the referees of matches? Defaults to False.
        round_info : bool, optional
            Include the rounds metadata of matches? Defaults to False.

        Returns
        -------
        list of dicts
            A list of matches with fields such as NoInTournament, LocalDate, LocalTime, etc.
            
        Notes
        ------
        Documentation: 
            https://www.fivb.org/VisSDK/VisWebService/GetBeachMatchList.html
        WinnerRank:
            -3 = The team is qualified for the qualification tournament. This value is used for a confederation quota or a federation quota match. The match should not be used for seeding or ranking.
            -1 = The team is qualified for the main draw. This value is used for a qualification tournament match. The match should not be used for seeding or ranking.
            0 = Not ranked. The t3eam continues playing in the tournamnet
            >0 = The team is ranked at the specified rank.


        """
        
        # Base fields for the match list
        base_fields = [
            "NoTournament", "NoPlayerA1", "NoPlayerA2",
            "NoPlayerB1", "NoPlayerB2", "NoTeamA", "NoTeamB",
            "TeamAName", "TeamBName", "TeamAFederationCode", 
            "TeamBFederationCode", 
            "NoInTournament", "LocalDate", "LocalTime",
            "TeamAName", "TeamBName", "Court",
            "MatchPointsA", "MatchPointsB",
            "PointsTeamASet1", "PointsTeamBSet1",
            "PointsTeamASet2", "PointsTeamBSet2",
            "PointsTeamASet3", "PointsTeamBSet3",
            "DurationSet1", "DurationSet2", "DurationSet3",
            "WinnerRank", "LoserRank"
        ]

        # Include referees if specified
        if ref_info:
            base_fields.extend([
                "NoReferee1", "NoReferee2",
                "Referee1FederationCode", "Referee1Name",
                "Referee2FederationCode", "Referee2Name"
            ])

        # Include round info if specified
        if round_info:
            base_fields.extend([
                "NoRound",
                "RoundBracket", "RoundName", 
                "RoundPhase", "RoundCode"
            ])

        # Create the XML request string
        fields_string = ' '.join(base_fields)
        xml_request = f"""
            <Requests>
                <Request Type='GetBeachMatchList' 
                        Fields='{fields_string}'>
                    <Filter NoTournament='{tournament_id}' InMainDraw='true' />
                </Request>
            </Requests>
        """

        # Set the URL for the request
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"

        # Send the request
        try:
            res = requests.post(url, data=xml_request, headers={'Content-Type': 'text/xml'})
            res.raise_for_status()  # Raise an error for bad responses
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return []

        # Parse the XML response
        soup = BeautifulSoup(res.content, 'xml')
        matches = soup.find_all('BeachMatch')

        # Extract match details using a list comprehension
        match_list = [
            {field: match.get(field) for field in base_fields}
            for match in matches
        ]

        return match_list

