import config
import sqlite3
import discord

from discord import ButtonStyle
from discord.ui import View, Select, ChannelSelect, Button, button, select

database = sqlite3.connect("./Databases/settings.sqlite")

class SettingsView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Edit Logging Channels", style=ButtonStyle.blurple)
    async def edit_logging_channels_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=EditLogChannelView())

class EditLogChannelView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Edit Ban Log Channel", style=ButtonStyle.blurple)
    async def edit_ban_log_channel_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=BanChannelSelectorView())
    
    @button(label="Edit Kick Log Channel", style=ButtonStyle.blurple)
    async def edit_kick_log_channel_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=KickChannelSelectorView())
    
    @button(label="Edit Timeout Log Channel", style=ButtonStyle.blurple)
    async def edit_timeout_log_channel_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=TimeoutChannelSelectorView())
    
    @button(label="Edit Warning Log Channel", style=ButtonStyle.blurple)
    async def edit_warning_log_channel_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=WarningChannelSelectorView())
    
    @button(label="Edit Role Update Log Channel", style=ButtonStyle.blurple)
    async def edit_role_log_channel_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=RoleUpdateChannelSelectorView())
    
    @button(label="Go Back", style=ButtonStyle.gray)
    async def go_back_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=SettingsView())

class BanChannelSelectorView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @select(cls=ChannelSelect, channel_types=[discord.ChannelType.text], placeholder='Select a channel for ban logs', min_values=1, max_values=1, row=0)
    async def ban_logs_channel_select(self, interaction: discord.Interaction, select: ChannelSelect):
        channel = interaction.guild.get_channel(select.values[0].id)
        database.execute("INSERT INTO LogChannels VALUES (?, NULL, ?, NULL, NULL, NULL) ON CONFLICT (guild_id) DO UPDATE SET ban_log_channel = ? WHERE guild_id = ?", (interaction.guild.id, channel.id, channel.id, interaction.guild.id,)).connection.commit()
        data = database.execute("SELECT warn_log_channel, ban_log_channel, kick_log_channel, timeout_log_channel, role_log_channel FROM LogChannels WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        settings_embed = interaction.message.embeds[0]
        settings_embed.set_field_at(
            index=0,
            name="Logging Channels:",
            value=f'''Ban Logs - {'Not set' if data[1] is None else interaction.guild.get_channel(data[1]).mention}
                    Kick Logs - {'Not set' if data[2] is None else interaction.guild.get_channel(data[2]).mention}
                    Timeout Logs - {'Not set' if data[3] is None else interaction.guild.get_channel(data[3]).mention}
                    Warning Logs - {'Not set' if data[0] is None else interaction.guild.get_channel(data[0]).mention}
                    Role Update Logs - {'Not set' if data[4] is None else interaction.guild.get_channel(data[4]).mention}
                ''',
            inline=False
        )
        await interaction.response.edit_message(embed=settings_embed, view=self)
    
    @button(label="Go Back", style=ButtonStyle.gray, row=1)
    async def go_back_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=EditLogChannelView())

class KickChannelSelectorView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @select(cls=ChannelSelect, channel_types=[discord.ChannelType.text], placeholder='Select a channel for kick logs', min_values=1, max_values=1, row=0)
    async def kick_logs_channel_select(self, interaction: discord.Interaction, select: ChannelSelect):
        channel = interaction.guild.get_channel(select.values[0].id)
        database.execute("INSERT INTO LogChannels VALUES (?, NULL, NULL, ?, NULL, NULL) ON CONFLICT (guild_id) DO UPDATE SET kick_log_channel = ? WHERE guild_id = ?", (interaction.guild.id, channel.id, channel.id, interaction.guild.id,)).connection.commit()
        data = database.execute("SELECT warn_log_channel, ban_log_channel, kick_log_channel, timeout_log_channel, role_log_channel FROM LogChannels WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        settings_embed = interaction.message.embeds[0]
        settings_embed.set_field_at(
            index=0,
            name="Logging Channels:",
            value=f'''Ban Logs - {'Not set' if data[1] is None else interaction.guild.get_channel(data[1]).mention}
                    Kick Logs - {'Not set' if data[2] is None else interaction.guild.get_channel(data[2]).mention}
                    Timeout Logs - {'Not set' if data[3] is None else interaction.guild.get_channel(data[3]).mention}
                    Warning Logs - {'Not set' if data[0] is None else interaction.guild.get_channel(data[0]).mention}
                    Role Update Logs - {'Not set' if data[4] is None else interaction.guild.get_channel(data[4]).mention}
                ''',
            inline=False
        )
        await interaction.response.edit_message(embed=settings_embed, view=self)
    
    @button(label="Go Back", style=ButtonStyle.gray, row=1)
    async def go_back_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=EditLogChannelView())

