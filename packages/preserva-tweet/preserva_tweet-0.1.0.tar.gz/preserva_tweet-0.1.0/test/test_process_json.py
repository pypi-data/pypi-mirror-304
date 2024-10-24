import json
import os.path
import xml
import pytest
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

from pyPreservica import *

from IngestTweets import *


def setup():
    pass


def tear_down():
    pass


@pytest.fixture
def setup_tweet_data():
    print("Setting up resources...")

    setup()

    yield "./test_data/tweets.js"

    print("Tearing down resources...")

    tear_down()


@pytest.fixture
def setup_account_data():
    print("Setting up resources...")

    setup()

    yield "./test_data/account.js"

    print("Tearing down resources...")

    tear_down()


@pytest.fixture
def setup_export_data():
    print("Setting up resources...")

    setup()

    yield "./test_data/twitter-2024-10-17"

    print("Tearing down resources...")

    tear_down()


def test_parse_folder(setup_export_data):
    path = setup_export_data
    assert os.path.exists(path)
    assert os.path.isdir(path)
    ingest_tweets(path)


def test_get_account_info(setup_account_data):
    path = setup_account_data
    assert os.path.exists(path)
    info = get_account_info(path)
    assert info.email == "drjamescarr@gmail.com"


def test_split_json_doc(setup_tweet_data):
    path = setup_data
    assert os.path.exists(path)

    upload = UploadAPI(username="carj_preview_sales_manager@preservica.com", password="E3K9djcwZ5",
                       server="preview.preservica.com")
    entity = EntityAPI(username="carj_preview_sales_manager@preservica.com", password="E3K9djcwZ5",
                       server="preview.preservica.com")

    folder = entity.folder("38466550-4007-4e8c-80a1-67590d5da47b")

    with open(path, "r", encoding="utf-8") as fp:
        json_data = fp.read()
        tweets: dict = json.loads(json_data)
        for tweet in tweets:
            id_str = tweet['tweet']['id_str']

            del tweet['tweet']['edit_info']

            retweeted = tweet['tweet']['retweeted']

            del tweet['tweet']['retweeted']

            tweet['tweet']['retweeted'] = retweeted

            tweet['tweet']['text'] = tweet['tweet']['full_text']

            tweet['tweet']['location'] = "location"

            tweet['tweet']['in_reply_to_screen_name'] = "in_reply_to_screen_name"

            tweet['tweet']['is_quote_status'] = False

            if 'user' not in tweet['tweet']:
                tweet['tweet']['user'] = {"name": "name", "screen_name": "screen_name", "location": "location"}

            s = json.dumps(tweet['tweet'])

            file_name = f"./test_data/{{{id_str}}}_[pyPreservica].json"

            with open(file_name, mode="wt", encoding="utf-8") as fpo:
                fpo.write(s)

            xml_object = xml.etree.ElementTree.Element('tweet', {"xmlns": "http://www.preservica.com/tweets/v1"})
            xml.etree.ElementTree.SubElement(xml_object, "id").text = id_str
            xml.etree.ElementTree.SubElement(xml_object, "full_text").text = tweet['tweet']['full_text']
            xml.etree.ElementTree.SubElement(xml_object, "created_at").text = tweet['tweet']['created_at']
            #xml.etree.ElementTree.SubElement(xml_object, "screen_name_sender").text = tweet['tweet']['screen_name']
            #for h in hashtags:
            #    xml.etree.ElementTree.SubElement(xml_object, "hashtag").text = str(h['text'])

            #xml.etree.ElementTree.SubElement(xml_object, "name").text = author
            #xml.etree.ElementTree.SubElement(xml_object, "retweet").text = str(full_tweet._json['retweet_count'])
            #xml.etree.ElementTree.SubElement(xml_object, "likes").text = str(full_tweet._json['favorite_count'])

            xml_request = xml.etree.ElementTree.tostring(xml_object, encoding='utf-8')

            metadata_document = open("metadata.xml", "wt", encoding="utf-8")
            metadata_document.write(xml_request.decode("utf-8"))
            metadata_document.close()

            asset_metadata = {"http://www.preservica.com/tweets/v1": "metadata.xml"}

            security_tag = "open"
            asset_title = tweet['tweet']['full_text']
            asset_description = id_str

            identifiers = {"tweet_id": id_str}

            p = complex_asset_package(preservation_files_list=[file_name], parent_folder=folder,
                                      Title=asset_description,
                                      Description=asset_title, CustomType="Tweet", Identifiers=identifiers,
                                      Asset_Metadata=asset_metadata, SecurityTag=security_tag)
            upload.upload_zip_package(p, folder=folder, callback=UploadProgressConsoleCallback(p))

            print(s)
