from pathlib import Path
from bs4 import BeautifulSoup
import re


def clean_text(text):
    """
    Remove excessive whitespace, tabs, and line breaks.
    """
    return re.sub(r"\s+", " ", text).strip()


def extract_terms(html_file):
    """
    Extract terms and definitions from the HTML.
    """

    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    terms = []

    # Find all term containers
    items = soup.select("div.key-term-list-item")

    print(f"\nFound {len(items)} key term containers.\n")

    for index, item in enumerate(items):

        term_span = item.select_one("span.key-term-text")
        definition_span = item.select_one("span.key-term-definition-text")

        if not term_span or not definition_span:
            continue

        term = clean_text(term_span.get_text())
        definition = clean_text(definition_span.get_text())

        terms.append((term, definition))

    return terms


def write_output(terms, output_file):

    with open(output_file, "w", encoding="utf-8", newline="\n") as f:

        for term, definition in terms:

            f.write(term.title())
            f.write("\n")

            f.write(definition)

            # exactly two newlines between entries
            
            f.write("\n\n")

def main():

    html_filename = input("Enter HTML filename: ").strip()

    html_path = Path(html_filename)

    if not html_path.exists():
        print("File not found.")
        return

    output_path = html_path.with_suffix(".txt")

    terms = extract_terms(html_path)
    print("\nFIRST RECORD BEING WRITTEN:")
    print(repr(terms[0][0]))
    print(repr(terms[0][1]))
    write_output(terms, output_path)

    print(f"\nExtracted {len(terms)} terms.")
    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    main()
