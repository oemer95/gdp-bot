from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

class GDPForecaster:
     def __init__(self, data_path="data/gdp_data.csv"):
        self.df = pd.read_csv(
            data_path,
            quotechar='"',
            skipinitialspace=True,
            na_values=["", "n/a", ".."]
        )

        # Strip column names and convert years to string
        self.df.columns = self.df.columns.str.strip()
        self.df = self.df.set_index('Year')
        self.df.columns = self.df.columns.str.strip()

        # Transpose: countries become index, years become columns
        self.df = self.df.transpose()
        self.df.index = self.df.index.str.strip()
        self.df.columns = self.df.columns.astype(str)

        # Convert GDP values to numeric, forcing errors to NaN
        self.df = self.df.apply(pd.to_numeric, errors='coerce')

     def forecast(self, country, n_years=5):
        try:
            country = country.strip()
            if isinstance(n_years, str):
                try:
                    n_years = int(n_years.strip())
                except ValueError:
                    n_years = 5
            
            if country not in self.df.index:
                return f"Country '{country}' not found in the dataset."
                
            # get the years
            years_cols = [col for col in self.df.columns if str(col).isdigit()]
            
            # get the GDP
            country_data = self.df.loc[country][years_cols]
            
            #remove NaN values
            valid_data = country_data.dropna()
            
            if len(valid_data) < 2:
                return f"Not enough data points to forecast GDP for {country}."
                
            years = np.array([int(y) for y in valid_data.index]).reshape(-1, 1)
            values = valid_data.values.reshape(-1, 1)

            model = LinearRegression()
            model.fit(years, values)

            # forecast
            last_year = years[-1][0]
            future_years = np.arange(last_year + 1, last_year + n_years + 1).reshape(-1, 1)
            forecast = model.predict(future_years).flatten()

            result = f"GDP Forecast for {country} (next {n_years} years):\n"
            result += "\n".join([f"{int(y)}: ${float(v):,.2f}" for y, v in zip(future_years.flatten(), forecast)])
            return result
            
        except Exception as e:
            return f"Forecasting failed: {str(e)}"