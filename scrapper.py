from bs4 import BeautifulSoup
import dryscrape


"""
    class of handling user's data and processing with scrapper data on Habr.career

    Fields:
        exp - user's experiaence
        spec - ueser's specialization
        page - current user's page on the site
        cur_vac - serial number of vacancy on the page
        vac_list - list of all the vaccancies on the page
"""


class Scrapper(object):

    def __init__(self):
        self.exp = 'no matter'
        self.spec = None
        self.page = 0
        self.cur_vac = 0
        self.vac_list = []

    # function of constructing the proper url with GET request
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

    # function of turning over the page
    def page_iteration(self):
        self.page += 1
        self.cur_vac = 0

        url = self.make_url(self.page)
        session = dryscrape.Session()
        session.visit(url)

        response = session.body()

        soup = BeautifulSoup(response, 'html.parser')
        vac_list = soup.find_all(class_='vacancy-card')

        return vac_list

    # function of scrapping the needed data (company name, vaccancy name, salary, skills, link)
    def search(self):
        if self.page == 0:
            self.vac_list = self.page_iteration()

        if self.cur_vac >= len(self.vac_list):
            self.vac_list = self.page_iteration()

        # Empty list - case of no data
        if not self.vac_list:
            return ('No more vaccancies with such parameters',)

        vac_block = ''

        information = self.vac_list[self.cur_vac].a.next.next
        company_name = information.a.text
        vaccancy_name = information.find_all(class_='vacancy-card__title-link')[0].text

        salary = 'Not mentioned'
        if len(information.find_all(class_='basic-salary')) != 0:
            salary = information.find_all(class_='basic-salary')[0].text
        if salary == '':
            salary = 'Not mentioned'

        skills = ''
        mashed_skills = information.find_all(class_='vacancy-card__skills')[0]
        skill_list = mashed_skills.find_all(class_='preserve-line')
        for skill in skill_list:
            skills += skill.text

        link = 'https://career.habr.com' + self.vac_list[self.cur_vac].a['href']
        self.cur_vac += 1

        return(company_name, vaccancy_name, salary, skills, link)
