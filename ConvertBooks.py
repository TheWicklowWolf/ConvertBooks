import os
import shutil
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


def copy_book(input_file, output_file):
    try:
        shutil.copy(input_file, output_file)
        logging.info(f"Copied {input_file} to {output_file}")
    except Exception as e:
        logging.error(f"Error copying {input_file}: {str(e)}")


def run_conversion():
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_limit) as executor:
        futures = []

        for root, dirs, files in os.walk(source_folder):
            if not dirs and not files:
                logging.error(f"The directory {source_folder} is empty.")
                return
            book_files = [file for file in files if any(file.endswith(format) for format in book_source_formats)]
            unique_books = set([os.path.splitext(book)[0] for book in book_files])

            for book in unique_books:
                for source_format in book_source_formats:
                    book_path = os.path.join(root, f"{book}{source_format}")
                    if os.path.exists(book_path):
                        input_file = book_path
                        break
                else:
                    logging.warning(f"No valid input file found for {book}")
                    continue

                for output_format in desired_output_formats:
                    relative_root = os.path.relpath(root, source_folder)
                    output_file_dir = os.path.join(destination_folder, relative_root)
                    if not os.path.exists(output_file_dir):
                        os.makedirs(output_file_dir, exist_ok=True)
                    output_file = os.path.join(output_file_dir, f"{book}{output_format}")
                    if not os.path.exists(output_file):
                        if source_format == output_format:
                            futures.append(executor.submit(copy_book, input_file, output_file))
                        else:
                            futures.append(executor.submit(convert_book, input_file, output_file))

        concurrent.futures.wait(futures)

    logging.info(f"Conversion Complete, sleeping...")


logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

app_name_text = os.path.basename(__file__).replace(".py", "")
release_version = os.environ.get("RELEASE_VERSION", "unknown")
logging.info(f"{'*' * 50}\n")
logging.info(f"{app_name_text} Version: {release_version}\n")
logging.info(f"{'*' * 50}")

book_source_formats = os.getenv("book_source_formats", ".epub,.mobi,.azw3").split(",")
desired_output_formats = os.getenv("desired_output_formats", ".mobi,.azw3").split(",")
schedule = os.getenv("schedule", "0").split(",")
schedule = [int(hour.strip()) for hour in schedule]
run_at_startup = os.getenv("run_at_startup", "false")
thread_limit = int(os.getenv("thread_limit", 1))

source_folder = "source"
if not os.path.exists(source_folder):
    os.makedirs(source_folder, exist_ok=True)

destination_folder = "destination"
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder, exist_ok=True)

if run_at_startup.lower() == "true":
    run_conversion()
    sleep(3600)

while True:
    if datetime.now().hour in schedule:
        run_conversion()
    else:
        logging.info(f"Current hour is {datetime.now().hour}. Not a scheduled run hour. Sleeping...")
    sleep(3600)
