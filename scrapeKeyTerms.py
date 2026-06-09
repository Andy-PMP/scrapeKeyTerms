from pathlib import Path
from bs4 import BeautifulSoup
import re
import sys

# Security Configuration
# Automatically use the script's directory as the allowed directory
SCRIPT_DIR = Path(__file__).parent
ALLOWED_DIR = SCRIPT_DIR
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB limit
ALLOWED_EXTENSIONS = {".html", ".htm"}


def validate_file_path(file_path):
    """
    Validate that the file path is within the allowed directory to prevent path traversal.
    
    Args:
        file_path (Path): The file path to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        resolved_path = file_path.resolve()
        allowed_resolved = ALLOWED_DIR.resolve()
        resolved_path.relative_to(allowed_resolved)
        return True
    except ValueError:
        return False


def validate_file_extension(file_path):
    """
    Validate that the file has an allowed extension.
    
    Args:
        file_path (Path): The file path to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return file_path.suffix.lower() in ALLOWED_EXTENSIONS


def validate_file_size(file_path):
    """
    Validate that the file doesn't exceed maximum size limit.
    
    Args:
        file_path (Path): The file path to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        file_size = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            print(f"Error: File size ({file_size / 1024 / 1024:.1f} MB) exceeds limit ({MAX_FILE_SIZE / 1024 / 1024:.1f} MB).")
            return False
        return True
    except OSError as e:
        print(f"Error checking file size: {e}")
        return False


def clean_text(text):
    """
    Remove excessive whitespace, tabs, and line breaks.
    
    Args:
        text (str): The text to clean
        
    Returns:
        str: Cleaned text
    """
    return re.sub(r"\s+", " ", text).strip()


def extract_terms(html_file):
    """
    Extract terms and definitions from the HTML.
    
    Args:
        html_file (Path): Path to the HTML file
        
    Returns:
        list: List of tuples containing (term, definition)
    """
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except FileNotFoundError:
        print(f"Error: File '{html_file}' not found.")
        return []
    except UnicodeDecodeError:
        print(f"Error: File '{html_file}' is not UTF-8 encoded.")
        return []
    except Exception as e:
        print(f"Error reading file '{html_file}': {e}")
        return []

    terms = []

    # Find all term containers
    try:
        items = soup.select("div.key-term-list-item")
        print(f"Found {len(items)} key term containers.")

        for index, item in enumerate(items):
            term_span = item.select_one("span.key-term-text")
            definition_span = item.select_one("span.key-term-definition-text")

            if not term_span or not definition_span:
                print(f"Warning: Skipping item {index} - missing required HTML elements (term_span or definition_span)")
                continue

            term = clean_text(term_span.get_text())
            definition = clean_text(definition_span.get_text())

            # Validate that we extracted actual content
            if not term or not definition:
                print(f"Warning: Skipping item {index} - empty term or definition")
                continue

            terms.append((term, definition))

    except Exception as e:
        print(f"Error parsing HTML structure: {e}")
        return []

    return terms


def extract_readings(html_file):
    """
    Extract assigned readings and URLs from the HTML.
    
    Args:
        html_file (Path): Path to the HTML file
        
    Returns:
        list: List of tuples containing (chapter_lesson_info, reading_title, url)
    """
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except Exception as e:
        print(f"Error reading file for readings extraction: {e}")
        return []

    readings = []

    try:
        # Find all lesson containers in the links section
        lessons = soup.select("div.links-container-row div.lesson")
        print(f"Found {len(lessons)} lesson sections for assigned readings.")

        for lesson_index, lesson in enumerate(lessons):
            # Extract lesson header info
            lesson_header = lesson.select_one("div.lesson-header")
            if not lesson_header:
                continue

            # Get chapter and lesson numbers
            lesson_index_spans = lesson_header.select("span.lesson-index")
            chapter_text = ""
            lesson_number = ""
            
            if len(lesson_index_spans) >= 1:
                chapter_text = clean_text(lesson_index_spans[0].get_text())
            if len(lesson_index_spans) >= 2:
                lesson_number = clean_text(lesson_index_spans[1].get_text())

            # Get lesson title
            lesson_title_div = lesson_header.select_one("div.lesson-title")
            
            if not chapter_text or not lesson_title_div:
                continue

            lesson_title = clean_text(lesson_title_div.get_text())
            
            if lesson_number:
                lesson_info = f"{chapter_text} | {lesson_number}: {lesson_title}"
            else:
                lesson_info = f"{chapter_text}: {lesson_title}"

            # Extract readings for this lesson
            lesson_links = lesson.select("div.lesson-link")
            
            for link_index, link in enumerate(lesson_links):
                # Get reading title
                title_span = link.select_one("span.title-text")
                if not title_span:
                    # Fallback: try to get from the link itself
                    title_link = link.select_one("a.link-title-link")
                    if title_link:
                        title_text = clean_text(title_link.get_text())
                    else:
                        continue
                else:
                    title_text = clean_text(title_span.get_text())

                # Get URL from link
                url_link = link.select_one("a.link-title-link")
                if not url_link or not url_link.get("href"):
                    url_link = link.select_one("a.link-url")
                
                if not url_link or not url_link.get("href"):
                    print(f"Warning: Skipping reading in {lesson_info} - missing URL")
                    continue

                url = url_link.get("href")

                if not title_text or not url:
                    print(f"Warning: Skipping reading in {lesson_info} - empty title or URL")
                    continue

                readings.append((lesson_info, title_text, url))

    except Exception as e:
        print(f"Error parsing HTML for readings: {e}")
        return []

    return readings


def write_output(terms, readings, output_file):
    """
    Write extracted terms and readings to output file.
    
    Args:
        terms (list): List of tuples containing (term, definition)
        readings (list): List of tuples containing (lesson_info, reading_title, url)
        output_file (Path): Path to the output file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8", newline="\n") as f:
            # Write KEY TERMS section
            f.write("KEY TERMS\n")
            f.write("=" * 50)
            f.write("\n\n")
            
            for term, definition in terms:
                f.write(term.title())
                f.write("\n")
                f.write(definition)
                # exactly two newlines between entries
                f.write("\n\n")

            # Write ASSIGNED READINGS section
            f.write("\n")
            f.write("ASSIGNED READINGS\n")
            f.write("=" * 50)
            f.write("\n\n")
            
            current_lesson = None
            for lesson_info, reading_title, url in readings:
                # Write lesson header if it changed
                if lesson_info != current_lesson:
                    if current_lesson is not None:
                        f.write("\n")  # spacing between lesson groups
                    f.write(lesson_info)
                    f.write("\n")
                    f.write("-" * 40)
                    f.write("\n")
                    current_lesson = lesson_info
                
                f.write(reading_title)
                f.write(" | ")
                f.write(url)
                f.write("\n")

        return True

    except PermissionError:
        print(f"Error: No write permission for directory '{output_file.parent}'")
        return False
    except Exception as e:
        print(f"Error writing to output file: {e}")
        return False


