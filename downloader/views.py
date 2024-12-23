from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import YouTubeDownloadForm
import yt_dlp
import os
from pathlib import Path

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
