# This package handles a lot of stuff that your operating system normally would (creating directories)
import os

try:
    # TimeSeries is the class which will allow us to pull stock information
    from alpha_vantage.timeseries import TimeSeries
    # This allows us to work with date objects
    from datetime import datetime
    # Allows us to wait
    from time import sleep
    # Pandas is used for dataframe manipulation
    import pandas as pd
except ImportError: # If packages don't exist, install them
    os.system('pip install alpha_vantage pandas datetime')
    from alpha_vantage.timeseries import TimeSeries
    from datetime import datetime
    from time import sleep
    import pandas as pd

class FX():
    def __init__(self):
        # Define API key (change this to yours)
        if os.path.exists('my_key'):
            with open('my_key') as f:
                key = f.read()
                self.my_key = key
        else:
            print('-'*50)
            self.my_key = input('What is your API key? ')
            print('-'*50)
            with open('my_key', 'w+') as f:
                f.write(self.my_key)


        # This creates a TimeSeries() object and authorizes your API key.
        # The TimeSeries() object is specific to their package so don't worry about exactly what it is
        self.ts = TimeSeries(key=self.my_key, output_format='pandas')

        # Create all of the directories for .csv (Excel) files to be saved
        if not os.path.exists('./data'):
            os.makedirs('./data')
        if not os.path.exists('./data/daily'):
            os.makedirs('./data/daily')
        if not os.path.exists('./data/monthly'):
            os.makedirs('./data/monthly')
        if not os.path.exists('./data/weekly'):
            os.makedirs('./data/weekly')
        if not os.path.exists('./data/intra'):
            os.makedirs('./data/intra')

    def get_intradata(self, ticker, interval='1min'):  # If no interval is supplied, use 1 minute
        # Call the .get_intraday() method with the ticker and interval
        data, meta_data = self.ts.get_intraday(symbol=ticker, interval=interval, outputsize='full')

        # Use the .to_csv() method from Pandas (If you don't know pandas yet you should look up some stuff on it)
        # Pandas is how you manipulate the excel files in python (adding new columns, booleans, etc.)
        data.to_csv(f'./data/intra/{ticker}_{datetime.today().date()}.csv')
        return data

    def monitor_stock(self, ticker):
        print(f'Beginning monitor of stock {ticker}')
        while True:  # Always continue looping
            try:  # The try/except cause it to continue retrying if it fails to get the data the first time
                data, meta_data = self.ts.get_intraday(symbol=ticker, interval='1min', outputsize='compact')
                data.reset_index(inplace=True)  # Reset the index (this is relatively unimportant)
                data = data.loc[data['date'] == max(data['date'])]  # Select the row of data where the date column is equal to its maximum

                #Fancy print the data... the end and flush parameters are used to overwrite whatever was last printed
                print(f"Now: {datetime.now().time()} | Time: {data['date'].iloc[0]} | Open: {data['1. open'].iloc[0]} | High: {data['2. high'].iloc[0]} | Low: {data['3. low'].iloc[0]} | Close: {data['4. close'].iloc[0]} | Volume: {data['5. volume'].iloc[0]}", end='\r', flush=True)
                sleep(5)  # Wait 5 seconds after returning data

            except KeyError:  # This catches the error that may arise when no data is returned
                pass  # This literally means "do nothing"
            except KeyboardInterrupt:  # This catches when you use Command+C to escape the monitor
                print('Exiting monitoring...')
                return  # Exit the monitor function

    def get_daily_data(self, ticker):
        # Call the get_daily() function on the ticker
        data, meta_data = self.ts.get_daily(ticker, outputsize='full')

        # Save the DataFrame
        data.to_csv(f'./data/daily/{ticker}_daily_data.csv')
        return data

    def get_weekly_data(self, ticker):  # Exact same as get_daily_data()
        data, meta_data = self.ts.get_weekly(ticker)
        data.to_csv(f'./data/weekly/{ticker}_weekly_data.csv')
        return data

    def get_monthly_data(self, ticker):  # Exact same as get_daily_data()
        data, meta_data = self.ts.get_monthly(ticker)
        data.to_csv(f'./data/monthly/{ticker}_monthly_data.csv')
        return data

    def command_loop(self, response):
        def pull_data():
            # Initialize variables that we will need
            r = ''
            tickers = []

            # This loop will collect a list of tickers to collect data of. The word 'done' causes it to end.
            while r != 'done':
                r = input('Enter a ticker or "done": ')
                if r != 'done':
                    # Append the user input to tickers if it's not done
                    tickers.append(r)

            # This is more advanced (I just learned you could do this) but its a list of functions so we can call them all
            fucntions = [self.get_intradata, self.get_daily_data, self.get_monthly_data, self.get_weekly_data]

            for t in tickers:  # Cycle through the tickers and get data for all of them
                for f in fucntions:  # Cycle through the different functions
                    s = False  # This boolean will become true only when a function was successful
                    while not s:  # While the data has not been saved, try to save it
                        try:
                            f(t)  # Try to perform the function
                            s = True  # This will only happen if the function was successful
                        except:
                            pass  # Keep trying...

        def monitor():
            # Get a stock to watch
            tick = input("Enter a ticker to monitor: ")
            self.monitor_stock(tick)

        d = {'pull': pull_data, 'monitor': monitor}
        d[response]()  # If response = 'pull' it will run pull_data, as shown above... Same for 'monitor'

    @staticmethod
    def UI():  # This isn't important but it basically just says "run this"
        fx = FX()
        while True:  # Always continue running

            # Print 2 rows of lines to separate previous printed stuff
            print('-'*50)
            print('-'*50)

            # Fancy-ish (not really) UI stuff
            print('Enter one of the following:')
            print('\t"pull" to pull stock data to Excel')
            print('\t"monitor" to monitor a stock real-time')
            print('-'*50)

            # Get the users desired task and send it to the command loop which will call the right function
            r = input('X: ')
            fx.command_loop(r)
