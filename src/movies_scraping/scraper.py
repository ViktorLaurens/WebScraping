from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

url = 'http://www.imdb.com/chart/top'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers, verify=True)

if response.status_code != 200:
    print(f"Failed to fetch data, status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Save prettified HTML to a file
with open('page_content.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())


movies = soup.select('td.titleColumn')
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]

print(f"Number of movies found: {len(movies)}")  # Debugging

movie_data = []

for index in range(0, len(movies)):
    try:
        movie_string = movies[index].get_text()
        print(f"Processing movie: {movie_string.strip()}")  # Debugging
        movie = ' '.join(movie_string.split()).replace('.', '')
        movie_title = movie[len(str(index))+1:-7]
        year = re.search(r'\((.*?)\)', movie_string).group(1)
        place = movie[:len(str(index))-(len(movie))]
        data = {
            "place": place,
            "movie_title": movie_title,
            "rating": ratings[index],
            "year": year,
            "star_cast": crew[index],
        }
        movie_data.append(data)
    except Exception as e:
        print(f"Error processing movie at index {index}: {e}")

for movie in movie_data:
    print(
        f"{movie['place']} - {movie['movie_title']} ({movie['year']}) - Starring: {movie['star_cast']}, Rating: {movie['rating']}"
    )

df = pd.DataFrame(movie_data)
df.to_csv('imdb_top_250_movies.csv', index=False)
