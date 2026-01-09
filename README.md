# MMDb - My Movie Database

A web application for movie enthusiasts to track, and discuss films with other users. Built with Flask and SQLite, MMDb provides a complete platform for maintaining a personal movie diary, watchlist, and community posts.

## Features

### **Movie Diary**
- Log and rate movies you've watched
- Add personal comments and ratings
- View your complete movie history

### **Watchlist**
- Create and manage a personal watchlist
- Add movies you want to watch
- Easily remove items from your list

### **Community Posts**
- Share your opinions about any movie
- Create detailed reviews and thoughts
- Like posts from other users
- Comment on posts and start discussions
- Edit or delete your own posts and comments
- Search posts by movie title

## Installation

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MMDb_progetto_natale
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python setup_db.py
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

```
MMDb_progetto_natale/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── auth.py                  # Authentication blueprint
│   ├── main.py                  # Main blueprint (home page)
│   ├── diary.py                 # Diary blueprint
│   ├── watchlist.py             # Watchlist blueprint
│   ├── post.py                  # Posts blueprint
│   ├── db.py                    # Database utilities
│   ├── schema.sql               # Database schema
│   ├── repositories/            # Data access layer
│   │   ├── user_repository.py
│   │   ├── movie_repository.py
│   │   ├── diary_repository.py
│   │   ├── watchlist_repository.py
│   │   └── post_repository.py
│   └── templates/               # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── auth/
│       ├── diary/
│       ├── watchlist/
│       └── post/
├── instance/                    # Instance folder (SQLite database)
├── run.py                       # Application entry point
├── setup_db.py                  # Database setup script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Author

Luca Bernardini - luca.bernardini@studenti.isissgobetti.it

## Other Project

https://github.com/LucaBernardinii/Briscola_Remastered_progetto_di_natale.git

## License

This project is open source and available under the MIT License.
