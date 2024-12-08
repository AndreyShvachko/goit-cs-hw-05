import asyncio
import os
from pathlib import Path
import shutil
import logging
import argparse

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def read_folder(source_folder: Path, output_folder: Path):

    for item in source_folder.iterdir():
        if item.is_dir():
            await read_folder(item, output_folder)
        elif item.is_file():
            await copy_file(item, output_folder)


async def copy_file(file_path: Path, output_folder: Path):
    try:
        extension = file_path.suffix.lstrip(".").lower() or "no_extension"
        target_folder = output_folder / extension
        target_folder.mkdir(parents=True, exist_ok=True)
        target_path = target_folder / file_path.name

        logging.info(f"Копіюється файл: {file_path} -> {target_path}")
        await asyncio.to_thread(shutil.copy2, file_path, target_path)
    except Exception as e:
        logging.error(f"помилка під час копіювання {file_path}: {e}")


async def main(source: str, output: str):

    source_folder = Path(source)
    output_folder = Path(output)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Вихідна папка {source} не існує або не є директорією.")
        return
    
    output_folder.mkdir(parents=True, exist_ok=True)
    await read_folder(source_folder, output_folder)
    logging.info("Сортування файлів завершено.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Сортування файлів за розширеннями.")
    parser.add_argument("source", type=str, help="Шлаях до вихідної папки.")
    parser.add_argument("output", type=str, help="Шлаях до папки призначення.")

    args = parser.parse_args()

    asyncio.run(main(args.source, args.output))

