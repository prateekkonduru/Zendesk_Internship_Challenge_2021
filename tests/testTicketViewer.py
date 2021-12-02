import unittest
from unittest.mock import patch
import json
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from view.appView import AppView
from model.apiRequestHandler import APIRequestHandler
from controller.appController import AppController


class MockResponse:
    def __init__(self, json_data="", status_code=""):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


# noinspection PyTypeChecker
def test_get_one_ticket(url="", auth=""):
    f2 = open('data (1).json', 'r')  # Sample json ticket data for one ticket.
    j2 = json.load(f2)
    f2.close()
    mockObject = MockResponse(j2, 200)
    return mockObject


# noinspection PyTypeChecker
def test_get_all_tickets(url="", auth=""):  # Sample json ticket data for bulk tickets
    f1 = open('data.json', 'r')
    # This file has 'next_page' as null so that tests don't get stuck in infinite loop trying to refer the same link
    # in this file again and again.
    j1 = json.load(f1)
    f1.close()
    mockObject = MockResponse(j1, 200)
    return mockObject


# NOTE: The following 3 responses don't return a json, so we don't need one in our mockObject
# noinspection PyTypeChecker
def test_get_bad_request_response(url="", auth=""):
    mockObject = MockResponse(status_code=400)
    return mockObject


# noinspection PyTypeChecker
def test_get_unauthorized_response(url="", auth=""):
    mockObject = MockResponse(status_code=401)
    return mockObject


# noinspection PyTypeChecker
def test_api_unavailable_response(url="", auth=""):
    mockObject = MockResponse(status_code=503)
    return mockObject


# noinspection PyTypeChecker
def test_invalid_ticket_id_response(url="", auth=""):
    mockObject = MockResponse({'error': 'RecordNotFound', 'description': 'Not found'}, 404)
    return mockObject


# Tests for apiRequestHandler.py module
class ModelTester(unittest.TestCase):
    # Happy unit test to get one ticket from API
    @patch('model.apiRequestHandler.requests.get', side_effect=test_get_one_ticket)
    # replace requests.get with my dummy function to simulate API network access.
    def test_api_get_one(self, test_get):  # mocking api interaction, response status code = 200
        api = APIRequestHandler()
        ticket_raw = api.requestAPI(False, 2)  # Raw ticket with unformatted dates
        self.assertEqual(len(ticket_raw), 1)
        assert "ticket" in ticket_raw
        self.assertEqual(ticket_raw["ticket"]["id"], 2)
        ticket = api.getTicket(2)  # Processed ticket with formatted dates
        self.assertEqual(len(ticket), 1)
        assert "ticket" in ticket
        self.assertEqual(ticket["ticket"]["id"], 2)

    # Happy unit test to get all tickets from API
    @patch('model.apiRequestHandler.requests.get', side_effect=test_get_all_tickets)
    # replace requests.get with my dummy function to simulate API network access.
    def test_api_get_all(self, test_get):  # mocking api interaction, response status code = 200
        api = APIRequestHandler()
        ticket_raw = api.requestAPI(True)  # Raw tickets with unformatted dates
        self.assertEqual(len(ticket_raw["tickets"]), 100)
        assert "tickets" in ticket_raw
        assert "next_page" in ticket_raw
        assert "previous_page" in ticket_raw
        assert "count" in ticket_raw
        ticket = api.getTickets()  # Processed tickets with formatted dates
        assert "tickets" in ticket
        assert "next_page" in ticket
        assert "previous_page" in ticket
        assert "count" in ticket
        self.assertEqual(len(ticket["tickets"]), 100)  # count = 101 in data.json, but actual length of json file = 100

    # Happy unit test
    def test_date_formatting(self):  # test date is formatted correctly
        api = APIRequestHandler()
        updated, created = api.formatDates("2021-11-29T12:34:23Z", "2021-10-29T12:34:23Z")
        self.assertEqual(updated, "2021-11-13 12:34:23")
        self.assertEqual(created, "2021-10-13 12:34:23")
    
    # Test to get bad request response from API
    @patch('model.apiRequestHandler.requests.get', side_effect=test_get_bad_request_response)
    # Test to get bad request from API, mocking the network access to simulate API call/request.
    def test_bad_request(self, test_get):
        api = APIRequestHandler()
        self.assertEqual(api.requestAPI(), 0)
        # testing that api.requestAPI returns 0 on general bad request (response status code = 400 in this case)
        self.assertEqual(api.getTickets(), False)
        # api.getTickets() returns 0, if api.requestAPI() returns 0 (bad request)
        self.assertEqual(api.getTicket('1'), False)
        # api.getTicket() returns 0, if api.requestAPI() returns 0 (bad request)
    
    # Test to get unauthorized response from API 
    @patch('model.apiRequestHandler.requests.get', side_effect=test_get_unauthorized_response)
    def test_unauthorized_request(self, test_get):
        api = APIRequestHandler()
        self.assertEqual(api.requestAPI(), None)
        # testing that api.requestAPI returns None on 401 unauthorized request
        self.assertEqual(api.getTickets(), 1)
        # api.getTickets() returns 1, if api.requestAPI() returns None (user not authorized)
        self.assertEqual(api.getTicket('1'), 1)
        # api.getTicket() returns 1, if api.requestAPI() returns None (user not authorized)

    # Test to get unavailable response from API    
    @patch('model.apiRequestHandler.requests.get', side_effect=test_api_unavailable_response)
    def test_api_unavailable_request(self, test_get):
        api = APIRequestHandler()
        self.assertEqual(api.requestAPI(), 1)
        # testing that api.requestAPI returns 1 on 503 API unavailable response
        self.assertEqual(api.getTickets(), 0)
        # Checking that api.getTickets() returns 0, if api.requestAPI() returns 1 (API unavailable)
        self.assertEqual(api.getTicket('1'), 0)
        # Checking that api.getTicket() returns 0, if api.requestAPI() returns 1 (API unavailable)

    # Test to get 404 Invalid ticket ID response from API, on requesting non-existent ticket ID    
    @patch('model.apiRequestHandler.requests.get', side_effect=test_invalid_ticket_id_response)
    def test_invalid_ticket_id_request(self, test_get):  # 404 Invalid Ticket ID Response
        api = APIRequestHandler()
        self.assertEqual(api.requestAPI(), False)
        self.assertEqual(api.getTicket('abcd'), -1)  # Invalid ticket ID 'abcd', fetches a response of -1 from getTicket


