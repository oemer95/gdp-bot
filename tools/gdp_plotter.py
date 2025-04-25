import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
import re

class GDPPlotter:
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

    def plot(self, country, start_year = None, end_year = None):
        try:
            country = country.strip()
            if country not in self.df.index:
                return f"Country '{country}' not found in the dataset."
                
            # get the years
            years_cols = [int(col) for col in self.df.columns if str(col).isdigit()]
            
           # Filter years based on timeframe if provided
            if start_year:
                start_year = int(start_year)
                years_cols = [y for y in years_cols if y >= start_year]
            if end_year:
                end_year = int(end_year)
                years_cols = [y for y in years_cols if y <= end_year]
           
            years_str = [str(y) for y in years_cols]
            # get the GDP data
            country_data = self.df.loc[country][years_str]
            
            # remove NaN values
            valid_data = country_data.dropna()
            
            if len(valid_data) < 2:
                return f"Not enough data points to plot GDP for {country}."
                
            years = [int(y) for y in valid_data.index]
            values = valid_data.values

            plt.figure(figsize=(10, 4))
            plt.plot(years, values, marker='o')
            
            # Create title based on the date range
            time_period = f"({min(years)}-{max(years)})"
            plt.title(f"GDP of {country} {time_period}")
            
            plt.xlabel("Year")
            plt.ylabel("GDP (USD)")
            plt.grid(True)
            plt.xticks(rotation=45)
            
            # format y-axis with commas for thousands
            plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))

            output_path = f"{country}_gdp_plot_{min(years)}-{max(years)}.png"
            plt.savefig(output_path, format="png", bbox_inches='tight')
            plt.close()
            return f"Plot saved to {output_path}"

        except Exception as e:
            return f"Could not generate plot: {str(e)}"    

    def extract_gdp_data_from_messages(messages):
        extracted_data = {}  # Format: {"country": {"year": value}}
    
        # Analyze only assistant messages
        for message in messages:
            if message['role'] == 'assistant':
                content = message['content']
            
                # Extract GDP data patterns
                gdp_pattern = r"The GDP of ([A-Za-z\s]+) in (\d{4}) was \$([0-9,]+\.\d{2})"
                matches = re.findall(gdp_pattern, content)
            
                for country, year, value in matches:
                    country = country.strip()
                    year = int(year)
                    value = float(value.replace(',', ''))
                
                    if country not in extracted_data:
                        extracted_data[country] = {}
                
                    extracted_data[country][year] = value
            
                # Also look for forecast data
                forecast_pattern = r"(\d{4}): \$([0-9,]+\.\d{2})"
                forecast_matches = re.findall(forecast_pattern, content)
            
                # If we found forecast data, try to determine the country from context
                if forecast_matches:
                    country_pattern = r"GDP Forecast for ([A-Za-z\s]+) \(next"
                    country_match = re.search(country_pattern, content)
                    if country_match:
                        country = country_match.group(1).strip()
                        if country not in extracted_data:
                            extracted_data[country] = {}
                    
                        for year, value in forecast_matches:
                            extracted_data[country][int(year)] = float(value.replace(',', ''))
    
        return extracted_data

    def plot_from_messages(self, memory, country, start_year=None, end_year=None):
        try:
        # Get the conversation history from your agent
            messages = memory.load_memory_variables({})["history"]
        
        # Extract GDP data from messages
            all_data = self.extract_gdp_data_from_messages(messages)
        
            country = country.strip()
            if country not in all_data:
                return f"No previously mentioned GDP data found for {country}."
        
            country_data = all_data[country]
        
        # Convert to lists and sort by year
            years = sorted([y for y in country_data.keys() 
                      if (start_year is None or y >= start_year) 
                      and (end_year is None or y <= end_year)])
        
            if not years:
                return f"No data available for {country} in the specified time period."
            
            values = [country_data[y] for y in years]
        
            plt.figure(figsize=(10, 4))
            plt.plot(years, values, marker='o')
            plt.title(f"GDP of {country} based on conversation ({min(years)}-{max(years)})")
            plt.xlabel("Year")
            plt.ylabel("GDP (USD)")
            plt.grid(True)
            plt.xticks(rotation=45)
        
            # Format y-axis with commas for thousands
            plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
        
            output_path = f"{country}_conversation_gdp_{min(years)}-{max(years)}.png"
            plt.savefig(output_path, format="png", bbox_inches='tight')
            plt.close()
        
            return f"Plot of previously mentioned GDP data saved to {output_path}"
        
        except Exception as e:
            return f"Could not generate plot from conversation history: {str(e)}"