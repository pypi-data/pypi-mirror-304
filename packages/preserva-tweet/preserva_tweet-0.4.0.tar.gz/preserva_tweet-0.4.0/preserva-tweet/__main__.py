"""
preserva-tweet  module definition

A python module for ingesting twitter data exports in Preservica

author:     James Carr
licence:    Apache License 2.0

"""

import argparse
import pathlib
import tempfile
import xml
import zipfile
from typing import Generator
from urllib.parse import urlparse
from xml.etree import ElementTree
import shutil
from dateutil import *
from dateutil.parser import *
from pyPreservica import *

TWEET_LABEL = "window.YTD.tweets.part0"
ACCOUNT_LABEL = "window.YTD.account.part0"
PROFILE_LABEL = "window.YTD.profile.part0"
MANIFEST_LABEL = "window.__THAR_CONFIG"

TWEET_ID = "tweet_id"

ASSET_FOLDER = "assets"
DATA_FOLDER = "data"
TWEETS_MEDIA = "tweets_media"
PROFILE_MEDIA = "profile_media"

TWEETS_FOLDER = "Tweets"
REPLIES_FOLDER = "Replies"
RETWEETS_FOLDER = "Retweets"

TWITTER_SCHEMA_NS = "http://www.preservica.com/metadata/group/twitter"


def group_metadata(metadata: MetadataGroupsAPI):
    # does Twitter metadata
    twitter_group_exists = False
    for group in metadata.groups():
        if group.schemaUri == TWITTER_SCHEMA_NS:
            twitter_group_exists = True
            break

    if not twitter_group_exists:
        fields = []
        fields.append(GroupField(field_id="tweet_id", name="tweet_id", field_type=GroupFieldType.STRING, visible=True,
                                 indexed=True, editable=True, minOccurs=1, maxOccurs=1))
        fields.append(GroupField(field_id="full_text", name="Full Text", field_type=GroupFieldType.STRING, visible=True,
                                 indexed=True, editable=True, minOccurs=1, maxOccurs=1))
        fields.append(GroupField(field_id="created_at", name="Created At", field_type=GroupFieldType.DATE, visible=True,
                                 indexed=True, editable=True, minOccurs=1, maxOccurs=1))
        fields.append(
            GroupField(field_id="screen_name_sender", name="User Name", field_type=GroupFieldType.STRING, visible=True,
                       indexed=True, editable=True))

        fields.append(
            GroupField(field_id="hashtag", name="Hash Tag", field_type=GroupFieldType.STRING, visible=True,
                       indexed=True, editable=True, minOccurs=0, maxOccurs=-1))

        fields.append(
            GroupField(field_id="screen_name_mention", name="Mentioned", field_type=GroupFieldType.STRING, visible=True,
                       indexed=True, editable=True, minOccurs=0, maxOccurs=-1))

        fields.append(
            GroupField(field_id="in_reply_to_screen_name", name="In Reply To Tweet User",
                       field_type=GroupFieldType.STRING, visible=True,
                       indexed=True, editable=True, minOccurs=0, maxOccurs=1))
        fields.append(
            GroupField(field_id="in_reply_to_user_id_str", name="In Reply To Tweet ID",
                       field_type=GroupFieldType.STRING, visible=True,
                       indexed=True, editable=True, minOccurs=0, maxOccurs=1))

        fields.append(
            GroupField(field_id="retweet", name="Retweets",
                       field_type=GroupFieldType.NUMBER, visible=True,
                       indexed=True, editable=True, minOccurs=0, maxOccurs=1))

        fields.append(
            GroupField(field_id="likes", name="Likes",
                       field_type=GroupFieldType.NUMBER, visible=True,
                       indexed=True, editable=True, minOccurs=0, maxOccurs=1))

        fields.append(
            GroupField(field_id="expanded_url", name="URLS",
                       field_type=GroupFieldType.STRING, visible=True,
                       indexed=True, editable=True, minOccurs=0, maxOccurs=-1))

        metadata.add_group(group_name="Twitter", group_description="Tweet Metadata", fields=fields)


