import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pyzipper

logging.basicConfig(level=logging.INFO)

TOKEN = 'YOUR_API_TOKEN_HERE'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello! Send me a file to convert to Zip.')

def convert_to_zip(update, context):
    file_id = update.message.document.file_id
    file_info = context.bot.get_file(file_id)
    file_path = file_info.file_path

    # Download the file
    context.bot.download_file(file_path, 'temp_file')

    # Create a Zip file
    with pyzipper.AESZipFile('output.zip', 'w', compression=pyzipper.ZIP_LZMA) as zip_file:
        zip_file.write('temp_file')

    # Send the Zip file back to the user
    context.bot.send_document(chat_id=update.effective_chat.id, document=open('output.zip', 'rb'))

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.document, convert_to_zip))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
