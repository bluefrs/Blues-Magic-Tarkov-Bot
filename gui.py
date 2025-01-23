import tkinter as tk
from tkinter import messagebox
from bot import TarkovBot
from config import save_config, load_config
from logs import write_normal_log, write_error_log
from threading import Thread
import asyncio
import os
import sys

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Blue's Magic Tarkov Bot")
        self.root.geometry("400x300")

        # Set the window icon (top-right corner)
        if getattr(sys, 'frozen', False):  # Check if the app is running as a packaged .exe
            # If running as an executable, get the path to the temporary directory where bundled files are stored
            icon_path = os.path.join(sys._MEIPASS, 'Tagilla.ico')
        else:
            # If running as a script, just use the local directory
            icon_path = 'Tagilla.ico'  # Assuming the icon is in the same folder as the script

        try:
            self.root.iconbitmap(icon_path)  # Set the window icon
        except Exception as e:
            print(f"Error setting window icon: {e}")

        # Dark Mode Background Color
        self.root.configure(bg="#2e2e2e")  # Dark grey background

        # Label Colors for Dark Mode
        self.label_bot_token = tk.Label(root, text="BOT Token:", bg="#2e2e2e", fg="white")
        self.label_bot_token.pack(pady=5)

        # Password Field for Dark Mode
        self.entry_bot_token = tk.Entry(root, width=40, show="*", bg="#444444", fg="white", relief="flat")
        self.entry_bot_token.pack(pady=5)

        self.label_channel_name = tk.Label(root, text="Channel Name:", bg="#2e2e2e", fg="white")
        self.label_channel_name.pack(pady=5)

        self.entry_channel_name = tk.Entry(root, width=40, bg="#444444", fg="white", relief="flat")
        self.entry_channel_name.pack(pady=5)

        self.button_start = tk.Button(root, text="Start Bot", command=self.start_bot, bg="#3e8e41", fg="white", relief="flat")
        self.button_start.pack(pady=10)

        self.button_stop = tk.Button(root, text="Stop Bot", command=self.stop_bot, bg="#e74c3c", fg="white", relief="flat")
        self.button_stop.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Not Logged In", fg="red", bg="#2e2e2e")
        self.status_label.pack(pady=20)

        # Load the config file if it exists and pre-fill the fields
        bot_token, channel_name = load_config()
        if bot_token and channel_name:
            self.entry_bot_token.insert(0, bot_token)
            self.entry_channel_name.insert(0, channel_name)

        # Initialize bot_thread to None
        self.bot_thread = None

    def update_status(self, status):
        """Update the status label in the GUI."""
        self.status_label.config(text=f"Status: {status}")

        # Check if the status contains 'Logged in as', indicating successful login
        if "Logged in as" in status:
            self.status_label.config(fg="green")  # Set color to green when logged in
        else:
            self.status_label.config(fg="red")  # Otherwise, keep it red (not logged in)

    def start_bot(self):
        print("Start Bot button clicked.")  # Debugging line
        bot_token = self.entry_bot_token.get()
        channel_name = self.entry_channel_name.get()
        if not bot_token or not channel_name:
            messagebox.showerror("Error", "Please fill in both fields.")
            return
        save_config(bot_token, channel_name)
        write_normal_log("Starting bot...")
        bot_thread = Thread(target=self.run_bot, args=(bot_token, channel_name))
        bot_thread.daemon = True
        bot_thread.start()
        self.bot_thread = bot_thread  # Save the bot thread for later use
        self.update_status("Bot Started")

    def stop_bot(self):
        if self.bot_thread:
            print("Stopping bot...")  # Debugging line
            # Update status and log the action
            self.update_status("Bot Stopped")
            write_normal_log("Bot stopped.")
            # Additional logic to stop the bot can be added here if needed
            # If you want to gracefully stop the bot, you can implement it in the bot's `TarkovBot` class
        else:
            messagebox.showerror("Error", "Bot is not running.")

    def run_bot(self, bot_token, channel_name):
        try:
            print("Starting bot...")  # Debugging line
            
            # Create and set a new event loop for the current thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)  # Set the newly created event loop as the current event loop
            
            # Now run the bot with the new event loop
            bot = TarkovBot(bot_token, channel_name, self)  # Pass the App instance to the bot
            loop.run_until_complete(bot.run())  # This should run the bot
            
        except Exception as e:
            print(f"Error starting bot: {e}")
            write_error_log(f"Error starting bot: {e}")
