import random
random_num = [3259235652, 7452047265, 5824057253, 1348211024, 8617558991, 8023209650,
             8021252111, 7032286388, 3910473250, 8023235544, 2583250054]
chosen_num = []
data = {}                                  #\xz

class Account:
    __pin = 1234
    def __init__(self, name, account_no, account_type, balance):
        self.name = name
        self.account_no = account_no
        self.account_type = account_type
        self.balance = balance
        if self.account_no in data:
            print('Account already exists')
        else:
            data[self.account_no] = [self.__pin, self.name]
            
        
        
    def __get_pin(self):
        return self.__pin
    
    def __set_pin(self, new_pin):
        self.__pin = new_pin
        data[self.account_no][0] = new_pin
        print(f'Your new account pin is {new_pin}')
    pin_code = property(__get_pin, __set_pin)
    
    def show_balance(self):
        print('You currently have ' + str(self.balance) + ' Naira')
        
    def withdraw(self):
        try:
            amount = int(input(f'Amount: '))
            input_pin = int(input('PIN: '))
        except ValueError:
            print('Error')
        else:
            if input_pin == Account.__pin:
                if amount <= self.balance:
                    new_bal = self.balance - amount
                    print(f'You have withdrawn {amount} Naira\n'
                          + f'Balance: {new_bal} Naira')
                    self.balance = new_bal
                else:
                    print('Insufficient Balance')
            else:
                print('Invalid PIN')

    def deposit(self):
        try:
            amount = int(input(f'Amount: '))
        except ValueError:
            print('Error!! Try again')
        else:
            new_bal = self.balance + amount
            print(f'You have deposited {amount} Naira into your account\n'
                  + f'Balance: {new_bal} Naira')
            self.balance = new_bal
        
    def transfer(self):
        recipient = input('Beneficiary Account Number: ')
        try:
            amount = int(input(f'Amount: '))
            input_pin = int(input('PIN: '))
        except ValueError:
            print('Error! Please try again')
        else:
            if input_pin == Account.__pin:
                if amount <= self.balance:
                    new_bal = self.balance - amount
                    print(f'You have successfully transferred {amount}' +
                         f' Naira to {recipient}')
                    print(f'Balance: {new_bal}')
                    self.balance = new_bal
                else:
                    print('Insufficient funds')
            else:
                print('Invalid PIN')
#\        
    
customer1 = Account('John James', 2617558991,'Savings', 100000)
customer2 = Account('Mariam Michael', 5314917417, 'Current', 240000)
customer3 = Account('Harry Clark', 220433275, 'Current', 500000)
account_list = [customer1, customer2, customer3]

def numbers():
    n = random.choice(random_num)
    return n
ans = 0

def start():
    global ans
    print('Welcome to MicroBank PLC') #What would you like to do?')
    try:
        ans = int(input('1: Login\n' +
                        '2: Create Account\n' + 
                       '3: Quit\n'))
    except ValueError:
        print('Choose an option')
start()
logged = False
logged_num = 0
while not logged:
    if ans == 1:
        try:
            account_num = int(input('Account Number: '))
            if account_num in data.keys():
                trys = 0
                while trys < 5:
                    pin = int(input('Account PIN: '))
                    if pin == data[account_num][0]:
                        print('Login Successfull ')
                        logged = True
                        logged_num = account_num
                        trys = 6
                    else:
                        trys += 1
                        print('Incorrect pin')
                        if trys == 5:
                            print('Too many attempts')
                            break
            else:
                print('Account doesnt exist..')
        except ValueError:
            print('NUMBER!!')
            
        
    elif ans == 2:
        name = input('Enter First and Last name:\n')
        acc_no = numbers()
        if acc_no in chosen_num:
            acc_no = numbers()
        else:
            chosen_num.append(acc_no)
        acc_type = input('Account type(current or savings): ')
        new_cust = Account(name, acc_no, acc_type, 0)
        print('')
        print('Account has been created')
        print(f'Account Name: {name}\nAccount Number: {acc_no}\n' +
              f'Account type: {acc_type}\nBalance: {0} Naira')
        account_list.append(new_cust)
        print('')
        start()
        
    elif ans == 3:
        print('Good bye')
        break
    else:
        print('Invalid option')
        break

while logged:
    
    print('==========================================================')
    data_keys = data.keys()
    list_keys = list(data_keys)
    for i in account_list:
        loop = getattr(i, 'account_no' )
        if loop == logged_num:
            obj = list_keys.index(loop)
            customer = account_list[obj]

               
    print(f'Welcome {customer.name}\nWhat would you like to do?\n')
    try:
        option = int(input('1: Account Balance\n'+
                          '2: Deposit\n'+
                          '3: Withdrawal\n'+
                          '4: Transfer\n'+
                          '5: Change PIN\n' +
                          '6: Exit\n'))
    except ValueError:
        print('Invalid Option')
    else:
        if option == 1:
            customer.show_balance()
        elif option == 2:
            customer.deposit()
        elif option == 3:
            customer.withdraw()
        elif option == 4:
            customer.transfer()
        elif option == 5:
            try:
                old_pin = int(input('Enter old pin(default is 1234): '))
                if old_pin == customer.pin_code:
                    new = int(input('Enter new account pin: '))
                    customer.pin_code = new
                else:
                    print('Invalid PIN')
            except ValueError:
                print('You can have letters in pin')
        elif option == 6:
            print('Thank you!!')
            break
        else:
            print('Invalid Option')
 

    