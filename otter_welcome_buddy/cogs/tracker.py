import discord
from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import CommandError
from discord.ext.commands import CommandNotFound
from discord.ext.commands import Context
from discord.ext.commands import MissingRequiredArgument

from otter_welcome_buddy.common.constants import OTTER_ADMIN
from otter_welcome_buddy.common.constants import OTTER_MODERATOR
from otter_welcome_buddy.common.utils.discord_ import get_channel_by_id
from otter_welcome_buddy.common.utils.discord_ import message_handler
from otter_welcome_buddy.common.utils.types.common import DiscordChannelType
from otter_welcome_buddy.formatters import messages
from otter_welcome_buddy.google_spreadsheet.sheet_manager import SheetManager
from otter_welcome_buddy.settings import ADMIN_ROLE_ID
from otter_welcome_buddy.settings import COLLABORATOR_ROLE_ID
from otter_welcome_buddy.settings import SUDO_CHANNEL_ID
from otter_welcome_buddy.settings import TRACKER_CHANNEL_ID


class Tracker(commands.Cog):
    """Tracker"""

    def __init__(self, bot: Bot, messages_dependency: type[messages.Formatter]):
        self.bot: Bot = bot
        self.messages_formatter: type[messages.Formatter] = messages_dependency
        self.sheet_manager = SheetManager()

    @commands.group(
        brief="Tracker Bot Commands",
        invoke_without_command=True,
    )
    async def process(self, ctx: Context) -> None:
        """Main command group for job application tracking"""
        await ctx.send_help(ctx.command)

    @commands.command()
    async def apply(self, ctx: Context, company: str) -> None:
        """
        Record the application process for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !process apply [company]

        Example:
        !process apply Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response: str = self.sheet_manager.insert_apply_data(discord_user, company)
        await ctx.send(message_handler(discord_user, company, insertion_response))

    @commands.command()
    async def online_assessment(self, ctx: Context, company: str) -> None:
        """
        Record the Online Assessment (OA) stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !process online_assessment [company]

        Example:
        !process online_assessment Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response: str = self.sheet_manager.insert_oa_data(discord_user, company)

        await ctx.send(
            message_handler(
                discord_user,
                company,
                insertion_response,
                process_state="an Online Assessment",
            ),
        )

    @commands.command()
    async def phone(self, ctx: Context, company: str) -> None:
        """
        Record the Phone Interview (Phone) stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !process phone [company]

        Example:
        !process phone Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response: str = self.sheet_manager.insert_phone_data(discord_user, company)

        await ctx.send(
            message_handler(
                discord_user,
                company,
                insertion_response,
                process_state="a Phone Interview",
            ),
        )

    @commands.command()
    async def interview(self, ctx: Context, company: str) -> None:
        """
        Record the Interview stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !process interview [company]

        Example:
        !process interview Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response: str = self.sheet_manager.insert_interview_data(discord_user, company)

        await ctx.send(
            message_handler(discord_user, company, insertion_response, process_state="a Interview"),
        )

    @commands.command()
    async def final_round(self, ctx: Context, company: str) -> None:
        """
        Record the Final Round stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !process final_round [company]

        Example:
        !process final_round Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response: str = self.sheet_manager.insert_finalround_data(discord_user, company)

        await ctx.send(
            message_handler(
                discord_user,
                company,
                insertion_response,
                process_state="a Final Round Interview",
            ),
        )

    @commands.command()
    async def offer(self, ctx: Context, company: str) -> None:
        """
        Record the Offer stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !process offer [company]

        Example:
        !process offer Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response: str = self.sheet_manager.insert_offer_data(discord_user, company)

        await ctx.send(
            message_handler(
                discord_user,
                company,
                insertion_response,
                process_state="an Offer",
                from_offer="1",
            ),
        )

    @commands.command()
    async def rejection(self, ctx: Context, company: str) -> None:
        """
        Record the Rejection stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !process rejection [company]

        Example:
        !process rejection Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response: str = self.sheet_manager.insert_rejection_data(discord_user, company)

        await ctx.send(
            message_handler(
                discord_user,
                company,
                insertion_response,
                process_state="a Rejection",
                from_offer="0",
            ),
        )

    @commands.command()
    async def add(self, ctx: Context, company: str) -> None:
        """
        Adds a company to the allowed companies list.

        Parameters:
        - *company (str): Variable-length argument representing the name of the company to be added.
        """
        channel_id: int = SUDO_CHANNEL_ID
        channel: DiscordChannelType | None = get_channel_by_id(self.bot, channel_id)
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] in companies:
            await ctx.send(
                f"**{company}** has been added before, please check our companies list. 📋",
            )
            return

        adm = ADMIN_ROLE_ID
        col = COLLABORATOR_ROLE_ID
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="Tracker Approval",
            description=f"<@&{adm}> <@&{col}> {self.messages_formatter.approval_message(company)}",
        )

        if isinstance(channel, TextChannel):
            await channel.send(embed=embed)

        await ctx.send(
            f"Request for approval has been submitted to include **{company}**. ⌛",
        )

    @commands.group(
        brief="Request for approval Commands",
        invoke_without_command=True,
    )
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def request(self, ctx: Context) -> None:
        """Main command group for companies approval"""
        await ctx.send_help(ctx.command)

    @commands.command()
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def accept(self, ctx: Context, company: str) -> None:
        """
        Includes a company in the companies portfolio

        Parameters:
        - *company (str): Variable-length argument representing the name of the company to be added.
        """
        channel_id: int = TRACKER_CHANNEL_ID
        channel: DiscordChannelType | None = get_channel_by_id(self.bot, channel_id)
        response: bool = self.sheet_manager.insert_company_data(company)

        embed = discord.Embed(
            colour=discord.Colour.green(),
            title="Company approved",
            description=f"{self.messages_formatter.company_approved_message(company)}",
        )

        if response:
            if isinstance(channel, TextChannel):
                await channel.send(embed=embed)
            await ctx.send(f"**{company}** accepted successfully. ✅")

    @commands.command()
    @commands.has_any_role(OTTER_ADMIN, OTTER_MODERATOR)
    async def reject(self, ctx: Context, company: str) -> None:
        """
        Rejects company to be included in the companies portfolio

        Parameters:
        - *company (str): Variable-length argument representing the name of the company to be added.
        """
        channel_id: int = TRACKER_CHANNEL_ID
        channel: DiscordChannelType | None = get_channel_by_id(self.bot, channel_id)

        embed = discord.Embed(
            colour=discord.Colour.red(),
            title="Company rejected",
            description=f"{self.messages_formatter.company_rejected_message(company)}",
        )

        if isinstance(channel, TextChannel):
            await channel.send(embed=embed)
        await ctx.send(f"**{company}** rejected successfully. ✅")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError) -> None:
        """
        Handle errors occurring during command execution.

        Parameters:
        - ctx (Context): The command context.
        - error (CommandError): The error that occurred.
        """
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Error: Missing parameter. ⚙️",
            )

        elif isinstance(error, CommandNotFound):
            await ctx.send(
                "Command not found. Please check the command syntax and try again. 📋",
            )

        else:
            # Handle other errors or log them as needed
            print(f"An error occurred: {type(error).__name__}: {str(error)}")


async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(Tracker(bot, messages.Formatter))
