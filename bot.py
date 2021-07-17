import telebot
from secrets import TOKEN
from scrapper import Scrapper

bot = telebot.TeleBot(TOKEN)
user = Scrapper()


@bot.message_handler(commands=['erase', 'help', 'set_exp', 'set_spec', 'search'])
def get_command_response(message):
	if message.text == '/help':
		commands_describ = [
			'Here is the list of the commands:',
			'/erase -- erase already set peremeters',
			'/help -- show this tab',
			'/search -- start job searching',
			'/set_exp -- set your job experiecne',
			'/set_spec -- set your specialization'
		]
		bot.reply_to(message, '\n'.join(commands_describ))

	if message.text == '/search':
		bot.reply_to(message, 'searching')

	if message.text == '/set_exp':
		experiences = [
			'intern',
			'junior',
			'middle',
			'senior',
			'lead',
			'no matter'
		]
		bot.reply_to(message, f'Choose your experience:\n{", ".join(experiences)}')

	if message.text == '/set_spec':
		bot.reply_to(message, 'setting specialization')

	if message.text == '/erase':
		user.exp = 'no matter'
		user.specialization = None
		bot.reply_to(message, 'your experience and specialization have been erased')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	bot.send_message(message.from_user.id, 'This is a work searcher bot\nType /help to see the commands')



bot.polling(none_stop=True)
