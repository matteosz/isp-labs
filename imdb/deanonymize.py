import csv

email = 'donald.trump@whitehouse.gov'

print('EX1')
# EX 1

# From plaintext creates mapping date -> rating for the given user
deanonim = {}
with open(f'anon_data/imdb-1.csv') as fopen:
    reader = csv.DictReader(fopen, fieldnames=['email', 'movie', 'date', 'rating'])
    for row in reader:
        if row['email'] == email:
            if deanonim.get(row['date']) is None:
                deanonim[row['date']] = set()
            deanonim[row['date']].add(row['rating'])

# Search the user hash in anon_data
matching = {}
highest = 0
email_hash = ''
with open(f'anon_data/com402-1.csv') as fopen:
    reader = csv.DictReader(fopen, fieldnames=['email', 'movie', 'date', 'rating'])
    for row in reader:
        if row['date'] in deanonim.keys() and row['rating'] in deanonim[row['date']]:
            if matching.get(row['email']) is None:
                matching[row['email']] = 0
            matching[row['email']] += 1
            if matching[row['email']] > highest:
                highest = matching[row['email']]
                email_hash = row['email']

print('Email hash: ' + email_hash)

movies = set()
# Find all movies hashes this user has seen
with open(f'anon_data/com402-1.csv') as fopen:
    reader = csv.DictReader(fopen, fieldnames=['email', 'movie', 'date', 'rating'])
    for row in reader:
        if row['email'] == email_hash:
            movies.add(row['movie'])
    
        
mapping = {}
# Find the tuple date - rating for each of that movie
for movie in movies:
    with open(f'anon_data/com402-1.csv') as fopen:
        reader = csv.DictReader(fopen, fieldnames=['email', 'movie', 'date', 'rating'])
        for row in reader:
            if row['movie'] == movie:
                if mapping.get(movie) is None:
                    mapping[movie] = {}
                if mapping[movie].get(row['date']) is None:
                    mapping[movie][row['date']] = set()
                mapping[movie][row['date']].add(row['rating'])


# Now search the plaintext of the given movies             
for movie in movies:
    print(f'-->Hash: {movie}: ', end='')
    movie_match = {} 
    movie_plain = ''
    best = 0
    with open(f'anon_data/imdb-1.csv') as fopen:
        reader = csv.DictReader(fopen, fieldnames=['email', 'movie', 'date', 'rating'])
        for row in reader:
            if row['date'] in mapping[movie].keys() and row['rating'] in mapping[movie][row['date']]:
                if movie_match.get(row['movie']) is None:
                    movie_match[row['movie']] = 0
                movie_match[row['movie']] += 1
                if movie_match[row['movie']] > best:
                    best = movie_match[row['movie']]
                    movie_plain = row['movie']

    print(movie_plain)

# EX 2
print('EX2')

# Map the movies with their frequencies in plaintext
plain_movies_freq = {}
user = {}
with open(f'anon_data/imdb-2.csv') as fopen:
    reader = csv.DictReader(fopen, fieldnames=['email', 'movie', 'date', 'rating'])
    for row in reader:
        if plain_movies_freq.get(row['movie']) is None:
            plain_movies_freq[row['movie']] = 0
        plain_movies_freq[row['movie']] += 1
        if row['email'] == email:
            if user.get(row['movie']) is None:
                user[row['movie']] = 0
            user[row['movie']] += 1

plain_movies = sorted(plain_movies_freq.items(), key=lambda x : x[1], reverse=True)

# Map the movies with their frequencies in anon
hash_movies_freq = {}
with open(f'anon_data/com402-2.csv') as fopen:
    reader = csv.DictReader(fopen, fieldnames=['email', 'movie', 'date', 'rating'])
    for row in reader:
        if hash_movies_freq.get(row['movie']) is None:
            hash_movies_freq[row['movie']] = 0
        hash_movies_freq[row['movie']] += 1

hash_movies = sorted(hash_movies_freq.items(), key=lambda x : x[1], reverse=True)
    
# Map hash to plaintext for movies
mapping = {}
iterator = iter(plain_movies)
for hash in hash_movies:
    mapping[hash] = next(iterator)[0]

# Find the users info
users = {}
with open(f'anon_data/com402-2.csv') as fopen:
    reader = csv.DictReader(fopen, fieldnames=['user', 'movie', 'date', 'rating'])
    for row in reader:
        if users.get(row['user']) is None:
            users[row['user']] = {}
        if mapping.get(row['movie']) is None:
            continue
        if users[row['user']].get(mapping[row['movie']]) is None:
            users[row['user']][mapping[row['movie']]] = 0
        users[row['user']][mapping[row['movie']]] += 1

mail_hash = ''     
# Check a match with user profiles
for id, value in users.items():
    found = True
    for movie, freq in value.items():
        if movie not in user.keys() or freq != user[movie]:
            found = False
            break
    if found is True:
        mail_hash = id
        break

print('Email hash: ' + mail_hash)

# Now search the films reviewed by user and convert into plaintext
with open(f'anon_data/com402-2.csv') as fopen:
    reader = csv.DictReader(fopen, fieldnames=['email', 'movie', 'date', 'rating'])
    for row in reader:
        if row['email'] == mail_hash:
            print(f'-->Hash: {row["movie"]}: ' + mapping[row['movie']])
