![Sentiment Analysis Logo](https://github.com/IbrahimJarrarD/SentAnalysis/blob/main/Sentiment%20Analysis.png?raw=true)


# Sentiment Analysis 

The aim of the project is to create a Sentiment Analysis tool in Python.
Using two data sources, first the tweets in English received from the twitter API and filtered based on search terms (name of the product) and second the scrapper the user reviews from twitter. 
Then it returns three or more sentiment categories: Negative, Neutral, Positive. this data is analyzed and visualized to show change of the sentiments over time and overall distribution of the sentiments.

## How To Use
To clone and install this application, you'll need Python and suitable IDE installed on your computer.
in addition to the following packages:
* From your command line:

* $ pip install requests
* $ pip install bs4
* $ pip install pandas
* $ pip install tweepy
- Alternatively, install directly from the GitHub repository: pip install git+https://github.com/tweepy/tweepy.git
* $ pip install langdetect
* $ pip install translate
* $ pip install matplotlib



## Download
In order to avoid a bot detection by Amazon, we recommend using Splash, Splash is a lightweight browser with an API designed spcifically for web scraping and rendering javascript and dynamic websites. We can quickly and easily send requests to the Splash instance and have it render the JS for us, and return the HTML to parse.
* To install Splash we first need to download docker desktop from here https://www.docker.com/products/docker-desktop
* Here are the instructions to install splash on docker https://splash.readthedocs.io/en/stable/
* When splash is installed please define the local host as 8050, or change the link in the get_soup function inside the amazonscrapper.py file.
![code](carbon.png)
To access the Twitter API, access must be requested from Twitter. You have to register for that with the given Link under the following #Credits.
Afterwards you can access the the data with your individual consumer_key, consumer_secret, access_token and access_token_secret. The information should be stored in a separate text file, which should be named "config.py" to be retrieved automatically by the code.
- [Download Power BI](https://www.microsoft.com/en-us/download/details.aspx?id=58494)

## Credits

This software uses the following open source packages:
** this should be changed later
- [Rapidapi For sentiment analysis](https://rapidapi.com/zyanyatech1/api/sentiment-analysis/)
- [Twitter API](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)
- [Marked - a markdown parser](https://github.com/chjj/marked)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Splash](https://splash.readthedocs.io/en/stable/)
- [SQLite ODBC driver](http://www.ch-werner.de/sqliteodbc)
- [MKL-Service package](http://github.com/IntelPython/mkl-service)


## Visulaization in Power BI

>You can do your visulization by using Power BI. In oreder to use SQlite3 as your source of Data you need to choose ODBC option as source. To see SQlite3 in drop down option you need to install SQLite ODBC driver(look here: http://www.ch-werner.de/sqliteodbc) on your local machine. 

>Secondly, You need to install MKL-Service package http://github.com/IntelPython/mkl-service to use Python script in power BI. Also you need to change path to avoid error. follow the step of this link https://www.programmersought.com/article/49216613936/.

>Lastly, there is no relative path fuctionality avilable to use your Power BI file in a different computer. So everytime it should be done manually. It is shortcome of Power BI https://community.powerbi.com/t5/Desktop/Relative-path-to-data-source/m-p/930339.
