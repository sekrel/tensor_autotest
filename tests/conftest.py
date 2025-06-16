import os
import glob
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="class")
def setup(request):
    chrome_options = webdriver.ChromeOptions()
    download_dir = os.path.join(os.getcwd(), "downloads")
    clear_downloads(download_dir)
    prefs = {
        "download.default_directory": download_dir,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    request.cls.driver = driver
    
    yield driver
    
    # Закрытие драйвера после тестов
    driver.quit()


def clear_downloads(directory):
    """Удаляет все файлы из указанной директории"""
    files = glob.glob(os.path.join(directory, '*'))
    for f in files:
        try:
            if os.path.isfile(f):
                os.remove(f)
        except Exception as e:
            print(f"Ошибка при удалении файла {f}: {e}")