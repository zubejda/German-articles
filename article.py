import re
import requests
from bs4 import BeautifulSoup


def get_german_article(word):
    url = f"https://de.wiktionary.org/wiki/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        word_class = soup.h3.a.string
        if "Substantiv" not in word_class:
            return None
        try:
            article = soup.find('table', class_='wikitable').find("td").string
            return article
        except:
            return None
    return None


def read_file(filepath):
    with open(filepath, "r", encoding="iso-8859-1") as fr:
        lines = fr.readlines()
    return lines


def find_articles(lines):
    pattern_to_remove = r'[^a-zA-ZäöüÄÖÜß\s]'
    all_words = []
    for l in lines:
        modified_string = re.sub(pattern_to_remove, '', l)
        modified_string = re.split(r'\s+', modified_string)
        modified_string = [item for item in modified_string if len(item) != 0]

        german = " ".join(modified_string[:-1])
        english = modified_string[-1] + "\n"
        with_article = get_german_article(german)
        if with_article is None:
            all_words.append(german + " - " + english)
            continue
        all_words.append(with_article[:-1] + " - " + english)
    return all_words


def write_file(filepath, lines):
    with open(filepath, 'w') as fw:
        for line in lines:
            fw.write(line)


if __name__ == "__main__":
    input_file = "path to the file with german words"
    output_file = "path to the file for saving"

    lines = read_file(input_file)
    article_lines = find_articles(lines)
    write_file(output_file, article_lines)
