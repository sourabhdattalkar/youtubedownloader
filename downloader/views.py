from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import YouTubeDownloadForm
import yt_dlp
import os
from pathlib import Path
'''
def download_video(request):
    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            
            # Set the download path to the user's Downloads folder
            downloads_path = os.path.join(Path.home(), "Downloads", "YouTubeDownloads")
            os.makedirs(downloads_path, exist_ok=True)  # Ensure the folder exists

            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),  # Save to Downloads folder
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get('title', 'video')
                    
                # Redirect to home with a success message
                messages.success(request, f"Video '{video_title}' downloaded successfully!")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('home')
    else:
        form = YouTubeDownloadForm()
    return render(request, 'downloader/home.html', {'form': form})
'''
from django.http import StreamingHttpResponse, Http404
import yt_dlp
import requests

from django.http import StreamingHttpResponse, Http404
import yt_dlp
import requests
'''
def stream_video(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            messages.error(request, "No URL provided!")
            return redirect('home')

        try:
            # Path to the cookies file
            cookies_file = 'youtube_cookies.txt'

            # Use yt_dlp to fetch video information
            ydl_opts = {
                'format': 'best',
                'noplaylist': True,
                'cookiefile': cookies_file,  # Pass the cookies file
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info['url']  # Direct URL to the video stream

            # Define generator to stream video data
            def video_stream():
                with requests.get(video_url, stream=True) as response:
                    response.raise_for_status()
                    for chunk in response.iter_content(chunk_size=8192):
                        yield chunk

            # Stream the video to the client
            response = StreamingHttpResponse(video_stream(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="video.mp4"'
            return response

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('home')

    return render(request, 'downloader/home.html')
'''
import yt_dlp
from django.shortcuts import render, redirect
from django.contrib import messages
import os
import os
from django.shortcuts import render, redirect
from django.contrib import messages
import yt_dlp

import os
import shutil
from django.shortcuts import render, redirect
from django.contrib import messages
import yt_dlp

def download_video(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            messages.error(request, "No URL provided!")
            return redirect('home')

        try:
            # Define the source and destination paths for the cookies file
            source_cookies_file = os.path.join(os.path.dirname(__file__), 'youtube_cookies.txt')
            destination_cookies_file = os.path.join('/tmp', 'youtube_cookies.txt')

            # Copy the cookies file to the /tmp directory
            shutil.copyfile(source_cookies_file, destination_cookies_file)

            # yt-dlp options with cookies
            ydl_opts = {
                'format': 'best',
                'noplaylist': True,
                'cookiefile': destination_cookies_file,  # Pass the cookies file to yt-dlp
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            messages.success(request, "Video downloaded successfully!")
            return redirect('home')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('home')

    return render(request, 'downloader/home.html')