def main():
    """
    Entry point for the module when run as python -m preserva-tweet

    Sets up the command line arguments and starts either the ingest or validation

    :return: 0
    """
    parser = argparse.ArgumentParser(
        prog='preserva-tweet',
        description='Ingest a Twitter Account History Export into Preservica',
        epilog='')

    parser.add_argument("-a", "--archive", type=pathlib.Path, help="Twitter export ZIP archive path", required=True)
    parser.add_argument("-c", "--collection", type=str, help="The Preservica parent collection uuid", required=True)

    parser.add_argument("-v", "--verbose", action='store_const', help="Print information as tweets are ingested",
                        required=False, default=False, const=True)
    parser.add_argument("-d", "--dry-run", help="process the twitter export without ingesting",
                        default=False, action='store_const', const=True)

    parser.add_argument("-u", "--username", type=str,
                        help="Your Preservica username if not using credentials.properties", required=False)
    parser.add_argument("-p", "--password", type=str,
                        help="Your Preservica password if not using credentials.properties", required=False)
    parser.add_argument("-s", "--server", type=str,
                        help="Your Preservica server domain name if not using credentials.properties", required=False)

    parser.add_argument("-t", "--security-tag", type=str, default="open",
                        help="The Preservica security tag of the ingested tweets (default is \"open\")", required=False)

    parser.add_argument("--validate", help="Validate the twitter ingest to check for missing tweets",
                        default=False, action='store_const', const=True)

    args = parser.parse_args()
    cmd_line = vars(args)
    archive_path = cmd_line['archive']

    dry_run = False
    if 'dry_run' in cmd_line:
        dry_run = bool(cmd_line['dry_run'])

    validate_ingest = False
    if 'validate' in cmd_line:
        validate_ingest = bool(cmd_line['validate'])

    verbose = False
    if 'verbose' in cmd_line:
        verbose = bool(cmd_line['verbose'])

    collection = cmd_line['collection']

    security_tag = "open"
    if 'security_tag' in cmd_line:
        security_tag = str(cmd_line['security_tag'])

    username = cmd_line['username']
    password = cmd_line['password']
    server = cmd_line['server']

    if (username is not None) and (password is not None) and (server is not None):
        if verbose:
            print(f"Using credentials from command line")
        entity: EntityAPI = EntityAPI(username=username, password=password, server=server)
        upload: UploadAPI = UploadAPI(username=username, password=password, server=server)
        groups: MetadataGroupsAPI = MetadataGroupsAPI(username=username, password=password, server=server)
    else:
        if verbose:
            print(f"Using credentials from credentials.properties file")
        entity: EntityAPI = EntityAPI()
        upload: UploadAPI = UploadAPI()
        groups: MetadataGroupsAPI = MetadataGroupsAPI()

    group_metadata(groups)

    # Check the preservica folder uuid provided on the command line is valid
    try:
        parent_folder = entity.folder(collection)
        if verbose:
            print(f"Ingesting Twitter Archive into {parent_folder.title}")
    except ReferenceNotFoundException:
        print(f"The collection uuid has not be found")
        return 1

    if verbose:
        print(entity)

    if os.path.exists(archive_path) and os.path.isfile(archive_path) and (str(archive_path).lower().endswith(".zip")):
        if verbose:
            print(f"Processing tweet export: {archive_path}")

        # unzip the archive into a temp directory which is cleaned up at the end
        with tempfile.TemporaryDirectory() as tmp_dir:
            if verbose:
                print(f"Extracting tweets into {tmp_dir}")
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(tmp_dir)

            if validate_ingest:
                print(f"Running validation mode only, tweets will not be ingested")
                validate(zip_folder=tmp_dir, entity=entity, verbose=verbose)
            else:
                if verbose:
                    if dry_run:
                        print(f"Running Ingest in dry-run mode, tweets will not be ingested")
                    else:
                        print(f"Running Ingest in production mode, tweets will be ingested")

                ingest_tweets(tmp_dir, parent_folder, entity, upload, security_tag, dry_run, verbose)
    else:
        print(f"{archive_path} is not a valid path")

    return 0


class ProgressConsoleCallback:
    """
    callback class to show the progress
    """

    def __init__(self, total_tweets: int, prefix='Progress:', suffix='', length=100, fill='█', print_end="\r",
                 verbose: bool = True):
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.printEnd = print_end
        self._size: int = int(total_tweets)
        self._seen_so_far: int = 0
        self._lock = threading.Lock()
        self.verbose = bool(verbose)
        if self.verbose:
            self.print_progress_bar(0)

    def __call__(self, num_tweets: int):
        with self._lock:
            self._seen_so_far = num_tweets
            percentage = (float(self._seen_so_far) / float(self._size)) * float(100.0)
            if self.verbose:
                self.print_progress_bar(percentage)
            if int(self._seen_so_far) == int(self._size):
                if self.verbose:
                    self.print_progress_bar(100.0)
                    sys.stdout.write(self.printEnd)
                    sys.stdout.flush()

    def print_progress_bar(self, percentage):
        filled_length = int(self.length * (percentage / 100.0))
        bar_sym = self.fill * filled_length + '-' * (self.length - filled_length)
        sys.stdout.write(
            '\r%s |%s| (%.2f%%) %s ' % (self.prefix, bar_sym, percentage, self.suffix))
        sys.stdout.flush()


