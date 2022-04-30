import streamlit as st
from myfunctions import myvideo
import datetime

st.set_page_config(layout='wide')
st.markdown("<h1 style='text-align:center'>YouTube Downloader</h1>", unsafe_allow_html=True)


url = st.text_input(label='', placeholder='Paste video or playlist URL')
#url = 'https://youtu.be/Kq5iPtAc_3I'
#url = 'https://youtube.com/playlist?list=PLbHrOSG7nVN1z4XoLX7_RC-WkgZHc3tnV'
# Checks if the url posted is a playlist
is_playlist = url[20:28] == 'playlist'




def display_video(title, thumbnail, lenght, stream_prop):
    """Displays detials about individual video"""

    video_container = st.container()
    # To keep things tidy
    with video_container:
        left_col, right_col = st.columns(2)

        # Image, title and video lenght
        left_col.image(thumbnail, width=500)
        right_col.write(f"<h5>{title}</h5>", unsafe_allow_html=True)
        right_col.write(f"<h5>{datetime.timedelta(seconds=lenght)}</h5>", unsafe_allow_html=True)
        
        # Create radio buttons with resolution and filesize
        download_options = []
        for p in stream_prop.values():
            res = p[0].strip("\"")
            size = round(p[1]/(1024*1024), 1)
            download_options.append(f"{res} {size}mb")

        video_res = '360p'
        def set_vid_res(option):
            video_res = option.split(' ')[0]

        for download_option in download_options:
            download_button = right_col.button(label=download_option, on_click=set_vid_res(download_option))
            
            
        
    
    # If the download button was clicked or not
    return download_button, video_res




def make_video(url):
    """Handles video creation, and download"""
    myvideo_obj = myvideo(url)

    # If an error occurs, display it and return
    if myvideo_obj.error_message != None:
        st.error(myvideo_obj.error_message)
        return
    else:
        # Get video details and display them
        video_details = myvideo_obj.get_video_details()
        download_button, video_res = display_video(video_details['title'], video_details['thumbnail'],
                                                    video_details['lenght'], video_details['stream_prop'])
        
        if download_button or download_all:
            myvideo_obj.download_video(video_res)
        


download_all = False

# Multiple videos
if is_playlist and url:
    st.progress(70)
    video_urls = myvideo.get_playlist_videos(url)

    if video_urls == None:
        st.error('No playlist was found')
    else:
        download_all = st.button(label=f'Download all {len(video_urls)} videos')
        # TODO Include total size and lenght
        for url in video_urls:
            make_video(url)

# Single video
elif url:
    st.progress(70)
    make_video(url)
