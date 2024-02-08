import logging

import discord
from discord.ext.commands import Bot
from discord.ext.commands import Context
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from otter_welcome_buddy.common.utils.types.common import DiscordChannelType
from otter_welcome_buddy.formatters.messages import Formatter

logger = logging.getLogger(__name__)


async def send_plain_message(ctx: Context, message: str) -> None:
    """Send a message as embed, this allows to use more markdown features"""
    try:
        await ctx.send(embed=discord.Embed(description=message, color=discord.Color.teal()))
    except discord.Forbidden:
        logger.exception("Not enough permissions to send the message")
    except discord.HTTPException:
        logger.exception("Sending the message failed")


def get_channel_by_id(bot: Bot, channel_id: int) -> DiscordChannelType | None:
    """
    Function to get the a channel by ID
    """
    return bot.get_channel(channel_id) if channel_id else None


def insert_company(company: str, creds: Credentials, sheet_id: str) -> bool:
    """
    Helper funcition to insert data into companies Google spreadsheet
    """
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        new_data = [[company]]
        body = {"values": new_data}
        sheet.values().append(
            spreadsheetId=sheet_id,
            range="Allowed Companies",
            valueInputOption="RAW",
            body=body,
        ).execute()

        return True

    except HttpError:
        return False


def message_handler(
    user: str,
    company: str,
    insertion_response: str,
    process_state: str = "",
    from_offer: str = "",
) -> str:
    """
    Helper function to hadle Bot messages
    """

    # '0': 'user' already applied to a certain 'company'
    if insertion_response == "0":
        return Formatter.already_applied_message(user, company)

    # '1': 'user' has an advanced process with 'company'
    if insertion_response == "1":
        return Formatter.advanced_process_message(user, company, process_state)

    # '2': 'user' has already received a desicion from 'company'
    if insertion_response == "2":
        return Formatter.final_desicion_message(user, company)

    # '3': 'user' moved forwrad in the process with 'company'
    if insertion_response == "3":
        return Formatter.successful_insertion_message(
            user,
            company,
            from_offer,
            process_state,
        )

    # '4': 'user' applied successfully to a certain 'company'
    if insertion_response == "4":
        return Formatter.apply_message(user, company)

    # '5': 'user' attempted to use a command before 'apply'
    return Formatter.proper_procedure_message(user, company)
