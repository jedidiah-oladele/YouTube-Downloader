import sys
import os
import shutil
from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Paste the location of your chromedriver.exe file
s = Service('C:\\Users\\HP\\Projects\\Python Projects\\pythonProject\\LearningSpace\\Automation\\WebScrapping'
            '\\chromedriver.exe')
# Paste your preferred download path
download_path = 'C:\\Users\\HP\\Downloads'
folder_name = 'New YouTube playist'


def split_playlist(user_browser):
    """Returns a list containing all video urls from a playlist"""

    # CSS selector may change, if YouTube updates their site
    video_elements = user_browser.find_elements(By.CSS_SELECTOR,
                                                'div#contents ytd-item-section-renderer>div#contents a#video-title')

    return [element.get_attribute('href') for element in video_elements]


def download_video(video_url):
    """Downloads a video using pytube"""

    print('Downloading...')
    try:
        downloaded_file = YouTube(video_url).streams.get_highest_resolution().download()
        print(f'"{os.path.basename(downloaded_file)}" downloaded')
    except:
        print('An error occurred. Please recheck the link provided')
        sys.exit()

    return downloaded_file


# TODO Selenium and browsers are only required for playlist. Don't use them when a single video is selected
browser = webdriver.Chrome(service=s)
browser.minimize_window()

user_link = input('Enter your link: ')
# https://youtu.be/Yv3eTjMqmmU
# https://youtube.com/playlist?list=PLeo1K3hjS3uu_n_a__MI_KktGTLYopZ12
# 3,20
# https://youtube.com/playlist?list=PLrOFa8sDv6jcp8E3ayUFZ4iNI8uuPjXHe
# 31,

try:
    print('Fetching site...')
    browser.get(user_link)
    browser.implicitly_wait(2)
except:
    print('An error occurred. Please recheck link or your internet connection')
    sys.exit()

# If the provided link is a playlist
if user_link[20:28] == 'playlist':

    # Create a new folder to save playlist videos
    download_path = download_path + '\\' + folder_name
    if not os.path.exists(download_path):
        os.makedirs(download_path + '\\' + folder_name)

    video_links = split_playlist(browser)
    print(f'This playlist contains {len(video_links)} videos')

    # Get a list slice to know howe many videos to download
    while True:
        playlist_slice = input('Press enter to download all videos or enter a range (e.g 1,12):').split(',')

        if playlist_slice:
            try:
                video_links = video_links[(int(playlist_slice[0])-1): (int(playlist_slice[1]))]
                break
            except TypeError:
                print('Invalid input entered')
            except IndexError:
                print('Slice entered is too large')
        else:
            break

    # Downloads individual videos
    print(f'About to download {len(video_links)} videos')
    for i, video_link in enumerate(video_links):
        video_file = download_video(video_link)

        # TODO Renaming requires fix for when a slice is used
        # Move and rename video
        shutil.move(video_file, download_path + f'\\{i+1}_' + os.path.basename(video_file))

# If provided link is a single video
else:
    video_file = download_video(user_link)
    shutil.move(video_file, download_path + '\\' + os.path.basename(video_file))

browser.quit()
print('Task done.')
