# project2-zaid-jamal
## Website URL: https://jamals-movie.fly.dev/

### Technologies Used
- WSL Ubuntu 
- Visual Studio Code 
- Git/GitHub 
### Frameworks Used
- Flask 
- fly.io  
### Libraries Used
- Flask Login 
- Flask SQLAlchemy
### APIs Used
- TMDB 
- WikiMedia 
### Languages Used
- Python 
- HTML/CSS 

### Setting Up
- Clone the repository onto your local machine 
- Ensure Python and pip have been installed 
- Run the following command in your terminal: ```python -m pip install -r requirements.txt ```
- Create a file called ".env" inside your cloned repository
- Go to the TMDB website and get an API key
- In the .env file, add the following line: ```TMDB_API_KEY = <your api key>```
- Go to https://fly.io/docs/hands-on/install-flyctl/ and use the appropriate command to install fly on your system
- Run ```flyctl launch``` and follow the steps. 
- When asked if you want to add a Postgres Database, type 'y' and save the credentials it gives you 
- The connection string you get should be in the following format: ```postgres://postgres:<Password>@<Hostname>:5432``` 
- Change the connection string to be  ```postgresql://postgres:<Password>@localhost:5432```
- In the .env file add the following line: ```DATABASE_URL = postgresql://postgres:<Password>@localhost:5432```
- Open another terminal window and run the following command: ```flyctl proxy 5432 -a <appname>``` where appname is simply the hostname fly gave you without the ".internal" at the end. (you can also find the appname by going to your fly.io dashboard)
- At the bottom of the movie.py file, add the following line: ```app.run()```
- In your terminal, run the following command: ```python3 movie.py```
- The terminal should print out a string of numbers which you can paste in your browser to view the website. 


