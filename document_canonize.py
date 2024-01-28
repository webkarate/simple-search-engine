from search import Search
import save_load

document_db_file_name = 'documents'


class DocumentDB:

    def __init__(self):
        self.database = save_load.load_object(document_db_file_name) or []


    def add_document(self, file_name, text):
        search = Search()
        frequency = search.get_efficient_words_from_text(text)
        words_weights = self.get_word_list_weights(frequency)
        self.database.append(Document(file_name, words_weights))
        save_load.save_object(self.database, document_db_file_name)


    def get_word_list_weights(self, frequency):
        max_frequency = max(frequency.values())

        weights = {}
        for word in frequency.keys():
            weights[word] = frequency[word] / max_frequency

        return weights


    def find_relative_documents(self, search, relevance_threshold):
        search_result = []
        for document in self.database:
            relevance = 0
            for search_word in search:
                found = document.words.get(search_word)
                if found != None:
                    relevance += found

            if relevance > relevance_threshold:
                search_result.append((document.file_name, relevance))

        search_result.sort(key=lambda a: a[1])
        return search_result


class Document:

    def __init__(self, file_name, words):
        self.file_name = file_name
        self.words = words
