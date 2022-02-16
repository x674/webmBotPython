from Telegram.Channel import start_bot
from ImageBoard.dvach import update_threads
from concurrent.futures import ThreadPoolExecutor
def main():
    executor = ThreadPoolExecutor(max_workers=4)
    # executor.submit(start_bot)
    executor.submit(update_threads)
    start_bot()
    print("Started!")  # Message: Hello work


if __name__ == "__main__":
    main()
