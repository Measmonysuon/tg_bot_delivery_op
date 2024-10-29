# Item Control System Bot

A Telegram bot designed to manage item inventory, enhancing workflow for system admins and the operations team. This bot allows for photo uploads, item tracking by client ID, item status checks, and real-time updates.

## Features

1. Add Item with Photo: Admins can upload item photos and details for tracking.
2. Check Unpicked Items: Operations team can check unpicked items for clients using their phone number.
3. Update Item Status: Mark items as "Picked Up" and update the status and pickup date via a button.

---

## Getting Started

### Prerequisites

- Python: Version 3.8 or higher
- Telegram Bot API token
- SQLite3

### Installation

1. Clone the Repository

   git clone https://github.com/your-username/item-control-bot.git
   cd item-control-bot

2. Install Dependencies

   pip install pyTelegramBotAPI requests
   pip install telebot

4. Set Up Database

   Run the database setup script:

   python database_setup.py

   This creates the `item_control.db` database with the `items` table.

5. Configure Telegram Bot

   - Obtain a bot token from BotFather: https://core.telegram.org/bots#botfather
   - Replace 'YOUR_TELEGRAM_BOT_API_KEY' in main.py with your token.

6. Run the Bot

   python main.py

---

## Bot Usage and Commands

1. Add Item with Photo (/add_item_photo)
   - Usage: /add_item_photo
   - Process:
     - Run the command to prompt for an item photo upload.
     - After the photo, the bot will ask for item details in this format:
       Owner ID, Package Number, Item Number, Client Phone
     - The photo and details are saved in the database.

2. Check Unpicked Items (/check_items)
   - Usage: /check_items
   - Process:
     - Run the command and enter the client’s phone number.
     - The bot lists all unpicked items for the client, with photos and details (arrival date, owner ID, package number, etc.).
     - Each item has an "Update Status to Picked Up" button to mark the item as collected.

3. Update Item Status (Button)
   - Usage: Click the "Update Status to Picked Up" button when the client picks up their item.
   - Process:
     - The bot updates the item’s status to "Picked Up" and logs the pickup date in the database.

---

## Code Structure

- database_setup.py: Sets up the SQLite database schema.
- main.py: Main bot script handling all commands and database interactions.

---

## 🗃️ Database Schema

The `items` table structure:

| Column             | Type     | Description                              |
|--------------------|----------|------------------------------------------|
| `id`               | INTEGER  | Primary Key                              |
| `owner_id`         | INTEGER  | ID of the item's owner                   |
| `item_package_num` | TEXT     | Item package number                      |
| `item_num`         | TEXT     | Item number                              |
| `client_phone`     | TEXT     | Client's phone number                    |
| `photo`            | BLOB     | Photo of the item                        |
| `send_date`        | TEXT     | Date item was sent                       |
| `receive_date`     | TEXT     | Date item was received                   |
| `pickup_date`      | TEXT     | Date item was picked up                  |
| `status`           | TEXT     | Status of item (default: Not Picked Up)  |
| `payment_status`   | TEXT     | Payment status (default: Pending)        |      

---

## Development Workflow

1. Database: Ensure the database (item_control.db) is created using database_setup.py.
2. Bot Commands: Follow usage instructions to interact with the bot as an admin or operations staff.
3. Testing: Test each command to confirm the bot saves and updates item details accurately.
4. Collaboration: Use feature branches and submit pull requests for new features or fixes.

---

## Contribution Guidelines

1. New Features: Open a GitHub Issue to discuss before implementing.
2. Code Style: Follow PEP8 guidelines for Python code.
3. Commit Messages: Use descriptive messages for clarity.

---

## License

This project is licensed under the MIT License.