# Tests for appView.py module
class ViewTester(unittest.TestCase):
    # Happy unit test
    # Testing that basic functionality of view is working as expected
    def test_view(self):
        j1 = test_get_one_ticket()
        j2 = test_get_all_tickets()
        view = AppView()
        self.assertEqual(view.displayTicket(j1.json_data), 0)
        self.assertEqual(view.displayTickets(j2.json_data, 1), 1)
        self.assertEqual(view.startMessage(), 0)
        self.assertEqual(view.quit(), 0)
        self.assertEqual(view.fetchTickets("all"), 0)
        self.assertEqual(view.printMenu(), 0)


# Tests for appController.py module
class ControllerTester(unittest.TestCase):
    # Happy unit test
    @patch("builtins.input", return_value='q')  # Simulate user quitting correctly to test quitting functionality
    def test_user_quit(self, input):
        controller = AppController()
        with self.assertRaises(SystemExit) as cm:
            controller.showMainMenu()
        self.assertEqual(cm.exception.code, 0)  # Confirming system raising expected exception code

    # Happy unit test
    # Simulate and test user inputs and related outputs to show all tickets then quit, followed by display all & paging.
    # ['1', 'q', '1', 'd', 'q']: Show all tickets (1) through menu then quit (q). Then display all (1), go down one page
    # (d) & quit (q)
    @patch("builtins.input", side_effect=['1', 'q', '1', 'd', 'q'])
    @patch('model.apiRequestHandler.requests.get', side_effect=test_get_all_tickets)
    def test_show_all(self, input, test_get):
        controller = AppController()
        with self.assertRaises(SystemExit) as cm:
            controller.showMainMenu()
        self.assertEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit) as cm:
            controller.showMainMenu()
        self.assertEqual(cm.exception.code, 0)
        self.assertEqual(controller.currPage, 2)  # We scrolled down one page, so checking if paging happened correctly.

    # Simulate and test user inputs for getting ticket ID's 2, 3 and 4 to get correct respective outputs.
    @patch("builtins.input", side_effect=['2', '3', '4'])
    @patch('model.apiRequestHandler.requests.get', side_effect=test_get_one_ticket)
    def test_show_one(self, input, test_get):  # Happy unit test
        controller = AppController()
        self.assertEqual(controller.showTicket(), 0)
        self.assertEqual(controller.currID, 2)
        self.assertEqual(controller.showTicket(), 0)
        self.assertEqual(controller.currID, 3)
        self.assertEqual(controller.showTicket(), 0)
        self.assertEqual(controller.currID, 4)

    # Testing invalid ticket ID request response
    @patch("builtins.input", side_effect=['199'])  # Ticket ID 199 doesn't exist. Testing that we get invalid response.
    @patch('model.apiRequestHandler.requests.get', side_effect=test_invalid_ticket_id_response)
    def test_invalid_ticket_id(self, input, test_get):
        controller = AppController()
        self.assertEqual(controller.showTicket(), False)  # Invalid ticket ID gets False response from showTicket()


if __name__ == "__main__":
    unittest.main()
