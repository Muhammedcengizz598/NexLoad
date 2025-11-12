#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    NEXLOAD - PREMIUM EDITION (OPTIMIZED)                  ║
║                   Professional Media Downloader - Parallel                ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  Creator: Muhammed Cengiz                                                 ║
║  Version: 2.0 Premium - Parallel Optimized                                ║
║  License: MIT                                                             ║
║                                                                           ║
║  Features:                                                                ║
║  • ⚡ Multi-threaded parallel downloads (4-8 concurrent)                  ║
║  • 🚀 Lightning-fast downloads with optimized performance                 ║
║  • 🌐 Multi-platform support (20+ platforms)                              ║
║  • 4K video quality & 320kbps audio                                       ║
║  • 📦 Batch download with concurrent processing                           ║
║  • 🔄 Advanced error handling & recovery                                  ║
║  • 💎 Clean & elegant terminal interface                                  ║
║  • 🧵 Thread-safe operations with queue management                        ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import platform
import threading
import time
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed, queue
from threading import Lock, Semaphore, Event
from queue import Queue, PriorityQueue
import traceback

class NexLoadCore:
    def __init__(self):
        self.system = platform.system().lower()
        self.downloads_path = self._get_downloads_path()
        self.required_packages = [
            'yt-dlp',
            'requests',
            'colorama',
            'tqdm',
            'mutagen'
        ]
        self.supported_sites = [
            'youtube', 'tiktok', 'instagram', 'twitter', 'x.com',
            'linkedin', 'pinterest', 'spotify', 'soundcloud',
            'facebook', 'vimeo', 'dailymotion', 'twitch', 'reddit',
            'bilibili', 'rumble', 'odysee', 'bitchute'
        ]
        self.quality_options = {
            '1': ('🎯 4K Ultra (3840x2160)', 'bestvideo[height<=2160]+bestaudio/best[height<=2160]'),
            '2': ('🔥 1440p QHD (2560x1440)', 'bestvideo[height<=1440]+bestaudio/best[height<=1440]'),
            '3': ('⚡ 1080p Full HD (1920x1080)', 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'),
            '4': ('💎 720p HD (1280x720)', 'bestvideo[height<=720]+bestaudio/best[height<=720]'),
            '5': ('🎬 480p SD (854x480)', 'bestvideo[height<=480]+bestaudio/best[height<=480]'),
            '6': ('📱 360p Mobile (640x360)', 'bestvideo[height<=360]+bestaudio/best[height<=360]'),
            '7': ('⚙️ 240p Low (426x240)', 'bestvideo[height<=240]+bestaudio/best[height<=240]'),
            '8': ('🔧 144p Minimal (256x144)', 'bestvideo[height<=144]+bestaudio/best[height<=144]'),
            '9': ('🎵 Audio Only (MP3 320kbps)', 'bestaudio/best')
        }
        
        # Thread management
        self.max_workers = self._get_optimal_workers()
        self.download_lock = Lock()
        self.stats_lock = Lock()
        self.progress_lock = Lock()
        self.download_semaphore = Semaphore(self.max_workers)
        self.stop_event = Event()
        
        # Download statistics
        self.download_stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'total_size': 0,
            'total_time': 0,
            'downloads': []
        }
        
        # Initialize colorama for cross-platform colors
        try:
            from colorama import init, Fore, Back, Style
            init(autoreset=True)
            self.colors = {
                'primary': Fore.CYAN + Style.BRIGHT,
                'secondary': Fore.MAGENTA + Style.BRIGHT,
                'success': Fore.GREEN + Style.BRIGHT,
                'warning': Fore.YELLOW + Style.BRIGHT,
                'error': Fore.RED + Style.BRIGHT,
                'info': Fore.BLUE + Style.BRIGHT,
                'highlight': Back.BLUE + Fore.WHITE + Style.BRIGHT,
                'reset': Style.RESET_ALL
            }
        except ImportError:
            self.colors = {key: '' for key in ['primary', 'secondary', 'success', 'warning', 'error', 'info', 'highlight', 'reset']}

    def _get_optimal_workers(self):
        """CPU sayısına göre optimal worker sayısını belirler"""
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        # 4-8 arası optimal worker sayısı
        return min(max(4, cpu_count), 8)

    def _get_downloads_path(self):
        """İşletim sistemine göre indirme klasörünü belirler"""
        if self.system == 'windows':
            return str(Path.home() / 'Downloads' / 'NexLoad')
        elif self.system == 'darwin':  # macOS
            return str(Path.home() / 'Downloads' / 'NexLoad')
        else:  # Linux/Android
            if os.path.exists('/sdcard'):
                return '/sdcard/Download/NexLoad'
            return str(Path.home() / 'Downloads' / 'NexLoad')

    def _clear_screen(self):
        """Ekranı temizler"""
        os.system('cls' if self.system == 'windows' else 'clear')

    def _print_header(self):
        """Gelişmiş başlık banner'ını yazdırır"""
        c = self.colors
        print(f"{c['primary']}╔══════════════════════════════════════════════════════════════════════════╗{c['reset']}")
        print(f"{c['primary']}║{c['highlight']}                    NEXLOAD v2.0 PREMIUM (PARALLEL)                    {c['primary']}║{c['reset']}")
        print(f"{c['primary']}║{c['secondary']}                 Professional Media Downloader - Optimized              {c['primary']}║{c['reset']}")
        print(f"{c['primary']}╠══════════════════════════════════════════════════════════════════════════╣{c['reset']}")
        print(f"{c['primary']}║ {c['info']}⚡ Multi-threaded{c['reset']} • {c['success']}4K Quality{c['reset']} • {c['secondary']}320kbps Audio{c['reset']} • {c['warning']}Batch Download{c['reset']}   {c['primary']}║{c['reset']}")
        print(f"{c['primary']}║ {c['info']}🌐 20+ Platforms:{c['reset']} YouTube, TikTok, Instagram, Pinterest, X...     {c['primary']}║{c['reset']}")
        print(f"{c['primary']}║ {c['info']}💎 Workers: {c['secondary']}{self.max_workers}{c['reset']} • {c['info']}Features:{c['reset']} {c['secondary']}Auto-merge • Smart fallback • Parallel{c['reset']}       {c['primary']}║{c['reset']}")
        print(f"{c['primary']}╚══════════════════════════════════════════════════════════════════════════╝{c['reset']}")
        print()

    def _print_loading_animation(self, text, duration=0):
        """Loading animasyonu - optimized"""
        c = self.colors
        print(f"{c['success']}✓{c['reset']} {text}")

    def _execute_command(self, command, show_output=False):
        """Sistem komutlarını çalıştırır"""
        try:
            if show_output:
                result = subprocess.run(command, shell=True, check=True, 
                                      capture_output=False, text=True)
            else:
                result = subprocess.run(command, shell=True, check=True, 
                                      capture_output=True, text=True)
            return True, result.stdout if not show_output else ""
        except subprocess.CalledProcessError as e:
            return False, str(e)

    def _install_package(self, package):
        """Paket yükler"""
        c = self.colors
        print(f"{c['info']}📦 Installing {c['highlight']}{package}{c['reset']}{c['info']}...{c['reset']}")
        commands = [
            f"{sys.executable} -m pip install --upgrade {package}",
            f"{sys.executable} -m pip install --force-reinstall {package}",
            f"pip3 install --upgrade {package}",
            f"pip install --upgrade {package}"
        ]
        
        for cmd in commands:
            success, output = self._execute_command(cmd)
            if success:
                print(f"{c['success']}✅ {package} successfully installed!{c['reset']}")
                return True
        
        print(f"{c['error']}❌ Failed to install {package}!{c['reset']}")
        return False

    def check_and_install_dependencies(self):
        """Gerekli kütüphaneleri kontrol eder ve yükler"""
        c = self.colors
        print(f"{c['info']}🔍 Scanning dependencies...{c['reset']}")
        missing_packages = []
        
        for package in self.required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"{c['success']}✅ {package}{c['reset']} - {c['success']}OK{c['reset']}")
            except ImportError:
                missing_packages.append(package)
                print(f"{c['warning']}⚠️ {package}{c['reset']} - {c['error']}MISSING{c['reset']}")

        if missing_packages:
            print(f"\n{c['warning']}📦 Installing {len(missing_packages)} missing packages...{c['reset']}")
            
            print(f"{c['info']}📦 Updating pip...{c['reset']}", end='', flush=True)
            self._execute_command(f"{sys.executable} -m pip install --upgrade pip --quiet")
            print(f"\r{c['success']}✓ Pip updated{c['reset']}")
            
            for package in missing_packages:
                if not self._install_package(package):
                    self._reinstall_all_packages()
                    return

        print(f"{c['info']}🔄 Updating yt-dlp...{c['reset']}", end='', flush=True)
        self._execute_command(f"{sys.executable} -m pip install --upgrade yt-dlp --quiet")
        print(f"\r{c['success']}✓ yt-dlp updated{c['reset']}")
        
        print(f"\n{c['success']}✅ All dependencies ready!{c['reset']}\n")

    def _reinstall_all_packages(self):
        """Tüm kütüphaneleri siler ve yeniden yükler"""
        c = self.colors
        print(f"\n{c['warning']}🔄 Corrupted package detected!{c['reset']}")
        print(f"{c['info']}🗑️ Reinstalling all packages...{c['reset']}")
        
        for package in self.required_packages:
            print(f"{c['warning']}🗑️ Uninstalling {package}...{c['reset']}")
            self._execute_command(f"{sys.executable} -m pip uninstall {package} -y")
            
        for package in self.required_packages:
            self._install_package(package)

    def _create_download_directory(self):
        """İndirme klasörünü oluşturur"""
        c = self.colors
        try:
            os.makedirs(self.downloads_path, exist_ok=True)
            print(f"{c['success']}📁 Download directory: {c['highlight']}{self.downloads_path}{c['reset']}")
        except Exception as e:
            print(f"{c['error']}❌ Cannot create directory: {e}{c['reset']}")
            self.downloads_path = os.getcwd()

    def _validate_url(self, url):
        """URL geçerliliğini kontrol eder"""
        if not url or not isinstance(url, str):
            return False
        
        url = url.strip().lower()
        valid_domains = [
            'youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com',
            'twitter.com', 'x.com', 'linkedin.com', 'pinterest.com', 'pin.it',
            'spotify.com', 'soundcloud.com', 'facebook.com', 'fb.watch',
            'vimeo.com', 'dailymotion.com', 'twitch.tv', 'reddit.com',
            'bilibili.com', 'rumble.com', 'odysee.com', 'bitchute.com'
        ]
        
        return any(domain in url for domain in valid_domains)

    def _create_logger(self):
        """yt-dlp için özel logger oluşturur"""
        c = self.colors
        class CustomLogger:
            def debug(self, msg):
                pass
            
            def info(self, msg):
                pass
            
            def warning(self, msg):
                if 'ffmpeg' in msg.lower() or 'error' in msg.lower():
                    pass
            
            def error(self, msg):
                pass
        
        return CustomLogger()

    def _get_ffmpeg_path(self):
        """FFmpeg yolunu bulur"""
        import shutil
        ffmpeg_path = shutil.which('ffmpeg')
        return ffmpeg_path if ffmpeg_path else None

    def _resolve_pinterest_url(self, url):
        """Pinterest kısa linkini uzun URL'ye dönüştürür"""
        try:
            import requests
            if 'pin.it' in url:
                response = requests.head(url, allow_redirects=True, timeout=10)
                return response.url
            return url
        except:
            return url

    def _get_video_info(self, url):
        """Video bilgilerini alır"""
        c = self.colors
        try:
            import yt_dlp
            
            if 'pin.it' in url.lower():
                url = self._resolve_pinterest_url(url)
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'no_color': True,
                'noprogress': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', []) or []
                return {
                    'title': info.get('title', 'Unknown Title'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown Uploader'),
                    'formats': len(formats),
                    'has_video': any(f.get('vcodec', 'none') != 'none' for f in formats),
                    'has_audio': any(f.get('acodec', 'none') != 'none' for f in formats)
                }
        except Exception as e:
            return None

    def _download_media(self, url, quality_format, is_audio_only=False, worker_id=0):
        """Medyayı indirir - Thread-safe"""
        c = self.colors
        download_info = {'success': False, 'filename': '', 'size': 0, 'speed': '', 'time': '', 'worker_id': worker_id}
        
        try:
            # Semaphore ile concurrent download kontrolü
            self.download_semaphore.acquire()
            
            import yt_dlp
            from tqdm import tqdm
            import time as time_module
            
            start_time = time_module.time()
            
            if 'pin.it' in url.lower():
                url = self._resolve_pinterest_url(url)
            
            if 'spotify.com' in url.lower():
                return False
            
            is_pinterest = 'pinterest.com' in url.lower()
            
            if is_audio_only:
                output_template = f'{self.downloads_path}/%(title)s.%(ext)s'
                format_selector = 'bestaudio/best'
            else:
                output_template = f'{self.downloads_path}/%(title)s.%(ext)s'
                format_selector = quality_format

            class ProgressHook:
                def __init__(self):
                    self.pbar = None
                    self.total_bytes = 0
                    self.final_filename = ''
                    self.last_update = 0

                def __call__(self, d):
                    if d['status'] == 'downloading':
                        if self.pbar is None:
                            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                            if total > 0:
                                self.total_bytes = total
                                self.pbar = tqdm(
                                    total=total, 
                                    unit='B', 
                                    unit_scale=True,
                                    desc=f'{c["info"]}[W{worker_id}] ⬇️{c["reset"]}',
                                    bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}',
                                    ncols=80,
                                    position=worker_id
                                )
                        
                        if self.pbar and 'downloaded_bytes' in d:
                            downloaded = d['downloaded_bytes']
                            if self.pbar.n < downloaded:
                                self.pbar.update(downloaded - self.pbar.n)
                    
                    elif d['status'] == 'finished':
                        if self.pbar:
                            self.pbar.close()
                        self.final_filename = d.get('filename', '')
                        download_info['filename'] = self.final_filename
                        download_info['size'] = self.total_bytes

            ydl_opts = {
                'format': format_selector,
                'outtmpl': output_template,
                'progress_hooks': [ProgressHook()],
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': False,
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'prefer_insecure': False,
                'socket_timeout': 30,
                'retries': 5,
                'fragment_retries': 5,
                'logger': self._create_logger(),
                'postprocessor_args': ['-loglevel', 'error'],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
            }

            if is_pinterest:
                ydl_opts.update({
                    'format': 'best[ext=mp4]/best[ext=webm]/best',
                    'socket_timeout': 60,
                    'retries': 10,
                    'fragment_retries': 10,
                    'skip_unavailable_fragments': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Referer': 'https://www.pinterest.com/',
                    }
                })

            if is_audio_only:
                ydl_opts.update({
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                })
            else:
                ydl_opts.update({
                    'postprocessors': [
                        {
                            'key': 'FFmpegVideoConvertor',
                            'preferedformat': 'mp4',
                        },
                        {
                            'key': 'FFmpegMetadata',
                        }
                    ],
                    'merge_output_format': 'mp4',
                    'prefer_ffmpeg': True,
                    'keepvideo': False,
                    'ffmpeg_location': self._get_ffmpeg_path(),
                    'postprocessor_args': ['-c:v', 'libx264', '-c:a', 'aac', '-strict', '-2'],
                })

            progress_hook = ProgressHook()
            ydl_opts['progress_hooks'] = [progress_hook]
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            end_time = time_module.time()
            elapsed = end_time - start_time
            
            if progress_hook.total_bytes > 0:
                speed_mbps = (progress_hook.total_bytes / (1024 * 1024)) / elapsed if elapsed > 0 else 0
                download_info['speed'] = f"{speed_mbps:.2f} MB/s"
                download_info['time'] = f"{int(elapsed // 60)}m {int(elapsed % 60)}s" if elapsed >= 60 else f"{elapsed:.1f}s"
            
            download_info['success'] = True
            
            # Thread-safe stats update
            with self.stats_lock:
                self.download_stats['successful'] += 1
                self.download_stats['total_size'] += progress_hook.total_bytes
                self.download_stats['total_time'] += elapsed
                self.download_stats['downloads'].append(download_info)
            
            return True

        except Exception as e:
            with self.stats_lock:
                self.download_stats['failed'] += 1
            return False
        finally:
            self.download_semaphore.release()

    def _fallback_download(self, url, is_audio_only=False, worker_id=0):
        """Alternatif kalitelerde indirme dener"""
        c = self.colors
        is_pinterest = 'pinterest.com' in url.lower()
        
        if is_audio_only:
            fallback_formats = ['bestaudio', 'best']
        else:
            if is_pinterest:
                fallback_formats = [
                    'best',
                    'best[height<=1080]',
                    'best[height<=720]',
                    'best[height<=480]',
                    'best[height<=360]',
                    'best[vcodec!=none]',
                    'best[acodec!=none]'
                ]
            else:
                fallback_formats = [
                    'best[height<=1080]',
                    'best[height<=720]',
                    'best[height<=480]',
                    'best[height<=360]',
                    'best'
                ]

        for fmt in fallback_formats:
            if self._download_media(url, fmt, is_audio_only, worker_id):
                return True
        
        return False

    def _download_worker(self, url, quality_format, is_audio_only, worker_id):
        """Worker thread fonksiyonu"""
        c = self.colors
        try:
            success = self._download_media(url, quality_format, is_audio_only, worker_id)
            
            if not success:
                success = self._fallback_download(url, is_audio_only, worker_id)
            
            return {
                'url': url,
                'success': success,
                'worker_id': worker_id
            }
        except Exception as e:
            with self.stats_lock:
                self.download_stats['failed'] += 1
            return {
                'url': url,
                'success': False,
                'worker_id': worker_id,
                'error': str(e)
            }

    def download_single_url(self):
        """Tek URL indirir"""
        c = self.colors
        while True:
            print(f"\n{c['primary']}╔═══════════════════════════════════════════════════════════════╗{c['reset']}")
            print(f"{c['primary']}║{c['highlight']}                      SINGLE DOWNLOAD                       {c['primary']}║{c['reset']}")
            print(f"{c['primary']}╚═══════════════════════════════════════════════════════════════╝{c['reset']}")
            
            url = input(f"\n{c['secondary']}🔗 Enter video/music URL (or 'q' to quit): {c['reset']}").strip()
            
            if url.lower() == 'q':
                return

            if not self._validate_url(url):
                print(f"{c['error']}❌ Invalid URL! Please enter a supported platform link.{c['reset']}")
                continue

            print(f"{c['info']}🔍 Fetching media information...{c['reset']}", end='', flush=True)
            info = self._get_video_info(url)
            print(f"\r{c['success']}✓ Media information retrieved{c['reset']}")
            
            if not info:
                print(f"{c['error']}❌ Cannot get media information!{c['reset']}")
                self._reinstall_all_packages()
                continue

            print(f"\n{c['success']}📊 MEDIA INFORMATION{c['reset']}")
            print(f"{c['info']}📺 Title: {c['highlight']}{info['title']}{c['reset']}")
            print(f"{c['info']}👤 Creator: {c['secondary']}{info['uploader']}{c['reset']}")
            if info['duration']:
                minutes, seconds = divmod(info['duration'], 60)
                print(f"{c['info']}⏱️ Duration: {c['warning']}{int(minutes)}:{int(seconds):02d}{c['reset']}")

            print(f"\n{c['primary']}🎯 SELECT QUALITY:{c['reset']}")
            for key, (desc, _) in self.quality_options.items():
                print(f"{c['secondary']}{key}.{c['reset']} {desc}")

            choice = input(f"\n{c['highlight']}👆 Make your choice (1-9): {c['reset']}").strip()
            
            if choice not in self.quality_options:
                print(f"{c['error']}❌ Invalid selection!{c['reset']}")
                continue

            desc, format_selector = self.quality_options[choice]
            is_audio_only = choice == '9'

            print(f"\n{c['success']}🚀 Downloading in '{desc.split(' ', 1)[1]}' quality...{c['reset']}")
            
            success = self._download_media(url, format_selector, is_audio_only, worker_id=0)
            
            if not success:
                print(f"{c['warning']}⚠️ First attempt failed, trying alternative methods...{c['reset']}")
                success = self._fallback_download(url, is_audio_only, worker_id=0)

            if success:
                print(f"{c['success']}✅ Download completed successfully!{c['reset']}")
            else:
                print(f"{c['error']}❌ Download failed. Please check the URL or try again later.{c['reset']}")

            input(f"\n{c['warning']}⏎ Press Enter to continue...{c['reset']}")
            break

    def download_multiple_urls(self):
        """Çoklu URL'leri paralel olarak indirir"""
        c = self.colors
        urls = []
        
        print(f"\n{c['primary']}╔═══════════════════════════════════════════════════════════════╗{c['reset']}")
        print(f"{c['primary']}║{c['highlight']}                   BATCH DOWNLOAD (PARALLEL)                  {c['primary']}║{c['reset']}")
        print(f"{c['primary']}╚═══════════════════════════════════════════════════════════════╝{c['reset']}")
        print(f"{c['info']}💡 Enter one URL per line, leave empty line to finish{c['reset']}")
        print(f"{c['info']}🧵 Parallel workers: {c['highlight']}{self.max_workers}{c['reset']}")
        
        while True:
            url = input(f"{c['secondary']}URL {len(urls)+1}: {c['reset']}").strip()
            
            if not url:
                break
                
            if self._validate_url(url):
                urls.append(url)
                print(f"{c['success']}✅ Added ({len(urls)} URLs){c['reset']}")
            else:
                print(f"{c['error']}❌ Invalid URL, skipping...{c['reset']}")

        if not urls:
            print(f"{c['error']}❌ No valid URLs found!{c['reset']}")
            return

        print(f"\n{c['success']}📦 {len(urls)} URLs ready for parallel download!{c['reset']}")
        print(f"{c['primary']}🎯 Select quality for all files:{c['reset']}")
        
        for key, (desc, _) in self.quality_options.items():
            print(f"{c['secondary']}{key}.{c['reset']} {desc}")

        choice = input(f"\n{c['highlight']}👆 Make your choice (1-9): {c['reset']}").strip()
        
        if choice not in self.quality_options:
            print(f"{c['error']}❌ Invalid selection!{c['reset']}")
            return

        desc, format_selector = self.quality_options[choice]
        is_audio_only = choice == '9'

        # Reset stats
        with self.stats_lock:
            self.download_stats = {
                'total': len(urls),
                'successful': 0,
                'failed': 0,
                'total_size': 0,
                'total_time': 0,
                'downloads': []
            }

        print(f"\n{c['success']}🚀 Starting parallel download with {self.max_workers} workers...{c['reset']}")
        print(f"{c['info']}📥 Processing {len(urls)} files in '{desc.split(' ', 1)[1]}' quality...{c['reset']}\n")
        
        start_time = time.time()
        
        # ThreadPoolExecutor ile paralel indirme
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            
            for idx, url in enumerate(urls):
                future = executor.submit(
                    self._download_worker,
                    url,
                    format_selector,
                    is_audio_only,
                    idx % self.max_workers
                )
                futures[future] = url
            
            # Tamamlanan görevleri takip et
            completed = 0
            for future in as_completed(futures):
                completed += 1
                try:
                    result = future.result()
                except Exception as e:
                    with self.stats_lock:
                        self.download_stats['failed'] += 1

        end_time = time.time()
        total_elapsed = end_time - start_time

        # Sonuç raporu
        table_width = 76
        print(f"\n{c['primary']}{'═' * table_width}{c['reset']}")
        print(f"{c['highlight']}{'  📦 PARALLEL BATCH DOWNLOAD - SUMMARY REPORT':^{table_width}}{c['reset']}")
        print(f"{c['primary']}{'═' * table_width}{c['reset']}")
        
        with self.stats_lock:
            stats = self.download_stats.copy()
        
        batch_rows = [
            ('📊 Total Files', f'{stats["total"]} files'),
            ('✅ Successful', f'{stats["successful"]} files', 'success'),
            ('❌ Failed', f'{stats["failed"]} files', 'error'),
            ('💾 Total Size', f'{stats["total_size"] / (1024 * 1024):.2f} MB'),
            ('⏱️ Total Time', f'{int(total_elapsed // 60)}m {int(total_elapsed % 60)}s'),
            ('🧵 Workers Used', f'{self.max_workers} threads'),
            ('📂 Save Location', str(Path(self.downloads_path).name)),
        ]
        
        for row in batch_rows:
            label = row[0]
            value = row[1]
            color_type = row[2] if len(row) > 2 else 'info'
            color_code = c.get(color_type, c['info'])
            print(f"{c['info']}  {label}{c['reset']}: {color_code}{value}{c['reset']}")
        
        print(f"{c['primary']}{'═' * table_width}{c['reset']}")
        print(f"{c['secondary']}  ✨ Full path: {c['warning']}{self.downloads_path}{c['reset']}")
        print(f"{c['primary']}{'═' * table_width}{c['reset']}\n")
        
        input(f"\n{c['warning']}⏎ Press Enter to continue...{c['reset']}")

    def show_download_stats(self):
        """İndirme istatistiklerini gösterir"""
        c = self.colors
        try:
            files = list(Path(self.downloads_path).glob('*'))
            videos = [f for f in files if f.suffix.lower() in ['.mp4', '.mkv', '.avi', '.mov']]
            audios = [f for f in files if f.suffix.lower() in ['.mp3', '.wav', '.m4a', '.aac']]
            
            print(f"\n{c['primary']}╔════════════════════════════════���══════════════════════════════╗{c['reset']}")
            print(f"{c['primary']}║{c['highlight']}                   DOWNLOAD STATISTICS                   {c['primary']}║{c['reset']}")
            print(f"{c['primary']}╚═══════════════════════════════════════════════════════════════╝{c['reset']}")
            print(f"{c['info']}📁 Location: {c['highlight']}{self.downloads_path}{c['reset']}")
            print(f"{c['secondary']}🎬 Video files: {c['success']}{len(videos)}{c['reset']}")
            print(f"{c['secondary']}🎵 Audio files: {c['success']}{len(audios)}{c['reset']}")
            print(f"{c['secondary']}📦 Total files: {c['warning']}{len(files)}{c['reset']}")
            print(f"{c['info']}🧵 Max Workers: {c['highlight']}{self.max_workers}{c['reset']}")
            
            if files:
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                size_mb = total_size / (1024 * 1024)
                print(f"{c['secondary']}💾 Total size: {c['highlight']}{size_mb:.2f} MB{c['reset']}")
                
                print(f"\n{c['primary']}📋 RECENT DOWNLOADS:{c['reset']}")
                recent_files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
                for i, file in enumerate(recent_files, 1):
                    if file.is_file():
                        size_mb = file.stat().st_size / (1024 * 1024)
                        print(f"{c['info']}{i}.{c['reset']} {c['secondary']}{file.name}{c['reset']} {c['warning']}({size_mb:.1f} MB){c['reset']}")
            
        except Exception as e:
            print(f"{c['error']}❌ Cannot get statistics: {e}{c['reset']}")

    def run(self):
        """Ana program döngüsü"""
        c = self.colors
        self._clear_screen()
        self._print_header()
        
        print(f"{c['info']}🚀 Initializing NexLoad Premium (Parallel Optimized)...{c['reset']}")
        self.check_and_install_dependencies()
        self._create_download_directory()
        print(f"{c['success']}✓ System ready with {self.max_workers} parallel workers!{c['reset']}\n")
        
        while True:
            self._clear_screen()
            self._print_header()
            
            print(f"{c['primary']}╔═══════════════════════════════════════════════════════════════╗{c['reset']}")
            print(f"{c['primary']}║{c['highlight']}                         MAIN MENU                         {c['primary']}║{c['reset']}")
            print(f"{c['primary']}╚═══════════════════════════════════════════════════════════════╝{c['reset']}")
            
            menu_options = [
                "🎬 Single Video/Audio Download",
                "📦 Batch URL Download (Parallel)",
                "📊 Download Statistics",
                "🔄 Refresh Dependencies",
                "❌ Exit NexLoad"
            ]
            
            for i, option in enumerate(menu_options, 1):
                print(f"{c['secondary']}{i}.{c['reset']} {option}")
            
            choice = input(f"\n{c['highlight']}👆 Select option (1-5): {c['reset']}").strip()
            
            if choice == '1':
                self.download_single_url()
            elif choice == '2':
                self.download_multiple_urls()
            elif choice == '3':
                self.show_download_stats()
                input(f"\n{c['warning']}⏎ Press Enter to continue...{c['reset']}")
            elif choice == '4':
                print(f"{c['info']}🔄 Refreshing dependencies...{c['reset']}")
                self._reinstall_all_packages()
                input(f"\n{c['warning']}⏎ Press Enter to continue...{c['reset']}")
            elif choice == '5':
                print(f"\n{c['success']}👋 NexLoad Premium is shutting down...{c['reset']}")
                print(f"{c['secondary']}💫 Thanks for using NexLoad - Professional Media Downloader{c['reset']}")
                break
            else:
                print(f"{c['error']}❌ Invalid selection!{c['reset']}")


def main():
    """Ana fonksiyon"""
    try:
        app = NexLoadCore()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Program stopped by user!")
        print(f"👋 Goodbye from NexLoad!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print(f"🔄 Reinstalling dependencies...")
        app = NexLoadCore()
        app._reinstall_all_packages()


if __name__ == "__main__":
    main()
