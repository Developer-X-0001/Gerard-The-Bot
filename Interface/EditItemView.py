import sqlite3
import discord

from discord import ButtonStyle, TextStyle
from discord.ui import Modal, TextInput, Select, RoleSelect, View, Button, button, select

database = sqlite3.connect("./Databases/shop.sqlite")

class EditItemSelectorView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ItemSelector())

class ItemSelector(Select):
    def __init__(self):
        data = database.execute("SELECT id, name, price, available FROM Items").fetchall()
        options = []
        for item in data:
            options.append(discord.SelectOption(label=item[1], description="Price: {} | {}".format(item[2], 'Available' if item[3] == 'yes' else 'Not Available'), value=item[0]))

        super().__init__(placeholder='Select an item to edit...', min_values=1, max_values=1, options=options, row=0)
    
    async def callback(self, interaction: discord.Interaction):
        data = database.execute("SELECT name, price, available, role, image_link FROM Items WHERE id = ?", (self.values[0],)).fetchone()
        role = interaction.guild.get_role(data[3])
        item_embed = discord.Embed(
            title="Editing Item",
            color=discord.Color.blue()
        )
        item_embed.add_field(name="Name:", value=data[0], inline=False)
        item_embed.add_field(name="Price:", value=data[1], inline=False)
        item_embed.add_field(name="Availability:", value="Available" if data[2] == 'yes' else 'Not Available', inline=False)
        item_embed.add_field(name="Role:", value=role.mention, inline=False)
        if data[4]:
            item_embed.set_thumbnail(url=data[4])

        await interaction.response.edit_message(embed=item_embed, view=ItemEditor(code=self.values[0]))

class ItemEditor(View):
    def __init__(self, code: str):
        self.item_id = code
        super().__init__(timeout=None)
        self.add_item(AvailabilitySelector(code=code))
    
    @select(cls=RoleSelect, placeholder="Edit role...", min_values=1, max_values=1, row=1)
    async def panelRoleSelect(self, interaction: discord.Interaction, select: RoleSelect):
        database.execute("UPDATE Items SET role = ? WHERE id = ?", (select.values[0].id, self.item_id,)).connection.commit()
        item_embed = interaction.message.embeds[0]
        item_embed.set_field_at(
            name="Role:",
            value=select.values[0].mention,
            inline=False,
            index=3
        )
        await interaction.response.edit_message(embed=item_embed)
    
    @button(label="Edit Name", style=ButtonStyle.blurple, row=2)
    async def edit_name_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(EditNameModal(code=self.item_id))

    @button(label="Edit Price", style=ButtonStyle.blurple, row=2)
    async def edit_price_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(EditPriceModal(code=self.item_id))

    @button(label="Edit Image", style=ButtonStyle.blurple, row=2)
    async def edit_image_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(EditImageModal(code=self.item_id))
    
    @button(label="Go Back", style=ButtonStyle.gray, row=3)
    async def edit_save_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=discord.Embed(description="Please select an item to edit it's information.", color=discord.Color.blue()), view=EditItemSelectorView(), ephemeral=True)

class AvailabilitySelector(Select):
    def __init__(self, code: str):
        self.item_id = code

        options = [
            discord.SelectOption(label="Yes", value='yes'),
            discord.SelectOption(label="No", value='no')
        ]

        super().__init__(placeholder="Edit availability...", min_values=1, max_values=1, options=options, row=0)

    async def callback(self, interaction: discord.Interaction):
        item_embed = interaction.message.embeds[0]
        item_embed.set_field_at(
            name="Availability:",
            value=self.values[0].capitalize(),
            inline=False,
            index=2
        )

        database.execute("UPDATE Items SET available = ? WHERE id = ?", (self.values[0], self.item_id,)).connection.commit()
        await interaction.response.edit_message(embed=item_embed)


class EditNameModal(Modal, title="Item Information Editor"):
    def __init__(self, code: str):
        self.item_id = code
        super().__init__(timeout=None)

    nameInput = TextInput(
        label="Name:",
        style=TextStyle.short,
        placeholder="Type item name...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        item_embed = interaction.message.embeds[0]
        item_embed.set_field_at(
            name="Name:",
            value=self.nameInput.value,
            inline=False,
            index=0
        )
        
        data = database.execute("SELECT name FROM Items WHERE name = ?", (self.nameInput.value,)).fetchone()
        if data is None:
            database.execute("UPDATE Items SET name = ? WHERE id = ?", (self.nameInput.value, self.item_id,)).connection.commit()
            await interaction.response.edit_message(embed=item_embed)

        else:
            await interaction.response.send_message(embed=discord.Embed(description="❌ Item with name **`{}`** already exists!".format(self.nameInput.value), color=discord.Color.red()), ephemeral=True)

class EditPriceModal(Modal, title="Item Information Editor"):
    def __init__(self, code: str):
        self.item_id = code
        super().__init__(timeout=None)

    priceInput = TextInput(
        label="Price:",
        style=TextStyle.short,
        placeholder="DIGIT ONLY! Type item price...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        item_embed = interaction.message.embeds[0]
        item_embed.set_field_at(
            name="Price:",
            value=self.priceInput.value,
            inline=False,
            index=1
        )
        
        if self.priceInput.value.isdigit():
            database.execute("UPDATE Items SET price = ? WHERE id = ?", (self.priceInput.value, self.item_id,)).connection.commit()
            await interaction.response.edit_message(embed=item_embed)

        else:
            await interaction.response.send_message(embed=discord.Embed(description="❌ Item price must be a digit!", color=discord.Color.red()), ephemeral=True)

class EditImageModal(Modal, title="Item Information Editor"):
    def __init__(self, code: str):
        self.item_id = code
        super().__init__(timeout=None)

    imageInput = TextInput(
        label="Image link:",
        style=TextStyle.short,
        placeholder="Type a valid image url...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        item_embed = interaction.message.embeds[0]
        try:
            item_embed.set_thumbnail(url=self.imageInput.value)
            database.execute("UPDATE Items SET image_link = ? WHERE id = ?", (self.imageInput.value, self.item_id,)).connection.commit()
            await interaction.response.edit_message(embed=item_embed)

        except:
            await interaction.response.send_message(embed=discord.Embed(description="❌ Invalid image link!", color=discord.Color.red()), ephemeral=True)