class ProfileInfo:
    def __init__(self, profile_dict: dict):
        self.bio = profile_dict['description']['bio']
        self.website = profile_dict['description']['website']
        self.location = profile_dict['description']['location']
        self.avatarMediaUrl = profile_dict['avatarMediaUrl']
        self.headerMediaUrl = profile_dict['headerMediaUrl']


class AccountInfo:
    def __init__(self, account_dict: dict):
        self.email = account_dict['email']
        self.createdVia = account_dict['createdVia']
        self.username = account_dict['username']
        self.accountId = account_dict['accountId']
        self.createdAt = account_dict['createdAt']
        self.accountDisplayName = account_dict['accountDisplayName']


def get_image(media: dict, zip_folder: str, has_video_element: bool, media_id_str: str, twitter_user: str,
              tweet_id: str):
    """
    Find the image file from the tweet, first looks up images in the media folder
    :param media:
    :param zip_folder:
    :param has_video_element:
    :param media_id_str:
    :param twitter_user:
    :param tweet_id:
    :return:
    """
    media_url_https = media["media_url_https"]
    if media_url_https:
        image_path = urlparse(media_url_https).path
        image_path = image_path[image_path.rfind("/") + 1:]
        image_name = f"{tweet_id}-{image_path}"
        image = os.path.join(os.path.join(os.path.join(zip_folder, DATA_FOLDER), TWEETS_MEDIA), image_name)

        if has_video_element:
            dest = f"{{{media_id_str}}}_[{twitter_user}]_thumb.jpg"
        else:
            dest = f"{{{media_id_str}}}_[{twitter_user}].jpg"
        if os.path.exists(image):
            shutil.copy(image, dest)
            if os.path.exists(dest) is True:
                return dest
        else:
            req = requests.get(media_url_https)
            if req.status_code == requests.codes.ok:
                if has_video_element:
                    image = f"{{{media_id_str}}}_[{twitter_user}]_thumb.jpg"
                else:
                    image = f"{{{media_id_str}}}_[{twitter_user}].jpg"
                image_name_document_ = open(image, "wb")
                image_name_document_.write(req.content)
                image_name_document_.close()
                return image


def get_video(media: dict, zip_folder: str, media_id_str: str, twitter_user: str, tweet_id: str):
    """
    Try and fetch a video from the zip archive, if its not available download it directly
    from the twitter server
    :param media:
    :param zip_folder:
    :param media_id_str:
    :param twitter_user:
    :param tweet_id:
    :return:
    """
    video_info = media["video_info"]
    variants = video_info["variants"]
    for v in variants:
        if v['content_type'] == 'video/mp4':
            video_url = v["url"]
            video_path = urlparse(video_url).path
            video_path = video_path[video_path.rfind("/") + 1:]
            video_name = f"{tweet_id}-{video_path}"
            video_name = os.path.join(os.path.join(os.path.join(zip_folder, DATA_FOLDER), TWEETS_MEDIA), video_name)
            dest = f"{{{media_id_str}}}_[{twitter_user}].mp4"
            if os.path.exists(video_name) is True:
                shutil.copy(video_name, dest)
                if os.path.exists(dest) is True:
                    return dest, True
            else:
                with requests.get(video_url, stream=True) as req:
                    video_name = f"{{{media_id_str}}}_[{twitter_user}].mp4"
                    with open(video_name, 'wb') as video_name_document_:
                        for chunk in req.iter_content(chunk_size=1024):
                            video_name_document_.write(chunk)
                            video_name_document_.flush()
                    return video_name, True


