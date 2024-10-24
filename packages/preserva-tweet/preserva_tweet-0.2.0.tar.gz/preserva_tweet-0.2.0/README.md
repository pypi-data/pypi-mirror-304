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

To install IngestTweets, simply run this simple command in your terminal of choice:

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

    $ python -m preserva-tweet -a twitter-2024-10-17.zip -c a7ad52e3-2cb3-4cb5-af2a-3ab08829a2a8

```
usage: preserva-tweet [-h] -a ARCHIVE -c COLLECTION [-v] [-d] [-u USERNAME] [-p PASSWORD] [-s SERVER] [-t SECURITY_TAG]

Ingest a Twitter Account History into Preservica

options:
  -h, --help            show this help message and exit
  -a ARCHIVE, --archive ARCHIVE
                        Twitter export ZIP archive path
  -c COLLECTION, --collection COLLECTION
                        The Preservica parent collection uuid
  -v, --verbose         Print information as tweets are ingested
  -d, --dry-run         Validate the twitter export without ingesting
  -u USERNAME, --username USERNAME
                        Your Preservica username if not using credentials.properties
  -p PASSWORD, --password PASSWORD
                        Your Preservica password f not using credentials.properties
  -s SERVER, --server SERVER
                        Your Preservica server domain name if not using credentials.properties
  -t SECURITY_TAG, --security-tag SECURITY_TAG
                        The Preservica security tag of the ingested tweets (default is "open")

```