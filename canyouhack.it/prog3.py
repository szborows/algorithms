# -*- coding: utf-8 -*-

import os
import re
import requests
import sys
import time

URL = 'http://canyouhack.it/Content/Challenges/Programming/Prog3.php'
COOKIES = {
    'SMFCookie416': '***',
}
HTML_HEAD_FMT = """<html><head><style>body {{ line-height:5px; }} table {{ margin: 20px auto; }} td{{text-align:center;}} .path {{ background-color: yellow; }} .c00{{width:20px;height:20px;border:0px;}} .c01{{width:20px;height:20px;border:0px;border-right:1px solid black;}} .c10{{width:20px;height:20px;border:0px;border-bottom:1px solid black;}} .c11{{width:20px;height:20px;border:0px;border-bottom:1px solid black;border-right:1px solid black;}} strong{{color:red;}} .p{0} {{ background-color: green; }} .p{1} {{ background-color: red; }}</style></head><body><table style="border:2px solid black;" cellspacing="0" cellpadding="0">"""
HTML_TAIL = """</table></body></html>"""
WIDTH = 40

class BorderType(object):
    NONE, RIGHT, BOTTOM, BOTTOM_RIGHT = range(4)

class Node(object):
    def getBorderType(self, css):
        return {
            'c00': BorderType.NONE,
            'c01': BorderType.RIGHT,
            'c10': BorderType.BOTTOM,
            'c11': BorderType.BOTTOM_RIGHT}[css]

    def __init__(self, css):
        css = css.split()
        self.borders, self.id_ = self.getBorderType(css[0]), int(css[1][1:])

    def __str__(self):
        return '{0}:{1}'.format(self.id_, self.borders)

    __repr__ = __str__

class Graph(object):
    def __init__(self, am, src, dest):
        self.am, self.src, self.dest = am, src, dest
        self.nodes = len(am[0])

    def toHtml(self, filename, path):
        html = HTML_HEAD_FMT.format(self.src, self.dest)
        height, width = len(self.am), len(self.am[0])

        def ix(y, x):
            try: return y * WIDTH + x
            except ZeroDivisionError: return 0

        for y in range(WIDTH):
            html += '<tr>\n'
            for x in range(WIDTH):
                css = 'c00'
                if y < (WIDTH - 1) and not self.am[ix(y, x)][ix(y + 1, x)]:
                    css = 'c10'
                if x < (WIDTH - 1) and not self.am[ix(y, x)][ix(y, x + 1)]:
                    css = ['c01', 'c11'][css == 'c10']
                html += '\t<td class="{0} p{1} {2}">.</td>\n'.format(css, ix(y, x), ['', ' path'][ix(y, x) in path])
            html += '</tr>\n'

        html += HTML_TAIL
        with open(filename, 'w') as fp:
            fp.write(html)

    def neighbors(self, id_):
        neighbors = []
        for y, row in enumerate(self.am[id_]):
            if self.am[id_][y]:
                neighbors.append(y)
        return neighbors

class Solver(object):
    def getHtml(self):
        if False and os.path.isfile('local.html'):
            with open('local.html') as fp:
                html = fp.read()
        else:
            response = requests.get(URL, cookies=COOKIES)
            if 200 != response.status_code:
                raise RuntimeError('Got wrong HTTP code: {0}'.format(response.code))
            html = response.text
        return html

    def saveHtml(self, filename, html):
        with open(filename, 'w') as fp:
            fp.write(html)

    def sendResults(self, path):
        url = URL + '?Answer=' + str(len(path))
        response = requests.get(url, cookies=COOKIES)
        print url
        print response.text[:1000]

    def buildGraph(self, nodes, src, dest):
        height = len(nodes)
        width = len(nodes[0])
        am = [[False for x in xrange(width * height)] for x in xrange(width * height)]

        def ix(y, x):
            try: return y * width + x
            except ZeroDivisionError: return 0

        for y, row in enumerate(nodes):
            for x, element in enumerate(row):
                if y < height and nodes[y][x].borders not in [BorderType.BOTTOM, BorderType.BOTTOM_RIGHT]:
                    # Add bottom one
                    am[ix(y, x)][ix(y + 1, x)] = am[ix(y + 1, x)][ix(y, x)] = True
                if x < width and nodes[y][x].borders not in [BorderType.RIGHT, BorderType.BOTTOM_RIGHT]:
                    # Add right one
                    am[ix(y, x)][ix(y, x + 1)] = am[ix(y, x + 1)][ix(y, x)] = True
                if y > 0 and nodes[y - 1][x].borders not in [BorderType.BOTTOM, BorderType.BOTTOM_RIGHT]:
                    # Add above one
                    am[ix(y, x)][ix(y - 1, x)] = am[ix(y - 1, x)][ix(y, x)] = True
                if x > 0 and nodes[y][x - 1].borders not in [BorderType.RIGHT, BorderType.BOTTOM_RIGHT]:
                    # Add left one
                    am[ix(y, x)][ix(y, x - 1)] = am[ix(y, x - 1)][ix(y, x)] = True
        return Graph(am, src, dest)

    def solve(self):
        t1 = time.time()
        print 'Starting...'
        html = self.getHtml()
        print 'Got html...'
        self.saveHtml('last.html', html)

        source, destination = map(int, re.findall('\.p(\d+)', html))

        nodes = []
        for htmlRow in re.findall('<tr>(.*?)</tr>', html, re.DOTALL):
            nodes.append([Node(x) for x in re.findall('<td class="([a-zA-Z0-9\s]+)">.*?</td>', htmlRow)])

        graph = self.buildGraph(nodes, source, destination)

        class Color(object):
            WHITE, GRAY, BLACK = range(3)

        colors = [Color.WHITE] * graph.nodes
        distances = [sys.maxint] * graph.nodes
        predecessors = [-1] * graph.nodes

        colors[source] = Color.GRAY
        distances[source] = 0
        predecessors[source] = None

        q = [source]

        while len(q):
            u = q.pop()
            for neighbor in graph.neighbors(u):
                if Color.WHITE == colors[neighbor]:
                    colors[neighbor] = Color.GRAY
                    distances[neighbor] = distances[u] + 1
                    predecessors[neighbor] = u
                    q.append(neighbor)
            colors[u] = Color.BLACK

        p = [destination]
        while p[-1] != source:
            p.append(predecessors[p[-1]])

        graph.toHtml('internal.html', p)

        print 'Sending answer...'
        self.sendResults(p)
        t2 = time.time()

        print 'Time taken:', (t2 - t1)

if __name__ == "__main__":
    Solver().solve()

