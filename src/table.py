import typing as t
import os

IMAGES_PATH = "resources/shadowrun/tables"


def find_longest_matching_block(str1: str, str2: str):
    if len(str1) != len(str2):
        raise ValueError("Strings must be the same length")

    longest = 0
    current = 0
    for i in range(0, len(str1)):
        if str1[i] == str2[i]:
            current += 1
        else:
            if current > longest:
                longest = current
            current = 0
    if current > longest:
        longest = current
    return longest


def get_string_match_score(query: str, to_match: str):
    total = 0
    for query_word in query.split(" "):
        word_best = 0
        for offset in range(-len(query_word) + 1, len(to_match)):
            query_slice = query_word[max(0, -offset):min(len(query_word), len(to_match) - offset)]
            to_match_slice = to_match[max(0, offset):min(len(to_match), offset + len(query_word))]
            word_best = max(word_best, find_longest_matching_block(query_slice, to_match_slice))
        total += word_best / len(query_word)
    return total / len(query.split(" ")) * 100


class Table:
    """Represents a table from one of the rulebooks"""

    path: str
    name: str
    book: str
    page: int

    def __init__(self, path: str, book: str):
        self.path = path
        self.page = int(path.split("\\")[-1].split("-")[0])
        self.name = path.split("-")[1].split(".")[0]
        self.book = book

    @classmethod
    def lookup_table(cls, query: str):
        """
        Find the table or tables with names most similar to the user's query
        :param query: The string to search for
        :return: A list of Tables
        """

        query = query.lower()
        query.replace(" table", "")

        scores: t.Dict[Table, float] = {}
        for table in tables:
            if table.name.lower() == query:
                return [table]
            scores[table] = get_string_match_score(query, table.name.lower())

        best_first = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)

        if scores[best_first[0]] == 100 and scores[best_first[1]] < 100:
            return [best_first[0]]

        best_score = scores[best_first[0]]
        results = sorted([tb for tb in best_first if scores[tb] > best_score - 20],
                         key=lambda tb: scores[tb] * 1000 - len(tb.name),
                         reverse=True)
        return results[0:min(len(results), 5)]


tables: t.List[Table] = []
for book_dir in [d for d in os.listdir(IMAGES_PATH) if os.path.isdir(os.path.join(IMAGES_PATH, d))]:
    book_dir_path = os.path.join(IMAGES_PATH, book_dir)
    for file in [os.path.join(book_dir_path, f) for f in os.listdir(book_dir_path)
                 if os.path.isfile(os.path.join(book_dir_path, f))]:

        tables.append(Table(file, book_dir))

if __name__ == "__main__":
    import timeit

    print("Enter a query")
    inp = input("> ")

    start = timeit.default_timer()

    results = Table.lookup_table(inp)

    stop = timeit.default_timer()

    print([tb.name for tb in results])
    print('Time: ', stop - start)