class TimeoutChannelSelectorView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @select(cls=ChannelSelect, channel_types=[discord.ChannelType.text], placeholder='Select a channel for timeout logs', min_values=1, max_values=1, row=0)
    async def timeout_logs_channel_select(self, interaction: discord.Interaction, select: ChannelSelect):
        channel = interaction.guild.get_channel(select.values[0].id)
        database.execute("INSERT INTO LogChannels VALUES (?, NULL, NULL, NULL, ?, NULL) ON CONFLICT (guild_id) DO UPDATE SET timeout_log_channel = ? WHERE guild_id = ?", (interaction.guild.id, channel.id, channel.id, interaction.guild.id,)).connection.commit()
        data = database.execute("SELECT warn_log_channel, ban_log_channel, kick_log_channel, timeout_log_channel, role_log_channel FROM LogChannels WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        settings_embed = interaction.message.embeds[0]
        settings_embed.set_field_at(
            index=0,
            name="Logging Channels:",
            value=f'''Ban Logs - {'Not set' if data[1] is None else interaction.guild.get_channel(data[1]).mention}
                    Kick Logs - {'Not set' if data[2] is None else interaction.guild.get_channel(data[2]).mention}
                    Timeout Logs - {'Not set' if data[3] is None else interaction.guild.get_channel(data[3]).mention}
                    Warning Logs - {'Not set' if data[0] is None else interaction.guild.get_channel(data[0]).mention}
                    Role Update Logs - {'Not set' if data[4] is None else interaction.guild.get_channel(data[4]).mention}
                ''',
            inline=False
        )
        await interaction.response.edit_message(embed=settings_embed, view=self)
    
    @button(label="Go Back", style=ButtonStyle.gray, row=1)
    async def go_back_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=EditLogChannelView())

class WarningChannelSelectorView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @select(cls=ChannelSelect, channel_types=[discord.ChannelType.text], placeholder='Select a channel for warning logs', min_values=1, max_values=1, row=0)
    async def warn_logs_channel_select(self, interaction: discord.Interaction, select: ChannelSelect):
        channel = interaction.guild.get_channel(select.values[0].id)
        database.execute("INSERT INTO LogChannels VALUES (?, ?, NULL, NULL, NULL, NULL) ON CONFLICT (guild_id) DO UPDATE SET warn_log_channel = ? WHERE guild_id = ?", (interaction.guild.id, channel.id, channel.id, interaction.guild.id,)).connection.commit()
        data = database.execute("SELECT warn_log_channel, ban_log_channel, kick_log_channel, timeout_log_channel, role_log_channel FROM LogChannels WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        settings_embed = interaction.message.embeds[0]
        settings_embed.set_field_at(
            index=0,
            name="Logging Channels:",
            value=f'''Ban Logs - {'Not set' if data[1] is None else interaction.guild.get_channel(data[1]).mention}
                    Kick Logs - {'Not set' if data[2] is None else interaction.guild.get_channel(data[2]).mention}
                    Timeout Logs - {'Not set' if data[3] is None else interaction.guild.get_channel(data[3]).mention}
                    Warning Logs - {'Not set' if data[0] is None else interaction.guild.get_channel(data[0]).mention}
                    Role Update Logs - {'Not set' if data[4] is None else interaction.guild.get_channel(data[4]).mention}
                ''',
            inline=False
        )
        await interaction.response.edit_message(embed=settings_embed, view=self)
    
    @button(label="Go Back", style=ButtonStyle.gray, row=1)
    async def go_back_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=EditLogChannelView())

class RoleUpdateChannelSelectorView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @select(cls=ChannelSelect, channel_types=[discord.ChannelType.text], placeholder='Select a channel for role update logs', min_values=1, max_values=1, row=0)
    async def role_update_logs_channel_select(self, interaction: discord.Interaction, select: ChannelSelect):
        channel = interaction.guild.get_channel(select.values[0].id)
        database.execute("INSERT INTO LogChannels VALUES (?, NULL, NULL, NULL, NULL, ?) ON CONFLICT (guild_id) DO UPDATE SET role_log_channel = ? WHERE guild_id = ?", (interaction.guild.id, channel.id, channel.id, interaction.guild.id,)).connection.commit()
        data = database.execute("SELECT warn_log_channel, ban_log_channel, kick_log_channel, timeout_log_channel, role_log_channel FROM LogChannels WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        settings_embed = interaction.message.embeds[0]
        settings_embed.set_field_at(
            index=0,
            name="Logging Channels:",
            value=f'''Ban Logs - {'Not set' if data[1] is None else interaction.guild.get_channel(data[1]).mention}
                    Kick Logs - {'Not set' if data[2] is None else interaction.guild.get_channel(data[2]).mention}
                    Timeout Logs - {'Not set' if data[3] is None else interaction.guild.get_channel(data[3]).mention}
                    Warning Logs - {'Not set' if data[0] is None else interaction.guild.get_channel(data[0]).mention}
                    Role Update Logs - {'Not set' if data[4] is None else interaction.guild.get_channel(data[4]).mention}
                ''',
            inline=False
        )
        await interaction.response.edit_message(embed=settings_embed, view=self)
    
    @button(label="Go Back", style=ButtonStyle.gray, row=1)
    async def go_back_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=EditLogChannelView())
