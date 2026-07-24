def print_summary(
    title: str,
    inserted: int,
    skipped: int,
):
    print()

    print("=" * 45)
    print(title)
    print("-" * 45)

    print(f"Insertados : {inserted}")
    print(f"Omitidos   : {skipped}")

    print("=" * 45)
