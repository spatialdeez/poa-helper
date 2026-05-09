import time, re, csv




def number_check_filter(input):
    try:
        input = int(input)
        return input
    except:
        return None
    
def check_filter(input, filter):
    for f in filter:
        if str(input) == str(f):
            return input
    return None

def fileImport():
    find_class_name = re.compile(r'^#') # regex pattern to detect category
    find_end = re.compile(r'^/end')  # Regex pattern to detect the end marker of category
    
    # initialize empty lists for each category
    non_current_assets = []
    current_assets = []
    equity = []
    non_current_liabilities = []
    current_liabilities = []
    
    current_category = None  # track active category
    
    # sole proprietorship
    with open('sp_category.txt', mode='r') as file:
        for line in file.readlines():
            line = line.strip() 
            # set the active category based on the current category line
            if find_class_name.search(line):
                if line == '#NON-CURRENT-ASSETS':
                    current_category = 'non_current_assets'
                elif line == '#CURRENT-ASSETS':
                    current_category = 'current_assets'
                elif line == '#EQUITY':
                    current_category = 'equity'
                elif line == '#NON-CURRENT-LIABILITIES':
                    current_category = 'non_current_liabilities'
                elif line == '#CURRENT-LIABILITIES':
                    current_category = 'current_liabilities'
            elif find_end.search(line):  # reset category when /end is reached
                current_category = None
            elif current_category and line:  # only append non-empty lines under an active category
                # append to the appropriate list based on current_category
                if current_category == 'non_current_assets':
                    non_current_assets.append(line)
                elif current_category == 'current_assets':
                    current_assets.append(line)
                elif current_category == 'equity':
                    equity.append(line)
                elif current_category == 'non_current_liabilities':
                    non_current_liabilities.append(line)
                elif current_category == 'current_liabilities':
                    current_liabilities.append(line)
    return non_current_assets, current_assets, equity, non_current_liabilities, current_liabilities


