import argparse
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def capture_screenshot(url, output_path, width=1200, height=800):
    """
    Capture a screenshot of a URL using Selenium.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--window-size={width},{height}")
    
    # Use webdriver-manager to handle driver installation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"Navigating to: {url}")
        driver.get(url)
        # Wait for page to load (dynamic content)
        time.sleep(3) 
        
        print(f"Capturing screenshot to: {output_path}")
        driver.save_screenshot(output_path)
        return True
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture Website Screenshot")
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("output", help="Output file path (PNG)")
    parser.add_argument("--width", type=int, default=1200, help="Viewport width")
    parser.add_argument("--height", type=int, default=800, help="Viewport height")
    
    args = parser.parse_args()
    
    success = capture_screenshot(args.url, args.output, args.width, args.height)
    exit(0 if success else 1)
