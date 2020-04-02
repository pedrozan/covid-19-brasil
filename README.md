# covid-19-brasil
An API for data on COVID-19 in Brazil. The data is updated based on information provided by Brazil's Health Ministry as soon as new numbers are available.

## Access to the API

The API is open and can be accessed on `https://covid-19-br.herokuapp.com/`. The available endpoints are well explained on the docs at `https://covid-19-br.herokuapp.com/docs` or `https://covid-19-br.herokuapp.com/redoc`.


## Running import

If you want to use this code to run your own API, use the following instructions to load the data to a MongoDB database from a local .csv file.

1 - Save the appropriate .csv files to the `data` folder
2 - Run the import script with:
```
python import_data.py {file_name_YYYYMMDD.csv} [-d|--date {YYYYMMDD}]
```
3 - Confirm when prompted
4 - All done!

