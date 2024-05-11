# messenger-stats
> Online platform for displaying Messenger conversation statistics

## 🗯️ Disclaimer
For privacy reasons, this project is self-hosted only. Authors of this repository do not provide any official hosted version of this application.

## ❓ How to run?
1. Clone this repo  
   `git clone https://github.com/danrog303/messenger-stats.git && cd messenger-stats`
2. Create directory for storing files - it will be shared by backend and stats service.  
   `mkdir /home/daniel/MessengerFiles`
3. Set required environment variables
   ```
   export MESSENGER_STATS_UPLOAD_DIR=/home/daniel/MessengerFiles
   export MESSENGER_STATS_SERVICE_URL=http://localhost:2137
   ```
4. Run the services
   ```
   ./backend/gradlew run
   cd frontend/ && npm npm i && npm start
   cd ../stats-service && python3 -m pip install -r requirements.txt && python3 chatstat_api.py
   ```

## ❓ How to use?
Go to the frontend website (http://localhost:3000 by default). Here you will see a detailed instruction on website usage.

## 🏛️ Project structure
1. **backend service**
   - Written in Java/Spring WebFlux
   - Responsible for accepting zip files, storing them on the server and unzipping them
   - Calls Python microservice and streams calculated statistics to the user
2. **frontend service**
   - Written in TypeScript/ReactJS
   - Displays form for sending the stats file
   - Displays graphs based on statistics sent by the backend
3. **stats service**
   - Written in Python/Flask
   - Uses Pandas to read through messages and calculate the statistics
   - Sends calculated statistics to backend by using SSE streams
   - Code is partially based on simonwongwong/Facebook-Messenger-Statistics repo

## 🎓 Note
The application was created as an project assignment during the sixth semester of studies at Bydgoszcz University of Science and Technology.

## ⚙️ Possible improvements
- better error handling in WebFlux portion of the app
- utilize containers to run and configure the whole application using a single script
- some unit testing to ensure everything's working correctly

## 🖼️ Screenshots
![stats-1](https://github.com/danrog303/messenger-stats/assets/32397526/0337cf6d-669a-4838-b6f9-95b9354867d9)  
![stats-2](https://github.com/danrog303/messenger-stats/assets/32397526/07ac6dc1-d2cb-40b6-93a1-67e63a53bb72)  

