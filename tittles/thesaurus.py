import requests
import xml.etree.ElementTree as ET
from collections import Counter

def fetch(category, adjectives):
    counter = Counter()
    for adjective in adjectives:
        r = requests.get('http://ngrams.ucd.ie/therex3/common-nouns/category.action', params={'cate': f'{adjective}:{category}', 'xml': 'true'})
        root = ET.fromstring(r.text)
        members = {member.text.strip(): int(member.attrib['weight']) for member in root.iter('Member')}
        members = {k: v / max(members.values()) / len(adjectives) for k, v in members.items()}
        counter.update(members)
    return counter

if __name__ == "__main__":
    import sys
    sys.path.insert(0,'..')
    import inputs
    emotion, word_pairs = inputs.get_input(False)
    # print(emotion, word_pairs)
    # exit()

    adjectives = list(word_pair[1] for word_pair in word_pairs if word_pair[0] == 'human')
    print('human:')
    print(' adjectives:', ', '.join(adjectives))
    print(' suggestions:')
    suggestions = fetch('person', adjectives)
    for suggestion in suggestions.most_common(10):
        print(f'  {suggestion[1]:.2f} {suggestion[0]}')

    adjectives = list(word_pair[1] for word_pair in word_pairs if word_pair[0] == 'animal')
    print('animal:')
    print(' adjectives:', ', '.join(adjectives))
    print(' suggestions:')
    suggestions = fetch('animal', adjectives)
    for suggestion in suggestions.most_common(10):
        print(f'  {suggestion[1]:.2f} {suggestion[0]}')
