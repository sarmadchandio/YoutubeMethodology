import json
import time

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class YoutubeExplorer:
    def __init__(self, videos):
        self.videos = videos

    # def check_video_stats(self):

    # Takes in a topic/categroy and returns mainstream videos of that topic from youtube.
    # Sort the search result by popularity and take first 10 links with the following filtration rules
    # Need to extract time, views, upload date
    def get_topic_videos(self, topic):
        topic = topic.lower()
        # Replace spaces with '+'
        topic = topic.replace(' ', '+')
        binary = FirefoxBinary('firefox/firefox-bin')
        options = webdriver.FirefoxOptions()
        browser = webdriver.Firefox(firefox_binary=binary, executable_path='./geckodriver', options=options)
        browser.implicitly_wait(0.5)
        try:
            browser.get("https://www.youtube.com/results?search_query={}".format(topic))
            expand_filters = browser.find_element(By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/div/ytd-toggle-button-renderer/a/tp-yt-paper-button')
            expand_filters.click()
            sort_by_rating = browser.find_element(By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[5]/ytd-search-filter-renderer[3]/a/div/yt-formatted-string')
            # This will sort videows by views
            sort_by_rating.click()
            time.sleep(1)
            browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(5)
            # views = browser.find_elements(By.XPATH, '//*[@id="metadata-line"]/span[1]')
            vid_info = browser.find_elements(By.XPATH, '//*[@id="metadata-line"]')
            vid_href = browser.find_elements(By.XPATH, '//*[@id="video-title"]')

            print(len(vid_href))
            print(len(vid_info))
            # for entry in zip(vid_info, vid_href):
            #     print(entry[0].text)
            #     print(entry[1].get_attribute('href'))
                
            
        except Exception as e:
            print(e)
            browser.close()
        finally:
            browser.close()





def main():
    videos = [v.strip() for v in open('their-tube.json')]
    youtube = YoutubeExplorer(videos)
    youtube.get_topic_videos('flat earth')


if __name__ == '__main__':
    main()



