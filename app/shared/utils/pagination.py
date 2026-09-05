def count_pages(total: int, limit: int) -> int:
    if limit < 1:
        raise ValueError("limit must be greater than 0")

    pages = total // limit

    if total % limit:
        pages += 1

    return pages
