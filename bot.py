#!/usr/bin/env python
import html
import json
import logging
import traceback
from time import time

import telegram
from numerize import numerize
from telegram import ParseMode, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from telegram.utils.helpers import escape_markdown

import constants
import repo
from models.api_response import APIResponse
from models.cet_balance import CETBalance
from models.cet_statistics import CETStatistics
# Enable logging
from models.chain import Chain
from models.token_by_address import TokenByAddress
from models.token_details import Token
from models.token_list import TokenList
from models.transaction import Transaction
from models.transaction_list import Transactions
from util import format_float

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    text = f'''
Hi {user.first_name}!

Welcome to coinex smart chain bot 🤖
You can interact with the coinex smart chain explorer with this bot.

Get list of available commands by sending /help
        '''
    update.message.reply_text(text)


def api_error_handler(update: Update, response: APIResponse):
    if response.code != 0:
        update.message.reply_text(response.message)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        """
<b>Here are the list of commands</b>

/start - Check status of the bot
/cet - Statistics of CET
/chain - Statistics of CSC
/tokens - Lists top 10 CRC20 tokens
/token &lt;contract&gt; - Check the details of a token
/tx - Check the details of a transaction
/txlist - Shows the latest transactions
/cet_balance &lt;address&gt; - Get the CET balance of an address
/balances  &lt;address&gt;  - Get the tokens by address
/holders - Number of CET holders
/explorer - Links of the CSC Explorers
/dapps - Links of dApps in the CSC Ecosystem
/info - Information about the bot
/help - How to use the bot
""", parse_mode=ParseMode.HTML)


