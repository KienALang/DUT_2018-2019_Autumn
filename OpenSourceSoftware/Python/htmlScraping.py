from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def getListPhoneLink():
	url = 'https://www.thegioididong.com/dtdd'
	links = []
	raw_html = simple_get(url)
	bsObject = BeautifulSoup(raw_html, 'html.parser')
	ulResultSet = bsObject.find_all('ul', class_='homeproduct')
	if len(ulResultSet) > 0:
		liResultSet = ulResultSet[0].find_all('li', class_='')
		for li in liResultSet:
			links.append(li.a.attrs['href'])

	return links


links = getListPhoneLink()
data = []
for link in links:
	# Get data: Name, Comment, Sentiment
	raw_html = simple_get('https://www.thegioididong.com'+link);
	bsObject = BeautifulSoup(raw_html, 'html.parser')
	title = bsObject.title.string.split('-')[0].strip()
	resultSet = bsObject.find_all('ul', class_="ratingLst")
	if len(resultSet) > 0 :
		ulTag = resultSet[0] # Get the first ul Tag
		liResultSet = ulTag.find_all('li', class_='par');
		for li in liResultSet:
			spanResultSet = li.find_all('span', class_='')
			iResultSet = li.find_all('i', class_='')
			iStartResultSet = li.find_all('i', class_='iconcom-txtstar')

			if (len(spanResultSet) > 1 & len(iResultSet) > 0):
				data.append((title, iResultSet[0].text, len(iStartResultSet)))


# open a csv file with w, so old data will be erased
with open('Phone.csv', 'w', encoding='utf-16le', newline='') as csv_file:
	 writer = csv.writer(csv_file)
	 # The for loop
	 for title, comment, star in data:
	 	writer.writerow([title, comment, star])
