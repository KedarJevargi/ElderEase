# ElderEase - Senior Companion Application

ElderEase is a comprehensive digital companion application designed to assist seniors in their daily lives. It provides various modes of assistance including information access, medical reminders, entertainment, and emergency services.

## Features

- **Information Mode**: Access to news, weather, and general facts
- **Religious Mode**: Mythological stories and religious teachings
- **Medical Info Mode**: Medication reminders and prescription queries
- **Entertainment Mode**: Show and music recommendations via YouTube
- **Order Mode**: Food delivery and cab booking automation
- **Communication Mode**: Contact list with one-tap calling
- **Safety & Security**: Emergency SOS button with guardian notification
- **AI Companion Mode**: Voice-interactive companion to reduce loneliness

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: YouTube API (for entertainment mode)
- **External Services**: Swiggy, Uber (for order mode)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/elder-ease.git
cd elder-ease
```

2. Set up the Python environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the application:
```bash
python backend/app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
elder-ease/
├── backend/
│   └── app.py
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── signup.html
│   ├── mode_template.html
│   ├── signup.js
│   ├── login.js
│   └── styles.css
├── .gitignore
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Font Awesome for icons
- Bootstrap for UI components
- Flask for the backend framework # ElderEase
