# DDownloader

**DDownloader** is a Python library to download HLS and DASH manifests and decrypt media files.

## Features
- Download HLS streams using `N_m3u8DL-RE`.
- Download DASH manifests and segments.
- Decrypt media files using `mp4decrypt`.

## Installation

Use the package manager [pip](https://pypi.org/project/DDownloader/0.1.0/) to install DDownloader.

```bash
pip install DDownloader==0.1.0
```

## Usage
- Download HLS content using the library:
```python
from manifest_downloader import HLSDownloader

hls_downloader = HLSDownloader("https://example.com/playlist.m3u8")
hls_downloader.download_with_n_m3u8dl()
```
- Download Dash content using the library:
```python
from manifest_downloader import DASHDownloader

dash_downloader = DASHDownloader("https://example.com/manifest.mpd")
dash_downloader.download_with_n_m3u8dl()
```
- To decrypt media files after downloading:
```python
from manifest_downloader import DecryptDownloader

decrypt_downloader = DecryptDownloader()
decrypt_downloader.set_manifest_url("https://example.com/manifest.mpd")
decrypt_downloader.set_decryption_key("0123456789abcdef0123456789abcdef")
decrypt_downloader.set_kid("1:0123456789abcdef0123456789abcdef")
decrypt_downloader.download_and_decrypt("encrypted_file.mp4", "decrypted_file.mp4")
```
- Here's a complete example demonstrating the use of all features:
```python
from manifest_downloader import HLSDownloader, DASHDownloader, DecryptDownloader

# HLS Download Example
hls_url = "https://example.com/playlist.m3u8"
hls_downloader = HLSDownloader(hls_url)
hls_downloader.download_with_n_m3u8dl()

# DASH Download Example
dash_url = "https://example.com/manifest.mpd"
dash_downloader = DASHDownloader(dash_url)
dash_downloader.download_with_n_m3u8dl()

# Decrypting Example
decrypt_downloader = DecryptDownloader()
decrypt_downloader.set_manifest_url(dash_url)
decrypt_downloader.set_decryption_key("0123456789abcdef0123456789abcdef")
decrypt_downloader.set_kid("1:0123456789abcdef0123456789abcdef")
decrypt_downloader.download_and_decrypt("encrypted_file.mp4", "decrypted_file.mp4")

```
