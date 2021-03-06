from bs4 import BeautifulSoup
import requests

main_endpoint = 'https://www.worldometers.info/coronavirus/{}'
def get_infections():
  url = main_endpoint.format('#countries')
  HTML = requests.get(url).content
  soup = BeautifulSoup(HTML,'html.parser')
  table_children = soup.select_one('#main_table_countries > tbody:nth-child(2)').find_all("tr")
  infections = {}
  for child in table_children :
    for index,td in enumerate(child.find_all('td')):
      if(index == 0):
        country_key = td.getText().replace(' ','')
        infections[td.getText().replace(' ','')] = {
            'total_cases' : '',
            'new_cases' : '',
            'total_deaths' : '',
            'new_deaths' : '',
            'total_recovered' : '',
            'active_cases' : '',
            'critical_cases' : ''
        }
      elif (index == 1):
        infections[country_key]['total_cases'] = td.getText()
      elif (index == 2):
          infections[country_key]['new_cases'] = td.getText()
      elif (index == 3):
          infections[country_key]['total_deaths'] = td.getText()
      elif (index == 4):
          infections[country_key]['new_deaths'] = td.getText()
      elif (index == 5):
          infections[country_key]['total_recovered'] = td.getText()
      elif (index == 6):
          infections[country_key]['active_cases'] = td.getText()
      elif (index == 7):
          infections[country_key]['critical_cases'] = td.getText()
  return {
     'worldwide_cases' : {
        'total_cases' : {
          'infected' : soup.select('#maincounter-wrap > div > span')[0].getText(),
          'deaths' : soup.select('#maincounter-wrap > div > span')[1].getText(),
          'cured' : soup.select('#maincounter-wrap > div > span')[2].getText(),
          'active_cases' : {
            'mid_condition' : soup.select_one('div.number-table-main').getText(),
            'critical_condition' : soup.select_one('div.panel_front > div:nth-child(3) > div:nth-child(2) > span').getText()
          },
          'closed_cases' : {
            'recovered' : soup.select_one(' div.panel_front > div:nth-child(3) > div:nth-child(1) > span').getText(),
            'deaths' : soup.select_one('div.panel_front > div:nth-child(3) > div:nth-child(2) > span').getText()
          }
        }
      },
      'infections' : infections
    }
def get_infections_by_name(country_name=None):
  if(country_name == None):
    raise Exception('You must specify a country name')
  response = get_infections()
  try:
    return {
      country_name : response['infections'][country_name]
      }
  except Exception:
    raise Exception('Seems like you entered a wrong country name')
def get_infected_countries():
  data = get_infections()
  countries = []
  for country in data['infections']:
    countries.append(country)
  return countries