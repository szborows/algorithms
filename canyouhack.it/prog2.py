# -*- coding: utf-8 -*-

# In production it would be worth to study David Norvig approach.

import re
import requests

URL = 'http://canyouhack.it/Content/Challenges/Programming/Prog2.php'
COOKIES = {
    'PHPSESSID': '***',
    'SMFCookie416': '***',
}

solved = None

def solve(sstr):
    global solved

    def same_row(i, j):
        return (i/9 == j/9)

    def same_col(i, j):
        return (i-j) % 9 == 0

    def same_block(i, j):
        return (i/27 == j/27 and i%9/3 == j%9/3)

    i = sstr.find('0')
    if -1 == i:
        solved = sstr
        return solved

    excluded_numbers = set()
    for j in range(9 * 9):
        if same_row(i,j) or same_col(i,j) or same_block(i,j):
            excluded_numbers.add(sstr[j])
    for m in '123456789':
        if m not in excluded_numbers:
            sstr = sstr[:i] + m + sstr[i+1:]
            solve(sstr)

    return solved

if __name__ == "__main__":
    response = requests.get(URL, cookies=COOKIES)
    if 200 != response.status_code:
        raise RuntimeError('Got wrong HTTP code: {0}'.format(response.code))
    html = response.text
    s1 = re.sub('<[a-zA-Z0-9"\-/:;\t\s=]+>', '', html).replace('\n', '').replace(' ', '').strip()

    notSolved = re.sub('[A-Z]', '0', s1)
    print notSolved
    solved = solve(notSolved)
    print solved

    p = {x: y for x, y in zip(s1, solved) if re.match('[^0-9]', x)}
    response = requests.get(URL+'?Answer='+','.join([p[sorted(p)[i]] for i in range(len(p))]), cookies=COOKIES)
    print response.text

