import requests
from datetime import datetime, timedelta


def get_trending_repositories(top_size, api_url):
    response_object = requests.get(api_url)
    json_dict = response_object.json()['items'][:top_size]
    repo_dict = {item['owner']['login']: item['name'] for item in json_dict}
    return repo_dict


def get_open_issues_count(top_size, api_url):
    response_object = requests.get(api_url)
    json_dict = response_object.json()['items'][:top_size]
    open_issues_count_dict = {item['owner']['login']:
                              item['open_issues_count']
                              for item in json_dict
                              }
    return open_issues_count_dict


def get_open_issues_urls(api_url, repo_dict, open_issues_count_dict):
    state = {'state': 'open'}
    issues_dict = {}
    for item in repo_dict:
        html_url_list = []
        response_object = requests.get(api_url.format(item, repo_dict[item]),
                                       params=state)
        if int(open_issues_count_dict[item]) == 0:
            html_url_list = []
        else:
            for i in range(0, int(open_issues_count_dict[item])):
                html_url_list.append(response_object.json()[i]['html_url'])
        issues_dict[item] = html_url_list
    return issues_dict


def get_necessary_date(days_count):
    time_now = datetime.now()
    time_delta = timedelta(days=days_count)
    necessary_date = datetime.strftime(time_now - time_delta, '%Y-%m-%d')
    return necessary_date


if __name__ == '__main__':
    top_size = 20
    days_count = 7
    date = get_necessary_date(days_count)
    repo_api_url = 'https://api.github.com/search/repositories?q=created:{0}\
                     &sort=stars'.format(date)
    issues_api_url = 'https://api.github.com/repos/{0}/{1}/issues'
    repo_dict = get_trending_repositories(top_size, repo_api_url)
    open_issues_count_dict = get_open_issues_count(top_size, repo_api_url)
    result = get_open_issues_urls(issues_api_url,
                                  repo_dict,
                                  open_issues_count_dict)
    for x, y, z in zip(sorted(result.keys()),
                       sorted(open_issues_count_dict.keys()),
                       repo_dict):
        print()
        print('Login: {0} Repository: {1} Open issues: {2}'.format(x,
              repo_dict[x], open_issues_count_dict[x]))
        if int(open_issues_count_dict[x]) != 0:
            for i, url in enumerate(result[x], 0):
                print('{0}: {1}'.format(i + 1, url))
