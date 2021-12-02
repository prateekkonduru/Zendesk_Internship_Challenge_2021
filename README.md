# Zendesk-Coding-Challenge-2021 :Production:

Zendesk 2021 Coding Challenge for Internship. Let's you view tickets on your Zendesk Account.<br /><br />

## Installation & Set-up
This app has been written in Python 3.8.0. The following are the installation instructions of Python 3.8.0 on 64-bit. Each of these installations come with **pip3** installation by default.

### Installation of Libraries/Modules used:

The libraries used are:

- **sys** (For exiting, using application packages etc.)
- **requests** (for API access and response)
- **mock, unittest** (for testing)
- **json** (for loading JSON data from file)
- **datetime** (for formatting dates)
- **math** (for rounding up page numbers)

## Application Usage:
To start using this app, download the git repository or the zip file. Open terminal/command line and go in the **controller** folder of this app through **cd** commands. Then type:<br /><br />

1. Sign up for a free trial with Zendesk: https://www.zendesk.com/register.

2. Update credentials in apiRequestHandler.py
        self.subdomain = "{subdomain}"
        self.loginID = "{Username}"
        self.password = "{Password}"  

3. Two simple steps to create test Tickets
- Copy the JSON here, and save it to a file called tickets.json on your computer.
- Use the cURL command below to POST the in this file to your new Zendesk account. You'll need to replace the , {email}, and{password} placeholders with the relevant details for your own Zendesk account. If you're not familiar with cURL, feel free to use whatever means you like to make the request. Postman is an easy option.

curl https://{subdomain}.zendesk.com/api/v2/imports/tickets/create_many.json -v -u {email_address}:{password} -X POST -d @tickets.json -H "Content-Type: application/json"

4. Run python appController.py
```
You should see the following screen:
```
-------------------------WELCOME TO ZENDESK TICKET VIEWER-------------------------
This application lets you view tickets and their details on your zendesk account
Please enter a command, to view command options, type 'menu': menu

Command Options:
Enter 1 to display all tickets
Enter 2 to display single ticket
Enter q to exit application
Enter 'menu' to display Command Menu

Enter your choice: 1
```
Use 'u' and 'd' (up and down) to page through tickets when viewing all tickets. 

5. Enter ticket ID after entering '2' to view specific ticket. The rest of the controls are as shown in the demo above (q to quit and 'menu' to display command menu).

## Application Testing:
For testing this app, go to the **"tests"** folder within the app on command line/terminal by using **cd** commands. Then type:<br /><br />

6. Run python testTicketViewer.py -b

**NOTE:** **"-b"** is used for supressing output/print statements during unit testing.<br /><br />
You should see a message similar to the following on your CLI Screen:
```
............
----------------------------------------------------------------------
Ran 12 tests in 0.13s

OK
```
