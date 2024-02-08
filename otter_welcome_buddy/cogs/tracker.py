from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import CommandError
from discord.ext.commands import CommandNotFound
from discord.ext.commands import Context
from discord.ext.commands import MissingRequiredArgument

from otter_welcome_buddy.common.utils.discord_ import get_channel_by_id
from otter_welcome_buddy.common.utils.discord_ import message_handler
from otter_welcome_buddy.common.utils.types.common import DiscordChannelType
from otter_welcome_buddy.google_spreadsheet.approval_button import ButtonAddCompany
from otter_welcome_buddy.google_spreadsheet.sheet_manager import SheetManager
from otter_welcome_buddy.settings import SUDO_CHANNEL_ID


class Tracker(commands.Cog):
    """Tracker"""

    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.sheet_manager = SheetManager()

    @commands.group(
        brief="Tracker Bot Commands",
        invoke_without_command=True,
        pass_context=True,
    )
    async def process(self, ctx: Context) -> None:
        """Main command group for job application tracking."""
        await ctx.send_help(ctx.command)

    @commands.command()
    async def apply(self, ctx: commands.Context, company: str) -> None:
        """
        Record the application process for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Apply [company]

        Example:
        !Process Apply Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response = self.sheet_manager.insert_apply_data(discord_user, company)
        await ctx.send(message_handler(discord_user, company, insertion_response))

    @commands.command()
    async def online_assessment(self, ctx: commands.Context, company: str) -> None:
        """
        Record the Online Assessment (OA) stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process OA [company]

        Example:
        !Process OA Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response = self.sheet_manager.insert_oa_data(discord_user, company)

        await ctx.send(
            message_handler(
                discord_user,
                company,
                insertion_response,
                process_state="an Online Assessment",
            ),
        )

    @commands.command()
    async def phone(self, ctx: commands.Context, company: str) -> None:
        """
        Record the Phone Interview (Phone) stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Phone [company]

        Example:
        !Process Phone Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response = self.sheet_manager.insert_phone_data(discord_user, company)

        await ctx.send(
            message_handler(
                discord_user,
                company,
                insertion_response,
                process_state="a Phone Interview",
            ),
        )

    @commands.command()
    async def interview(self, ctx: commands.Context, company: str) -> None:
        """
        Record the Interview stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Interview [company]

        Example:
        !Process Interview Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response = self.sheet_manager.insert_interview_data(discord_user, company)

        await ctx.send(
            message_handler(discord_user, company, insertion_response, process_state="a Interview"),
        )

    @commands.command()
    async def final_round(self, ctx: commands.Context, company: str) -> None:
        """
        Record the Final Round stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Final_round [company]

        Example:
        !Process Final_round Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response = self.sheet_manager.insert_finalround_data(discord_user, company)

        await ctx.send(
            message_handler(
                discord_user,
                company,
                insertion_response,
                process_state="a Final Round Interview",
            ),
        )

    @commands.command()
    async def offer(self, ctx: commands.Context, company: str) -> None:
        """
        Record the Offer stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Offer [company]

        Example:
        !Process Offer Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response = self.sheet_manager.insert_offer_data(discord_user, company)

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
    async def rejection(self, ctx: commands.Context, company: str) -> None:
        """
        Record the Rejection stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Rejection [company]

        Example:
        !Process Rejection Google
        """
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] not in companies:
            await ctx.send(
                f"**{company}** is not registered, try to request to add this company first. 📋",
            )
            return

        discord_user: str = ctx.author.name
        insertion_response = self.sheet_manager.insert_rejection_data(discord_user, company)

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
    async def add(self, ctx: commands.Context, company: str) -> None:
        """
        Adds a company to the allowed companies list.

        Parameters:
        - *company (str): Variable-length argument representing the name of the company to be added.
        """
        channel_id: int = SUDO_CHANNEL_ID
        channel: DiscordChannelType | None = get_channel_by_id(self.bot, channel_id)

        discord_user: str = ctx.author.name
        companies: list = self.sheet_manager.get_allowed_companies()

        if [company] in companies:
            await ctx.send(
                f"**{company}** has been added before, please check our companies list. 📋",
            )
            return

        await ctx.send(
            f"Request for approval has been submitted to include **{company}**. ⌛",
        )
        if isinstance(channel, TextChannel):
            await channel.send(
                f"Incoming pending approval to include **{company}** in our companies portfolio. ⌛",
            )

        view = ButtonAddCompany(timeout=36000)
        if isinstance(channel, TextChannel):
            message = await channel.send(view=view)
        view.message = message
        await view.wait()

        if view.response:
            # update spread sheet
            response = self.sheet_manager.insert_company_data(company)

            if response:
                await ctx.send(
                    f"New company!, {company} has been added to our companies portfolio. 🤩",
                )
                await ctx.author.send(
                    f"{discord_user}, your request to include {company} has been approved ✅",
                )

        else:
            await ctx.author.send(
                f"Sorry, your request to include {company} has been rejected. ❌",
            )
            await ctx.send(
                f"Request to include {company} in our portfolio has been rejected. ❌",
            )

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
    await bot.add_cog(Tracker(bot))
