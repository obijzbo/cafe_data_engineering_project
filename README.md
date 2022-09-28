## Installation

Run install.sh from the folder named shell_files. This will install all the components that is essential to run this program
Also mongoDB should be installed in the local device. 

```bash
. shell_files/install.sh
```

```bash
wget https://downloads.mongodb.com/compass/mongodb-compass_1.33.1_amd64.deb ##for linux 20.04
```
```bash
sudo dpkg -i mongodb-compass_1.33.1_amd64.deb
```


## Usage

Run data_collector.py to scrape data.
Run db_upload.py to upload scraped data to the database. Run the command below to execute the API.
```bash
uvicorn app_fastApi:app --reload
```

## Discussion
Data from chillox haven't been scraped. As they only have a photo of the menu. And even though text can be extracted from that image, they don't follow the same order. Under the folder named DATA, you can find the image on which OCR was applied. In scenarios like this, if number of data is big enough, text can be extracted using a ml model in a meaningful way. Or can be extracted using bounding box.

When passing data through the API, there are three parameters - location, menu and price. 
For the sake of simplicity, it will only work if location matches with the branch name and menu matches with the values of "index". In this portion i was a bit confused on how to handle this to generalize the data. One idea was to group all food index in three categories, namely "MEAL", "DRINKS" and "APPETIZER". But wasn't too sure if that would be a good idea. Therefore it wasn't implemented.
