"""
LinkedIn profile scraper for extracting skills
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

def extract_skills_from_linkedin(profile_url, linkedin_email, linkedin_password):
    """
    Extract skills from a LinkedIn profile using Selenium
    """
    try:
        # Set up Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize driver
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        # Log in to LinkedIn
        driver.get('https://www.linkedin.com/login')
        
        # Wait for and fill in email
        email_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        email_field.send_keys(linkedin_email)
        
        # Fill in password
        password_field = driver.find_element(By.ID, 'password')
        password_field.send_keys(linkedin_password)
        
        # Click login button
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
        # Wait for login to complete
        time.sleep(3)
        
        # Navigate to profile
        driver.get(profile_url)
        
        # Wait for skills section to load
        time.sleep(3)
        
        # Try to find and click "Show more skills" button
        try:
            show_more = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Show more skills"]')
            show_more.click()
            time.sleep(2)
        except NoSuchElementException:
            pass  # Button might not exist if all skills are already shown
        
        # Extract skills
        skills = []
        skills_section = driver.find_elements(By.CSS_SELECTOR, '.skill-category-entity__name')
        
        for skill in skills_section:
            skills.append(skill.text.strip())
        
        # Close browser
        driver.quit()
        
        return skills
        
    except TimeoutException:
        print("Timeout waiting for LinkedIn page to load")
        if 'driver' in locals():
            driver.quit()
        return []
        
    except Exception as e:
        print(f"Error scraping LinkedIn profile: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return [] 