from models import Author, Quote


def search_quotes(query):
    # Функція для пошуку цитат за ім'ям автора, тегом чи набором тегів
    if query.startswith("name:"):
        author_name = query[len("name:"):].strip()
        author = Author.objects(fullname__iexact=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            return quotes.to_json()
        else:
            return "Author not found."

    elif query.startswith("tag:"):
        tag = query[len("tag:"):].strip()
        quotes = Quote.objects(tags__in=[tag])
        return quotes.to_json()

    elif query.startswith("tags:"):
        tag_list = query[len("tags:"):].strip().split(',')
        quotes = Quote.objects(tags__in=tag_list)
        return quotes.to_json()

    elif query == "exit":
        return "Exiting the script."

    else:
        return "Invalid command. Please enter a valid command."

# Вхідний цикл
while True:
    user_input = input("Enter command: ")
    result = search_quotes(user_input)
    print(result.encode('utf-8').decode('utf-8'))
    if user_input == "exit":
        break

if __name__ == '__main__':
    print(search_quotes('name:'))
    print(search_quotes('tag:'))
    print(search_quotes('tags:'))

    quotes = Quote.objects().all()
    print([e.to_json() for e in quotes])