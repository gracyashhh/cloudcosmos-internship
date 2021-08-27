import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://boston.craigslist.org/search/npo"
job_dict = {}
job_num = 0
while True:
    response = requests.get(url)
    print(response)

    data = response.text

    soup = BeautifulSoup(data, 'html.parser')

    jobs = soup.find_all('div', {'class': 'result-info'})
    for job in jobs:
        title = job.find('a', {'class': 'result-title'}).text
        l = job.find('span', {'class': 'result-hood'})
        location = l.text[2:-1] if l else "N/A"
        date = job.find('time', {'class': 'result-date'}).text
        link = job.find('a', {'class': 'result-title'}).get('href')

        j_response = requests.get(link)
        j_data = j_response.text
        j_soup = BeautifulSoup(j_data, 'html.parser')
        j_description = j_soup.find('section', {'id': 'postingbody'}).text
        j_attr_tag = j_soup.find('p', {'class': 'attrgroup'})
        j_attr = j_attr_tag.text if j_attr_tag else "N/A"

        job_num += 1
        job_dict[job_num] = [title, location, date, link, j_attr, j_description]

        # print("Job Title:", title)
        # print("Location:", location)
        # print("Date:", date)
        # print("Link:", link)
        # print("Job description:\n", j_description)
        # print("Job attributes:", j_attr, "\n")

    url_tag = soup.find('a',{'title':'next page'})
    if url_tag.get('href'):
        url = 'https://boston.craigslist.org' + url_tag.get('href')
        print(url)
    else:
        break

print("Number of jobs:",job_num)
job_dict_df = pd.DataFrame.from_dict(job_dict, orient='index', columns=['Job Title','Location','Date','Link','Job attribute','Job description'])
print(job_dict_df.head())
job_dict_df.to_csv('job_list.csv')