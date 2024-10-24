import os
import subprocess
import logging
import coloredlogs

# Set up logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

class DASH:
    def __init__(self):
        self.manifest_url = None
        self.output_name = None
        self.decryption_key = None
        self.binary_path = os.path.join(os.path.dirname(__file__), 'bin', 'N_m3u8DL-RE')

    def dash_downloader(self):
        if not self.manifest_url:
            logger.error("Manifest URL is not set.")
            return
        
        command = self._build_command()
        
        logger.debug(f"Running command: {' '.join(command)}")
        self._execute_command(command)

    def _build_command(self):
        command = [
            self.binary_path,
            self.manifest_url,
            '--auto-select',
            '-mt',
            '--thread-count', '12',
            '--save-dir', 'downloads',
            '--tmp-dir', 'downloads',
            '--save-name', self.output_name
        ]
        if self.decryption_key:
            command.append(f'--key {self.decryption_key}')
        return command

    def _execute_command(self, command):
        try:
            subprocess.run(command, check=True)
            logger.info("Downloaded using N_m3u8DL-RE")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error during download: {e}")
        except FileNotFoundError:
            logger.error(f"Binary not found at: {self.binary_path}")