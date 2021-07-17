import telebot
from secrets import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'set_exp', 'set_spec', 'search', 'erase'])
def get_command_response(message):
	if message.text == '/help':
		commands_describ = [
			'Here is the list of the commands:\n',
			'/help -- show this tab\n',
			'/search -- start job searching\n',
			'/set_exp -- set your job experiecne\n',
			'/set_spec -- set your specialization\n',
			'/erase -- erase already set peremeters'
		]
		bot.reply_to(message, ''.join(commands_describ))

	if message.text == '/search':
		bot.reply_to(message, 'searching')

	if message.text == '/set_exp':
		bot.reply_to(message, 'setting experience')

	if message.text == '/set_spec':
		bot.reply_to(message, 'setting specialization')

	if message.text == '/erase':
		bot.reply_to(message, 'erasing already set paremeters')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	bot.send_message(message.from_user.id, 'This is a work searcher bot\nType /help to see the commands')



bot.polling(none_stop=True)
