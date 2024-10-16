import mysql.connector as sql
import random
import time 
import re
import datetime as dt
import pwinput as pw

mycon = sql.connect(host = "localhost", user = "root" , passwd = "", database = "Money_minder")

mycursor = mycon.cursor()
mycon.autocommit = True

# mycursor.execute("CREATE DATABASE Money_minder") 
# mycursor.execute("CREATE TABLE customer(id INT(4) AUTO_INCREMENT PRIMARY KEY,fullname VARCHAR(255),email VARCHAR(255) UNIQUE,password VARCHAR(255) UNIQUE,accountNumber VARCHAR(255),date VARCHAR(255),accountBalance VARCHAR(255))")
 


from colorama import init,Fore,Back,Style
init()

class Banking_app():
        def __init__(self) -> None:
            
            self.home()
            self.account = random.randint(0000000000,999999999)

        def home(self):
            
#             # self.account = random.randint(0000000000,999999999)
            print(Fore.GREEN + "WELCOME TO PYTHON BANK".center(100,"~"))
            print(Style.RESET_ALL)
            print("1.Sign Up\n2.Login")
            option = int(input("Option:").strip())
            if option == 1:
                 self.sign()
              
            elif option == 2:
                self.login() 
            else :
                print("Invalid input.\nPlease try again later")
                time.sleep(5)
                self.home() 
# bb=Banking_app()
        def sign(self):
            self.account = random.randint(0000000000,999999999)
            print("You're about to create an account with us ...")
            fullname = input("Fullname:").strip().lower()
            email =  input("Email:").strip().lower()      
            password = int(input("Enter your 4-digit pin:".strip()))
            accountbal=0
            account_no =(self.account)
            print('This is your account number: ', account_no)
            

            dat = dt.datetime.now()
            date = dat 
            # # print(date)
            pattern=r'^\w+@\w+\.\w+$'
            matches = re.match(pattern,email)

            # print(matches)
            if matches:
                print(Fore.GREEN + f"You've successfully create an account with us.\nHere is your account number:{self.account}")
                print(Style.RESET_ALL)
                query="INSERT INTO customer(fullname,email,password,accountNumber,date,accountBalance) VALUE(%s,%s,%s,%s,%s,%s)"
                value = (fullname,email,password,self.account,date,accountbal)
                mycursor.execute(query,value)
                mycon.commit()
                self.login()
            else:
                print(Fore.RED + "Invalid email")
                print(Style.RESET_ALL)
                self.home()
           
        #     print(mycursor.rowcount,"row added")
             

        def login(self):
            # print("YOU'RE ABOUT TO LOGIN")
            accountNumber = int(input("Account number:".strip()))
            password = pw.pwinput()
            query = 'SELECT fullname, accountNumber, accountBalance FROM customer WHERE accountNumber= %s AND password= %s'
            value= (accountNumber,password)
            mycursor.execute(query,value)
            details = mycursor.fetchmany()
        #     account = details[][4]
        #     print(details)      
        #     if account == accoun and password :
            if details:
                print("Login successful\n1.Deposit\n2.Withdraw\n3.Check Balance\n4.Transfer\n5.Close account\n6.Details\n7.Recharge\n8.Exit")
                option = int(input("Option:").strip())
                if option == 1:
                    self.deposit()
                elif option == 2:
                    self.withdraw()
                elif option == 3:
                    self.balance() 
                elif option == 4:
                    self.transfer() 
                elif option == 5:
                    self.close() 
                elif option == 6:
                    self.detail()
                elif option == 7:
                    self.recharge()
                elif option == 8:
                    exit()
                else:
                    print("Input numbers from 1-7.")
                    time.sleep(3)
            else:
                user = input('Invalid login details, press 1 to reset password:')
                if user == '1':
                        self.reset_password()
                else:
                     self.login()
        def reset_password(self):
                email = input('Email: ')
                query = 'SELECT fullname, accountNumber, accountBalance FROM customer WHERE email= %s'
                values = (email,)
                mycursor.execute(query,values)
                details = mycursor.fetchone()
                # print(details)
                if details:
                        print(Fore.GREEN + f'Email verified successfully.')
                        print(Style.RESET_ALL)
                        new_password = input('New password: ')

                        query = 'UPDATE customer SET password = %s WHERE email =%s'
                        values = (new_password, email)
                        mycursor.execute(query,values)
                        # print(mycursor.rowcount,'user password reset successfully.')
                        self.login()

                else:
                        print('Invalid Email Address.')
                        self.login()       
        

            
        def deposit(self):
            
            deposit = int(input("Enter the amount you wish to deposit:"))
            account_no = input("Your account_no:")
            password = pw.pwinput()
            que = "SELECT * FROM customer WHERE accountNumber = %s and password = %s"
            val = (account_no,password)
            mycursor.execute(que,val)
            result  = mycursor.fetchall()
        #     print(result)
            account_balance = result[0][6]
            balance = int(account_balance)+int(deposit)
            query = "UPDATE customer SET accountBalance=%s WHERE accountNumber = %s"
            val = (balance, account_no)
            mycursor.execute(query,val) 
            mycon.commit()
            print(Fore.GREEN + f"You've successfully deposited #{deposit}.\nThanks for banking with us.")
            print(Style.RESET_ALL)
            print("You now have #",balance)


        def withdraw(self) :

                withdraw = int(input("Enter the amount you wish to withdraw:").strip()) 
                account = input("Input your account number:")
                password = pw.pwinput()
                q="SELECT * FROM customer WHERE accountNumber = %s and password = %s"
                v = (account,password)
                mycursor.execute(q,v)
                result = mycursor.fetchall()
                # print(result)
                accountbal=result[0][6]
                if int(accountbal) > int(withdraw):
                        balance = int(accountbal) - int(withdraw)
                        query = "UPDATE customer SET accountBalance = %s WHERE accountNumber = %s"
                        value = (balance,account)
                        mycursor.execute(query,value)
                        mycon.commit()
                        print(Fore.GREEN + f"Dear customer, your withdrawal of #{withdraw} is successful.")
                        print(Style.RESET_ALL)
                else:
                        print(Fore.RED + "Insufficient balance\nTry and fund your account.")
                        print(Style.RESET_ALL)



        def balance(self):
                
                account = input("Enter your account number:").strip()
                password = pw.pwinput()
                p = "SELECT * FROM customer WHERE accountNumber = %s and password=%s"
                q = (account,password)
                mycursor.execute(p,q)
                result = mycursor.fetchall()
                accountbal=result[0][6]
                print("Dear customer, your account balance is #",accountbal,'.')
        
        def transfer(self):
