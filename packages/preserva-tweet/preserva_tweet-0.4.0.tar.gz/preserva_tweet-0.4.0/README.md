# preserva-tweet

## Ingest Tweets from a Twitter Export into Preservica

This library provides a Python module which will ingest a Twitter export
zip file into Preservica as individual tweets with any attached media files such as images or video.
The tweets can then be rendered directly from within Preservica.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/carj/preserva-tweet

## Support 

preserva-tweet is 3rd party open source client and is not affiliated or supported by Preservica Ltd.
There is no support for use of the library by Preservica Ltd.
Bug reports can be raised directly on GitHub.

Users of preserva-tweet should make sure they are licensed to use the Preservica REST APIs. 

## License

The package is available as open source under the terms of the Apache License 2.0

## Installation

preserva-tweet is available from the Python Package Index (PyPI)

https://pypi.org/project/preserva-tweet/

To install preserva-tweet, simply run this simple command in your terminal of choice:

    $ pip install preserva-tweet

## Downloading your Twitter Archive

### Step 1

 Log in to your X account and open the Settings and Privacy panel. 
 Go to the “Your Account” tab and select “Download an Archive of Your Data.

### Step 2

For security purposes, you’ll need to re-enter your password. You’ll also need to provide a verification code.

### Step 3

Once you’ve successfully completed these steps, you’ll see an option to request your archive. 
Click the “Request Archive” button to begin processing.

### Step 4

The button will change to “Requesting Archive” and you’ll see a notice that your request is pending. 
Now it’s time to wait. It can take 24hrs for the export to be ready.

### Step 5

When your archive is ready to download, you’ll get both an email in your inbox and a notification in your X account. 
Since Twitter archives are only available for a limited time, pay attention to the expiration date.

## Ingesting Tweets

To run the module specify the location of the twitter export using the -a or --archive flag.
The parent Preservica collection for the tweets must be specified using the -c --collection flag as a UUID

preserva-tweet uses the pyPreservica python library for ingesting content. This means that preserva-tweet can use the
same authentication methods as pyPreservica for reading Preservica credentials. See: 
https://pypreservica.readthedocs.io/en/latest/intro.html#authentication


    $ python -m preserva-tweet -a twitter-2024-10-17.zip -c a7ad52e3-2cb3-4cb5-af2a-3ab08829a2a8

```
usage: preserva-tweet [-h] -a ARCHIVE -c COLLECTION [-v] [-d] [-u USERNAME] [-p PASSWORD] [-s SERVER] [-t SECURITY_TAG] [--validate]

Ingest a Twitter Account History Export into Preservica

options:
  -h, --help            show this help message and exit
  -a ARCHIVE, --archive ARCHIVE
                        Twitter export ZIP archive path
  -c COLLECTION, --collection COLLECTION
                        The Preservica parent collection uuid
  -v, --verbose         Print information as tweets are ingested
  -d, --dry-run         process the twitter export without ingesting
  -u USERNAME, --username USERNAME
                        Your Preservica username if not using credentials.properties
  -p PASSWORD, --password PASSWORD
                        Your Preservica password if not using credentials.properties
  -s SERVER, --server SERVER
                        Your Preservica server domain name if not using credentials.properties
  -t SECURITY_TAG, --security-tag SECURITY_TAG
                        The Preservica security tag of the ingested tweets (default is "open")
  --validate            Validate the twitter ingest to check for missing tweets


```



## Notes

The preserva-tweet program does need an internet connection to run. Most of the images and video's are fetched from 
the ZIP archive, but some assets such as thumbnails for the videos are fetched directly from the twitter servers.

For large Twitter accounts the export will come as multiple ZIP files. Just run the program once for each ZIP file.
preserva-tweet will not ingest the same tweet twice if the script is re-run against the same ZIP file. 
This also means you can always do an new export 
in the future and re-run the program to add in any new tweets.

For Preservica NewGen interface customers preserva-tweet will create a custom metadata group to store tweet metadata. 

## Validate Mode

preserva-tweet has a validation mode which is enabled using the --validate flag.
This will check that each tweet within the ZIP archive has been ingested into Preservica. This mode can be run after
the main ingest and will provide details of any tweets which were not ingested successfully.

    $ python -m preserva-tweet -a twitter-2024-10-17.zip -c a7ad52e3-2cb3-4cb5-af2a-3ab08829a2a8 --validate


