import telebot
from secrets import TOKEN
from scrapper import Scrapper

bot = telebot.TeleBot(TOKEN)
user = Scrapper()


@bot.message_handler(commands=['erase', 'help', 'set_exp', 'set_spec', 'search', 'start', 'user_info'])
def get_command_response(message):
	if message.text == '/help' or message.text == '/start':
		commands_describ = [
			'Here is the list of the commands:',
			'/erase -- erase already set peremeters',
			'/help -- show this tab',
			'/search -- start job searching',
			'/set_exp -- set your job experiecne',
			'/set_spec -- set your specialization',
			'/user_info -- show info about your experience and specialization'
		]
		bot.reply_to(message, '\n'.join(commands_describ))

	if message.text == '/search': #add page=0
		searcher(message)

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
		bot.register_next_step_handler(message, exp_chooser);

	if message.text == '/set_spec':
		bot.reply_to(message, 'Enter your specialization:')
		bot.register_next_step_handler(message, spec_chooser);

	if message.text == '/erase':
		user.exp = 'no matter'
		user.spec = None
		bot.reply_to(message, 'Your experience and specialization have been erased')

	if message.text == '/user_info':
		bot.reply_to(message, f'Your experience: {user.exp}\nYour specialization: {user.spec}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	bot.send_message(message.from_user.id, 'This is a work searcher bot\nType /help to see the commands')


def exp_chooser(message):
	exp = message.text.lower()
	if exp == 'intern' or exp == '0':
		user.exp = 'intern'
	elif exp == 'junior' or exp == '1':
		user.exp = 'junior'
	elif exp == 'middle' or exp == '2':
		user.exp = 'middle'
	elif exp == 'senior' or exp == '3':
		user.exp = 'senior'
	elif exp == 'lead' or exp == '4':
		user.exp = 'lead'
	else:
		user.exp = 'no matter'

	bot.send_message(message.from_user.id, f'Your experience set to {user.exp}')


def spec_chooser(message):
	user.spec = message.text
	bot.send_message(message.from_user.id, f'Your specialization set to {user.spec}')


def search_controller(message):
	if message.text.lower() == 'next':
		searcher(message)
	else:
		bot.send_message(message.from_user.id, 'stopped searching')
		user.page = 0

def searcher(message):
	ans =  user.search()
	if len(ans) == 1:
		bot.send_message(message.from_user.id, ans[0])
		user.page = 0
	else:
		company_name, vaccancy_name, salary, skills, link = ans
		listing = [
			f'{vaccancy_name}',
			f'company: {company_name}',
			f'salary: {salary}',
			f'skills needed: {skills}',
			f'link: {link}'
		]
		bot.send_message(message.from_user.id, '\n\n'.join(listing))
		bot.send_message(message.from_user.id, 'type "next" to continue searching')

		bot.register_next_step_handler(message, search_controller);



bot.polling(none_stop=True)
