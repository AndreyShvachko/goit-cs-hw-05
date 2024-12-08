import requests
import re
from collections import Counter
from multiprocessing import Pool
import matplotlib.pyplot as plt


def fetch_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def map_function(chunk):
    words = re.findall(r'\b\w+\b', chunk.lower())
    return Counter(words)


def reduce_function(counters):
    total_counter = Counter()
    for counter in counters:
        total_counter.update(counter)
    return total_counter


def split_text_into_chunks(text, num_chunks):
    '''Розбиває текст на декілька частин'''
    text_length = len(text)
    chunk_size = text_length // num_chunks
    return [text[i:i + chunk_size] for i in range(0, text_length, chunk_size)]


def visualize_top_words(word_freq, top_n=10):
    """Візуалізує топ - N найчастіше вживаних слів"""
    top_words = word_freq.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10,6))
    plt.bar(words,  counts, color='skyblue')
    plt.xlabel('Words', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Top Words by Frequency', fontsize=16)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # URL тексту для аналізу
    url = "https://www.gutenberg.org/files/11/11-0.txt"  # Аліса в країні чудес
    num_chunks = 4  # Кількість потоків

    # Завантаження тексту
    print("Завантаження тексту...")
    text = fetch_text_from_url(url)

    # Розбиття тексту на частини
    print("Розбиття тексту на частини...")
    chunks = split_text_into_chunks(text, num_chunks)

    # Застосування MapReduce
    print("Аналіз тексту за допомогою MapReduce...")
    with Pool(num_chunks) as pool:
        mapped = pool.map(map_function, chunks)
    word_freq = reduce_function(mapped)

    # Візуалізація результатів
    print("Візуалізація результатів...")
    visualize_top_words(word_freq, top_n=10)


