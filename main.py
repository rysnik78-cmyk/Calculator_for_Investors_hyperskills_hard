from enum import Enum
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv


Investor_base = declarative_base()
class Financial(Investor_base):
    __tablename__ = "financial"
    ticker = Column(String(30), primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)

class Companies(Investor_base):
    __tablename__ = "companies"
    ticker = Column(String(30), primary_key=True)
    name = Column(String(30))
    sector = Column(String(30))

class BaseLogic:
    def __init__(self):
        self.engine = create_engine("sqlite:///investor.db", echo=False)
        Investor_base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, future=True)
        self.load_from_csv('companies.csv', 'companies')
        self.load_from_csv('financial.csv', 'financial')
        print('Database created successfully!')

    def load_from_csv(self, file_path, table_name):
        financial_column_names = ['ticker',
                                  'ebitda',
                                  'sales',
                                  'net_profit',
                                  'market_price',
                                  'net_debt',
                                  'assets',
                                  'equity',
                                  'cash_equivalents',
                                  'liabilities']
        companies_column_names = ['ticker', 'name', 'sector']
        if table_name == 'financial':
            column_names = financial_column_names
        elif table_name == 'companies':
            column_names = companies_column_names
        session = self.Session()

        with open(file_path) as data_from_file:
            file_reader = csv.DictReader(data_from_file, delimiter=",", lineterminator="\n", fieldnames=column_names)
            count = 0

            for line in file_reader:
                if count == 0:
                    all_columns = [line]
                    count += 1
                    continue
                else:
                    for key in line.keys():
                        if not line[key]:
                            line[key] = None
                    if table_name == 'financial':
                        session.add_all([Financial(ticker = line['ticker'],
                                ebitda = line['ebitda'],
                                sales = line['sales'],
                                net_profit = line['net_profit'],
                                market_price = line['market_price'],
                                net_debt = line['net_debt'],
                                assets = line['assets'],
                                equity = line['equity'],
                                cash_equivalents = line['cash_equivalents'],
                                liabilities = line['liabilities'])])

                    elif table_name == 'companies':
                        session.add_all([Companies(ticker=line['ticker'],
                                               name = line['name'],
                                               sector = line['sector'])])
                    count += 1
        session.commit()


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
    database_engine = BaseLogic()

    # main_logic = Main_Logic()
