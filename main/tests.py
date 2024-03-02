import requests
from bs4 import BeautifulSoup

def scrape_instagram_profile(username):
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        profile_picture = soup.select_one('meta[property="og:image"]')['content']
        bio = soup.find('meta', property='og:description')['content'].split('-')[0].strip()
        return profile_picture, bio
    else:
        return None, None

# Example usage
username = '_heiscollins'
profile_picture, bio = scrape_instagram_profile(username)
print("Profile Picture URL:", profile_picture)
print("Bio:", bio)