#         print("You're about to transfer")
                account = input("Your account number:").strip()
                password = pw.pwinput()
                q = "SELECT * FROM customer WHERE accountNumber=%s and password=%s"
                v = (account,password)
                mycursor.execute(q,v)
                result = mycursor.fetchall()
                accountbal = result[0][6]
                if result:
                        amount = int(input("Input the amount you wish to transfer:").strip())
                        if int(accountbal) > int(amount):
                                total = int(accountbal)-int(amount)
                                quey = "UPDATE customer SET accountBalance = %s WHERE accountNumber = %s"
                                vale = (total,account)
                                mycursor.execute(quey,vale)
                                mycon.commit
                                numb = int(input("Enter reciever's account number:").strip()) 
                                name  = input("Input reciever's account name:").strip().lower()
                                query = "SELECT * FROM customer WHERE accountNumber = %s and fullname = %s"
                                val = (numb,name)
                                mycursor.execute(query,val)
                                resut = mycursor.fetchall()
                                accout = resut[0][6] 
                                print(resut)
                                if resut:
                                    tital  = int(accout) +int(amount)
                                    qury = "UPDATE customer SET accountBalance = %s WHERE accountNumber = %s"
                                    value = (tital,numb)
                                    mycursor.execute(qury,value)
                                    mycon.commit()
                                    print(Fore.GREEN + f"Dear customer,you've successfully transfer {amount} to {numb} and your balance is", total)
                                    print(Style.RESET_ALL)
                                else:
                                    print(Fore.RED + "Invalid input")
                                    print(Style.RESET_ALL)    
                        else:
                                print(Fore.RED + "Insufficient funds\nPlease fund your account")
                                print(Style.RESET_ALL)
                else:
                    print(Fore.RED + "Invalid inputs\nPlease try again later")
                    print(Style.RESET_ALL)
                    self.login()


        def close(self):
