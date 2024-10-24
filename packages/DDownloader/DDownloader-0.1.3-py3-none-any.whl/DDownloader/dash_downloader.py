import requests
import os
import xml.etree.ElementTree as ET
import subprocess

class DASHDownloader:
    def __init__(self, manifest_url):
        self.manifest_url = manifest_url
        self.binary_path = os.path.join(os.path.dirname(__file__), 'bin', 'N_m3u8DL-RE')

    def download_with_n_m3u8dl(self):
        command = [self.binary_path, self.manifest_url]
        try:
            exit_code = subprocess.run(command, check=True)
            print("Downloaded using N_m3u8DL-RE")
        except subprocess.CalledProcessError as e:
            print(f"Error during download: {e}")

    def download_manifest(self):
        response = requests.get(self.manifest_url)
        response.raise_for_status()
        return response.content

    def download_segments(self, manifest_content, output_dir='downloads'):
        os.makedirs(output_dir, exist_ok=True)
        root = ET.fromstring(manifest_content)

        for adaptation_set in root.findall('.//AdaptationSet'):
            for representation in adaptation_set.findall('Representation'):
                base_url = representation.attrib.get('baseURL', '')
                for segment in representation.findall('.//SegmentURL'):
                    segment_url = base_url + segment.attrib['media']
                    self.download_segment(segment_url, output_dir)

    def download_segment(self, segment_url, output_dir):
        response = requests.get(segment_url, stream=True)
        response.raise_for_status()

        filename = os.path.join(output_dir, segment_url.split("/")[-1])
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded: {filename}")