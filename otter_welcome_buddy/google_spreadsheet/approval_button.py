import discord
from pyparsing import Any
from pyparsing import Optional


class ButtonAddCompany(discord.ui.View):
    """Creates a button"""

    response: bool = False

    def __init__(self, *args: dict[str, dict[str, Any]], **kwargs: Optional[float]) -> None:
        super().__init__(*args, **kwargs)
        self.message: discord.Message | None = None

    @discord.ui.button(
        label="Accept",
        style=discord.ButtonStyle.success,
    )
    async def accept(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button["ButtonAddCompany"],
    ) -> None:
        """Button to accept"""
        print(button)
        await interaction.response.send_message("Company accepted successfully! ✅")
        self.response = True
        self.stop()
        await self.disable_items()

    @discord.ui.button(
        label="Decline",
        style=discord.ButtonStyle.red,
    )
    async def decline(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button["ButtonAddCompany"],
    ) -> None:
        """Button to decline"""
        print(button)
        await interaction.response.send_message("Company declined successfully! ❌")
        self.response = False
        self.stop()
        await self.disable_items()

    async def disable_items(self) -> None:
        """Disable items"""
        for item in self.children:  # type: discord.ui.Item
            if isinstance(item, discord.ui.Button):
                item.disabled = True
        if self.message:
            await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        """Disable buttons"""
        if self.message:
            await self.message.channel.send("This request has expired! ⌛")
            await self.disable_items()