def statistics_cet(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    text = build_cet_statistics_text(update)
    keyboard = [[InlineKeyboardButton("Refresh 🔃", callback_data='update_statistics_cet')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


def build_cet_statistics_text(update):
    response = repo.api_request(repo.STATISTICS_CET)
    api_error_handler(update, response)

    data = CETStatistics.from_dict(response.data)
    percent = float(data.percent) * 100
    if percent > 0:
        percent_text = "+" + format_float(percent)
    else:
        percent_text = format_float(percent)

    return f"""
<b>CET Statistics</b>

Price:  ${"{:0,.2f}".format(float(format_float(data.price)))}

Price Change(24H): {percent_text}%

Circulating market value: ${"{:0,.2f}".format(float(data.liquidity))}
"""


def cmd_statistics_chain(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    text = build_statistics_chain_text(update)
    keyboard = [[InlineKeyboardButton("Refresh 🔃", callback_data='update_statistics_chain')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


def build_statistics_chain_text(update):
    response = repo.api_request(repo.STATISTICS_CHAIN)
    api_error_handler(update, response)
    chain = Chain.from_dict(response.data)

    return f'''
<b>CSC Statistics</b>
 
Latest Block Height: {chain.latest_height}

Avg. block time (Latest 5000 blocks): {chain.average_time}s

Active Validators: {chain.active}

Total Staked Assets:  {"{:0,.2f}".format(float(chain.staking))}

Total Tx amount: {numerize.numerize(chain.tx_count)}

TPS: {"{:0,.3f}".format(float(chain.tx_per_second))}
'''


def call_back_handler(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    text = ""
    if query.data == "update_statistics_chain":
        text = build_statistics_chain_text(update)
    elif query.data == "update_statistics_cet":
        text = build_cet_statistics_text(update)
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=query.message.reply_markup)


def tokens(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    response = repo.api_request(repo.TOKENS)
    if response.code != 0:
        update.message.reply_text(response.message)
    else:
        token_list = list()
        for data in response.data["records"]:
            token_list.append(TokenList.from_dict(data))

        text = "<b>Top 10 tokens in CSC </b>\n\n"
        for index, token in enumerate(token_list):
            text += f'<b>{index + 1}.Name :</b> {token.name} {" ⭐" if token.star else ""}\n' \
                    f'<b>Symbol:</b> {token.symbol}\n' \
                    f'<b>No. of Holders : </b> {token.holder_count} \n' \
                    f'<b>Total Supply :</b> {format_float(token.total_supply)}\n' \
                    f'<b>Tx Count :</b> {token.tx_count}\n' \
                    f'<b>Contract Address :</b> \n <code> {token.contract} </code>\n' \
                    f'\n\n'
        update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def token_details(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    message_array = update.message.text.strip().split(" ")
    if len(message_array) == 2:
        token_address = str(message_array[1])
        response = repo.api_request(repo.TOKEN.format(token_address))
        if response.code != 0:
            update.message.reply_text(response.message)
        else:
            token = Token.from_dict(response.data)
            text = f"""
<b>Token info</b>

Symbol : {token.symbol}

Name : {token.name}

Total supply : {format_float(token.total_supply)} {token.symbol}
 
Holders : {token.holder_count}
 
Tx amount : {token.tx_count}

Verification Status : {"Verified ✅" if token.verify else "UnVerified"}

Token Type : {"CRC20" if token.token_type == 1 else "CRC721"}

<b>More Info</b>

Creator Address : <code> {token.create_info.creator} </code>

Created at : {telegram.utils.helpers.from_timestamp(token.create_info.timestamp)}

Contract address : \n <code>{token.contract}</code>
"""
            update.message.reply_text(text, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
            "Use /token <token address> to get details about a token")


def cet_balance(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    message_array = update.message.text.strip().split(" ")
    if len(message_array) == 2:
        address = str(message_array[1])
        response = repo.api_request(repo.ADDRESS_BALANCE.format(address))
        if response.code != 0:
            update.message.reply_text(response.message)
        else:
            cet_bal = CETBalance.from_dict(response.data)

            update.message.reply_text(
                f"""
<b>Address :</b>  \n{cet_bal.address.address}

<b>Balance :</b>  {format_float(cet_bal.balance)}
    """, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("Use /cet_balance <address> to get CET balance of an address")


def balances(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    message_array = update.message.text.strip().split(" ")
    if len(message_array) == 2:
        address = str(message_array[1])
        response = repo.api_request(repo.ADDRESS_TOKENS_BALANCE.format(address))
        if response.code != 0:
            update.message.reply_text(response.message)
        else:
            balance_list = TokenByAddress.from_dict(response.data)
            message = ""

            for crc20 in balance_list.crc20:
                message += f"""
<b>Name :</b> {crc20.token_info.name}
<b>Symbol :</b> {crc20.token_info.symbol}
<b>Address :</b> <code> \n{crc20.token_info.contract} <code>
<b>Balance :</b>  {format_float(crc20.balance)}
\n
   """
            if message == "":
                message = "This address does not have any tokens"
            update.message.reply_text(message, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
            "Use /balances <address> to get the token balances of an address")


def transaction_details(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    message_array = update.message.text.strip().split(" ")
    if len(message_array) == 2:
        tx_hash = str(message_array[1])
        response = repo.api_request(repo.TRANSACTION.format(tx_hash))
        if response.code != 0:
            update.message.reply_text(response.message)
        else:
            transaction = Transaction.from_dict(response.data)

            text = f"""
<b>Transaction Info</b>

Tx Hash: <code>{transaction.tx_hash}</code>

Status: {get_transaction_status_type(transaction.status)}

Block: {transaction.height} 
 
Confirmed at: {telegram.utils.helpers.from_timestamp(transaction.timestamp)} 
 
From: <code>{transaction.from_address.address}</code> <b>{transaction.from_address.alias}</b>

To:  <i>{get_address_type(transaction.to_address.type)}</i> - <code>{transaction.to_address.address}</code> <b>{transaction.to_address.alias}</b>

Amount: {transaction.value} <b>CET</b> | <b>$</b>{transaction.value_usd} 

Tx fee: {transaction.fee} <b>CET</b> | <b>$</b>{transaction.fee_usd} 

Gas Price: {transaction.gas_price} 

Gas Limit: {transaction.gas_limit}

Gas Used:  {transaction.gas_used}

Nonce:  {transaction.nonce} 

Index: {transaction.index}

Data:  <code>{transaction.data}</code>

"""
            keyboard = [
                [InlineKeyboardButton("View on Explorer", url=f'https://www.coinex.net/tx/{transaction.tx_hash}')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

    else:
        update.message.reply_text(
            "Use /tx <tx hash> to get details for a transaction")


def get_address_type(address_type: int):
    if address_type == 0:
        return "Common"
    elif address_type == 1:
        return "Validator"
    elif address_type == 2:
        return "Contract"
    elif address_type == 3:
        return "CRC20"
    elif address_type == 4:
        return "CRC721"
    elif address_type == 127:
        return "System contract"


def get_transaction_status_type(status_code: int):
    if status_code == 0:
        return "Failure"
    elif status_code == 1:
        return "Success"
    elif status_code == 2:
        return "Pending"
    elif status_code == 3:
        return "Replaced"


def transactions(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    response = repo.api_request(repo.TRANSACTIONS.format(int(time()) - 120, int(time())))
    if response.code != 0:
        update.message.reply_text(response.message)
    else:
        if len(response.data) == 0:
            update.message.reply_text("<b>No transactions have been made at the last 2 minutes</b>\n\n",
                                      parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        else:
            tx_list = list()
            for data in response.data:
                tx_list.append(Transactions.from_dict(data))

            text = "<b>LATEST TRANSACTIONS</b>\n\n"
            for index, transaction in enumerate(tx_list):
                text += f'Tx Hash: <code>{transaction.tx_hash}</code>\n' \
                        f'Method: {transaction.method}\n' \
                        f'Block Height:   {transaction.height} \n' \
                        f'Time: {telegram.utils.helpers.from_timestamp(transaction.timestamp)} \n' \
                        f'From: <code> {transaction.from_address.address} </code>\n' \
                        f'To: <code>{transaction.to_address.address}</code>\n' \
                        f'Amount (CET): {transaction.amount}\n' \
                        f'Tx Fee (CET): {transaction.fee}\n' \
                        f'\n\n'
            update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def cet_holders(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    response = repo.api_request(repo.STATISTICS_CET_HOLDERS)
    data = response.data
    if response.code != 0:
        update.message.reply_text(response.message)
    else:
        update.message.reply_text("Total CET holders 🔥 => {} ".format(data["total"]))


def info(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""
<b>Telegram bot to interact with CoinEx Smart Chain functions</b>

<b>Developed by @zinary</b>
    """, parse_mode=ParseMode.HTML)


def donate(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    update.message.reply_text(
        f"""
<i>Donate to the developer ✨</i>
CET / BTC / ETH / BNB / USDT

<code>{constants.DEV_WALLET_ADDRESS}</code>
""", parse_mode=ParseMode.HTML)


def explorer(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    text = """
<b>✅ Mainnet</b>
https://www.coinex.net/

<b>✅ Testnet</b> 
https://testnet.coinex.net/
"""
    update.message.reply_text(text, disable_web_page_preview=True, parse_mode=ParseMode.HTML)


def show_typing(update: Update, context: CallbackContext):
    context.bot.send_chat_action(
        chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)


def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    # Finally, send the message
    context.bot.send_message(chat_id=constants.DEV_CHAT_ID, text=message, parse_mode=ParseMode.HTML)


def dapps(update: Update, context: CallbackContext) -> None:
    show_typing(update, context)
    text = ""
    with open('db/db.json', 'r') as db:
        data = json.load(db)
        dapps = data["dapps"]

        for index, item in enumerate(dapps):
            text += f"""
<b>✅ {item["name"]}</b>
{item["description"]}
{item["url"]}
"""

    update.message.reply_text(text, disable_web_page_preview=True, parse_mode=ParseMode.HTML)


def message_handler(update):
    text = update.message.text
    update.message.reply_text(text + " is not a valid command")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(constants.BOT_TOKEN, use_context=True, workers=20)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_error_handler(error_handler)
    # on different commands - answer in Telegram
    # dispatcher.add_handler(MessageHandler(BaseFilter(Filters.text), message_handler))
    dispatcher.add_handler(CallbackQueryHandler(call_back_handler))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("cet", statistics_cet))
    dispatcher.add_handler(CommandHandler("chain", cmd_statistics_chain))
    dispatcher.add_handler(CommandHandler("tokens", tokens))
    dispatcher.add_handler(CommandHandler("token", token_details))
    dispatcher.add_handler(CommandHandler("txlist", transactions))
    dispatcher.add_handler(CommandHandler("tx", transaction_details))
    dispatcher.add_handler(CommandHandler("cet_balance", cet_balance))
    dispatcher.add_handler(CommandHandler("balances", balances))
    dispatcher.add_handler(CommandHandler("holders", cet_holders))
    dispatcher.add_handler(CommandHandler("info", info))
    # dispatcher.add_handler(CommandHandler("donate", donate))
    dispatcher.add_handler(CommandHandler("explorer", explorer))
    dispatcher.add_handler(CommandHandler("dapps", dapps))

    # Start the Bot
    updater.start_polling(drop_pending_updates=True)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
