def item_to_text(item):
    text = f"{item.description}\n" \
              f"\n*{item.price} €*\n" \
              f"*{item.address}*\n" \
              f"[⁠]({item.img})"
    return text


def make_url(url, chat_id, mode='markdown', message='', item_url=''):
    url_for_request = url
    url_for_request = url_for_request.replace("{chat_id}", chat_id)
    url_for_request = url_for_request.replace("{parse_mode}", mode)
    url_for_request = url_for_request.replace("{text}", message)
    url_for_request = url_for_request.replace("{item_url}", item_url)

    return url_for_request