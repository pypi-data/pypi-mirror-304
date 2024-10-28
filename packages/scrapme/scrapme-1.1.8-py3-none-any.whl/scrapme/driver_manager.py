import os
import platform
import requests
import tarfile
import zipfile
from pathlib import Path
import subprocess
import shutil

class DriverManager:
    """Manages the download and setup of geckodriver."""
    
    GECKODRIVER_BASE_URL = "https://github.com/mozilla/geckodriver/releases/download"
    VERSION_MAP = {
        '127': '0.35.0',  # Firefox 127.x
        '115': '0.34.0',  # Firefox ESR 115.x
        '102': '0.33.0',  # Firefox ESR 102.x
    }

    @staticmethod
    def get_firefox_version():
        """Get installed Firefox version."""
        try:
            output = subprocess.check_output(['firefox', '--version']).decode()
            version = output.split()[-1].split('.')[0]
            return version
        except Exception:
            return None

    @staticmethod
    def get_platform_info():
        """Get platform specific information for geckodriver."""
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == 'linux':
            if machine == 'x86_64' or machine == 'amd64':
                return 'linux64'
            elif 'aarch64' in machine or 'arm64' in machine:
                return 'linux-aarch64'
            else:
                return 'linux32'
        elif system == 'darwin':
            if 'arm64' in machine:
                return 'macos-aarch64'
            else:
                return 'macos'
        elif system == 'windows':
            if machine == 'amd64' or machine == 'x86_64':
                return 'win64'
            else:
                return 'win32'
        return None

    @classmethod
    def download_geckodriver(cls):
        """Download and setup geckodriver."""
        try:
            # Get Firefox version and platform
            firefox_version = cls.get_firefox_version()
            platform_info = cls.get_platform_info()
            
            if not firefox_version or not platform_info:
                raise Exception("Could not determine Firefox version or platform")

            # Determine geckodriver version based on Firefox version
            base_version = firefox_version
            geckodriver_version = None
            for ver, driver_ver in cls.VERSION_MAP.items():
                if int(base_version) >= int(ver):
                    geckodriver_version = driver_ver
                    break

            if not geckodriver_version:
                geckodriver_version = cls.VERSION_MAP[max(cls.VERSION_MAP.keys())]

            # Create download URL
            if platform.system().lower() == 'windows':
                filename = f"geckodriver-v{geckodriver_version}-{platform_info}.zip"
            else:
                filename = f"geckodriver-v{geckodriver_version}-{platform_info}.tar.gz"

            download_url = f"{cls.GECKODRIVER_BASE_URL}/v{geckodriver_version}/{filename}"

            # Download file
            response = requests.get(download_url)
            response.raise_for_status()

            # Create driver directory
            driver_dir = Path.home() / '.webdrivers'
            driver_dir.mkdir(parents=True, exist_ok=True)

            # Save and extract the file
            archive_path = driver_dir / filename
            with open(archive_path, 'wb') as f:
                f.write(response.content)

            # Extract the archive
            if filename.endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(driver_dir)
            else:
                with tarfile.open(archive_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(driver_dir)

            # Make geckodriver executable on Unix-like systems
            driver_path = driver_dir / ('geckodriver.exe' if platform.system().lower() == 'windows' else 'geckodriver')
            if platform.system().lower() != 'windows':
                driver_path.chmod(0o755)

            # Clean up
            archive_path.unlink()

            return str(driver_path)
        except Exception as e:
            raise Exception(f"Failed to download geckodriver: {str(e)}")

    @classmethod
    def setup_driver(cls):
        """Setup geckodriver and return its path."""
        try:
            # Check if geckodriver is in PATH
            if shutil.which('geckodriver'):
                return shutil.which('geckodriver')

            # Check if we have a cached driver
            driver_path = Path.home() / '.webdrivers' / ('geckodriver.exe' if platform.system().lower() == 'windows' else 'geckodriver')
            if driver_path.exists():
                return str(driver_path)

            # Download and setup new driver
            return cls.download_geckodriver()
        except Exception as e:
            raise Exception(f"Failed to setup geckodriver: {str(e)}")