def add_media(tweet: dict, zip_folder: str, content_objects: list, twitter_user: str, tweet_id: str):
    if 'extended_entities' in tweet:
        extended_entities = tweet['extended_entities']
        if "media" in extended_entities:
            media = extended_entities["media"]
            for med in media:
                media_id_str = med["id_str"]
                has_video = False
                if "video_info" in med:
                    co, has_video = get_video(med, zip_folder, media_id_str, twitter_user, tweet_id)
                    content_objects.append(co)
                    if has_video:
                        co = get_image(med, zip_folder, has_video, media_id_str, twitter_user, tweet_id)
                        content_objects.append(co)
                    continue
                if "media_url_https" in med:
                    co = get_image(med, zip_folder, has_video, media_id_str, twitter_user, tweet_id)
                    content_objects.append(co)


def manifest(account_document: str, verbose: bool = False):
    with open(account_document, "r", encoding="utf-8") as fp:
        json_data = fp.read()
        updated_doc = json_data.replace(f"{MANIFEST_LABEL} =", "")
        manifest_info = json.loads(updated_doc)
        if verbose:
            print(f"Found Export for account name: {manifest_info['userInfo']['userName']} "
                  f" {manifest_info['userInfo']['accountId']}")
        json_files = manifest_info['dataTypes']['tweets']['files']

    return json_files


def get_profile_image(zip_folder, avatar_media_url: str, account_id: str):
    image_path = urlparse(avatar_media_url).path
    image_path = image_path[image_path.rfind("/") + 1:]
    image_name = f"{account_id}-{image_path}"
    image = os.path.join(os.path.join(os.path.join(zip_folder, DATA_FOLDER), PROFILE_MEDIA), image_name)
    if os.path.exists(image) is True:
        return image
    else:
        response = requests.get(avatar_media_url)
        if response.status_code == requests.codes.ok:
            with open("avatar_media_url.jpg", "wb") as image_name_document:
                image_name_document.write(response.content)
                image_name_document.flush()
            return image_name_document


def validate(zip_folder: str, entity: EntityAPI, verbose: bool):
    """
    Validate the ingest, check if each tweet has been ingested.
    :param zip_folder:
    :param entity:
    :param verbose:
    :return:
    """
    if os.path.isdir(zip_folder) is False:
        print("The tweet export directory is not a folder")
        return

    subfolders = [f.name for f in os.scandir(zip_folder) if f.is_dir()]
    assert len(subfolders) == 2
    assert 'data' in subfolders
    assert 'assets' in subfolders
    data_folder = os.path.join(zip_folder, 'data')
    assert os.path.isdir(data_folder)
    manifest_json = os.path.join(data_folder, 'manifest.js')
    json_files = manifest(manifest_json, verbose)

    total_tweets = 0
    for jf in json_files:
        total_tweets = int(jf['count'])

    not_ingested = []

    print(f"The Archive contains {total_tweets} tweets")
    for jf in json_files:

        tweet_json = os.path.join(zip_folder, jf['fileName'])

        for tweet in split_into_docs(tweet_json, jf['globalName']):
            tweet_id: str = tweet['tweet']['id_str']

            set_assets = entity.identifier(TWEET_ID, tweet_id)
            if len(set_assets) > 0:
                print(f"Tweet {tweet_id} has been ingested")
            else:
                print(f"Tweet {tweet_id} has not been ingested")
                not_ingested.append(tweet['tweet'])

    if len(not_ingested) == 0:
        print(f"All Tweets have beem ingested")
    else:
        print(f"The following tweets have not been ingested")
        for t in not_ingested:
            title = t['full_text']
            title = (title[:50] + '..') if len(title) > 50 else title
            print(f"{t['id_str']}: {title}")
        print("")
        print(f"** Rerun the script again to ingest the missing tweets **")


