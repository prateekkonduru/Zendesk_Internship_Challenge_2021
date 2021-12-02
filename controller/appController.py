import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from view.appView import AppView
from model.apiRequestHandler import APIRequestHandler


class AppController:
    def __init__(self):
        self.view = AppView()  # An AppView instance being used by this class.
        self.api = APIRequestHandler()  # An APIRequestHandler instance being used by this class
        self.input = ""  # Input given by user
        self.currID = 999  # A random ticket ID. This points to the ticket we are currently viewing.
        self.currPage = 999  # A random page number. This points to the current page we are viewing.

    def run(self):  # Driver method
        self.showMainMenu()

    def getInput(self):  # Prompts user for input
        self.input = input()

    def showMainMenu(self):  # Main menu view controller
        self.view.startMessage()
        while True:
            self.getInput()  # Get user input
            if self.input == "menu":  # Display app menu
                self.view.printMenu()
            elif self.input == '1':  # Show all tickets
                response = self.showTickets()
                if response is None:
                    self.view.displayInputMessage("\nEnter a command, to view command menu, type 'menu': ", 0)
                    # Display input prompt message
            elif self.input == '2':  # Show one ticket
                response = self.showTicket()
                if response is False:
                    self.view.displayInputMessage("\nEnter a command, to view command menu, type 'menu': ", 0)
                    # Display input prompt message
            elif self.input == 'q':  # Quit app
                sys.exit(self.view.quit())  # Print quit message and quit
            else:
                self.view.displayInputMessage(
                    "Invalid input, please enter a valid command. To view command options type 'menu': ",
                    1)  # Invalid user input for menu
            self.input = ""

    def showTickets(self):  # Controller method to display all tickets. Handles user inputs for paging requests
        try:
            self.view.fetchTickets("all")  # Fetching display message
            tickets = self.api.getTickets()  # Get all tickets
            assert tickets not in [-1, 0, 1, False]
            page = self.view.displayTickets(tickets, 1)
        except AssertionError as e:
            self.view.errorCode = self.api.errorCode
            if tickets == -1:  # No tickets on account
                self.view.displayBadRequest("No tickets on account to display")
            elif tickets == 1:  # Can't authenticate with API
                self.view.displayBadRequest("API authentication not permitted or invalid user credentials.")
            elif tickets == 0:  # API unavailable
                self.view.displayBadRequest("API unavailable. Please try again later")
            elif tickets is False:  # Other Bad Requests
                self.view.displayBadRequest("Unknown Bad Request")
            self.view.errorCode = None
            self.api.errorCode = None
            return None
        while True:
            self.getInput()
            if self.input == 'q':  # Quit app
                sys.exit(self.view.quit())  # Print quit message and quit
            elif self.input == "menu":  # Show menu
                self.view.printMenu()
                break
            elif self.input == "d":  # Page down
                page += 1
                page = self.view.displayTickets(tickets, page)
            elif self.input == "u":  # Page up
                page -= 1
                page = self.view.displayTickets(tickets, page)
            else:
                self.view.displayInputMessage(
                    "Page command error. 'd' to go down, 'u' to go up, 'menu' for menu and 'q' for quit: ", 1)
                # Invalid user input for ticket paging
            self.input = ""
            self.currPage = page
        return 0

    def showTicket(self):  # Controller method for displaying one ticket in view
        self.view.displayInputMessage("Enter the ticket ID: ", 0)  # Display ticket ID input message
        self.getInput()  # Get ticket ID
        ticketID = self.input
        self.input = ""
        try:
            self.view.fetchTickets(ticketID)  # Get ticket
            ticket = self.api.getTicket(ticketID)
            assert ticket not in [-1, 0, 1, False]
            self.view.displayTicket(ticket)  # Display ticket
            self.currID = int(ticketID)  # Current ticket ID
            return 0
        except AssertionError as e:
            self.view.errorCode = self.api.errorCode
            if ticket == 1:  # Can't authenticate with API
                self.view.displayBadRequest("API authentication not permitted or invalid user credentials.")
            elif ticket == -1:  # Ticket ID not valid
                self.view.displayBadRequest("The ticket ID you gave is not a valid ID")
            elif ticket == 0:  # API unavailable
                self.view.displayBadRequest("API unavailable. Please try again later")
            elif ticket is False:  # Other Bad Requests
                self.view.displayBadRequest("Unknown Bad Request")
            self.view.errorCode = None
            self.api.errorCode = None
            return False


if __name__ == "__main__":
    t = AppController()
    t.run()  # Starting point of the application
