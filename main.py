import enum
from enum import Enum
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import operator
import csv
import os
from sqlalchemy.sql.operators import ilike_op

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
        self.Session = sessionmaker(bind=self.engine, future=True, autoflush=False)
        self.financial_column_names = ['ticker',
                                  'ebitda',
                                  'sales',
                                  'net_profit',
                                  'market_price',
                                  'net_debt',
                                  'assets',
                                  'equity',
                                  'cash_equivalents',
                                  'liabilities']
        self.companies_column_names = ['ticker', 'name', 'sector']
        self.path = os.getcwd() + '\\investor.db'

        with self.Session() as session:
            company = session.scalar(select(Companies.ticker))

        if company is None:
            # print("loading")
            self.load_from_csv('companies.csv', 'companies')
            self.load_from_csv('financial.csv', 'financial')

        # if os.path.isfile(self.path):
        #     print("not loading")
        # else:
        #     print("loading")
        #     self.load_from_csv('companies.csv', 'companies')
        #     self.load_from_csv('financial.csv', 'financial')
        # else:
        #
        # print('Database created successfully!')


    def load_from_csv(self, file_path, table_name):
        if table_name == 'financial':
            column_names = self.financial_column_names
        elif table_name == 'companies':
            column_names = self.companies_column_names

        with open(file_path) as data_from_file:
            file_reader = csv.DictReader(data_from_file, delimiter=",", lineterminator="\n", fieldnames=column_names)
            count = 0
            for line in file_reader:
                if count == 0:
                    count += 1
                    continue
                else:
                    count += 1
                    for key in line.keys():
                        if not line[key]:
                            line[key] = None
                    if table_name == 'financial':
                        self.add_financial_data(line)
                    elif table_name == 'companies':
                        self.add_company_data(line)

    def company_data_input(self):
        company_data = {}
        for key, text in TableElements.Companies.value.items():
            # company_data[key] = input(text)
            input_text = input(text)
            # print(key)
            company_data[key]=input_text
        # print(company_data)
        return company_data

    def add_company_data(self, row):
        # print(row['ticker'])
        session = self.Session()
        session.add_all([
            Companies(ticker=row['ticker'], name=row['name'], sector=row['sector'])
    ])
        session.commit()

    def financial_data_input(self, company_ticker):
        financial_data = {}
        for key, text in TableElements.Financial.value.items():
            if key == 'ticker':
                financial_data[key] = company_ticker
            else:
                financial_data[key] = float(input(text))
        return financial_data

    def add_financial_data(self, row):
        session = self.Session()
        session.add_all([Financial(ticker=row['ticker'],
                                       ebitda=row['ebitda'],
                                       sales=row['sales'],
                                       net_profit=row['net_profit'],
                                       market_price=row['market_price'],
                                       net_debt=row['net_debt'],
                                       assets=row['assets'],
                                       equity=row['equity'],
                                       cash_equivalents=row['cash_equivalents'],
                                       liabilities=row['liabilities'])])
        session.commit()

    def add_company(self):
        company_data = self.company_data_input()
        self.add_company_data(company_data)
        financial_data = self.financial_data_input(company_data['ticker'])
        self.add_financial_data(financial_data)
        print('Company created successfully!')

    def retrieve_company(self):
        company_name = input('Enter company name: ')

        session = self.Session()
        query = select(Companies)
        # print(type(query))
        # print(query)
        result = session.scalars(query)
        if not list(result):
            return None
        companies_dictionary_with_string_in_name = self.company_dict_from_base(string_in_company_name=company_name)
        if not companies_dictionary_with_string_in_name:
            return None
        self.print_list_of_companies_from_dict(companies_dictionary_with_string_in_name, prefix=True, ticker=False)
        chosen_company_number = int(input('Enter company number: \n'))
        chosen_key = list(companies_dictionary_with_string_in_name.keys())[chosen_company_number]
        return chosen_key # company ticker

    def read_company_from_base(self):
        chosen_company_ticker = self.retrieve_company()
        if chosen_company_ticker is None:
            print('Company not found!')
        else:
            self.print_financial_indicators(chosen_company_ticker)

    def print_financial_indicators(self, company_ticker):
        indicator_dict = self.financial_indicators(company_ticker)
        session = self.Session()
        query = select(Companies).where(Companies.ticker == company_ticker)
        company = session.scalar(query)
        print(company.ticker, company.name)
        for key, value in indicator_dict.items():
            print(f'{key} = {value}')


    def financial_indicators(self, company_ticker):
        def verified_division_round(a, b):
            if a is None or b is None:
                return 'None'
            else:
                return round(a / b, 2)

        session = self.Session()
        query = select(Financial).where(Financial.ticker == company_ticker)
        financial = session.scalar(query)
        # P/E = Market price / Net profit
        # P/S = Market price / Sales
        # P/B = Market price / Assets
        # ND/EBITDA = Net debt / EBITDA
        # ROE = Net profit / Equity
        # ROA = Net profit / Assets
        # L/A = Liabilities / Assets
        indicators = {'ticker': company_ticker}

        indicators['P/E'] = verified_division_round(financial.market_price, financial.net_profit)
        indicators['P/S'] = verified_division_round(financial.market_price, financial.sales)
        indicators['P/B'] = verified_division_round(financial.market_price , financial.assets)
        indicators['ND/EBITDA'] = verified_division_round(financial.net_debt , financial.ebitda)
        indicators['ROE'] = verified_division_round(financial.net_profit , financial.equity)
        indicators['ROA'] = verified_division_round(financial.net_profit , financial.assets)
        indicators['L/A'] = verified_division_round(financial.liabilities , financial.assets)
        session.close()
        return indicators


    def update_company_from_base(self):
        chosen_company_ticker = self.retrieve_company()
        if chosen_company_ticker is None:
            print('Company not found!')
        else:
            new_data = self.financial_data_input(chosen_company_ticker)
            # print(new_data)
            session = self.Session()
            query = session.query(Financial).where(Financial.ticker == chosen_company_ticker)
            query.update({
                            "ticker": chosen_company_ticker,
                            "ebitda": new_data['ebitda'],
                            "sales": new_data['sales'],
                            "net_profit": new_data['net_profit'],
                            "market_price": new_data['market_price'],
                            "net_debt": new_data['net_debt'],
                            "assets": new_data['assets'],
                            "equity": new_data['equity'],
                            "cash_equivalents": new_data['cash_equivalents'],
                            "liabilities": new_data['liabilities']})
            session.commit()
            print('Company updated successfully!')

    def delete_company_from_base(self):
        chosen_company_ticker = self.retrieve_company()
        if chosen_company_ticker is None:
            print('Company not found!')
        else:
            session = self.Session()
            query = session.query(Financial)
            my_filter = query.filter(Financial.ticker == chosen_company_ticker)
            my_filter.delete()
            query = session.query(Companies)
            my_filter = query.filter(Companies.ticker == chosen_company_ticker)
            my_filter.delete()
            print('Company deleted successfully!')
            session.commit()

    def company_dict_from_base(self, string_in_company_name = None):
        session = self.Session()
        query = select(Companies)
        result = session.scalars(query).all()
        if not result:
            return None
        company_dictionary = {}
        for company in result:
            if string_in_company_name:
                if string_in_company_name.lower() in str(company.name).lower():
                    company_dictionary[company.ticker] = {'name': company.name, 'sector': company.sector}
            else:
                company_dictionary[company.ticker] = {'name': company.name, 'sector': company.sector}
        if not company_dictionary:
            return None
        else:
            return company_dictionary

    def print_list_of_companies_from_dict(self,company_dict, prefix=False, ticker=True, name=True, sector=False, sorted=False, reverse=False):
        company_count = 0
        for key in company_dict.keys():
            string_to_print = ''
            if prefix:
                string_to_print += str(company_count) + ' '
            if ticker:
                string_to_print += key + ' '
            if name:
                string_to_print += company_dict[key]['name']
            if sector:
                string_to_print += ' ' + company_dict[key]['sector']
            print(string_to_print)
            company_count += 1

    def print_sorted_list_of_all_companies(self):
        print('COMPANY LIST')
        companies_dictionary_with_string_in_name = self.company_dict_from_base()
        if companies_dictionary_with_string_in_name:
            sorted_company_dict = dict(sorted(companies_dictionary_with_string_in_name.items(), key=operator.itemgetter(0)))
            self.print_list_of_companies_from_dict(sorted_company_dict, prefix=False, ticker=True, sector=True)

    def print_top_ten_according_to_indicator(self, indicator='all'):
        # TODO dokończy tą funckję
        session = self.Session()
        query = select(Companies.ticker)
        results = session.scalars(query).all()
        all_companies_indicator_dict = {}
        for ticker in results:
            indicator_calculated = self.financial_indicators(ticker)[indicator]
            if indicator_calculated != 'None':
                all_companies_indicator_dict[ticker] = indicator_calculated
        sorted_dict_by_indicator = dict(sorted(all_companies_indicator_dict.items(), key=operator.itemgetter(1), reverse=True))
        print('TICKER', indicator)
        count = 0
        for key, value in sorted_dict_by_indicator.items():
            count = count + 1
            print(key, value)
            if count == 10:
                break

