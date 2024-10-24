import os
import subprocess

class DecryptDownloader:
    def __init__(self):
        self.kid = None
        self.key = None
        self.manifest_url = None
        self.binary_path = os.path.join(os.path.dirname(__file__), 'bin', 'mp4decrypt')  # Adjust if necessary

    def set_manifest_url(self, manifest_url):
        self.manifest_url = manifest_url

    def set_decryption_key(self, key):
        self.key = key

    def set_kid(self, kid):
        self.kid = kid

    def download_and_decrypt(self, input_file, output_file):
        if not self.key:
            print("Decryption key is not set.")
            return

        self.download_media_file()  # Placeholder for your download logic

        command = [self.binary_path, '--key', f'{self.kid}:{self.key}', input_file, output_file]
        try:
            exit_code = subprocess.run(command, check=True)
            print(f"Decrypted file saved as: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during decryption: {e}")

    def download_media_file(self):
        if not self.manifest_url:
            print("Manifest URL is not set.")
            return

        print(f"Downloading media from: {self.manifest_url}")