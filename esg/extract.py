from concurrent.futures import ThreadPoolExecutor, as_completed

from extractors.erm import erm_articles
from extractors.esgtoday import esgtoday_articles
from extractors.esgnews import esgnews_articles
from extractors.greenbiz import greenbiz_articles
from extractors.ec import ec_articles
from extractors.unep import unepfi_articles
from extractors.unglobalcompact import unglobalcompact_articles
from extractors.sustainablefitch import sustainablefitch_articles
from extractors.cdp import cdp_articles
from extractors.globalreporting import globalreporting_articles
from extractors.sasb import sasb_articles
from extractors.weform import weform_articles
from extractors.khaleejtimes import khaleejtimes_articles
from extractors.gulfnews import gulfnews_articles
from extractors.tnn import tnn_articles
from extractors.esma import esma_articles
from extractors.secgov import secgov_articles
from extractors.fca import fca_articles
from extractors.sca import sca_articles
from extractors.sustainalytics import sustainalytics_articles
from extractors.pwc import pwc_articles
from extractors.bcg import bcg_articles
from extractors.mckinsey import mckinsey_articles
from extractors.reuters import reuters_articles

from extractors.publcations.erm import erm_pub
from extractors.publcations.unepfi import unepfi_pub
from extractors.publcations.sustainalytics import sustainalytics_pub

from events.events import all_events

extractors = [
    erm_articles,
    esgtoday_articles,
    esgnews_articles,
    greenbiz_articles,
    ec_articles,
    unepfi_articles,
    unglobalcompact_articles,
    sustainablefitch_articles,
    cdp_articles,
    globalreporting_articles,
    sasb_articles,
    weform_articles,
    khaleejtimes_articles,
    gulfnews_articles,
    tnn_articles,
    esma_articles,
    secgov_articles,
    fca_articles,
    sca_articles,
    sustainalytics_articles,
    pwc_articles,
    bcg_articles,
    mckinsey_articles,
    reuters_articles,

    erm_pub,
    unepfi_pub,
    sustainalytics_pub,

    all_events,

]

def run_extractors_concurrently():
    with ThreadPoolExecutor() as executor: 
        futures = {executor.submit(extractor): extractor.__name__ for extractor in extractors}
        for future in as_completed(futures):
            extractor_name = futures[future]
            try:
                future.result()
                print(f"{extractor_name} completed successfully.")
            except Exception as e:
                print(f"{extractor_name} raised an exception: {e}")

from time import sleep

def run_every_hour():
    while True:
        run_extractors_concurrently()
        # Sleep for one hour
        sleep(3600)
        print("Sleeping for 1 hour...")

if __name__ == "__main__":
    run_every_hour()