#        print("You're about to delete your account")
            account = input("Enter your account number:")
            password = pw.pwinput()
            q = "SELECT * FROM customer WHERE accountNumber=%s and password=%s"
            v = (account,password)
            mycursor.execute(q,v)
            result = mycursor.fetchone()
            if result:
                print("These are your details".center(50,"`"))
                # print("Your id = ",result[0] )
                print("Your name = ",result[1])
                print("Your email = ",result[2])
                print("Your password= ",result[3])
                print("Your account number= ",result[4])
                print("The date you registered = ",result[5])
                print("Your account balance = ",result[6])
                print("Are you sure you want close your account")
                print("1.YES\n2.NO")
                option = int(input("Option:").strip())
                if option == 1:
                    print(Fore.RED + "You're about to delete your account")
                    print(Style.RESET_ALL) 
                    account = int(input("Enter your account number:").strip())
                    password = pw.pwinput()
                    delete = "DELETE FROM customer WHERE accountNumber=%s and password =%s"
                    value = (account,password)
                    mycursor.execute(delete,value)
                    print(Fore.GREEN+ f"Dear customer you've successfully deleted {account} account\nThank you for banking with us")
                    print(Style.RESET_ALL) 

                elif option == 2:
                         self.login()
                else:
                         print("Input number from number 1-2\n Try again later")

        def detail(self):
            account = input("Your account number:").strip()
            password = pw.pwinput()
            q = "SELECT * FROM customer WHERE accountNumber=%s and password=%s"
            v = (account,password)
            mycursor.execute(q,v)
            result = mycursor.fetchone()
            if result:
                # print("Your id = ",result[0] )
                print("Your name = ",result[1])
                print("Your email = ",result[2])
                print("Your password= ",result[3])
                print("Your account number= ",result[4])
                print("The date you registered = ",result[5])
                print("Your account balance = ",result[6])  

            else:
                 print(Fore.GREEN+'ERROR!')


        def recharge(self):
            # print("You're about to recharge")
            account = input("Enter account number:").strip()
            password = pw.pwinput()
            q="SELECT * FROM customer WHERE accountNumber=%s and password=%s"
            v=(account,password)
            mycursor.execute(q,v)
            result = mycursor.fetchall()
            accountbal=result[0][6]
            if result:
                recharge = int(input("Enter the reciver phone number:").strip())
                # account = input("Enter account number:").strip()
                amount = int(input("Amount:#").strip())
                if int(accountbal) > int(amount):
                   total=int(accountbal)-int(amount)
                   print("1.MTN\n2.GLO\n3.ETISALAT\n4.AIRTEL")
                   option = int(input("Option:").strip())
                   if option == 1:
                       print(f"Dear customer, the recharge of {amount} MTN card was successful\nYur balance is #",total)
                   elif option==2:
                       print(f"Dear customer, the recharge of {amount} GLO card was successful\nYour balance is #",total)
                   elif option==3:
                       print(f"Dear customer, the recharge of {amount} ETISALAT card was successful\nyour balance is #",total)
                   elif option==4:
                       print(f"Dear customer, the recharge of {amount} AIRTEL card was successful\nyour balance is #",total)
                   query = "UPDATE customer SET accountBalance = %s WHERE accountNumber = %s"
                   value = (total,account)
                   mycursor.execute(query,value)
                   mycon.commit()
                else:
                       print("Insufficient fund\nPlease fund your wallet")
            else:
                print("Invalid input\nPlease try agian later")              
    
bb=Banking_app() 
   

       

 


    

    





   

           
 

