import streamlit as st
from myfunctions import myvideo
import datetime

st.set_page_config(layout='wide')
st.markdown("<h1 style='text-align:center'>YouTube Downloader</h1>", unsafe_allow_html=True)


url = st.text_input(label='', placeholder='Paste video or playlist URL')
#url = 'https://youtu.be/Kq5iPtAc_3I'
#url = 'https://youtu.be/cwk417UfnTU'
#url = 'https://youtube.com/playlist?list=PLbHrOSG7nVN1z4XoLX7_RC-WkgZHc3tnV'
#url = 'https://youtube.com/playlist?list=PLVD3APpfd1tuZG0pek_JaPYRhGwpJj3Jd'
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

        # This complex logic is just to display the video lenght in a prettier format
        timedelta_obj = datetime.timedelta(seconds=lenght)
        time = str(timedelta_obj).split(sep=':')
        if int(time[-3]) > 0:
            right_col.write(f"<h5>{timedelta_obj}</h5>", unsafe_allow_html=True)
        else:
            right_col.write(f"<h5>{time[-2]}:{time[-1]}</h5>", unsafe_allow_html=True)

        
        # Create radio buttons with resolution and filesize
        download_options = []
        for p in stream_prop.values():
            res = p[0].strip("\"")
            size = round(p[1]/(1024*1024), 1)
            download_options.append(f"{res} {size}mb")

        # TODO current playlist default
        download_res = '360p'
        def set_vid_res(option):
            download_res = option.split(' ')[0]

        for download_option in download_options:
            download_button = right_col.button(label=download_option, on_click=set_vid_res(download_option))
            
            
        
    
    # If the download button was clicked or not
    return download_button, download_res




def make_video(url):
    """Handles video creation, and download"""

    #@st.cache(allow_output_mutation=True)
    def get_video_obj(url):
        return myvideo(url)
    myvideo_obj = get_video_obj(url)

    # If an error occurs, display it and return
    if myvideo_obj.error_message != None:
        st.error(myvideo_obj.error_message)
        return
    else:
        # Get video details and display them
        video_details = myvideo_obj.get_video_details()
        download_button, download_res = display_video(video_details['title'], video_details['thumbnail'],
                                                    video_details['lenght'], video_details['stream_prop'])


        return {'myvideo_obj': myvideo_obj,
                'download_button': download_button,
                'download_res': download_res}




# Multiple videos
if is_playlist and url:
    
    # Get individual video URLs
    with st.spinner('Extracting playlist'):

        @st.cache(allow_output_mutation=True, show_spinner=False)
        def get_playlist(url):
             return myvideo.get_playlist_videos(url)
        playlist = get_playlist(url)
        

    if playlist == None or playlist == []:
        st.error('No playlist was found')

    else:
        video_urls = playlist['urls']
        total_lenght = playlist.get('lenght', 0)

        # Display playlist information
        # TODO Include total size
        col1, col2 = st.columns(2)
        download_all = col2.button(label=f'Download all')
        with col1:
            # This complex logic is just to display the video lenght in a prettier format
            timedelta_obj = datetime.timedelta(seconds=total_lenght)
            time = str(timedelta_obj).split(sep=':')
            if int(time[-3]) > 0:
                st.write(f'{len(video_urls)} videos found {timedelta_obj} long')
            else:
                st.write(f'{len(video_urls)} videos found {time[-2]}:{time[-1]} long')


        
        with st.spinner('Fetching videos'):
            for url in video_urls:
                vids = make_video(url)
        # Download clicked videos
        for vid in vids:
            if vid['download_button']:
                vid['myvideo_obj'].download_video(vid['video_res'])
        # Download all videos
        if download_all:
            for vid in vids:
                vid['myvideo_obj'].download_video(vid['video_res'])


# Single video
elif url:
    with st.spinner('Fetching video'):
        vid = make_video(url)
    
    if vid['download_button']:
        vid['myvideo_obj'].download_video(vid['video_res'])
        

