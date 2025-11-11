# 🎬 NexLoad - Professional Media Downloader

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-Muhammedcengizz598-black.svg)](https://github.com/Muhammedcengizz598)

> **NexLoad** - Lightning-fast, professional-grade media downloader supporting 20+ platforms including YouTube, Pinterest, Instagram, TikTok, and more.

---

## ✨ Features

- 🎯 **Multi-Platform Support**: YouTube, Pinterest, Instagram, TikTok, Twitter/X, LinkedIn, Spotify, SoundCloud, Facebook, Vimeo, and 10+ more
- ⚡ **Lightning-Fast Downloads**: Optimized performance with parallel processing
- 🎬 **Multiple Quality Options**: 4K, 1440p, 1080p, 720p, 480p, 360p, and audio-only formats
- 🔄 **Smart Fallback System**: Automatically tries alternative formats if primary fails
- 🎵 **Audio Extraction**: Convert videos to MP3 at 320kbps
- 📦 **Batch Downloads**: Download multiple videos at once
- 🛡�� **DRM Detection**: Identifies and alerts about protected content
- 💾 **Automatic Organization**: Downloads saved to dedicated folder
- 🎨 **Beautiful CLI Interface**: Color-coded, user-friendly terminal interface
- 🔧 **Auto-Dependency Management**: Automatically installs and updates required packages

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- FFmpeg (for video processing)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Muhammedcengizz598/NexLoad.git
cd NexLoad
```

2. **Run the application**
```bash
python NexLoad.py
```

The application will automatically:
- Check for required dependencies
- Install missing packages
- Update yt-dlp to the latest version
- Create a downloads folder

---

## 📖 Usage

### Interactive Mode

Simply run the program and follow the prompts:

```bash
python NexLoad.py
```

**Main Menu Options:**
1. 🎬 Single Video/Audio Download
2. 📦 Batch URL Download
3. 📊 Download Statistics
4. 🔄 Refresh Dependencies
5. ❌ Exit NexLoad

### Single Download Example

```
🔗 Enter video/music URL (or 'q' to quit): https://www.youtube.com/watch?v=dQw4w9WgXcQ

📊 MEDIA INFORMATION
📺 Title: Rick Astley - Never Gonna Give You Up
👤 Creator: Rick Astley
⏱️ Duration: 3:32

🎯 SELECT QUALITY:
1. 🎯 4K Ultra (3840x2160)
2. 🔥 1440p QHD (2560x1440)
3. ⚡ 1080p Full HD (1920x1080)
4. 💎 720p HD (1280x720)
5. 🎬 480p SD (854x480)
6. 📱 360p Mobile (640x360)
7. ⚙️ 240p Low (426x240)
8. 🔧 144p Minimal (256x144)
9. 🎵 Audio Only (MP3 320kbps)

👆 Make your choice (1-9): 3
```

### Batch Download Example

```
URL 1: https://www.youtube.com/watch?v=video1
URL 2: https://www.youtube.com/watch?v=video2
URL 3: https://pin.it/shortlink
[Leave empty to finish]
```

---

## 🎯 Supported Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| YouTube | ✅ Full Support | All video types |
| Pinterest | ✅ Full Support | Videos & GIFs |
| Instagram | ✅ Full Support | Posts & Reels |
| TikTok | ✅ Full Support | All videos |
| Twitter/X | ✅ Full Support | Videos & GIFs |
| LinkedIn | ✅ Full Support | Video posts |
| Facebook | ✅ Full Support | Videos & streams |
| Vimeo | ✅ Full Support | Public videos |
| Dailymotion | ✅ Full Support | All videos |
| Twitch | ✅ Full Support | VODs & clips |
| Reddit | ✅ Full Support | Video posts |
| Bilibili | ✅ Full Support | Chinese platform |
| SoundCloud | ✅ Full Support | Audio tracks |
| Spotify | ⚠️ DRM Protected | Cannot download |
| Rumble | ✅ Full Support | Alternative platform |
| Odysee | ✅ Full Support | Decentralized platform |

---

## 📁 Download Organization

All downloads are automatically saved to:

**Windows:**
```
C:\Users\[YourUsername]\Downloads\NexLoad\
```

**macOS:**
```
~/Downloads/NexLoad/
```

**Linux:**
```
~/Downloads/NexLoad/
```

---

## ⚙️ Quality Options Explained

| Option | Resolution | Use Case |
|--------|-----------|----------|
| 4K Ultra | 3840x2160 | High-end displays, archival |
| 1440p QHD | 2560x1440 | Gaming monitors, high-quality viewing |
| 1080p Full HD | 1920x1080 | Standard HD, most common |
| 720p HD | 1280x720 | Streaming, lower bandwidth |
| 480p SD | 854x480 | Mobile devices, quick download |
| 360p Mobile | 640x360 | Smartphones, minimal storage |
| 240p Low | 426x240 | Very low bandwidth |
| 144p Minimal | 256x144 | Extreme low bandwidth |
| Audio Only | MP3 320kbps | Music extraction |

---

## 🔧 Requirements

### Python Packages
- **yt-dlp**: Core downloading engine
- **requests**: HTTP library for web requests
- **colorama**: Terminal color support
- **tqdm**: Progress bar display
- **mutagen**: Audio metadata handling

### System Requirements
- **FFmpeg**: Required for video processing and merging
  - Windows: `choco install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org)
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`

---

## 🐛 Troubleshooting

### Issue: "FFmpeg not found"
**Solution:**
```bash
# Windows (using Chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### Issue: "DRM Protected Content"
**Solution:** This content is legally protected. NexLoad cannot download DRM-protected content.

