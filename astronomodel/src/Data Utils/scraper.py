from bs4 import BeautifulSoup
import requests as r
import re
import pickle

# Logging Setup
import logging

logger = logging.getLogger('scraper')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('scraper.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('-----Scraper Started-----')

#
# URL Fetching TODO: page urls can be generated without the initial fetch: schema: ap{year}{month}{day}.html
#
ARCHIVE_URL = "https://apod.nasa.gov/apod/archivepixFull.html"
BASE_URL = "https://apod.nasa.gov/apod/"
archive_html = r.get(ARCHIVE_URL).text

soup = BeautifulSoup(archive_html, "html.parser")
links = soup.find_all('a', href=re.compile("ap\d{6}\.html"))  # regex match for apod links
urls = []

for link in links:
    url = urls.append(link.get('href'))

del links

logger.info("Found " + str(len(urls)) + " URLs")

#
# annotated_texts = {} # -  only needed not in recovery mode

# Midstop recovery:
with open('annotations.pkl', 'rb') as handle:
    annotated_texts = pickle.load(handle)


def parse_info_text(text):
    text = repr(s)
    text = text.split("Explanation:")[1]
    text = text.split("\\n\\n\\n \\n ")[0]  # At this point we should have the full description with \n's
    if "Tomorrow's picture:" in text:
        text = text.split("Tomorrow's picture:")[0]
    if "NASA Coverage:" in text:
        text = text.split("NASA Coverage:")[0]
    if "Imagery" in text:
        text = text.split("Imagery")[0]

    text = str(text.replace("\\n", " "))
    text = text.replace("\\", "")
    text = text.strip()
    text = ' '.join(text.split())

    return text


for i in range(10357, len(urls)):
    try:
        url = urls[i]
        ID = url[2:8]

        if ID in annotated_texts.keys():
            logger.info(f"Already collected data for given URL, skipping: {ID}")
            continue

        page_url = BASE_URL + url
        response = r.get(page_url)

        print(ID)
        if response.status_code != 200:
            logger.error("Status code " + str(response.status_code) + f"for url: {page_url}" + f"at {i + 1}")
            continue

        page_html = response.text

        soup = BeautifulSoup(page_html, "html.parser")

        s = soup.body.get_text()

        text_annotation = parse_info_text(s)

        try:
            link = soup.find_all('a', href=re.compile("image\/.*"))[0]
        except Exception as e:
            logger.error(f"Likely a video at ID: {ID}, skipping")
            continue

        image_url = link.get("href")  # TODO 1-line this stuff
        image_type = image_url.split(".")[1]
        if "jpg" == image_type:
            pass
        elif "png" == image_type:
            pass
        elif "gif" == image_type:
            pass
        else:
            logger.error(f"Not a valid jpg/png/gif for: {ID}")
            continue

        response = r.get(BASE_URL + image_url)
        if response.status_code == 200:
            with open(f"Images/{ID}.{image_type}", 'wb') as f:
                f.write(response.content)
                logger.info(f"Image saved: {ID}")
            annotated_texts[ID] = text_annotation
        else:
            logger.error(f"Failed for {ID}, skipping")

        logger.info(f"Saved {i + 1} of {len(urls)}")

        if i % 40 == 0:
            with open("annotations.pkl", 'wb') as f:
                pickle.dump(annotated_texts, f)
            logger.info(f"Updated pkl dict file on image # {i + 1}")
    except Exception as e:
        logger.error(f"Uknown error at index: {i + 1}, ID:{ID}, Error: {str(e)}")

with open("annotations.pkl", 'wb') as f:
    pickle.dump(annotated_texts, f)

logger.info(f"Finished writing data set at {i}")
logger.info(f"------ Scraper finished, exiting. ------")