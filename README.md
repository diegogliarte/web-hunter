# Web Hunter

##  📜 Introduction
WebHunter is a practical web scraping tool designed to gather data from various online sources. It's built in Python and offers a streamlined way to scrape information, store it, and send notifications about new or updated content.

## 🌟 Features
- Versatile Scrapers: Includes scrapers for Humble Bundle, Fanatical, and SteamDB.
- Effective Notifications: Supports email and Discord notifications.
- SQLite Database: Manages scraped data efficiently.
- Error Logging: Keeps track of issues for troubleshooting.

## 🛠 Installation
1. Clone the Repository:
```bash
git clone git@github.com:diegogliarte/web-hunter.git
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```

3, Environment Setup:
Create a .env file in the root directory.
Populate it with necessary SMTP and Discord configurations.


## 🚀 Usage
Use main.py to start the scraping process.
``` bash
python main.py --scrapers humble_bundle fanatical steamdb --notifiers email discord
```

## 🤝 Contributing
We welcome contributions! If you have suggestions or improvements:

- Fork the Repository.
- Create a New Branch for your changes.
- Submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support
For support or queries, feel free to open an issue on the GitHub repository.


