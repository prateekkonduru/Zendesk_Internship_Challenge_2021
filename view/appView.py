import math


class AppView:
    def __init__(self):
        self.page_limit = 25
        self.errorCode = None

    def startMessage(self):  # Displays Start message on CLI screen
        print("\n\n-------------------------WELCOME TO ZENDESK TICKET VIEWER-------------------------")
        print("This application lets you view tickets and their details on your zendesk account")
        print("Please enter a command, to view command options, type 'menu': ", end="")
        return 0

    def displayBadRequest(self, message):  # Displays bad request message on CLI screen
        if self.errorCode is not None:
            print("\nBad request. Error getting data from API. Error Code:", self.errorCode)
        print(message)
        return 1

    def displayInputMessage(self, message, type):
        print(message, end="")        
        return type  # Returns 0 on input prompt type messages, returns 1 on input error type messages

    def printMenu(self):  # Displays Command Menu on CLI Screen
        print("\nCommand Options:")
        print("Enter 1 to display all tickets")
        print("Enter 2 to display single ticket")
        print("Enter q to exit application")
        print("Enter 'Menu' to display Command Menu")
        print("\nEnter your choice: ", end="")
        return 0

    def quit(self):  # Displays quit message and quits the App.
        print("\nExiting Zendesk Ticket Viewer. . . . . .")
        print("Exiting successful, see you soon.\n")
        return 0

    def fetchTickets(self, ticketID):  # Displays loading tickets message on CLI screen
        if ticketID == "all":
            print("\nFetching tickets, please wait . . . . .")
        else:
            print("\nFetching ticket", ticketID + ",", "please wait . . . . .")
        return 0

    def displayTickets(self, ticketsJSON, pageNo):  # Displays tickets details with pagination on CLI screen
        ticketsArr = ticketsJSON["tickets"]
        # rounding up ticket pages
        totalPages = math.ceil(float(len(ticketsArr)) / float(self.page_limit))
        # circular rotation of pages after limit or before start
        if pageNo > totalPages:
            pageNo = 1
        elif pageNo < 1:
            pageNo = totalPages
        pageTickets = 0
        ticketOffset = (pageNo - 1) * self.page_limit
        print("")
        for i in range(int(ticketOffset), int(self.page_limit + ticketOffset)):
            if i < len(ticketsArr):
                if ticketsArr[i]["id"] is None:
                    continue
                else:
                    print("<" + ticketsArr[i]["status"] + ">", "Ticket", ticketsArr[i]["id"], "opened by",
                          ticketsArr[i]["requester_id"], "updated at", ticketsArr[i]["updated_at"])
                pageTickets += 1
        print("\nDisplaying", pageTickets, "tickets on page", pageNo, "of", totalPages)
        print("\nEnter 'd' to go down, 'u' to go up, 'menu' for menu and 'q' for quit: ", end="")
        return pageNo  # Current page no

    def displayTicket(self, ticketsJSON):  # Displays one ticket details on CLI screen
        if "ticket" in ticketsJSON:
            print("\n" + "<" + ticketsJSON["ticket"]["status"] + ">", "Ticket", ticketsJSON["ticket"]["id"], "subject", "'" +
                  ticketsJSON["ticket"]["subject"] + "'", "opened by", ticketsJSON["ticket"]["requester_id"], "updated at",
                  ticketsJSON["ticket"]["updated_at"])
            print("\nPlease enter a command, to view command menu, type 'menu': ", end="")
            return 0
        else:
            return 1
