# Simple Banking System
Simple Bank System
This is a Graphical User Interface (GUI) based Simple Bank System built using Python and Tkinter. This application allows users to create a bank account, deposit and withdraw funds, and view their balance. It’s designed as a simple banking interface to demonstrate basic banking operations in a GUI environment.

Features
Account Registration: Users can register a new bank account by entering their account number, username, and initial deposit.
View Balance: Users can view their current account balance.
Deposit Money: Users can deposit money into their account.
Withdraw Money: Users can withdraw money from their account, provided they have sufficient balance.
Real-time Feedback: The app provides real-time feedback on successful transactions and error messages for invalid actions.
Installation
To run this project, make sure you have Python installed on your system. Tkinter comes pre-installed with Python, so no additional installations are required.

Clone the repository or download the code files.

Open a terminal or command prompt in the project folder.

Run the following command to start the application:

bash
Copy code
python bank_system.py
Code Structure
BankAccount Class
This class represents a bank account and includes methods for:

Deposit: Adds funds to the account balance.
Withdraw: Deducts funds from the account balance if sufficient funds are available.
Check Balance: Displays the current balance.
GUI Components
Account Registration Form: Allows the user to enter an account number, username, and initial balance for registration.
Transaction Buttons: Includes buttons for account actions like deposit, withdraw, and balance inquiry.
Labels for Feedback: Displays feedback messages for each action, such as successful transactions, insufficient funds, or invalid input.
Key Components in the GUI
t1, t2, t3: Entry fields for account number, username, and amount.
l4, l5: Labels to display feedback messages for transactions and balance information.
Buttons: Buttons that trigger different bank account functions:
Registration: Registers a new account.
View Balance: Retrieves and displays the account balance.
Deposit: Deposits a specified amount.
Withdraw: Withdraws a specified amount.
Usage
Account Registration:

Enter an account number and username in the designated fields.
Specify an initial deposit amount and click Registration.
A confirmation message will appear indicating a successful account registration.
View Balance:

Enter your account number and click View Balance to see your current balance.
Deposit Money:

Enter your account number and the deposit amount.
Click Deposit to add funds to your account.
Withdraw Money:

Enter your account number and the withdrawal amount.
Click Withdraw to deduct funds from your account balance (if funds are sufficient).
Screenshots
You can add screenshots of your application here to provide users with a visual overview of the interface.

Future Improvements
Database Integration: Currently, the account information is stored in a dictionary, which resets when the app closes. Integrating a database would allow persistent storage of account data.
Login Authentication: Adding user authentication (such as passwords) would improve security for account access.
Error Handling: Enhanced error handling for cases like invalid input types and edge cases.
Technologies Used
Python: Core programming language.
Tkinter: Used for creating the GUI elements.
License
This project is open-source and available for use.

