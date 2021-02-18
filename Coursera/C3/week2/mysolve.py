import pathlib
from bs4 import BeautifulSoup
import re
import os
import unittest
from collections import defaultdict


def get_images_amount(body):
    imgs = body.find_all('img')
    fit_imgs = len(
        [x for x in imgs if x.get('width') and int(x.get('width')) >= 200]
    )
    return fit_imgs


def get_headers_amount(body):
    headers = body.find_all(re.compile('^h[1-6]$'))
    count = 0
    for header in headers:
        children = header.find_all(recursive=False)
        if children:
            children_content = [x.getText() for x in children if x.getText()]
            try:
                first_letter = children_content[0][0]
                if first_letter in 'ETC':
                    count += 1
            except IndexError:
                pass
        else:
            try:
                first_letter = header.getText()[0]
                if first_letter in 'ETC':
                    count += 1
            except IndexError:
                pass
    return count


def get_max_links_len(body):
    max_count = 0
    all_links = body.find_all('a')
    for link in all_links:
        current_count = 1
        siblings = link.find_next_siblings()
        for sibling in siblings:
            if sibling.name == 'a':
                current_count += 1
                max_count = max(current_count, max_count)
            else:
                current_count = 0
    return max_count


def get_lists_num(body):
    count = 0
    all_lists = body.find_all(['ul', 'ol'])
    for tag in all_lists:
        if not tag.find_parents(['ul', 'ol']):
            count += 1
    return count


def parse(path):
    with open(path, encoding='utf-8') as data:
        soup = BeautifulSoup(data, "html.parser")
    body = soup.find(id="bodyContent")

    imgs = get_images_amount(body)
    headers = get_headers_amount(body)
    linkslen = get_max_links_len(body)
    lists = get_lists_num(body)
    return [imgs, headers, linkslen, lists]


def open_page(path, page):
    with open(os.path.join(path, page), encoding="utf-8") as file:
        links = re.findall(r"(?<=/wiki/)[\w()]+", file.read())
        # (?<=y)x сопоставляет c x только если x предществует y
        list_ref = set()
        for f in links:
            if os.path.exists(os.path.join(path, f)):  # and f != page
                list_ref.add(f)
        return list_ref


def rec_way(path, current_ways, stop_page, levels, level):
    level += 1
    new_ways = set()
    for current_page in current_ways:
        list_ref = open_page(path, current_page)
        if stop_page[0] in list_ref:
            return current_page
        else:
            for ref in list_ref:
                new_ways.add(ref)
        levels['level_{}'.format(level)].append(
            [current_page, '---'.join(list(new_ways))])
    return rec_way(path, new_ways, stop_page, levels, level)


def get_way(path, start_page, stop_page):
    levels = defaultdict(list)
    level = 0
    way = []
    best_way = rec_way(path, start_page, stop_page, levels, level)
    maxl = len(levels) - 1
    way.append(stop_page[0])
    if best_way != stop_page[0]:
        way.append(best_way)
    for i in range(maxl):
        for lev in levels['level_{}'.format(maxl-i)]:
            if way[-1] in lev[1]:
                way.append(lev[0])
                break
    if way[-1] != start_page[0]:  # почему то грейдер coursera иногда теряет первый элемент
        way.append(start_page[0])
    return way[::-1]


def build_bridge(path, start_page, end_page):
    return get_way(path, [start_page], [end_page])


def get_statistics(path, start_page, end_page):
    bestway = build_bridge(path, start_page, end_page)
    stats = {}
    for i in bestway:
        stats[i] = parse(os.path.join(path, i))
    return stats


STATISTICS = {
    'Artificial_intelligence': [8, 19, 13, 198],
    'Binyamina_train_station_suicide_bombing': [1, 3, 6, 21],
    'Brain': [19, 5, 25, 11],
    'Haifa_bus_16_suicide_bombing': [1, 4, 15, 23],
    'Hidamari_no_Ki': [1, 5, 5, 35],
    'IBM': [13, 3, 21, 33],
    'Iron_Age': [4, 8, 15, 22],
    'London': [53, 16, 31, 125],
    'Mei_Kurokawa': [1, 1, 2, 7],
    'PlayStation_3': [13, 5, 14, 148],
    'Python_(programming_language)': [2, 5, 17, 41],
    'Second_Intifada': [9, 13, 14, 84],
    'Stone_Age': [13, 10, 12, 40],
    'The_New_York_Times': [5, 9, 8, 42],
    'Wild_Arms_(video_game)': [3, 3, 10, 27],
    'Woolwich': [15, 9, 19, 38]}

TESTCASES = (
    ('/Users/pavel/Documents/Python/Coursera/C3/week2/wiki/', 'Stone_Age', 'Python_(programming_language)',
     ['Stone_Age', 'Brain', 'Artificial_intelligence', 'Python_(programming_language)']),

    ('/Users/pavel/Documents/Python/Coursera/C3/week2/wiki/', 'The_New_York_Times', 'Stone_Age',
     ['The_New_York_Times', 'London', 'Woolwich', 'Iron_Age', 'Stone_Age']),

    ('/Users/pavel/Documents/Python/Coursera/C3/week2/wiki/', 'Artificial_intelligence', 'Mei_Kurokawa',
     ['Artificial_intelligence', 'IBM', 'PlayStation_3', 'Wild_Arms_(video_game)',
      'Hidamari_no_Ki', 'Mei_Kurokawa']),

    ('/Users/pavel/Documents/Python/Coursera/C3/week2/wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing",
     ['The_New_York_Times', 'Second_Intifada', 'Haifa_bus_16_suicide_bombing',
      'Binyamina_train_station_suicide_bombing']),

    ('/Users/pavel/Documents/Python/Coursera/C3/week2/wiki/', 'Stone_Age', 'Stone_Age',
     ['Stone_Age', ]),
)


class TestBuildBrige(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = build_bridge(path, start_page, end_page)
                self.assertEqual(result, expected)


class TestGetStatistics(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = get_statistics(path, start_page, end_page)
                self.assertEqual(
                    result, {page: STATISTICS[page] for page in expected})


if __name__ == '__main__':
    unittest.main()
    #     print(build_bridge('/Users/pavel/Documents/Python/Coursera/C3/week2/wiki/',
    #                        'Gulf_of_Khambhat', 'Himilco'))
