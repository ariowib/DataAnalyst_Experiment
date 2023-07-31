#TSLA VS GME#

#Line 1#
#Installing Addon that needed, in this case yfinance#
!pip install yfinance==0.1.67
!mamba install bs4==4.10.0 -y
!pip install nbformat==4.2.0

#Line 2#
#Install yfinance, pandas, request, BeautifulSoup, and plots#
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Line 3#
#Defining make_graph function#
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Line 4#
#Use Ticker function and history to extract stock information and set period to max#
tsla = yf.Ticker('TSLA')
tsla_history_data = tsla.history(Period ='max')
tsla_history_data

#Line 5#
tsla_history_data.reset_index(inplace=True)
tsla_history_data.tail(5)

#Line 6#
#Requesting the url#
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
html_data  = requests.get(url).text
print(html_data)

#Line 7#
#Parse the HTML with beautiful_soup#
soup = BeautifulSoup(html_data, 'html5lib')
tslasoup = soup.find_all("tbody")[1]

#Line 8#
#Extract the table and store it into dataframe#
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in tslasoup.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    Revenue = col[1].text
    
    tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":Revenue}, ignore_index=True)

tesla_revenue

#Line 9#
#remove the comma and dollar sign and null or empty strings from Revenue column#
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

#Now move to GME by using the same method#
#Line 10#
GameStop = yf.Ticker("GME")
gme_data = GameStop.history(period='max')
gme_data.reset_index(inplace=True)

#Line 11#
url1 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
html_data1 = requests.get(url1).text
soup1 = BeautifulSoup(html_data1,"html.parser")
gmesoup = soup1.find_all("tbody")[1]

#Line 12#
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in gmesoup.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    Revenue = col[1].text
    
    gme_revenue = tesla_revenue.append({"Date":date, "Revenue":Revenue}, ignore_index=True)

gme_revenue

#Line 13#
gme_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

gme_revenue.tail(5)

#Line 14#
#Plot Tesla Stock Graph#
make_graph(tsla_history_data, tesla_revenue, 'Tesla')

#Line 15#
#Plot GameStop Stock Graph#
make_graph(gme_data, gme_revenue, 'GameStop')


