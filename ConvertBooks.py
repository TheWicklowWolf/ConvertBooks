import os
import subprocess
from time import sleep
from datetime import datetime
import logging
import concurrent.futures


def convert_book(input_file, output_file):
    try:
        subprocess.run(["ebook-convert", input_file, output_file], check=True)
        logging.info(f"Converted {input_file} to {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {input_file}: {e}")
    except Exception as e:
        logging.error(f"Error converting {input_file}: {str(e)}")


def convert_books():
    if not os.path.exists(path_to_books):
        logging.error(f"The directory {path_to_books} does not exist.")
        logging.error(f"Sleeping...")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_limit) as executor:
        futures = []

        for root, _, files in os.walk(path_to_books):
            book_files = [file for file in files if any(file.endswith(format) for format in desired_formats)]
            unique_books = set([os.path.splitext(book)[0] for book in book_files])

            for book in unique_books:
                for format in desired_formats:
                    if os.path.exists(f"{book}{format}"):
                        input_file = os.path.join(root, f"{book}{format}")
                        break

                for file_format in desired_formats:
                    output_file = os.path.join(root, f"{book}{file_format}")
                    if not os.path.exists(output_file):
                        futures.append(executor.submit(convert_book, input_file, output_file))

        concurrent.futures.wait(futures)


logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
path_to_books = os.getenv("path_to_books", "path/to/books")
desired_formats = os.getenv("desired_formats", ".epub,.mobi,.azw3").split(",")
schedule = os.getenv("schedule", "0").split(",")
schedule = [int(hour.strip()) for hour in schedule]
run_at_startup = os.getenv("run_at_startup", "false")
thread_limit = int(os.getenv("thread_limit", 1))

if run_at_startup.lower() == "true":
    convert_books()
while True:
    if datetime.now().hour in schedule:
        convert_books()
    else:
        logging.info(f"Current hour is {datetime.now().hour}. Not a scheduled run hour. Sleeping...")
    sleep(3600)
