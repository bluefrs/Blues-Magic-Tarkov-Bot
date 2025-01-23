from twitchio.ext import commands
from utils import run_query, get_ammo_offsets
from logs import write_normal_log, write_error_log
from tkinter import messagebox
import asyncio

BOT_NICK = "TarkovFlea"  # Define your bot's Twitch username here

class TarkovBot(commands.Bot):
    def __init__(self, bot_token, channel_name, app):
        super().__init__(token=bot_token, prefix="!", initial_channels=[channel_name])
        self.bot_token = bot_token
        self.channel_name = channel_name
        self.app = app  # Pass the App instance to update the GUI

    async def event_ready(self):
        # Update the status once the bot is logged in
        print(f"Logged in as {self.nick}")
        write_normal_log(f"Bot logged in as {self.nick}")
        
        # Use the Tkinter after method to safely update the GUI from a separate thread
        self.app.root.after(0, self.app.update_status, f"Logged in as {self.nick}")

    async def event_message(self, message):
        if message.author and message.author.name.lower() == BOT_NICK.lower():
            return  # Ignore the bot's own messages

        if message.content.startswith(self._prefix):
            await self.handle_commands(message)  # Process commands


    @commands.command(name="ammo")
    async def ammo(self, ctx, *, ammo_name: str):
        offsets = get_ammo_offsets(ammo_name)

        if not offsets:
            await ctx.send(f"Ammo type '{ammo_name}' not found in the database.")
            write_error_log(f"Ammo type '{ammo_name}' not found in the database.")
            return

        for offset in offsets:
            query = f"""
            {{
                ammo(limit: 1, offset: {offset}) {{
                    item {{
                        shortName
                        name
                    }}
                    damage
                    fragmentationChance
                    penetrationPower
                }}
            }}
            """

            try:
                result = run_query(query)
                items = result.get("data", {}).get("ammo", [])
                
                # Check if results are too broad (more than 5 results)
                if len(items) > 5:
                    await ctx.send("Query too broad. Please be more specific.")
                    write_error_log(f"Query for ammo '{ammo_name}' returned more than 5 results.")
                    continue  # Skip further processing for this offset

                if not items:
                    await ctx.send(f"Ammo '{ammo_name}' not found.")
                    write_error_log(f"Ammo '{ammo_name}' not found.")
                    continue

                item = items[0]
                name = item['item'].get("name", "Data not available")
                damage = item.get("damage", "Data not available")
                penetration = item.get("penetrationPower", "Data not available")
                frag_chance = item.get("fragmentationChance", "Data not available")
                frag_chance = f"{frag_chance * 100:.1f}%" if isinstance(frag_chance, float) else frag_chance

                response = f"{name}: Damage: {damage}, Penetration: {penetration}, Fragmentation Chance: {frag_chance}."
                await ctx.send(response)
                write_normal_log(f"Responded to !ammo command: {response}")
            except Exception as e:
                await ctx.send("An error occurred while fetching ammo data.")
                write_error_log(f"Error in !ammo command: {e}")
                print(f"Error in !ammo command: {e}")  # Log error

    @commands.command(name="flea")  # Changed to !flea
    async def flea(self, ctx, *, item_name: str):
        if len(item_name) < 3:
            await ctx.send("Please provide at least 3 characters for the item search.")
            write_error_log("Item search term too short for !flea command.")
            return

        query = f"""
        {{
            items(name: "{item_name}") {{
                name
                avg24hPrice
                lastLowPrice
            }}
        }}
        """

        try:
            result = run_query(query)
            items = result.get("data", {}).get("items", [])
            
            # Check if results are too broad (more than 5 results)
            if len(items) > 5:
                await ctx.send("Query too broad. Please be more specific.")
                write_error_log(f"Query for flea '{item_name}' returned more than 5 results.")
                return  # Stop further processing for this query

            if not items:
                await ctx.send(f"No items found for keyword '{item_name}'.")
                write_error_log(f"No items found for keyword '{item_name}'.")
                return

            for item in items:
                avg_24h = item.get("avg24hPrice")
                if avg_24h is None:
                    write_normal_log(f"Skipped item with no avg24hPrice: {item.get('name', 'Unknown')}")
                    continue

                name = item.get("name", "N/A")
                last_low_offer = item.get("lastLowPrice", "Data not available")
                last_low_offer_str = f"₽{last_low_offer:,}" if last_low_offer is not None else "Not Available"

                response = f"{name} \n24A: ₽{avg_24h:,} \nLowestOffer: {last_low_offer_str}"
                await ctx.send(response)
                write_normal_log(f"Responded to !flea command with: {response}")
        except Exception as e:
            await ctx.send("An error occurred while fetching item data.")
            write_error_log(f"Error in !flea command: {e}")
            print(f"Error in !flea command: {e}")  # Log error
