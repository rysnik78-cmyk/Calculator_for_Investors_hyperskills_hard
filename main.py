from enum import Enum

#  time_parser = EVENT_CONSTANTS[event['type']].value['time parser']
# class EVENT_CONSTANTS(Enum):
#     note = {'time input': 'Enter datetime in "YYYY-MM-DD HH:MM" format: ', 'time parser': '%Y-%m-%d %H:%M',
#             'name input': 'Enter text: ', 'quantity input': 'How many notes would you like to add: ',
#             're_pattern': r'\d\d\d\d-\d\d-\d\d \d\d:\d\d'}
#     birthday = {'time input': 'Enter date of birth in "YYYY-MM-DD" format: ', 'time parser': '%Y-%m-%d',
#                 'name input': 'Enter name: ',
#                 'quantity input': 'How many dates of birth would you like to add: ',
#                 're_pattern': r'\d\d\d\d-\d\d-\d\d'}

class MENU_ELEMENTS(Enum):
    MENU = {'MAIN MENU' : {0: 'Exit',1: 'CRUD operations',2: 'Show top ten companies by criteria'},
            'CRUD MENU' : {0: 'Back',1: 'Create a company', 2: 'Read a company',3: 'Update a company',4: 'Delete a company', 5: 'List all companies'},
            'TOP TEN MENU': {0: 'Back',1: 'List by ND/EBITDA', 2: 'List by ROE', 3: 'List by ROA'}}

class Main_Logic():
    def __init__(self):
        self.program_status = 'MAIN MENU'
        self.main_loop()

    def print_actual_menu(self, menu_type):
        print(menu_type)
        for key, menu_text in MENU_ELEMENTS.MENU.value[menu_type].items():
            print(key, menu_text)

    def main_loop(self):
        while True:
            self.print_actual_menu(self.program_status)
            print('\nEnter an option:')
            ni = 'Not implemented!'
            io = 'Invalid option!'
            command = input()
            match self.program_status, command:
                case 'MAIN MENU', '0':
                    print('Have a nice day!')
                    break
                case 'MAIN MENU', '1':
                    self.program_status = 'CRUD MENU'
                    continue
                case 'MAIN MENU', '2':
                    self.program_status = 'TOP TEN MENU'
                    continue
                case 'MAIN MENU', _:
                    print(io)
                    continue
                case 'CRUD MENU', '0':
                    self.program_status = 'MAIN MENU'
                    continue
                case 'CRUD MENU', '1':
                    print(ni)
                    self.program_status = 'MAIN MENU'
                    continue
                case 'CRUD MENU', '2':
                    print(ni)
                    self.program_status = 'MAIN MENU'
                    continue
                case 'CRUD MENU', '3':
                    print(ni)
                    self.program_status = 'MAIN MENU'
                    continue
                case 'CRUD MENU', '4':
                    print(ni)
                    self.program_status = 'MAIN MENU'
                    continue
                case 'CRUD MENU', _:
                    print(io)
                    continue
                case 'TOP TEN MENU', '0':
                    self.program_status = 'MAIN MENU'
                    continue
                case 'TOP TEN MENU', '1':
                    print(ni)
                    self.program_status = 'MAIN MENU'
                    continue
                case 'TOP TEN MENU', '2':
                    print(ni)
                    self.program_status = 'MAIN MENU'
                    continue
                case 'TOP TEN MENU', '3':
                    print(ni)
                    self.program_status = 'MAIN MENU'
                    continue
                case 'TOP TEN MENU', _:
                    print(io)
                    continue

if __name__ == '__main__':
    main_logic = Main_Logic()
