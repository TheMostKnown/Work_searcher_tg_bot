from requests_html import HTMLSession
from bs4 import BeautifulSoup

# + добавить исключения
class Scrapper(object):

	def __init__(self):
		self.exp = 'no matter'
		self.spec = None
		self.page = 0
		self.cur_vac = 0
	#https://career.habr.com/vacancies?page=2&q=python&qid=4&type=all

	def make_url(self, page):
		params = []

		params.append(f'page={page}')

		if self.spec is not None:
			params.append(f'q={self.spec}')

		if self.exp == 'intern':
			params.append('qid=1')
		elif self.exp == 'junior':
			params.append('qid=3')
		elif self.exp == 'middle':
			params.append('qid=4')
		elif self.exp == 'senior':
			params.append('qid=5')
		elif self.exp == 'lead':
			params.append('qid=6')

		url = 'https://career.habr.com/vacancies?' + '&'.join(params)
		if url[-1] == '?':
			url += 'type=all'
		else:
			url += '&type=all'

		return url

	
	def page_iteration(self):
		self.page += 1

		url = self.make_url(self.page)
		session = HTMLSession()

		r = session.get(url)
		if r != 200:
			return []

		r.html.render()
		soup = BeautifulSoup(r.html.html, 'html.parser')
		vac_list = soup.find_all(class_='vacancy-card')

		return vac_list


	def search(self):
		if self.page == 0:
			vac_list = self.search_iteration()

		if self.cur_vac >= len(vac_list):
			vac_list = self.page_iteration()

		# Пустой список
		if not vac_list:
			return 'No more vaccancies with such parameters'

		company_name = vac_list[self.cur_vac].a.next.next.a.text
		vaccancy_name = vac_list[self.cur_vac].a.next.next.a.next.next.next.text

		link = 'https://career.habr.com' + vac_list[self.cur_vac].a['href']
		self.cur_vac += 1




def main():
	url = 'https://career.habr.com/vacancies?type=all'
	session = HTMLSession()

	r = session.get(url)

	r.html.render()  # this call executes the js in the page
	#response = requests.get(url)
	soup = BeautifulSoup(r.html.html, 'html.parser')
	vac_list = soup.find_all(class_='vacancy-card')
	print(vac_list[0].a.next.next.a.next.next.next.text)
	#print(vac_list[0].a['href'])

if __name__ == "__main__":
	main()