def ingest_tweets(zip_folder: str, parent_folder: Folder, entity: EntityAPI, upload: UploadAPI,
                  security_tag: str = "open", dry_run: bool = False, verbose: bool = False):
    if os.path.isdir(zip_folder) is False:
        print("The tweet export directory is not a folder")
        return
    subfolders = [f.name for f in os.scandir(zip_folder) if f.is_dir()]
    assert len(subfolders) == 2
    assert 'data' in subfolders
    assert 'assets' in subfolders
    data_folder = os.path.join(zip_folder, 'data')
    assert os.path.isdir(data_folder)
    account_json = os.path.join(data_folder, 'account.js')
    profile_json = os.path.join(data_folder, 'profile.js')
    manifest_json = os.path.join(data_folder, 'manifest.js')
    json_files = manifest(manifest_json, verbose)
    account_info: AccountInfo = get_account_info(account_json)
    profile_info: ProfileInfo = get_profile_info(profile_json)

    xml.etree.ElementTree.register_namespace("", TWITTER_SCHEMA_NS)

    account_folder = None
    if not dry_run:
        set_idents = entity.identifier("account ID", account_info.accountId)
        if len(set_idents) == 0:

            # create top level tweet folder using account info
            account_folder = entity.create_folder(title=account_info.username,
                                                  description=account_info.accountDisplayName,
                                                  security_tag=security_tag,
                                                  parent=parent_folder.reference)

            profile_image = get_profile_image(zip_folder, profile_info.avatarMediaUrl, account_info.accountId)

            entity.add_thumbnail(account_folder, profile_image)
            entity.add_identifier(account_folder, "account email", account_info.email)
            entity.add_identifier(account_folder, "account username", account_info.username)
            entity.add_identifier(account_folder, "account display name", account_info.accountDisplayName)
            entity.add_identifier(account_folder, "account ID", account_info.accountId)

        else:
            account_folder = set_idents.pop()

    total_tweets = 0
    for jf in json_files:
        total_tweets = int(jf['count'])

    callback = ProgressConsoleCallback(total_tweets, verbose=verbose)

    current_tweet: int = 0

    ingest_tweet_folder = None
    ingest_retweet_folder = None
    ingest_replies_folder = None

    if dry_run is False:
        set_idents = entity.identifier("TWEETS for Account", account_info.accountId)
        if len(set_idents) == 0:
            ingest_tweet_folder = entity.create_folder(title=TWEETS_FOLDER, description=TWEETS_FOLDER,
                                                       security_tag=security_tag,
                                                       parent=account_folder.reference)
            entity.add_identifier(ingest_tweet_folder, "TWEETS for Account", account_info.accountId)
        else:
            ingest_tweet_folder = set_idents.pop()

        set_idents = entity.identifier("Replies for Account", account_info.accountId)
        if len(set_idents) == 0:
            ingest_replies_folder = entity.create_folder(title=REPLIES_FOLDER, description=REPLIES_FOLDER,
                                                         security_tag=security_tag, parent=account_folder.reference)
            entity.add_identifier(ingest_replies_folder, "Replies for Account", account_info.accountId)
        else:
            ingest_replies_folder = set_idents.pop()

        set_idents = entity.identifier("Retweets for Account", account_info.accountId)
        if len(set_idents) == 0:
            ingest_retweet_folder = entity.create_folder(title=RETWEETS_FOLDER, description=RETWEETS_FOLDER,
                                                         security_tag=security_tag, parent=account_folder.reference)
            entity.add_identifier(ingest_retweet_folder, "Retweets for Account", account_info.accountId)
        else:
            ingest_retweet_folder = set_idents.pop()

    for jf in json_files:

        tweet_json = os.path.join(zip_folder, jf['fileName'])

        for tweet in split_into_docs(tweet_json, jf['globalName']):
            tweet_id: str = tweet['tweet']['id_str']

            current_tweet = current_tweet + 1

            set_assets = entity.identifier(TWEET_ID, tweet_id)
            if len(set_assets) > 0:
                callback(int(current_tweet))
                continue

            tweet['tweet']['user'] = {"name": account_info.accountDisplayName, "screen_name": account_info.username,
                                      "location": profile_info.location}
            tweet_str: str = json.dumps(tweet['tweet'])

            content_objects = list()

            file_name = f"./{{{tweet_id}}}_[{account_info.username}].json"

            with open(file_name, mode="wt", encoding="utf-8") as fpo:
                fpo.write(tweet_str)

            if os.path.isfile(file_name):
                content_objects.append(file_name)

            add_media(tweet['tweet'], zip_folder, content_objects, account_info.username, tweet_id)

            xml_object = xml.etree.ElementTree.Element('twitter', {"xmlns": TWITTER_SCHEMA_NS})
            xml.etree.ElementTree.SubElement(xml_object, "tweet_id").text = tweet['tweet']['id_str']
            xml.etree.ElementTree.SubElement(xml_object, "full_text").text = tweet['tweet']['full_text']

            created_date = tweet['tweet']['created_at']
            dt = parse(created_date)
            xml.etree.ElementTree.SubElement(xml_object, "created_at").text = dt.isoformat()

            xml.etree.ElementTree.SubElement(xml_object, "screen_name_sender").text = account_info.accountDisplayName

            if 'hashtags' in tweet['tweet']['entities']:
                hashtags = tweet['tweet']['entities']['hashtags']
                if hashtags is not None:
                    for h in hashtags:
                        xml.etree.ElementTree.SubElement(xml_object, "hashtag").text = str(h['text'])

            if 'user_mentions' in tweet['tweet']['entities']:
                user_mentions = tweet['tweet']['entities']['user_mentions']
                if user_mentions is not None:
                    for h in user_mentions:
                        xml.etree.ElementTree.SubElement(xml_object, "screen_name_mention").text = str(h['screen_name'])

            if 'in_reply_to_screen_name' in tweet['tweet']:
                in_reply_to_screen_name = tweet['tweet']['in_reply_to_screen_name']
                xml.etree.ElementTree.SubElement(xml_object, "in_reply_to_screen_name").text = in_reply_to_screen_name

            if 'in_reply_to_user_id_str' in tweet['tweet']:
                in_reply_to_user_id_str = tweet['tweet']['in_reply_to_user_id_str']
                xml.etree.ElementTree.SubElement(xml_object, "in_reply_to_user_id_str").text = in_reply_to_user_id_str

            xml.etree.ElementTree.SubElement(xml_object, "retweet").text = str(tweet['tweet']['retweet_count'])
            xml.etree.ElementTree.SubElement(xml_object, "likes").text = str(tweet['tweet']['favorite_count'])

            if 'urls' in tweet['tweet']['entities']:
                urls = tweet['tweet']['entities']['urls']
                if urls is not None:
                    for url in urls:
                        xml.etree.ElementTree.SubElement(xml_object, "expanded_url").text = str(url['expanded_url'])

            xml_request = xml.etree.ElementTree.tostring(xml_object, encoding='utf-8')

            metadata_document = open(f"{tweet_id}-metadata.xml", "wt", encoding="utf-8")
            metadata_document.write(xml_request.decode("utf-8"))
            metadata_document.close()

            asset_metadata = {TWITTER_SCHEMA_NS: f"{tweet_id}-metadata.xml"}

            asset_title = str(tweet['tweet']['full_text'])
            asset_description = str(tweet['tweet']['id_str'])

            identifiers = {TWEET_ID: tweet['tweet']['id_str']}

            if not dry_run:
                ingest_folder = ingest_tweet_folder

                if "in_reply_to_user_id_str" in tweet['tweet']:
                    ingest_folder = ingest_replies_folder

                if asset_title.startswith("RT "):
                    ingest_folder = ingest_retweet_folder

                p = complex_asset_package(preservation_files_list=content_objects, parent_folder=ingest_folder,
                                          Title=asset_title,
                                          Description=asset_description, CustomType="Tweet", Identifiers=identifiers,
                                          Asset_Metadata=asset_metadata, SecurityTag=security_tag)
                upload.upload_zip_package(p, folder=account_folder)

            callback(int(current_tweet))
            os.remove(f"{tweet_id}-metadata.xml")
            for obj in content_objects:
                os.remove(obj)
    if verbose:
        print(f"Processed {current_tweet} tweets")


