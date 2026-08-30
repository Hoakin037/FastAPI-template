def count_pages(total: int, limit: int) -> int:
    pages = total // limit

    if total % limit:
        pages += 1

    return pages
