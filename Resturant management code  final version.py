from datetime import datetime # the datetime module is going to be imported to get the timestamp of when the order is placed and the work hours are logged in for the week 
from matplotlib import pyplot as plot # The purpose of this module is to plot the pie chart
import getpass 
import sqlite3

def menu_setup():
    key= sqlite3.connect('resturant.db')
    cursor= key.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_inventory(
            name TEXT PRIMARY KEY,
            price REAL,
            category TEXT,
            quantity_ordered INTEGER DEFAULT 0
         )
     ''')
    cursor.execute("INSERT OR IGNORE INTO menu_inventory VALUES ('Mac and Cheese', 30.00, 'Main', 0)")
    cursor.execute("INSERT OR IGNORE INTO menu_inventory VALUES ('Cheeseburger', 50.00, 'Main', 0)")
    cursor.execute("INSERT OR IGNORE INTO menu_inventory VALUES ('Ceaser Salad', 20.00, 'Main', 0)")
    cursor.execute("INSERT OR IGNORE INTO menu_inventory VALUES ('Pizza', 30.00, 'Main', 0)")
    cursor.execute("INSERT OR IGNORE INTO menu_inventory VALUES ('Ziti', 25.00, 'Main', 0)")
    cursor.execute("INSERT OR IGNORE INTO menu_inventory VALUES ('Duck', 50.00, 'Main', 0)")
    cursor.execute("INSERT OR IGNORE INTO menu_inventory VALUES ('Steak', 75.00, 'Main', 0)")
    key.commit()
    key.close()
 
class Server: # This is the server class which is going to be accessed by the server who is placing the orders , adding items etc, there are various attributes initialized like the name values,menu etc 
    def __init__(self,name):
        # We are initializng a constructor with the server needing to put their name so that the order history can be saved at different files which changes according to the name of the server. We are also initialzing an attribute called self.menu which is storing a dictionary with name of food item being the key and the price being the value in each dictionary. There is also an empty list initiated called self.order_history to store the name of food items ordered by each consumer. 
        menu_setup() 
        self.name= name
        print("Welcome "+ name )
        conn=sqlite3.connect("resturant.db")
        cursor= conn.cursor()
        cursor.execute("SELECT name, price FROM menu_inventory")
        self.menu= [{row[0]:row[1]} for row in cursor.fetchall()]
        conn.close()
        self.name_values=[]  # There is this list initiated in order to ensure that the add_item method works so we can easily add new items by comparing food items in lower case and check this list. 
        self.purchase_history=[] # This list is responsible to save the food items that are being purchased when ordered by one table 
        for item in self.menu: # The menu is being iteratred over to save it in the name values list in lowercase to compare when purchasing and adding new items to the menu
            for name1 in item:
                self.name_values.append(name1.lower())
                
    def show_menu(self): 
        # The purpose of this method is to show the menu by going through self.menu which was initialized in the constructor and then going through each dictionary in the list self.menu to print each item in the menu along with its price for customers to see. 
        print("Today's menu contains")
        for i in self.menu:
            for item1 in i:
                print(item1.title() + " :$ "+ str(i[item1]))
                print() #This is used so that there is going to be a gap between two items in the menu 
        # There is a nested loop used here as we are first going over the list to acess all the dictonaries and then we loop through each dictionary to print each food item and then its price by casting the price as a string otherwise we cant concentate the value of price to a string.
    
    def add_item(self): # The purpose of the method is to be adding new items to the menu as there is a stock menu initialized and the server is going to be adding new items to the menu for the current day. 
        new_item={}
        while True:
            try: # The statement is being put in so that the errors can be handled gracefully in specific to price so if there is an input given which cannot be converted to a float, the program will not crash but instead move to the except statements. 
                name= input("Enter a new item into the menu (without commas): ") # There is a name that is going to be asked without commas as there is split(",") in another method which is going to give the wrong name and values when creating the pie chart 
                if "," in name: # This condition is going to hold true when there is a comma in the name variable with an error message displayed , with the user prompted again to write another name without commas 
                    print("Commas are not allowed,Please try again! ")
                else:
                    price= float(input("Enter the price for the item: "))
                    if price >0: 
                        if name.lower() not in self.name_values : # This is being used in order to check if the food item in lowercase  is going to be inside our existing food items in the menu and in this case our food item is not in the menu as it is not in this list so it will add the food item to the menu and this list 
                            new_item[name.title()]=round(price,2) # There is a dictionary being created where the food item is going to be the key and the price at 2 decima places is going to be the value 
                            self.menu.append(new_item)# The menu is going to be updated by appending the new dictionary at the end.
                            self.name_values.append(name.lower())# This list is also going to be updated so that whenever this function is going to be called again , the list should reflect that this food item is  entered to the menu in lowercase and cannot be re-entered again
                            conn = sqlite3.connect('resturant.db')
                            cursor= conn.cursor()
                            
                            cursor.execute('''
                                INSERT INTO menu_inventory(name,price,category,times_ordered)
                                VALUES (?,?,?,?)
                            ''', (name.title(), price, 'General',0))
                            break
                        else: #This statement is going to be ensuring that if the food item is already in the name of food items list, then the message saying that the item is already in the menu is displayed.
                            print("Item already exists in the menu for today, Please add another item")
                    else:
                        print("Enter a price greater than 0 ")
            except ValueError: # This except statement is more specific to the current method which is that there is a wrong input put in for price, which will be resulting in a ValueError that is going to be gracefully handeled with this statement.
                print("You have not added the right input for price, Please try again ")
            except: # This except statement is going to be handling all other general errors other than ValueError in order to handle any unknown error which handles other errors gracefully and does not crash the program. 
                print("An unknown error has occured, Please try again!")
    
    def change_price(self): # The purpose of this method is to enablw the server to change the price of the food items in the menu
        while True: # This allows for the method to run continously until the right input of name and price is entered 
            name= input("Enter the name of the dish you want to change in the menu: ") # The name of the item on the asked is asked and then stored in this variable 
            if name.lower() in self.name_values: # If the name inputted in lower case is going to be found in the food items list , the new price of the food item is asked
                try: # This is going to be handling all the errors gracefully without crashing the program 
                    price= float(input("Enter the new price for the item: ")) # The new price of the food item is going to be inputted and then using an iterator , the value of the food item is going to be updated 
                    for num in range(len(self.menu)):
                        for i in self.menu[num]:
                            if i.lower()== name.lower(): # The names are being compared and checked in lower case to ensure that the program does not crash and no new duplicates in lower case are added to the menu 
                                if self.menu[num][i] != price and price >0 : # This condition is going to be checking if price is more than 0
                                    self.menu[num][i]= price 
                                    conn = sqlite3.connect('resturant.db')
                                    cursor= conn.cursor
                                    cursor.execute('''
                                        UPDATE menu_inventory
                                        SET price= ?
                                        WHERE name= ?
                                    ''', (price, name.title()))
                                    print("Price changed for "+ i)
                                    break # This statement is going to be breaking the inner loop if the task is done succesfully 
                                else: # This condition is going to hold true if the price of the food item is going to be the same as it is in the menu with a message displayed for the user to put in new values and the menu is shown for reference 
                                    print("This is the exisiting or invalid  price for the item, Please enter a new price! ")
                                    self.show_menu()
                    return(True)# This is going to be breaking the while loop if the task is done successfully so that there is no infinite loop
                
                except ValueError: # This exception is called when there is a value error when entering the value for price without crashing the program  by displaying a message and allowing the user to prompt again 
                    print("Please enter the right value of price ")
            else: # This condition holds true when the food item is not going to be found in the menu with a message displayed, the menu shown again and the server allowed to input another food item 
                print("Food item is not in the menu, Please Try Again ")
                print()
                self.show_menu()
                print()
                
                        
    def order_items(self): # This method is going to be allowing the server to place an order for each table. 
        menu_setup()
        while True: # This is so that the code will be running continously for the sever to continously add orders to the system.
            choice= input("If you want to add another purchase type in O or press Q when you are done: ") # There is a choice for the server to add more items or quit the function after the order has been placed.
            if choice== "O" or choice== "o":
                purchase= input("What does your customer want to eat? ") # There is an input asked to add the food item that the customer wants to eat 
                if purchase.lower() in self.name_values:# The code is again going to be checking the updated food items name list to verify if the food item in lowercase  asked by the customer actually is in the menu.
                    self.purchase_history.append(purchase) # If the item does exist in the menu then the food item is going to be added to the list.
                    conn = sqlite3.connect('resturant.db')
                    cursor = conn.cursor() 
                    cursor.execute("UPDATE menu_inventory SET quantity_ordered=  quantity_ordered+1 WHERE name =?", (purchase,))
                    conn.commit()
                    conn.close()
                else: # This statement is going to be called when the food item is not going to be in the food items list meaning the item is not in the menu so invalid item is displayed. 
                    print("Item does not exist in the menu, Please have a look at the menu and try again")
                    self.show_menu() # The menu is going to be showed to check what items are actually in the menu by calling the function
            elif choice== "Q" or choice== "q": # This option is for when the server want to quit the program and then according to length of purchase_history, there are different messages printed.
                if len(self.purchase_history)>0:# If there are going to be items ordered , the item names are going to be printed and shown. 
                    print("Your customer has ordered: ")
                    for  i in range(len(self.purchase_history)): # the length of the list is going to be used so that the items can be printed in a numbered manner.
                        print(str(i+1) + ")-  " + self.purchase_history[i].title()) 
                    break # This statement is going to be breaking out of the loop as the user is selected to Quit the ordering system. 
                else:# This statement will be running when there are going to be no items ordered outputting a message and then terminating the loop to prevent an infinite loop.
                    print("Your customer has ordered nothing! Please check what seems to be the problem.")
                    break
                        
            else: # This statement is called if the input of choice entered is not Q or O displaying an error message and allowing the server to input again.
                print("An error seems to have occured! ,Please try again.")
                print()
                
    def get_total(self): # The purpose of this method is to calculate the total bill according to the items ordered by the customer
        total=0.00
        if len(self.purchase_history)>0: # Checking the length of the purchase list, it can be determined if there are items ordered or not  
            for i in self.purchase_history:
                for x in self.menu:
                    for d in x:
                        if i.lower()== d.lower():# This is used to check if the food item is going to be in each dictionary in the menu list
                            total+= x[d] # By looping through purchase list and then looping through the menu , the value of total is going to be incrimented with the price of each menu item according to the food ordered by the customer
        return(total) # The total bill is going to be returning which will either be the total value calculated if there are items ordered by the customer or otherwise, 0 will be returned.
    
    def apply_discount(self):# The purpose of this method is to apply a discount on the total bill depending on some set amounts. 
        total_bill= self.get_total()# The value of the total bill that was calculated from the previous function is going to be saved to this variable.
        if float(total_bill)>=50: # We are running a comparision where if the total bil is equal to or more than 50 then there is a 35% discount given to the bill
            total_bill= float(total_bill)*0.65
        elif float(total_bill)>=30:# If the total_bill is going to be equal to 30 or more but the bill is less than 50 then there is a 25% discoutn given
            (total_bill) = float(total_bill) *0.75
        elif float(total_bill)>=20: # If the total_bill is going to be equal to or more than 20 but less than 30 then there is a 20% discount given.
            total_bill= total_bill* 0.80
        else:# This condition is for if the total bill is going to be less than 20.
            (total_bill) = float(total_bill) *1.00
        return(float(total_bill))# The discounted bill is now going to be returned in a float form 
    
    def show_bill(self):# The purpose of this method is to be displaying the bill with the menu items ordered and give the total amount.
        print("Your bill is:- ")
        for i in self.purchase_history: # The purpose is going to be iterating over the list where in each menu item is being printed along with the price of each time by iterating over the menu list.
            for x in self.menu:
                 for d in x:
                     if i.lower()== d.lower():
                        print(d + " $"+ str(x[d]))   
        undiscounted_bill= self.get_total() #  The get total method is called from  above so that the undiscounted bill is returned and stored with this variable.
        discounted_bill= self.apply_discount()# The discount method with the current amount is being discounted as the function is calculating using the total bill
        save= (float(undiscounted_bill) - float(discounted_bill))# We are calculating how much amount of money is being saved by subtracting the undiscounted bill with the discounted bill.
        if save>0.00:# This is the condition if there is going to be savings more than 0, meaning there is a discount applied.
            print("Your original total was: $"+ f"{undiscounted_bill:.2f}")
            print("Your new total is: $"+ f"{discounted_bill:.2f}")
            print("You have saved: $"+ f"{save:.2f}")
            # The values printed are the original total at 2 decimal places , then the new total at 2 decimal places and then the savings when the discount is applied at 2 decimal places
        else: 
            print("Your total is: $"+ f"{discounted_bill:.2f}")
        # The value printed here is the value if there is no  amount of money saved.
        
    def save_order_history(self): # The purpose of this method is to be saving the order history into a csv file according to the server's name.
        discounted_bill= self.apply_discount() # type: ignore
        full_datetime= str(datetime.now()) # We are calling the datetime module to obtain the current time in days and time  when the order is being put in place and then casted as a string 
        date_time_part= full_datetime.split('.')[0] # Our whole current datetime which has now been casted as a string, we are spliting the string using (.) to only get the date and the time  data_lst.append(date_time_part)# In the data list, the new date time string is being added 
        try:
            clean = ', '.join(self.purchase_history)
            conn = sqlite3.connect("resturant.db")
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS all_orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_name TEXT,
                    items_ordered TEXT,
                    total_bill REAL,
                    timestamp TEXT
                )
            ''')
            cursor.execute('INSERT INTO all_orders (server_name, items_ordered, total_bill, timestamp) VALUES (?,?,?,?)', (self.name, clean, discounted_bill, date_time_part))
            conn.commit()
            conn.close()
        except sqlite3.Error:
            print("There is an SQL Error, Please Try Again! ")
            return(False)
        except:  # This condition is called to deal with any other unknown errors other than Input / Output Error and prevent the program from crashing x
            print("There seems to be another error ,Please Try Again")
            return(False)

    def get_money(self):# The purpose of this method is to recieve money from the customer and then according to how much of the bill is paid , the customer has to constantly pay until the total bill is paid
        balance= self.apply_discount()# The total discounted bill is being called and stored in this variable
        while True: # This conditon is reposible to ensure that the user can add some certain amount of money which is used to pay for the bill
            try: # This condition is put in to handle any errors which can arise without crashing the program
                money_gotten= float(input("Please add an amount to pay for your bill ")) 
                if money_gotten>0: # This condition is going to ensure that the amount of money added is going to be positive and more than 0 and not negative so that the total amount the customer needs to pay does not increase 
                    if money_gotten< balance: # This is a condition where the money given by the customer is less than the total bill resulting in the the amount of money remainign being calculated by taking the difference between the bill and the money recieved
                        money_remaining= balance-money_gotten
                        balance= money_remaining # Now the variable that is storing the total discounted bill is going to store how much money remaining is there to pay
                        print(f"You need to give ${balance:.2f} more.") # This message is being printed to inform the customer as to how much money do they need to give more to pay for their bill
                    elif money_gotten> balance:  # This condition is going to be called when the customer is paying more than the total bill with some change being return by subtracting the money gotten with the total bill and then terminating the loop as the change is being returned and the customer owes the resturant no more money
                        return_change= money_gotten- balance
                        print("Your change is $"+ f"{return_change:.2f}")
                        self.purchase_history=[]  # The purchase history is going to be updated with the list being empty so that a new order can be taken
                        return(True)
                   
                    else: # This condition is going to be called when the money recieved by the customer is the same as the bill resulting in a message being printed and then the loop being terminated as there is no money owed and then the purchase history list  is going to be emptied
                        print("Whole amount is paid!")
                        self.purchase_history=[] 
                        return(True)
                
                else: # This condition is going to be true when there is an amount equal to and less than 0 is added , with the user prompted to add another amount more than 0
                    print("Please enter an amount greater than 0 ")
            except ValueError: # This exception is there to handle any value error which may arise if the input given cannot be converted to a float to prevent any error from crashing the program by printing a message and prompting the server to write the value again 
                print("You have put in the wrong input for the money recieved by the customer , Please Try Again!")
            except:# This condtition is there to handle any general exceptions other than a Value Error to prevent the program from crashing and allowing the server to input values again
                print("There seems to be another error, Please Try Again!")
                  
    def work_per_week(self): # The purpose of this method is for the server to add how many days  and hours of the week they are working 
        while True: # This statement is there to ensure that each sever is adding the right inputs in by constantly prompting them until they add the right inputs
            try: # There is error handling done here to ensure that the program wont crash if there is an error  
                hours_work= float(input("How many hours have you worked per day: ")) # This is going to be getting the input of how many has the servers logged per day
                days_per_week= float(input("How any days have you worked per week: "))# This is going to be getting the input regarding how many days are worked in the week
                full_datetime= str(datetime.now())
                date_time_part= full_datetime.split('.')[0]
                if (days_per_week<= 7 and days_per_week>0):# This is going to be checking if the days of the week entered is 7 or less which are the number of days in a week 
                    if hours_work>0 and hours_work<=12:# This condition checks if the hours worked per day is more than 0 and less than equal to 12 hours per day
                        salary=  days_per_week* hours_work*16.00 #This variable is calculating the salary by taking all the wage per week and multiplying with 16 which is the hourly rate
                        conn= sqlite3.connect("resturant.db")
                        cursor= conn.cursor()
                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS wages_per_week (
                            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            server_name TEXT,  <-- This is the key column!
                            salary_per_weeek TEXT,
                            timestamp TEXT
                            )
                        ''')
                        cursor.execute('INSERT INTO wages_per_week VALUES (?,?,?)', (self.name,salary, date_time_part ))
                        conn.commit()
                        conn.close()
                    else:
                        print("Please enter the right number of hours worked per day between 1 and 12 .")
                else:# This condition is going to be called if the number of days entered are greater than 7, which is not posible in a week
                    print("Please enter right number of days worked per week.")
            except sqlite3.Error:
                print("There is a SQL related problem, Please Try Again !")
            except ValueError: # This will be handling value errors if the value of hours worked or days worked is not going to be converted to a float
                print("Please enter the right inputs for both questions ")
            except: # All other general exceptions is going to be handled.
                print("There is an unknown error, Please Try Again !")


class Manager: #This is another class called which is going to be accessed by the manager of the resturant only
    def __init__(self, name): # This is going to be initializing the new attributes when this object will be created 
        self.name= name
        self.bonus= [] # This is a list created to store the bonuses of all the servers with the key being the server name and value is the bonus amount 
        
    def authenticate(self): # The purpose of this method is to be checking if the person who is going to be acessing manager class is actually the manager by them putting in a password which is compared to the password set for the class 
        count =0 
        while count< 3: # There are going to be three attemps for the person to be put in the right password
            password= getpass.getpass("Please enter your password to authenticate:- ")
            if password== "P@$$w0rd2o25":
                print("Welcome! " + self.name) # if the right password is put in then it wll display a message saying welcome
                return(True)
            else:
                count=count+1 # If the password is wrong, the attempt is going to be incrimenting by 1 until 3 tries are reached 
                print("Try Again! You have "+ str(count) + "/3 tries remaining ")
        print("You have failed to authenticate yourself!!") # This mesage is going to be displayed if after 3 tries also , the correct password is not identified 
        return(False)
    
    
    def read_file(self, name ): # The purpose of this method is to be reading the order history file of each server according to their name and then calculate the total bill overall in the file
        count=0
        try:
            conn=sqlite3.connect("resturant.db")
            cursor= conn.cursor()
            cursor.execute("SELECT SUM(total_bill) FROM all_orders WHERE server_name = ?", (name, ))
            result= cursor.fetchone()
            conn.close()
            
            if result and result[0] is not None:
                total_sale= round (result[0],2)
                return(total_sale)
            else:
                return(0.0)
            
        except: # All other common errors is going to be handled here other than FilenotFoundError 
            print("There seems to be an unknown error, Please try again!")
            return(False)
            
    def calculate_bonus(self,name): # The purpose of this method is to take the total sales from each server and then take the wage earned by a worker each weak and according to that calculate the bonus 
        total_wages=0 
        bonus_key= {} # This is going to be initializing an empy dictionary which will be storing the name of the server as they key and the bonus as a value 
        bonus_amount=0
        conn=sqlite3.connect("resturant.db")
        cursor= conn.cursor()
        cursor.execute("SELECT SUM(salary_per_week) FROM all_orders WHERE wages_per_week = ?", (name, ))
        result= cursor.fetchone()
        conn.close()
        try:
            total_wages=round(result[0],2)
            total_amount= self.read_file(name) #The read file function which is going to be returning the total amount of sales done by a particular server and is then going to be saving it 
            if total_amount != False: # If the total amount returned is not going to be False and then according to the total number of sales done, and bonus is calculated according to the percentage of wages earned 
                    if total_amount>=200 and total_amount< 300:
                        bonus_amount= total_wages* 0.10
                    elif total_amount >=300 and total_amount< 500:
                        bonus_amount= total_wages * 0.15
                    elif total_amount>= 500:
                        bonus_amount= total_wages* 0.25
                    else:
                        bonus_amount= total_wages*0
                    bonus_key[name]= bonus_amount # The dictionary is going to be updated with the name being the key and the value being the calculated bonus amount 
                    self.bonus.append(bonus_key) # The dictionary is going to be appen ding to the bonus list which is initialized in the attributes 
                    return(True)
            else: # This condition will be holding true if the total_amount is going to be returning False  displaying the message that bonuses cannot be calculated 
                    print("The bonus amount cannot be calculated!") 
                    return(False)
        except KeyError: # This statement is going to be handling a key error where the header "Total Salary per week" cannot be found in the file
            print("Key cannot be found!")
        except sqlite3.Error: 
            print("This database does not exist, Please Try Again")
            return(False)
        except: # All other common errors is going to be handled here other than FilenotFoundError 
            print("There seems to be another error, Please Try Again")
            return(False)
        
    def show_bonuses(self): #The purpose of this method is to display all the bonuses that are to be given to the servers in a numbered fmanner 
        if len(self.bonus)>0: # If length of the bonus list is going to be more than 1, then all the bonuses are going to be displayed 
            print("Bonuses to be presented this month are: ")
            for i in range(len(self.bonus)): # The bonus list is going to be iterated through by using the length of the list to display the bonus amounts for each server in the list in a numbered manner 
                for k in self.bonus[i]:
                    print(str(i+1)+ ". $"+ str(self.bonus[i][k]) + " for  " + k )
            return(True)
        else: # This condition is going to be holding true if the length of the bonus list is 0, meaning that no bonuses are to be presented which is displayed as a message 
            print("No bonuses are to be presented this month")
            return(False)
        
    def display_chart(self,name): # The purpose of this method is to display the order history for each server as a pie chart by accessing their file and displaying it as a chart 
        try: # This statement is going to be handling all the errors gracefully without crasing the program 
            master_lst=[] # This is the clean list which is going to be consisting of all the food items ordered in the file 
            name_lst=[] # The purpose of this list is going to be to storing the name of the food items 
            values_lst=[]# The count of each food item is going to be saved in this list 
            count=0
            conn=sqlite3.connect("resturant.db")
            cursor= conn.cursor()
            cursor.execute("SELECT items_ordered FROM all_orders WHERE server_name= ?", (name,))
            result= cursor.fetchall()
            conn.commit()
            conn.close()
            if not result:
                print("No data is found ")
                return(None)
            
            for i in result:
                order= i[0]
                items= order.split(", ")
                for item in items:
                    clean= item.strip().title()
                    master_lst.append(clean)
            
            set_name= {i for i in master_lst}
            name_lst= list(set_name)
            
            for x in name_lst:
                count=0
                for d in master_lst:
                    if d==x:
                        count+=1
                values_lst.append(count)
            
            
            if len(values_lst)>0:
                    fig= plot.figure(figsize=(10,10))# The command is going to be creating a new figure and its size is being set up for a 10*10 dimension 
                    plot.pie(values_lst, labels= name_lst) # This command is going to plot a pie chart using the values with each value having a label according to the name of food item
                    plot.title("Order history for " + name) # This command is going to be giving a title for the pie chart which has the name of the server 
                    plot.show() #This command is going to be displaying the pie chart to the manager 
                    print("Pie chart has been plotted! ")
                    return(True)
            else:
                    print("It is not possible as there is no data ")
                    return(None)
        except sqlite3.Error: # The purpose of this is going to be handling an error of the file not being found gracefully by printing an error mesage 
            print("")
            return(False)
        except KeyError: # This statement is going to handle any key error if "Items ordered " header cannot be found in the order history file displaying an error message
                print("Key cannot be found!")
                return(False)
        except:  #All other common errors is going to be handled here other than FilenotFoundError 
            print("There seems to be an unknown error, Please try again!")
            return(False)
    # The debugger was also used in this function to identify what is happening with split_items and what was happning with count each time in order to ensure that the right quantitiy of the pie chart was plotted for each value 
    
    def show_bestselling_items(self):
        try:
            conn= sqlite3.connect("resturant.db")
            cursor= conn.cursor()
            cursor.execute("SELECT name, quantity_ordered FROM menu_inventory ORDER BY quantity_ordered DESC")
            data_items= cursor.fetchall()
            for i in data_items:
                print( i[0] + " - Sold: "+  str(i[1]))
            conn.close() 
        except sqlite3.Error:
            print('There is a SQL error, Please Try Again!')
        except:
            print('There is an unknown error, Please Try Again!')
    
    def show_most_productive_employee(self):
        try:
            conn= sqlite3.connect("resturant.db")
            cursor= conn.cursor()
            cursor.execute("SELECT server_name, salary_per_weeek FROM wages_per_week ORDER BY CAST (salary_per_weeek AS REAL) DESC")
            salary_items= cursor.fetchall()
            print("Highest Earners")
            for i in salary_items:
                print(i[0] + " - Amount: $" + str(i[1]))
            conn.close()
        except sqlite3.Error:
            print('There is a SQL error, Please Try Again!')
        except:
            print('There is an unknown error, Please Try Again!')
        
print("Welcome to the Resturant Management System")
while True:
    print("Please select an option from below")
    option= input("Access the program (A), Quit the program (Q): ")
    
    if option == "A" or option =="a": 
        type_person= input("Please enter if you are a server(S) or a manager(M): ") # The variable is asking if the person logging in the system is a server or a manager
        if type_person== "S" or  type_person== "s": # If the person is going to be in putting S for server, then a new object is going to forming with the server class 
            name_Server= input("Enter your name: ")               
            m= Server(name_Server.title())
            print()
            while True: # The loop is going to be running infinitely until the server wants to exit the program when they are done. 
                print("Options \n Add items to the menu : A \n Change the price for an item in the menu : C \n  Show menu: S \n  Take an order and show the bill: T  \n Log hours in : L \n  Exit the program :E " ) # The server has options of adding items to the menu, showing the menu, displaying the bill, log in hours and quit the program 
                options= input("What option do you want to take: ") # This variable is going to be asking the server to input what they want to do from the options above 
                if options == "A" or options =="a": # If option A which is adding items to the menu is chosen then add_item method is going to be called in the class to add items new items to self.menu
                    m.show_menu()
                    print()
                    m.add_item()
                    print()
                elif options =="C" or options== "c": # If the option to change the price of food items in the menu is chosen then the change_price method in the server class is going to be called allowing the server to change the price of a food item 
                    m.change_price()
                    print()
                elif options == "S" or options== "s": # If the option show menu is chosen , then the menu is going to be shown to the consumer 
                    m.show_menu()
                    print()
                elif options == "T" or options == "t":# If option T is chosen with the consumer going to be ordering items , showing the bill to the consumer, saving the food order to the order history file and lastly get money from the consumer 
                    m.order_items()
                    print()
                    m.show_bill()
                    print()
                    m.save_order_history()
                    m.get_money()
                    print()
                elif options== "L" or options== "l": # If option L is going to be chosen then the server is going to be able to log in their work hours in work_per_week 
                    m.work_per_week()
                elif options =="E" or options =="e":
                    print("Exiting!")
                    break
                else:# This condition is true if none of the options above is chosen asking the server to put the right option in and first priting a message
                    print("Invalid option. Please try again.")
        elif type_person== "M" or type_person== "m": # If the persion is going to be putting M for manager, there is going to be a new object created with the manager class 
            name_Manager= input("Enter your name: ")          
            s= Manager(name_Manager)
            authentication= s.authenticate() # After a new manager object is created, the person who is going to be the manager has to authenticate their details 
            if authentication== True: # If the authentication is going to be passed the manager will have some options to choose from 
                while True:# The loop is going to be running infinitely until the manager wants to exit the program when they are done. 
                    print("Options:-\n Calculate bonus for each person: B \n Show all the bonuses that are to be given this month : S \n Display the items ordered by each server in a pie chart :P \n Which item is sold the most :W \n Most productive employee :M \n Exit the program :E ")
                    options_manager= input("Please enter the letter of the option you want: ") # According to the options given to the manager, they can choose anyone 
                    if options_manager== "B" or options_manager== "b": # If the option chosen by the manager is to calculate the bonus for a server, the calculate_bonus method in the manager function is called 
                        name= input("Please enter the name of the person whose bonus you want to calculate:  ")
                        s.calculate_bonus(name)
                        print("Bonus calculated for "+ name)
                    elif options_manager== "S" or options_manager== "s": # If the option to show bonuses is chosen, then the method called show_bonuses is called and all the bonuses to be given are displayed
                        s.show_bonuses()
                    elif options_manager=="P" or options_manager=="p": # If this option is chosen,then the name of the server is going to be asked to input and then a pie chart of their order history is going to be displayed 
                        name1= input("Enter the name of the server whoose order history pie chart you want to see: ")
                        s.display_chart(name1)
                    elif options_manager== "W" or options_manager=="w":
                        s.show_bestselling_items()
                    elif options_manager== "M" or options_manager=="m":
                        s.show_most_productive_employee()
                    elif options_manager =="E" or options_manager =="e":
                        print("Exiting!")
                        break
                    else: # This condition holds true if none of the options are going to be chosen meaning a message is going to be displayed and the manager is asked to choose another option
                        print("Invalid option. Please try again.")
        else: # This message is going to be printed if neither S or M is chosen meaning a message is going to be displayed 
            print("Wrong input entered, Please Try Again!")
    elif option =="Q" or option =="q":# This is the last option that can be chosen which is going to be quitting the program
        print("Quitting the program ")
        break
    else: # This condition is going to be holding True if eiter A or Q is not selected asking the user to prompt again 
        print("No option is selected, please select a right option ")