def get_profile_info(account_document):
    with open(account_document, "r", encoding="utf-8") as fp:
        json_data = fp.read()
        updated_doc = json_data.replace(f"{PROFILE_LABEL} =", "")
        profile_info = json.loads(updated_doc)
        info: ProfileInfo = ProfileInfo(profile_info[0]['profile'])
        return info


def get_account_info(account_document):
    with open(account_document, "r", encoding="utf-8") as fp:
        json_data = fp.read()
        updated_doc = json_data.replace(f"{ACCOUNT_LABEL} =", "")
        account_info = json.loads(updated_doc)
        info: AccountInfo = AccountInfo(account_info[0]['account'])
        return info


def split_into_docs(tweets_document, label) -> Generator:
    with open(tweets_document, "r", encoding="utf-8") as fp:
        json_data = fp.read()
        updated_doc = json_data.replace(f"window.{label} =", "")
        tweets: dict = json.loads(updated_doc)
        for tweet in tweets:
            retweeted = tweet['tweet']['retweeted']
            del tweet['tweet']['retweeted']
            tweet['tweet']['retweeted'] = retweeted
            tweet['tweet']['is_quote_status'] = False
            tweet['tweet']['text'] = tweet['tweet']['full_text']
            yield tweet


if __name__ == "__main__":
    sys.exit(main())
