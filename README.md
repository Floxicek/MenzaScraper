# MenzaScraper

MenzaScraper is a small project that notifies you when your favorite food is available in the CTU canteen.

## Features

- Get discord notifications for your favorite meals.
- Scrape lunch menus from CTU canteens.
- Easy to configure and use.
- Supports multiple canteens.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Floxicek/MenzaScraper.git
   ```
2. Navigate to the project directory:
   ```bash
   cd MenzaScraper
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your settings in `config.json`.

5. Add your discord Webhook in `.env`.

   ```.env
   WEBHOOK_URL=https://discord.com/api/webhooks/yoursecretcreds
   ```

6. Run the scraper:
   ```bash
   python scraper.py
   ```

## Usage

I suggest running the scraper using cron to get notified regularly

## License

This project is licensed under the MIT License.
