from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super().get_context_data()
        if self.request.GET:
            url = 'http://www.nfl.com/players/search?category=name&filter={}&playerType={}'
            data = requests.get(url.format(self.request.GET.get('player_name'), self.request.GET.get('playerType')))
            # print(data.text)
            souper = BeautifulSoup(data.text, 'html.parser')
            if self.request.GET.get('playerType') == 'current':
                table = souper.find('table', {'class': 'data-table1'})
                all_a_tags = table.findAll('a')[::2]
                # player_link = []
                player_link=[(x.get('href'), x.get_text()) for x in all_a_tags]
                # print(player_link)
                context['player_name'] = player_link
                return context
            elif self.request.GET.get('playerType') == 'historical':
                table = souper.find('table', {'class': 'data-table1'})
                all_a_tags = table.find_all('a')
                player_link = [(x.get('href')+'?historical=True', x.get_text()) for x in all_a_tags]
                context['player_name'] = player_link
                return context

class PlayerView(TemplateView):
    template_name = 'player.html'

    def get_context_data(self, player_url):
        context = super().get_context_data()
        page = requests.get('http://www.nfl.com/' + player_url)
        souper = BeautifulSoup(page.text, 'html.parser')
        # context['table'] = souper.find_all('table', {'class': 'data-table1'})[1].contents
        # print(context['table'])
        # return context
        if self.request.GET.get('historical') == "True":
            context['table'] = souper.findAll('table', {'class': 'data-table1'})[0].contents
            return context
        else:
            context['table'] = souper.findAll('table', {'class': 'data-table1'})[1].contents
            return context
