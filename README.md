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
Data from chillox haven't been scraped. As they only have a photo of the menu. And even though text can be extracted from that image, they don't follow the same order. Under the folder named DATA, you can find the image after applying OCR.