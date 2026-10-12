#!/usr/bin/env python3
"""Generate crawler-readable pages using only the Python standard library."""
import argparse
import html
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"\{\{([a-zA-Z0-9_-]+)\}\}")
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")


def read_json(name):
    return json.loads((ROOT / 'data' / f'{name}.json').read_text())


def escape(value):
    return html.escape(str(value), quote=True)


def safe_url(value):
    if value and (urlsplit(value).scheme not in ('', 'https', 'http', 'mailto') or value.startswith('//')):
        raise ValueError(f'Unsupported content URL: {value!r}')
    return escape(value)


def render(source, values):
    return TOKEN.sub(lambda match: values[match[1]], source)


def month_year(value):
    year, month, _ = value.split('-')
    return f'{MONTHS[int(month) - 1]} {year}'


def card(title, detail='', url=''):
    content = f'<div class="box11"><h3 class="bio">{title}</h3>{detail}</div>'
    if url:
        content = f'<a href="{safe_url(url)}" style="text-decoration: none;">{content}</a>'
    return content


def generate():
    profile = read_json('profile')
    personal = profile['personal']
    publications = read_json('publications')['publications']
    blog = read_json('blog')['blogPosts']
    site = read_json('site')
    base = site['url']
    if not base.startswith('https://') or not base.endswith('/'):
        raise ValueError('data/site.json url must be an absolute HTTPS URL ending in /')
    name = escape(personal['name'])
    interests = ', '.join(f'<span class="highlight-text">{escape(interest)}</span>' for interest in personal['researchInterests'])
    about = f'''Hi there! Welcome to {escape(personal['name'].split()[0])}'s homepage.<br><br>
I am a {escape(personal['title'])} in the {escape(personal['department'])} at <span class="highlight-text">{escape(personal['university'])}</span>, advised by {escape(personal['advisor'])}. I began my doctoral studies in {escape(personal['startDate'])}.<br><br>
My research interests are focused on {interests}, and their intersections.<br><br>
I serve as a reviewer for {escape(personal['reviewer'])}.<br>'''
    values = {
        'name': name,
        'contact': f'{escape(personal["email"])}<br><span class="university-name">{escape(personal["university"])}</span><br>{escape(personal["location"])}',
        'profile-image': safe_url(personal['profileImage']),
        'about': about,
        'year': profile['lastUpdated'][:4],
        'last-update': month_year(profile['lastUpdated']),
        'education-items': '\n'.join(card(
            f'{escape(edu["degree"])}, <span class="university-name">{escape(edu["institution"])}</span>',
            f'<div class="bio1">{escape(edu["location"])}<br>{escape(edu["period"])}</div>'
        ) for edu in profile['education']),
        'publication-items': '\n'.join(card(
            escape(pub['title']),
            f'<div class="bio1">{escape(pub["authors"]).replace(name, f"<strong>{name}</strong>")}<br><i>{escape(pub["venue"])}</i></div>',
            pub['url']
        ) for pub in publications),
        'blog-items': '\n'.join(card(
            escape(post['title']),
            f'<div class="post-date">{escape(month_year(post["date"]))}</div>' if post.get('date') else '',
            post['url']
        ) for post in blog),
    }
    for social in profile['socialMedia']:
        key = 'social-' + social['platform'].lower().replace(' ', '-')
        values[key] = safe_url(social['url'])
    person_id = base + '#person'
    person = {
        '@type': 'Person', '@id': person_id, 'name': personal['name'],
        'url': base, 'jobTitle': personal['title'],
        'description': site['pages']['index.html']['description'],
        'image': urljoin(base, personal['profileImage']),
        'affiliation': {'@type': 'CollegeOrUniversity', 'name': personal['university']},
        'knowsAbout': personal['researchInterests'],
        'sameAs': [s['url'] for s in profile['socialMedia'] if s['url'].startswith('https://')],
    }
    outputs = {}
    for page, info in site['pages'].items():
        canonical = base if page == 'index.html' else urljoin(base, page)
        is_profile = page in ('index.html', 'aboutMe.html')
        page_schema = {
            '@type': 'ProfilePage' if is_profile else 'WebPage',
            '@id': canonical + '#webpage', 'url': canonical,
            'name': info['title'], 'description': info['description'], 'inLanguage': 'en',
            'isPartOf': {'@id': base + '#website'},
            'mainEntity' if is_profile else 'about': {'@id': person_id},
        }
        graph = {
            '@context': 'https://schema.org',
            '@graph': [
                {'@type': 'WebSite', '@id': base + '#website', 'url': base, 'name': personal['name'], 'author': {'@id': person_id}},
                person if is_profile else {'@type': 'Person', '@id': person_id, 'name': personal['name'], 'url': base},
                page_schema,
            ],
        }
        # Prevent content values from closing the JSON-LD script element.
        structured_data = json.dumps(graph, ensure_ascii=False, indent=2).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
        metadata = render((ROOT / 'includes' / 'head.html').read_text(), {
            'title': escape(info['title']), 'description': escape(info['description']),
            'canonical': escape(canonical), 'name': name,
            'image': escape(urljoin(base, personal['profileImage'])),
            'structured-data': structured_data,
            'verification': f'<meta name="google-site-verification" content="{escape(site["googleSiteVerification"])}">' if site.get('googleSiteVerification') else '',
        })
        components = {}
        for component in ('nav', 'profile-header', 'about-summary', 'education', 'publications', 'social-links', 'blog-posts', 'footer'):
            heading = 'h1' if (component, page) in (('about-summary', 'aboutMe.html'), ('blog-posts', 'blog.html')) else 'h2'
            content = render((ROOT / 'includes' / f'{component}.html').read_text(), {**values, 'heading': heading})
            if component == 'nav':
                content = content.replace(f'class="nav-link" href="{page}"', f'class="nav-link active" href="{page}" aria-current="page"')
            components[component] = content
        source = (ROOT / '_templates' / page).read_text()
        outputs[page] = render(source, {**components, 'title': escape(info['title']), 'metadata': metadata})
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    namespace = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    sitemap = ET.Element(namespace + 'urlset')
    for page in site['pages']:
        entry = ET.SubElement(sitemap, namespace + 'url')
        ET.SubElement(entry, namespace + 'loc').text = base if page == 'index.html' else urljoin(base, page)
    ET.indent(sitemap, space='  ')
    outputs['sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(sitemap, encoding='unicode') + '\n'
    outputs['robots.txt'] = f'''# Public pages and assets are available to search engines and AI crawlers.
# No crawl delay or restrictions on rendering resources.
User-agent: *
Allow: /

Sitemap: {urljoin(base, 'sitemap.xml')}
'''
    verification_file = site.get('googleSiteVerificationFile')
    if verification_file:
        if not re.fullmatch(r'google[a-f0-9]+\.html', verification_file):
            raise ValueError('Invalid Google verification filename')
        verification_content = (ROOT / 'data' / verification_file).read_text()
        if verification_content.strip() != f'google-site-verification: {verification_file}':
            raise ValueError('Google verification file content does not match its filename')
        outputs[verification_file] = verification_content
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if committed output differs from the current content and templates')
    args = parser.parse_args()
    stale = []
    for name, content in generate().items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(name)
        else:
            path.write_text(content)
            print(f'Generated {name}')
    if stale:
        parser.exit(1, 'Generated files are out of date: ' + ', '.join(stale) + '\nRun python3 scripts/build_site.py and commit the results before deploying.\n')
    if args.check:
        print('All generated pages, metadata, sitemap, and robots.txt are up to date.')


if __name__ == '__main__':
    main()
