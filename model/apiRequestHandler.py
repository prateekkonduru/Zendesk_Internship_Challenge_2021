"""
Model of the model package in MVC pattern. Does all the API stuff: authentication, fetching tickets, processing data got 
from the API, formatting dates.
It can be extended in the future to add extra functionality like posting new data up on the server, token 
authentication etc.
"""
import requests
import datetime


class APIRequestHandler:
    def __init__(self):
        self.URL = ""
        self.data = {}  # This is where ticket data goes
        self.subdomain = "{subdomain}"  # Zendesk API subdomain
        self.loginID = "{Username}"  # Zendesk API username
        self.password = "{Password}"  # Zendesk API password
        self.errorCode = None

    # Method to get all tickets in user's account and return them or return an appropriate error value
    def getTickets(self):
        ticketsJSON = self.requestAPI(True, "")
        if ticketsJSON in [1, False, None, 0] or "tickets" not in ticketsJSON:
            if ticketsJSON is None:
                return 1  # Invalid user credentials or authentication not enabled
            elif ticketsJSON == 1:
                return 0  # If API is unavailable
            elif ticketsJSON == 0:
                return False  # All other bad requests
            elif ticketsJSON is False or "tickets" not in ticketsJSON:
                # For if no tickets exist
                return -1

        elif ticketsJSON not in [1, False, None, 0] and "tickets" in ticketsJSON:
            for i in range(len(ticketsJSON["tickets"])):
                updated, created = self.formatDates(ticketsJSON["tickets"][i]["updated_at"],
                                                    ticketsJSON["tickets"][i]["created_at"])
                ticketsJSON["tickets"][i]["updated_at"] = str(updated)  # Setting the formatted dates
                ticketsJSON["tickets"][i]["created_at"] = str(created)  # Setting the formatted dates
            return ticketsJSON

    # Method to get one ticket details from API and return it, or return appropriate error value
    def getTicket(self, ticketID):
        ticketsJSON = self.requestAPI(False, ticketID)
        if ticketsJSON not in [None, False, 1, 0] and "ticket" in ticketsJSON:
            updated, created = self.formatDates(ticketsJSON["ticket"]["updated_at"],
                                                ticketsJSON["ticket"]["created_at"])
            ticketsJSON["ticket"]["updated_at"] = str(updated)
            ticketsJSON["ticket"]["created_at"] = str(created)
            return ticketsJSON
        elif ticketsJSON in [None, False, 1, 0]:
            if ticketsJSON is False:
                return -1  # Invalid ticket ID
            elif ticketsJSON == 1:
                return 0  # If API is unavailable
            elif ticketsJSON is None:
                return 1  # Invalid user credentials
            elif ticketsJSON == 0:
                return False  # All other bad requests
            return False

    # Method to connect and query the Zendesk API to fetch tickets
    def requestAPI(self, all=True, id=""):

        if all:
            self.URL = "https://" + self.subdomain + ".zendesk.com/api/v2/tickets.json"
        else:
            self.URL = "https://" + self.subdomain + ".zendesk.com/api/v2/tickets/" + str(id) + ".json"
        try:
            response = requests.get(self.URL, auth=(self.loginID, self.password))
            if response.status_code != 200:
                # print("Bad request. Error getting data from API. Error Code: ", r.status_code)
                self.errorCode = response.status_code
                if response.status_code == 401:
                    return None  # Authentication not allowed or invalid user credentials
                elif response.status_code == 404:  # 404 = No tickets or invalid ticket ID
                    return False
                elif response.status_code == 503:  # API unavailable
                    return 1
                return 0  # For all other bad requests
            self.data = response.json()  # Or json.loads(r.text) can also work
            new = self.data
            next_page = []
            # Go through all web pages containing tickets and add them to tickets json. One page can contain 100 tickets
            # Make sure user has chosen to display all tickets, next page exists and has not been already visited.
            while all and new["next_page"] is not None and new["next_page"] not in next_page:
                self.URL = new["next_page"]
                next_page.append(self.URL)
                response = requests.get(self.URL, auth=(self.loginID, self.password))
                new = response.json()
                # print("Next: ", new["next_page"])
                self.data["tickets"].extend(new["tickets"])  # Adding new tickets found in the next API web page.

            return self.data
        except requests.exceptions.RequestException as e:
            return 0
        except ConnectionError:
            return 0

    # Method to convert date format of ticket into good print
    def formatDates(self, updatedAt, createdAt):
        t1 = datetime.datetime.strptime(updatedAt, "%Y-%m-%dT%H:%M:%SZ")
        t2 = datetime.datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%SZ")
        updated = "%d-%d-%d %d:%d:%d" % (t1.year, t1.month, t1.day, t1.hour, t1.minute, t1.second)
        created = "%d-%d-%d %d:%d:%d" % (t2.year, t2.month, t2.day, t2.hour, t2.minute, t2.second)
        return updated, created
