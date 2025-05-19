import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.io as pio
pio.renderers.default = "browser"  # Set the default renderer to open in the browser
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

#use requests to get the HTML content of the page for GameStop
#url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
url = " https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

data = requests.get(url).text
soup = BeautifulSoup(data, 'html.parser')

# --- GameStop Revenue Extraction ---
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in soup.find_all("tbody")[0].find_all('tr'):
    col = row.find_all("td")
    if len(col) < 2:
        continue  # Skip rows that don't have both Date and Revenue
    date = col[0].text.strip()
    revenue = col[1].text.replace(',', '').replace('$', '').strip()
    gme_revenue = pd.concat([gme_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)

# Only print the cleaned DataFrame with Date and Revenue columns
print(gme_revenue[['Date', 'Revenue']].tail())

# --- Tesla Revenue Extraction ---
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in soup.find_all("tbody")[1].find_all('tr'):
    col = row.find_all("td")
    if len(col) < 2:
        continue  # Skip rows that don't have both Date and Revenue
    date = col[0].text.strip()
    revenue = col[1].text.replace(',', '').replace('$', '').strip()
    tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)

# Only print the cleaned DataFrame with Date and Revenue columns
print(tesla_revenue[['Date', 'Revenue']].tail())
print(tesla_revenue[['Date', 'Revenue']].head())

# Download Tesla stock data
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
print(tesla_data.head())

# Download GameStop stock data
gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
print(gme_data.head())

print(gme_revenue[['Date', 'Revenue']].tail())  # Show last 5 rows of GameStop revenue

#make graph function
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True)
    fig.show()  # This will open the graph in your default browser
    # Remove IPython display code for script use
    # from IPython.display import display, HTML
    # fig_html = fig.to_html()
    # display(HTML(fig_html))

#make graph for Tesla
make_graph(tesla_data, tesla_revenue, 'Tesla Stock Price and Revenue')
#make graph for GameStop
gme_title = 'GameStop Stock Price and Revenue'
make_graph(gme_data, gme_revenue, gme_title)