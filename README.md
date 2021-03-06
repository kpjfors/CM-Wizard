# CM-Wizard
Tools for managing postings on CardMarket, and a local database of cards. Uses CardMarkets API, Flask, and a local SQLite database. \
\
Requires app tokens from CardMarket.\
\
To install:\
-Fill in your tokens in a file called ```auth.txt``` in root directory. For formatting see ```exampleauth.txt```\
-Run setup.sh (preferrably in a virtual environment). \
-You are done! \
\
To use:\
-```python3 cmwizard.py``` will start a local webserver. Go to ```localhost:5000``` to populate your database.\
-```python3 poster.py``` will post cards from your db to CardMarket if they trend higher than your specified price (default is 1.5€).\
-```python3 update.py``` updates the price for the cards already posted to CardMarket. \
-Alternatively you can run included shell script ```interval_run.sh``` to run poster and update at a specified interval (default = 4 hours). 