class TableElements(Enum):
    Financial = {'ticker': "Enter ticker (in the format 'MOON'):",
                  'ebitda': "Enter ebitda (in the format '987654321'):",
                  'sales': "Enter sales (in the format '987654321'):",
                  'net_profit': "Enter net profit (in the format '987654321'):",
                  'market_price': "Enter market price (in the format '987654321'):",
                  'net_debt': "Enter net debt (in the format '987654321'):",
                  'assets': "Enter assets (in the format '987654321'):",
                  'equity': "Enter equity (in the format '987654321'):",
                  'cash_equivalents': "Enter cash equivalents (in the format '987654321'):",
                  'liabilities': "Enter liabilities (in the format '987654321'):"}
    Companies = {'ticker': "Enter ticker (in the format 'MOON')",
                 'name': "Enter company (in the format 'Moon Corp'):",
                 'sector': "Enter industries (in the format 'Technology'):"}


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
        print('Welcome to the Investor Program!')
        while True:
            self.print_actual_menu(self.program_status)
            print('Enter an option:')
            ni = 'Not implemented!'
            io = 'Invalid option!'
            command = input()
            match self.program_status, command:
                case 'MAIN MENU', '0':
                    print('Have a nice day!')
                    # os.remove("investor.db")
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
                    database_engine.add_company()
                    self.program_status = 'MAIN MENU'
                    continue
                case 'CRUD MENU', '2':
                    database_engine.read_company_from_base()
                    self.program_status = 'MAIN MENU'
                    continue
                case 'CRUD MENU', '3':
                    database_engine.update_company_from_base()
                    self.program_status = 'MAIN MENU'
                    continue
                case 'CRUD MENU', '4':
                    database_engine.delete_company_from_base()
                    self.program_status = 'MAIN MENU'
                    continue
                case 'CRUD MENU', '5':
                    database_engine.print_sorted_list_of_all_companies()
                    self.program_status = 'MAIN MENU'
                    continue
                case 'CRUD MENU', _:
                    print(io)
                    continue
                case 'TOP TEN MENU', '0':
                    self.program_status = 'MAIN MENU'
                    continue
                case 'TOP TEN MENU', '1':
                    database_engine.print_top_ten_according_to_indicator(indicator='ND/EBITDA')
                    self.program_status = 'MAIN MENU'
                    continue
                case 'TOP TEN MENU', '2':
                    database_engine.print_top_ten_according_to_indicator(indicator='ROE')
                    self.program_status = 'MAIN MENU'
                    continue
                case 'TOP TEN MENU', '3':
                    database_engine.print_top_ten_according_to_indicator(indicator='ROA')
                    self.program_status = 'MAIN MENU'
                    continue
                case 'TOP TEN MENU', _:
                    print(io)
                    self.program_status = 'MAIN MENU'
                    continue



if __name__ == '__main__':
    database_engine = BaseLogic()
    main_logic = Main_Logic()
