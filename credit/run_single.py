from pathlib import Path
import logging, sys
from logging.handlers import RotatingFileHandler
import time
import traceback

# Setup logging
LOG_DIR = Path.home() / "news-extractor" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "single_runner.log"

logger = logging.getLogger("runner")
logger.setLevel(logging.INFO)

# file (rotates ~5MB, keep 5 backups)
fh = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

# console
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

logger.handlers.clear()
logger.addHandler(fh)
logger.addHandler(ch)
logger.propagate = False

def run_single_extractor(extractor_func):
    name = extractor_func.__name__
    t0 = time.time()
    logger.info("[START] %s", name)
    try:
        results = extractor_func()
        logger.info("[DONE]  %s in %.2fs", name, time.time() - t0)
        
        # Optional: Print results if it returns a list
        if isinstance(results, list):
            print(f"Found {len(results)} items.")
            # Uncomment to see details
            # for item in results:
            #     print(item)
        elif results:
             print(f"Result: {results}")

    except Exception as e:
        logger.error("[FAIL]  %s: %s", name, e)
        logger.debug("Traceback for %s:\n%s", name, traceback.format_exc())

if __name__ == "__main__":
    # --- INSTRUCTIONS ---
    # 1. Import the extractor function you want to test.
    #    You can copy the import line from extract.py
    
    # Example imports:
    from articles.sovereigns.centralasia.adb import adb_sov as ar
    # from articles.global_.moodys import global_moodys
    
    # 2. Call run_single_extractor with the function
    
    # Example usage (uncomment to run):
    run_single_extractor(ar)
    
    #print("Please edit this file to import and run the specific extractor you need.")
