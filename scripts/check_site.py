#!/usr/bin/env python3
"""Validate the delivered HTML without JavaScript or third-party dependencies."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.elements = []
        self.body_text = []
        self.schemas = []
        self.in_body = False
        self.schema = None
        self.ids = set()
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        self.elements.append((tag, attributes))
        if 'id' in attributes:
            assert attributes['id'] not in self.ids, f'Duplicate ID: {attributes["id"]}'
            self.ids.add(attributes['id'])
        if tag == 'body':
            self.in_body = True
        if tag == 'script' and attributes.get('type') == 'application/ld+json':
            self.schema = ''

    def handle_data(self, value):
        if self.in_body:
            self.body_text.append(value)
        if self.schema is not None:
            self.schema += value

    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
        if tag == 'script' and self.schema is not None:
            self.schemas.append(json.loads(self.schema))
            self.schema = None


def main():
    site = json.loads((ROOT / 'data/site.json').read_text())
    profile = json.loads((ROOT / 'data/profile.json').read_text())
    publications = json.loads((ROOT / 'data/publications.json').read_text())['publications']
    posts = json.loads((ROOT / 'data/blog.json').read_text())['blogPosts']
    base = site['url']
    canonicals = set()
    titles = set()
    descriptions = set()
    for filename, metadata in site['pages'].items():
        source = (ROOT / filename).read_text()
        assert '{{' not in source, f'{filename}: unresolved template'
        page = Page(source)
        assert sum(tag == 'h1' for tag, _ in page.elements) == 1, f'{filename}: expected one h1'
        assert sum(tag == 'main' for tag, _ in page.elements) == 1, f'{filename}: expected one main'
        canonical = [attrs['href'] for tag, attrs in page.elements if tag == 'link' and attrs.get('rel') == 'canonical']
        expected = base if filename == 'index.html' else urljoin(base, filename)
        assert canonical == [expected], f'{filename}: wrong canonical'
        canonicals.add(expected)
        descriptions_on_page = [attrs['content'] for tag, attrs in page.elements if tag == 'meta' and attrs.get('name') == 'description']
        assert descriptions_on_page == [metadata['description']]
        titles.add(metadata['title'])
        descriptions.add(metadata['description'])
        links = [attrs for tag, attrs in page.elements if tag == 'a' and 'nav-link' in attrs.get('class', '').split()]
        assert {attrs['href'] for attrs in links} == set(site['pages']), f'{filename}: missing navigation'
        assert [attrs['href'] for attrs in links if attrs.get('aria-current') == 'page'] == [filename]
        assert len(page.schemas) == 1, f'{filename}: missing structured data'
        graph = page.schemas[0]['@graph']
        person = next(item for item in graph if item['@type'] == 'Person')
        assert person['name'] == profile['personal']['name']
        if filename in ('index.html', 'aboutMe.html'):
            assert person['knowsAbout'] == profile['personal']['researchInterests']
            text = ' '.join(page.body_text)
            assert profile['personal']['title'] in text
            assert all(topic in text for topic in profile['personal']['researchInterests'])
        if filename in ('index.html', 'research.html'):
            text = ' '.join(page.body_text)
            assert all(pub['title'] in text for pub in publications), f'{filename}: publications require JavaScript'
        if filename == 'blog.html':
            assert all(post['title'] in ' '.join(page.body_text) for post in posts)
        for tag, attrs in page.elements:
            url = attrs.get('href') if tag in ('a', 'link') else attrs.get('src') if tag in ('img', 'script') else attrs.get('data') if tag == 'object' else None
            if url is None:
                continue
            assert url, f'{filename}: empty {tag} URL'
            parts = urlsplit(url)
            if not parts.scheme and not parts.netloc and parts.path:
                assert (ROOT / unquote(parts.path)).is_file(), f'{filename}: missing local target {url}'
        print(f'Validated {filename}: static content, links, headings, metadata, and JSON-LD')
    assert len(titles) == len(site['pages']) and len(descriptions) == len(site['pages'])
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    assert {loc.text for loc in sitemap.findall('.//{*}loc')} == canonicals
    robots = RobotFileParser()
    robots.parse((ROOT / 'robots.txt').read_text().splitlines())
    for agent in ('Googlebot', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ClaudeBot', 'PerplexityBot'):
        assert all(robots.can_fetch(agent, url) for url in canonicals)
        assert robots.can_fetch(agent, urljoin(base, 'assets/js/script.js'))
    assert robots.site_maps() == [urljoin(base, 'sitemap.xml')]
    verification_file = site.get('googleSiteVerificationFile')
    if verification_file:
        assert (ROOT / verification_file).read_bytes() == (ROOT / 'data' / verification_file).read_bytes()
        assert robots.can_fetch('Googlebot', urljoin(base, verification_file))
    print('Validated sitemap and search/AI crawler access.')


if __name__ == '__main__':
    main()
