Final Project Documentation: Restaurant Management System
By:- Manvik Gupta, Date:- 15th December 2025 

Introduction
The purpose of my project is to create a realistic restaurant management system for both employees and managers. As noticed in a real world scenario, automatic and accurate tracking of orders, automated financial calculations and employee performance is really critical for a restaurant to be successful and running effectively. The main issues that my piece of software solves are order management which allows servers to meticulously record digitals customer orders to ensure that everything is documented and that there are going to be no communication lapses between the servers ,customers and also other servers so that the restaurant can be running effictively. Additionally the program ensures that there is financial accuracy within the restaurant.The software is going to be automatically calculating long and complex bills which involve different amounts of discounts applied at different price brackets to give the right total amount with discount applied to the customer.Order history and work logs are being saved to csv files which can be accessed anytime by the manager can be written by the server later,with no data being lost.Lastly,there are various management options in the manager class like calculating the bonus and representing the server order history as a pie chart.
How does the code accomplish this
The project is going to be accomplishing these goals by building the system using Python, implementing Object-Oriented Programming principles to separate the workings of the programme into two main roles:-
The first one is the server class which has various implementations:-
A)-  Data structures:- Uses a list of dictionaries to store the meny allowing to easily manage and update the list . Lists are also being used to write to files, read from files and to store data like names of food items, clean items ordered in the file. 
B)-  Logic:- There are various methods such as apply_discount, which will be using nested if and else statements so that at different price brackets there are going to be different amounts of discounts applied so there are going to be different total bills. 
C)-  File I/O:- There are csv and os modules being utilized in the code to safely ensure that order history data with the time stamp and total bills is being saved along with the wages per week in separate files , with the os module used to ensure that the file is being saved properly in all operating systems without crashing the code.
D)-  Error handling :- There are try/except statements used throughout the code so that various specific errors in each method can be handled gracefully by displaying error messages and preventing the program from crashing with errors. 

The second class was the Manager class which had various implementations::-
A)-  Security:- There has been a password put in place to ensure that only managers can only access the manager class as the manager class has access to sensitive data like bonuses with three attempts only 
B)-  Data analysis:- The pandas library is used to efficiently read and process different datas like items ordered and the bills for each order
C)-  Visualization:- The Matplotlib library is used to vizualize the order history data in terms of what food items are ordered the most by each server as a pie chart for better understanding of the statistics of each server’s order history. 

User Guide
One prerequisite to ensure that the program is running properly, ensure that Python is installed along with the libraries of Pandas and Matplotlib. Both these libraries can be installed using the terminal with the command:- pip install pandas matplotlib

How to run the code
1)- Ensure that the python file is being saved in a separate folder as the order history and wage files are saving in the same place
2)- Then follow the instructions that are asked in the code to run it effectively.
3)- Also ensure that you have given all the permissions to VSCode when first opening the .py file.

Future Updates
Currently, the code is not complete and in the future I want to add multiple new features which is going to be making the code more robust, more functional and much more practical for restaurants such as bringing in a productivity meter to measure the productivity for each server according to how many sales have they done, how nice are they to customers etc using customer feedback. Secondly, I want to put in more caching so that if one server was to create two different objects, they would be the exact same so that there can be more features added like logging hours per day more accurately and ensuring that the salary per week is recorded once every week . Lastly, I want to put in more predictive analysis formulas using LLM API’s like Google Gemini API and  also other mathematial formulas to analyze which food items are selling the most overall and what food items does the customer want. 




