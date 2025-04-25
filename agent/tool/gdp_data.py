import pandas as pd

class GDPData:
    def __init__(self, data_path="data/gdp_data.csv"):
        self.df = pd.read_csv(
            data_path,
            quotechar='"',
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

    def get_gdp(self, country, year):
        if country is None or year is None:
            return "Invalid query format. Please provide a country and year like 'Germany, 2010'."
        
        try:
            gdp_value = self.df.loc[country][str(year)]
            if pd.isna(gdp_value):
                return f"GDP data for {country} in {year} is not available."
            return f"The GDP of {country} in {year} was ${gdp_value:,.2f}."
        except KeyError:
            return f"Sorry, I couldn't find GDP data for {country} in {year}."
        except Exception as e:
            return f"Error retrieving GDP data: {str(e)}"

    def get_economic_opinion(self, gdp_value, country):
        if gdp_value > 2_000_000_000_000:
            return f"The GDP of {country} is very high, indicating a strong and developed economy."
        elif gdp_value > 500_000_000_000:
            return f"The GDP of {country} is moderate, suggesting a stable economy with potential."
        elif gdp_value > 100_000_000_000:
            return f"The GDP of {country} is low, indicating a developing economy or economic challenges."
        else:
            return f"The GDP of {country} is very low, suggesting a small or struggling economy."

    def economic_opinion_tool_func(self, input: str) -> str:
        import re

        country_match = re.search(r"[A-Za-z\s]+", input)
        if not country_match:
            return "Sorry, I couldn't understand the country name."

        country = country_match.group().strip()

        year_match = re.search(r"\d{4}", input)
        if year_match:
            year = int(year_match.group())
        else:
            # Default to latest year in dataset
            year = sorted([int(y) for y in self.df.columns if y.isdigit()])[-1]

        try:
            gdp = float(self.df.loc[country][str(year)])
        except:
            return f"No GDP data available for {country} in {year}."

        opinion = self.get_economic_opinion(gdp, country)
        return f"In {year}, {opinion}"

    def compare_gdp(self, countries, year):
        if countries is None or year is None:
            return "Invalid query format. Please provide countries and year like 'Germany, France, UK, 2010'."
        
        try:
            values = {}
            missing = []
            for country in countries:
                try:
                    value = self.df.loc[country][str(year)]
                    if not pd.isna(value):
                        values[country] = value
                    else:
                        missing.append(country)
                except KeyError:
                    missing.append(country)
            
            if not values:
                return f"Could not find GDP data for any of the specified countries in {year}."
                
            sorted_vals = sorted(values.items(), key=lambda x: x[1], reverse=True)
            result = "\n".join([f"{c}: ${v:,.2f}" for c, v in sorted_vals])
            
            if missing:
                result += f"\n\nNote: GDP data not available for: {', '.join(missing)}"
                
            return result
        except Exception as e:
            return f"Error comparing countries: {str(e)}"