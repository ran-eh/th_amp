# Weather service

# Choices
## Approach
I am a fan of using the agile/YAGNI in data design.  I prefer to start small and simple, trusting that additional needs will reveal themselves over time.  In this project as well, I went for simple and light weight whenever possible.
## Database
Postgres is a good non-cloud starter system for any application.  This decision may be reconsidered later should the size of the data increase
and analytics needs become more complex.  At that point analyics data may
be split off into a columnar database, while Postgres will continue to
be used as the application database.

## Data ingestion and modeling
The requirements comfortably match the limitations of the API service' free tier.  I chose to use the realtime and timeline endpoints, and store the results in a schema that closely matches their output.  This allowed me to simply use `pandas.DataFrame.to_sql`, and not worry about schema maintenance for now, as to_sql both created and populates the table as needed.

As a starting point, I decided to overwrite data table on every ingestion.  However, extensing it to store historical data is easy should the need arise down the line.

## Orchestration
Again, to keep things simple, I use basic python constructs (`while True`/`time.Sleep`).  Bigger guns (e.g. Airflow) may be added later.

## Scraper app
Nothing much to see here, just api calls and `pandas.DataFrame.to_sql` for writing to the database.

# Running instructions
Clone the repo
```
git clone https://github.com/ran-eh/th_amp.git
cd th_amp
```
With the docker daemon running, start the containers
```
docker compose up -d
```
Open the notebook
```
http://127.0.0.1:8888/lab/tree/dash.ipynb
```

# Developmemt environment
I used vscode, and config files for it are included in the repo.  

## Debugging te Python app
To make postgres available locally, add the following line to /etc/hosts
```
sudo echo 127.0.0.1 db >> /etc/hosts
```

Create a virtual python environment and install the dependencies
```
pyenv install 3.12 # if needed
pyenv virtualenv 3.12 weather
pyenv activate weather
pip install -r weather/requirements
```

In vscode, open the repo directory.  Open weather/main.py, and select the above pyenv for the python environment.
Use the `Python Debugger: main.py` launch item to run the code in the debugger.