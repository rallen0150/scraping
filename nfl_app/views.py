from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super().get_context_data()
        if self.request.GET:
            url = 'http://www.nfl.com/players/search?category=name&filter={}&playerType=current'
            data = requests.get(url.format(self.request.GET.get('player_name')))
            # print(data.text)
            souper = BeautifulSoup(data.text, 'html.parser')
            table = souper.find('table', {'class': 'data-table1'})
            all_a_tags = table.findAll('a')[::2]#[43].get('href')
            # for x in all_a_tags:
            #     print(x.get('href'))
            player_link = []
            player_link=[(x.get('href'), x.get_text()) for x in all_a_tags]
                # player_link.append(x.get('href'))
                # player_link.append(x.get_text())

            print(player_link)
            context['player_name'] = player_link
            # for counter, tag in enumerate(all_a_tags):
            #     print(counter, tag)
            # print(data.text)
            # print(counter, player_link)
        return context

class PlayerView(TemplateView):
    template_name = 'player.html'

    def get_context_data(self, player_url):
        context = super().get_context_data()
        page = requests.get('http://www.nfl.com/' + player_url)
        souper = BeautifulSoup(page.text, 'html.parser')
        context['table'] = souper.find_all('table', {'class': 'data-table1'})[1].contents
        # for x in context['table']:
        #     x.replace('\n', '')
        print(context['table'])

        return context
