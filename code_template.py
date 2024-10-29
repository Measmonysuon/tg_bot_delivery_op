import os
import sqlite3
from telebot import TeleBot, types
import requests
from datetime import datetime

# Telegram Bot Token
bot = TeleBot('YOUR_TELEGRAM_BOT_API_KEY')

# Database setup function
def setup_database():
    conn = sqlite3.connect("item_control.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        item_package_num TEXT,
        item_num TEXT,
        client_phone TEXT,
        photo_path TEXT,
        send_date TEXT,
        receive_date TEXT,
        pickup_date TEXT,
        status TEXT DEFAULT 'Not Picked Up',
        payment_status TEXT DEFAULT 'Pending'
    )''')
    
    conn.commit()
    conn.close()

# Call the database setup function
setup_database()

# Database connection function
def db_connect():
    conn = sqlite3.connect('item_control.db')
    return conn, conn.cursor()

# Function to save photo in a specific directory
def save_photo(file_id, owner_id):
    # Create a folder for the owner_id if it doesn't exist
    folder_path = f"photos/{owner_id}"
    os.makedirs(folder_path, exist_ok=True)

    # Download the photo
    file_info = bot.get_file(file_id)
    photo_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'
    photo_data = requests.get(photo_url).content

    # Save the photo with a timestamp in the filename
    photo_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    photo_path = os.path.join(folder_path, photo_name)
    with open(photo_path, "wb") as photo_file:
        photo_file.write(photo_data)
    
    return photo_path

# 1. Adding an item with photo
@bot.message_handler(commands=['add_item_photo'])
def add_item_photo(message):
    msg = bot.reply_to(message, "Please send the item photo for the client.")
    bot.register_next_step_handler(msg, handle_photo_upload)

def handle_photo_upload(message):
    if message.photo:
        # Prompt for additional item details after receiving the photo
        msg = bot.reply_to(message, "Please provide the item details in this format:\nOwner ID, Package Number, Item Number, Client Phone")
        bot.register_next_step_handler(msg, lambda m: save_item_details(m, message.photo[-1].file_id))
    else:
        bot.reply_to(message, "No photo detected. Please try again by sending a valid image.")

def save_item_details(message, file_id):
    try:
        owner_id, package_num, item_num, client_phone = message.text.split(', ')
        
        # Save the photo in a user-specific folder and get the file path
        photo_path = save_photo(file_id, owner_id)
        
        # Save photo path and item details to the database
        conn, cursor = db_connect()
        cursor.execute('''INSERT INTO items (owner_id, item_package_num, item_num, client_phone, photo_path, send_date)
                          VALUES (?, ?, ?, ?, ?, ?)''', 
                       (owner_id, package_num, item_num, client_phone, photo_path, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
        
        bot.reply_to(message, "Item details and photo saved successfully.")
    except Exception as e:
        bot.reply_to(message, "Error saving item details. Please ensure correct format.\nError: " + str(e))

# 2. Checking items not picked up by a client
@bot.message_handler(commands=['check_items'])
def check_items(message):
    msg = bot.reply_to(message, "Enter the client phone number to check their unpicked items.")
    bot.register_next_step_handler(msg, show_unpicked_items)

def show_unpicked_items(message):
    client_phone = message.text
    conn, cursor = db_connect()
    
    cursor.execute('''SELECT id, send_date, owner_id, item_package_num, item_num, client_phone, status, payment_status, photo_path 
                      FROM items WHERE client_phone = ? AND status = "Not Picked Up"''', 
                   (client_phone,))
    items = cursor.fetchall()
    conn.close()

    if items:
        for item in items:
            item_id, send_date, owner_id, package_num, item_num, client_phone, status, payment_status, photo_path = item
            caption = (f"**Item Details**\n"
                       f"Arrival Date: {send_date}\n"
                       f"Owner ID: {owner_id}\n"
                       f"Package Number: {package_num}\n"
                       f"Item Number: {item_num}\n"
                       f"Client Phone: {client_phone}\n"
                       f"Status: {status}\n"
                       f"Payment Status: {payment_status}")
            
            # Send item photo with caption and an inline "Update Status" button
            with open(photo_path, 'rb') as photo_file:
                bot.send_photo(message.chat.id, photo_file, caption=caption, parse_mode="Markdown")
            
            # Add an inline button for operation team to update status
            markup = types.InlineKeyboardMarkup()
            update_button = types.InlineKeyboardButton("Update Status to Picked Up", callback_data=f"update_{item_id}")
            markup.add(update_button)
            bot.send_message(message.chat.id, "Update this item?", reply_markup=markup)
    else:
        bot.reply_to(message, "No unpicked items found for this client.")

# 3. Callback for updating item status
@bot.callback_query_handler(func=lambda call: call.data.startswith('update_'))
def update_item_status(call):
    item_id = int(call.data.split('_')[1])
    
    conn, cursor = db_connect()
    cursor.execute("UPDATE items SET status = 'Picked Up', pickup_date = ? WHERE id = ?", 
                   (datetime.now().strftime('%Y-%m-%d'), item_id))
    conn.commit()
    conn.close()
    
    bot.answer_callback_query(call.id, "Item status updated to Picked Up.")
    bot.send_message(call.message.chat.id, "The item status has been updated to 'Picked Up'.")

# Start polling
bot.polling()
