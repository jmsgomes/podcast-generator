import encodings.utf_8
import yaml
import xml.etree.ElementTree as xml_tree
import encodings
import time

encoding = encodings.utf_8.getregentry().name


def duration_to_seconds(duration: str) -> int:
    hours, minutes, seconds = duration.split(':')
    return (int(hours) * 60 + int(minutes)) * 60 + int(seconds)


with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

    rss_element = xml_tree.Element('rss', {
        'version': '2.0',
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
    })

link_prefix = yaml_data['link']
item_type = 'audio/mpeg'
channel_element = xml_tree.SubElement(rss_element, 'channel')
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(channel_element, 'link').text = link_prefix
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(
    channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(
    channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'itunes:type').text = 'serial'
xml_tree.SubElement(channel_element, 'itunes:image', {
    'href': link_prefix + yaml_data['image'],
})
xml_tree.SubElement(channel_element, 'itunes:category', {
    'text': yaml_data['category'],
})
xml_tree.SubElement(channel_element, 'itunes:explicit').text = 'false'

for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'itunes:episodeType').text = 'full'
    xml_tree.SubElement(item_element, 'itunes:title').text = item['title']
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'enclosure', {
        'length': item['length'].replace(',', ''),
        'type': item_type,
        'url': link_prefix + item['file'],
    })
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']
    xml_tree.SubElement(
        item_element, 'itunes:duration').text = str(duration_to_seconds(item['duration']))
    xml_tree.SubElement(item_element, 'itunes:explicit').text = 'false'
    xml_tree.SubElement(
        item_element, 'itunes:author').text = yaml_data['author']


output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding=encoding, xml_declaration=True)
