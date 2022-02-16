import json
import time
import csv
import re

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class YoutubeExplorer:
    def __init__(self, videos, topics):
        self.videos = videos    # list of videos to filter
        self.topics = topics    # list of topics to get mainstream vids
    # def check_video_stats(self):

    # Takes in a list of topics/keywords and returns mainstream/popular videos of that keywords from youtube.
    # Sort the search result by popularity and take first 40 links with the following filtration rules
    def get_topic_videos(self):
                
        csv_rows = []
        for topic in self.topics:
            topic = topic.lower()
            # Replace spaces with '+'
            topic = topic.replace(' ', '+')
            binary = FirefoxBinary('firefox/firefox-bin')
            options = webdriver.FirefoxOptions()
            browser = webdriver.Firefox(firefox_binary=binary, executable_path='./geckodriver', options=options)
            browser.implicitly_wait(0.5)
            try:
                # Search the keyword
                browser.get("https://www.youtube.com/results?search_query={}".format(topic))
                # Click on filter_menu
                expand_filters = browser.find_element(By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/div/ytd-toggle-button-renderer/a/tp-yt-paper-button')
                expand_filters.click()

                # Sort videos by views
                sort_by_rating = browser.find_element(By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[5]/ytd-search-filter-renderer[3]/a/div/yt-formatted-string')
                sort_by_rating.click()
                time.sleep(3)
                
                # Scroll down to bottom to load more videos (this makes a total of 40 vids)
                # browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                # time.sleep(5)
                
                # Extract views and upload date
                # vid_info = browser.find_elements(By.XPATH, '//*[@id="metadata-line"]')
                # Extract the video url
                vid_href = browser.find_elements(By.XPATH, '//*[@id="video-title"]')
                # Extract vid title
                vid_info = browser.find_elements(By.XPATH, '//*[@id="video-title"]/yt-formatted-string')

                print(len(vid_href))
                print(len(vid_info))
                for entry in zip(vid_info,  vid_href):
                    title = entry[0].text
                    string = entry[0].get_attribute('aria-label')
                    url = entry[1].get_attribute('href')
                    upload_date = re.search(r'\d+ (years?|minutes?|seconds?|days?|weeks?|months?) ago', string).group(0)
                    remaining_string = string.split(upload_date)[1]
                    views = remaining_string.split('views')[0].split(' ')[-2]
                    duration = ' '.join(remaining_string.split('views')[0].split(' ')[1:-2])
                    
                    print('{} --- {} --- {} --- {} --- {}'.format(topic, title, upload_date, views, duration))
                    csv_rows.append([topic.replace('+',' '), title, views, upload_date, duration, url])
                    # print(string)
                    # print('---------------------')

                    # break
            except Exception as e:
                print(e)
                browser.close()
            finally:
                browser.close()
        
        # After collecting all the videos 
        with open('video_list1.csv', 'w') as csvfile:
            csv_fields = ['Keywords', 'Title', 'Views', 'Upload Date', 'Duration', 'URL']
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(csv_fields)
            csvwriter.writerows(csv_rows)

    





def main():
    videos = [v.strip() for v in open('their-tube.json')]
    # youtube = YoutubeExplorer(videos, ['Flat Earth Debunked', 'Abortion Rights', 'Women Rights', 'Climate Change'])
    youtube = YoutubeExplorer(videos, ['Abortion Rights', 'Women Rights'])
    youtube.get_topic_videos()


if __name__ == '__main__':
    main()