def main():
    """
    Main function to orchestrate the scraping and output process.
    """
    # Get filename from command-line argument or user input
    if len(sys.argv) > 1:
        html_filename = sys.argv[1]
        print(f"Processing: {html_filename}\n")
    else:
        html_filename = input("Enter HTML filename: ").strip()

    # Validate input is not empty
    if not html_filename:
        print("Error: Filename cannot be empty.")
        return

    html_path = Path(html_filename)

    # Validate file extension
    if not validate_file_extension(html_path):
        print(f"Error: File must have one of these extensions: {', '.join(ALLOWED_EXTENSIONS)}")
        return

    # Validate file exists
    if not html_path.exists():
        print(f"Error: File '{html_path}' not found.")
        return

    # Validate file is actually a file (not a directory)
    if not html_path.is_file():
        print(f"Error: '{html_path}' is not a file.")
        return

    # Validate path doesn't contain path traversal attempts
    if not validate_file_path(html_path):
        print("Error: Invalid file path. Access denied.")
        return

    # Validate file size
    if not validate_file_size(html_path):
        return

    # Extract terms
    print("\n--- EXTRACTING KEY TERMS ---")
    terms = extract_terms(html_path)

    # Validate we extracted at least some terms
    if not terms:
        print("Error: No valid terms were extracted from the HTML file.")
        return

    # Display first record for verification
    print("\nFIRST TERM RECORD:")
    print(f"Term: {repr(terms[0][0])}")
    print(f"Definition: {repr(terms[0][1])}")

    # Extract readings
    print("\n--- EXTRACTING ASSIGNED READINGS ---")
    readings = extract_readings(html_path)

    if readings:
        print(f"\nFIRST READING RECORD:")
        print(f"Lesson: {repr(readings[0][0])}")
        print(f"Title: {repr(readings[0][1])}")
        print(f"URL: {repr(readings[0][2])}")
    else:
        print("Warning: No assigned readings were extracted from the HTML file.")

    # Write output
    output_path = html_path.with_suffix(".txt")
    if write_output(terms, readings, output_path):
        print(f"\n--- OUTPUT SUMMARY ---")
        print(f"Extracted {len(terms)} key terms.")
        print(f"Extracted {len(readings)} assigned readings.")
        print(f"Output written to: {output_path}")
    else:
        print("Error: Failed to write output file.")
        return


if __name__ == "__main__":
    main()