def financial_statements_creator():
    non_current_assets, current_assets, equity, non_current_liabilities, current_liabilities = fileImport()
    inputted_non_current_assets = {}
    inputted_current_assets = {}
    inputted_equity = {}
    inputted_non_current_liabilities = {}
    inputted_current_liabilities = {}
    total = 0

    regex_patterns = {'prepaid expense': re.compile(r'^prepaid'), # current asset
                      'income receivable': re.compile(r'income receivable$'), # current asset
                      'expense payable': re.compile(r'expense payable$'), # current liabilities
                      'received in advance': re.compile(r'received in advance$') # current liabilities
                      }

    # test
    # print(non_current_assets, current_assets, equity, non_current_liabilities, current_liabilities)
    
    def amount_add_account():
        while True:
            value = input('Enter the amount in the account > ')
            value = number_check_filter(value)
            if value == None:
                print('Not a number! Enter a valid number')
                continue
            break
        return value
    
    while True:
        print('\n' + '-'*30 +'FINANCIAL STATEMENTS CREATOR' + '-'*30)
        print('\nNOTES: If there is something you want to add into the financial statement calculator but it does not exist do add them to sp_category.txt for sole proprietorship')
        print('How would you like to input the data values?\n1. Enter values and name manually\n2. Import .csv\n3. Import excel')
        answer = input('> ')
        answer = number_check_filter(answer)
        if answer == 1:
            print('NOTES: 1. Owner\'s equity if it is a loss please enter \'profit\' and put a negative number instead.\nREQUIRED values to calculate: drawings (if you dont have the value, enter 0 to not interfere in calculations)')
            while True:
                key = input('Enter the name of account (enter 0 to finish) >')
                if key in non_current_assets:
                    value = amount_add_account()
                    inputted_non_current_assets[key] = value
                elif key in current_assets:
                    value = amount_add_account()
                    inputted_current_assets[key] = value
                elif key in equity:
                    value = amount_add_account()
                    inputted_equity[key] = value
                elif key in non_current_liabilities:
                    value = amount_add_account()
                    inputted_non_current_liabilities[key] = value
                elif key in current_liabilities:
                    value = amount_add_account()
                    inputted_current_liabilities[key] = value
                elif key == '0':
                    break
                else:
                    match = False
                    for k, v in regex_patterns.items():
                        if v.search(key):
                            if k in ['prepaid expense', 'income receivable']:
                                value = amount_add_account()
                                inputted_current_assets[key] = value
                            elif k in ['expense payable', 'received in advance']:
                                value = amount_add_account()
                                inputted_current_liabilities[key] = value
                            match = True
                            break
                    if not match:
                        print('Account not in any valid category! Try again.')
                        continue
        
        # import csv using pandas
        elif answer == 2:
            file_contents = {}
            filename = input('Please input .csv filename (must be in same directory as program, header must be name and value): ') 
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for rows in reader:
                    try:
                        file_contents[rows['name']] = rows['value']
                    except:
                        print('Header must be name and value (name,value) in the .csv file')
                        break
            file.close()
            for key, value in file_contents.items():
                if key in non_current_assets:
                    inputted_non_current_assets[key] = int(value)
                elif key in current_assets:
                    inputted_current_assets[key] = int(value)
                elif key in equity:
                    inputted_equity[key] = int(value)
                elif key in non_current_liabilities:
                    inputted_non_current_liabilities[key] = int(value)
                elif key in current_liabilities:
                    inputted_current_liabilities[key] = int(value)
                elif key == '0':
                    break
                else:
                    match = False
                    for k, v in regex_patterns.items():
                        if v.search(key):
                            if k in ['prepaid expense', 'income receivable']:
                                inputted_current_assets[key] = int(value)
                            elif k in ['expense payable', 'received in advance']:
                                inputted_current_liabilities[key] = int(value)
                            match = True
                            break
                    if not match:
                        print('Account not in any valid category! Try again.')
                        continue



        print(inputted_non_current_assets, inputted_current_assets, inputted_equity, inputted_non_current_liabilities, inputted_current_liabilities)
        with open('fs.txt', mode='w') as file:
            title_width = 45
            col_width = 25
            
            # non current assets
            total_non_current_aasets = 0
            file.write(f"{'Assets':<{title_width}}{'$':>{col_width}}{'$':>{col_width}}{'$':>{col_width}}\n")
            file.write(f"{'Non-current Assets':<{title_width}}{'Cost':>{col_width}}{'acc. depreciation':>{col_width}}{'Net book value':>{col_width}}\n")
            for nca, amount in inputted_non_current_assets.items():
                while True:
                    inputted_acc_dep = number_check_filter(input(f'Enter accumulated depreciation of {nca} (type 0 for no depreciation): '))
                    if inputted_acc_dep is None:
                        print('Not a number! Enter a valid number')
                        continue
                    net_book_value = int(amount) - int(inputted_acc_dep)
                    total_non_current_aasets += net_book_value
                    break

                file.write(f"{nca:<{title_width}}{amount:>{col_width}}{inputted_acc_dep:>{col_width}}{net_book_value:>{col_width}}\n")

            file.write(f"{'Total':<{title_width}}{'':>{col_width}}{'':>{col_width}}{total_non_current_aasets:>{col_width}}\n\n")

            # current assets
            total_current_assets = 0
            file.write("Current Assets\n")
            file.write(f"{'':<{title_width}}{'':>{col_width}}{'':>{col_width}}{'':>{col_width}}\n")
            for ca, amount in inputted_current_assets.items():
                if ca in ['trade receivables', 'trade receivable']:
                    allowance_tr = number_check_filter(input('Allowance for impairment of trade receivables (type 0 if none): '))
                    if allowance_tr != 0:
                        file.write(f"{'trade receivables':<{title_width}}{amount:>{col_width}}{'':>{col_width}}{'':>{col_width}}\n")
                        file.write(f"{'Allowance for impairment of trade receivables':<{title_width}}{allowance_tr:>{col_width}}{'':>{col_width}}{'':>{col_width}}\n")
                        file.write(f"{'Net trade receivables':<{title_width}}{'':>{col_width}}{(amount - allowance_tr):>{col_width}}{'':>{col_width}}\n")
                        total_current_assets += (amount - allowance_tr)
                    else:  
                        file.write(f"{ca:<{title_width}}{'':>{col_width}}{amount:>{col_width}}{'':>{col_width}}\n")
                        total_current_assets += amount
                else:
                    file.write(f"{ca:<{title_width}}{'':>{col_width}}{amount:>{col_width}}{'':>{col_width}}\n")
                    total_current_assets += amount

            file.write(f"{'Total':<{title_width}}{'':>{col_width}}{'':>{col_width}}{total_current_assets:>{col_width}}\n\n")

            # total assets
            total_balance_1 = (total_current_assets + total_non_current_aasets)
            file.write(f"{'Total assets':<{title_width}}{'':>{col_width}}{'':>{col_width}}{(total_current_assets + total_non_current_aasets):>{col_width}}\n\n")

            # owners equity
            try:
                total_equity = sum(inputted_equity.values()) - (inputted_equity['drawings'] * 2)
            except KeyError:
                total_equity = sum(inputted_equity.values())
            file.write('Owner\'s equity\n')
            file.write(f"{'Capital':<{title_width}}{'':>{col_width}}{'':>{col_width}}{total_equity:>{col_width}}\n\n")

            # non current liabilites
            total_non_current_liabilities = 0
            file.write('Non-current liabilities\n')
            for ncl, amount in inputted_non_current_liabilities.items():
                file.write(f"{'Long-term borrowings':<{title_width}}{'':>{col_width}}{'':>{col_width}}{amount:>{col_width}}\n")
                total_non_current_liabilities += amount
            
            # current liabilities
            total_current_liabilities = 0
            file.write('\nCurrent liabilites\n')
            for cl, amount in inputted_current_liabilities.items():
                file.write(f"{cl:<{title_width}}{'':>{col_width}}{amount:>{col_width}}{'':>{col_width}}\n")
                total_current_liabilities += amount
            file.write(f"{'Total':<{title_width}}{'':>{col_width}}{'':>{col_width}}{total_current_liabilities:>{col_width}}\n\n")
            
            total_balance_2 = (total_non_current_liabilities + total_current_liabilities + total_equity)
            file.write(f"{'Total equity and liabilities':<{title_width}}{'':>{col_width}}{'':>{col_width}}{(total_non_current_liabilities + total_current_liabilities + total_equity):>{col_width}}\n\n")
            
            if total_balance_1 == total_balance_2:
                file.write('\n\n Balance OK')
            else:
                file.write('The statement is not balanced. Do check your numbers again')
        file.close()


        


def onStart():
    # Variables
    while True:
        print('1. Print out financial statements')
        answer = input('> ')
        answer = number_check_filter(answer)
        if answer == 1:
            financial_statements_creator()

if __name__ == '__main__':
    onStart()