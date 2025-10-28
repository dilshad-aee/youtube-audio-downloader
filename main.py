import os
import threading
from pathlib import Path
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import yt_dlp

# Android-specific imports
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path


class YouTubeAudioDownloader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # Request Android permissions if on Android
        if platform == 'android':
            request_permissions([
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
            # Set Android-specific download path
            self.download_path = os.path.join(
                primary_external_storage_path(),
                'Download'
            )
        else:
            # Set default download path for desktop
            self.download_path = str(Path.home() / "Downloads")
        
        # Title
        title = Label(
            text='YouTube Audio Downloader',
            size_hint=(1, 0.1),
            font_size='24sp',
            bold=True,
            color=(0.2, 0.6, 1, 1)
        )
        self.add_widget(title)
        
        # URL Input Section
        url_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        url_label = Label(text='YouTube URL:', size_hint=(0.2, 1), halign='right')
        self.url_input = TextInput(
            hint_text='Enter YouTube video URL here...',
            multiline=False,
            size_hint=(0.8, 1)
        )
        url_layout.add_widget(url_label)
        url_layout.add_widget(self.url_input)
        self.add_widget(url_layout)
        
        # Download Path Section
        path_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        path_label = Label(text='Save to:', size_hint=(0.2, 1), halign='right')
        self.path_input = TextInput(
            text=self.download_path,
            multiline=False,
            size_hint=(0.6, 1),
            readonly=True
        )
        browse_btn = Button(
            text='Browse',
            size_hint=(0.2, 1),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        browse_btn.bind(on_press=self.show_file_chooser)
        path_layout.add_widget(path_label)
        path_layout.add_widget(self.path_input)
        path_layout.add_widget(browse_btn)
        self.add_widget(path_layout)
        
        # Download Button
        self.download_btn = Button(
            text='Download Audio',
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 1, 1),
            font_size='18sp',
            bold=True
        )
        self.download_btn.bind(on_press=self.start_download)
        self.add_widget(self.download_btn)
        
        # Progress Bar
        progress_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.15), spacing=5)
        self.progress_label = Label(
            text='Ready to download',
            size_hint=(1, 0.4),
            color=(0.7, 0.7, 0.7, 1)
        )
        self.progress_bar = ProgressBar(max=100, size_hint=(1, 0.6))
        progress_layout.add_widget(self.progress_label)
        progress_layout.add_widget(self.progress_bar)
        self.add_widget(progress_layout)
        
        # Status/Info Area
        self.status_label = Label(
            text='Enter a YouTube URL and click Download Audio',
            size_hint=(1, 0.49),
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top',
            color=(0.8, 0.8, 0.8, 1)
        )
        self.add_widget(self.status_label)
        
        # Bind window resize
        Window.bind(on_resize=self.on_window_resize)
    
    def on_window_resize(self, instance, width, height):
        self.status_label.text_size = (width - 40, None)
    
    def show_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        file_chooser = FileChooserListView(
            path=self.download_path,
            dirselect=True,
            size_hint=(1, 0.9)
        )
        
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        select_btn = Button(text='Select', background_color=(0.2, 0.6, 1, 1))
        cancel_btn = Button(text='Cancel', background_color=(0.8, 0.3, 0.3, 1))
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(file_chooser)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Select Download Folder',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def select_path(instance):
            if file_chooser.selection:
                self.download_path = file_chooser.selection[0]
            else:
                self.download_path = file_chooser.path
            self.path_input.text = self.download_path
            popup.dismiss()
        
        select_btn.bind(on_press=select_path)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def update_status(self, message, dt=None):
        self.status_label.text = message
    
    def update_progress(self, value, dt=None):
        self.progress_bar.value = value
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                # Extract percentage from the status string
                percent_str = d.get('_percent_str', '0%').strip().replace('%', '')
                percent = float(percent_str)
                
                downloaded = d.get('_downloaded_bytes_str', 'N/A')
                total = d.get('_total_bytes_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                
                status_msg = f"Downloading: {percent:.1f}%\n"
                status_msg += f"Size: {downloaded} / {total}\n"
                status_msg += f"Speed: {speed} | ETA: {eta}"
                
                Clock.schedule_once(lambda dt: self.update_status(status_msg), 0)
                Clock.schedule_once(lambda dt: self.update_progress(percent), 0)
            except:
                pass
        
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self.update_status('Processing audio...'), 0)
            Clock.schedule_once(lambda dt: self.update_progress(100), 0)
    
    def download_audio(self, url, output_path):
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'quiet': False,
                'no_warnings': False,
            }
            
            Clock.schedule_once(lambda dt: self.update_status('Fetching video information...'), 0)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown')
                
                Clock.schedule_once(
                    lambda dt: self.update_status(f'Downloading: {video_title}\n\nStarting download...'),
                    0
                )
                
                # Download
                ydl.download([url])
                
                success_msg = f'✓ Download Complete!\n\n'
                success_msg += f'Title: {video_title}\n'
                success_msg += f'Saved to: {output_path}'
                
                Clock.schedule_once(lambda dt: self.update_status(success_msg), 0)
                Clock.schedule_once(lambda dt: self.update_progress(100), 0)
                Clock.schedule_once(lambda dt: setattr(self.download_btn, 'disabled', False), 0)
                Clock.schedule_once(lambda dt: setattr(self.download_btn, 'text', 'Download Audio'), 0)
        
        except Exception as e:
            error_msg = f'✗ Error occurred:\n\n{str(e)}\n\nPlease check the URL and try again.'
            Clock.schedule_once(lambda dt: self.update_status(error_msg), 0)
            Clock.schedule_once(lambda dt: self.update_progress(0), 0)
            Clock.schedule_once(lambda dt: setattr(self.download_btn, 'disabled', False), 0)
            Clock.schedule_once(lambda dt: setattr(self.download_btn, 'text', 'Download Audio'), 0)
    
    def start_download(self, instance):
        url = self.url_input.text.strip()
        
        if not url:
            self.status_label.text = '✗ Please enter a YouTube URL'
            return
        
        if not url.startswith(('http://', 'https://')):
            self.status_label.text = '✗ Please enter a valid URL (must start with http:// or https://)'
            return
        
        # Disable button during download
        self.download_btn.disabled = True
        self.download_btn.text = 'Downloading...'
        self.progress_bar.value = 0
        
        # Start download in a separate thread
        download_thread = threading.Thread(
            target=self.download_audio,
            args=(url, self.download_path)
        )
        download_thread.daemon = True
        download_thread.start()


class YouTubeAudioApp(App):
    def build(self):
        # Only set window size on desktop
        if platform not in ('android', 'ios'):
            Window.size = (700, 550)
        Window.clearcolor = (0.15, 0.15, 0.15, 1)
        return YouTubeAudioDownloader()


if __name__ == '__main__':
    YouTubeAudioApp().run()
