from commands import getoutput
import requests
from lxml import html
from itertools import permutations
import marshal
from random import shuffle
from jinja2 import Template

def stopwords():
    return marshal.loads(open("stopwords.marshal").read())

def words_from_url(url):
    page = requests.get(url)
    doc = html.fromstring(page.text)
    words = reduce(lambda a,b: a+b, [ [w.strip() for w in w.lower().split() if w.isalnum()] for w in doc.xpath('//p/text()') ])

    return list(words)

def groups(words):
    words = list(set(words) - set(stopwords()))
    shuffle(words)
    groups = zip(*(iter(words),) * 2)

    return sorted(groups, key=lambda ary: len(''.join(ary)), reverse=False)

def query_domain(domains):
    for domain in domains.split():
        results = [result for result in getoutput('nslookup %s 8.8.8.8' % domain).split('\n') if result.startswith('** server can') and result.endswith('NXDOMAIN')]
        for result in results:
            return result

def domains(url):
    t = Template(open("domain.html").read())

    for g in groups(words_from_url(url)):
        x = query_domain(' '.join(['%s.com' % (w) for w in [''.join(w) for w in list(permutations(g))]]))
        if x:
            x = x.replace("** server can't find", "")
            x = x.replace(": NXDOMAIN", "")
            x = x.strip()

            yield t.render(domain=x)
        else:
            yield ''