### Issue: "Video not available"
**Solution:** The video may be:
- Deleted or removed
- Private or restricted
- Geographically blocked
- Temporarily unavailable

### Issue: Download fails repeatedly
**Solution:**
1. Check your internet connection
2. Try a different quality option
3. Use the "Refresh Dependencies" option
4. Restart the application

### Issue: Slow download speed
**Solution:**
1. Check your internet connection
2. Try a lower quality option
3. Close other bandwidth-consuming applications
4. Try downloading at a different time

---

## 📊 Statistics & Monitoring

View your download history and statistics:

```
📊 DOWNLOAD STATISTICS
📁 Location: NexLoad
🎬 Video files: 42
🎵 Audio files: 15
📦 Total files: 57
💾 Total size: 2,847.50 MB

📋 RECENT DOWNLOADS:
1. Video Title 1 (245.3 MB)
2. Video Title 2 (156.8 MB)
3. Audio Track 1 (8.5 MB)
```

---

## 🔐 Privacy & Security

- ✅ No data collection
- ✅ No account required
- ✅ All processing is local
- ✅ No tracking or analytics
- ✅ Open source (MIT License)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Muhammedcengizz598

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact & Support

- **GitHub**: [@Muhammedcengizz598](https://github.com/Muhammedcengizz598)
- **Issues**: [Report a bug](https://github.com/Muhammedcengizz598/NexLoad/issues)
- **Discussions**: [Start a discussion](https://github.com/Muhammedcengizz598/NexLoad/discussions)

---

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Core downloading engine
- [FFmpeg](https://ffmpeg.org) - Video processing
- [Colorama](https://github.com/tartley/colorama) - Terminal colors
- All contributors and users

---

## ⚠️ Legal Notice

**Important:** NexLoad is designed for downloading content that you have the right to download. Users are responsible for:

- Respecting copyright laws in their jurisdiction
- Obtaining proper permissions from content creators
- Complying with platform terms of service
- Not using this tool for illegal purposes

The developers are not responsible for misuse of this software.

---

## 🎯 Roadmap

- [ ] GUI Interface (PyQt/Tkinter)
- [ ] Playlist support
- [ ] Subtitle downloading
- [ ] Video conversion options
- [ ] Cloud storage integration
- [ ] Scheduled downloads
- [ ] Download queue management
- [ ] Advanced filtering options

---

## 📈 Statistics

- ⭐ **20+ Supported Platforms**
- 🎬 **Multiple Quality Options**
- ⚡ **Lightning-Fast Downloads**
- 🔄 **Smart Fallback System**
- 💾 **Automatic Organization**

---

## 🌟 Show Your Support

If you find NexLoad helpful, please consider:
- ⭐ Starring the repository
- 🔗 Sharing with friends
- 🐛 Reporting bugs
- 💡 Suggesting features
- 🤝 Contributing code

---

**Made with ❤️ by Muhammed Cengiz**

*Last Updated: 2024*
