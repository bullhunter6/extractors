#banks
from articles.banks.middle_east.ifc import me_ifc
from articles.banks.middle_east.tnn import tnn_articles
from articles.banks.middle_east.gulfnews_bk import gulfnews_banks
from articles.banks.middle_east.sca import sca_articles
#from articles.banks.middle_east.reuters import reuters_articles
from articles.banks.middle_east.isdb import isdb_banks
from articles.banks.middle_east.khaleejtimes import khaleejtimes_articles
from articles.banks.middle_east.fitch import me_fitch
from articles.banks.middle_east.moodys import fi_me_moodys
from articles.banks.middle_east.arabnews import arabnews_me
from articles.banks.middle_east.snp import snp_me

from articles.banks.central_asia.kursiv import kursiv_articles
from articles.banks.central_asia.forbes import forbeskz_banks
from articles.banks.central_asia.fitch import ca_fitch
from articles.banks.central_asia.adb import adb_articles
from articles.banks.central_asia.moodys import fi_ca_moodys
from articles.banks.central_asia.uzdaily import bk_uzdaily
from articles.banks.central_asia.gazeta import gazeta_bk
from articles.banks.central_asia.nurkz import nurkz_bk
from articles.banks.central_asia.ifc import ca_ifc

from articles.banks.CA_ME.moodys import moodys_news
from articles.banks.CA_ME.kpmg import kpmg
from articles.banks.CA_ME.pwc import pwc_articles
from articles.banks.CA_ME.deloitte import deloitte
#from articles.banks.CA_ME.mckinsey import mck_articles
from articles.banks.CA_ME.bcg import bcg
from articles.banks.CA_ME.ey import ey_articles
from articles.banks.CA_ME.snp import snp_bk
from articles.banks.CA_ME.adb import both_adb_articles

from articles.banks.ratingactions.fitch_racs_ca import fitch_racs_ca
from articles.banks.ratingactions.fitch_racs_me import fitch_racs_me
from articles.banks.ratingactions.moodys_me import fi_ra_me_moodys
from articles.banks.ratingactions.moodys_ca import fi_ra_ca_moodys

#corporates
from articles.corporates.middleeast.gulfnews_cp import gulfnews_cp
from articles.corporates.middleeast.fitch import me_cp_fitch
#from articles.corporates.middleeast.moodys import crop_me_moodys
from articles.corporates.middleeast.arabnews import arabnews_cp
from articles.corporates.middleeast.arabianbusiness import arabianbusiness_cp
from articles.corporates.middleeast.zawya import zawya_cp
from articles.corporates.middleeast.khaleejtimes import khaleejtimes_articles

from articles.corporates.centralasia.adb_cp import adb_cp
#from articles.corporates.centralasia.oldchamber import oldchamber
from articles.corporates.centralasia.davaktiv import davaktiv
from articles.corporates.centralasia.moodys import crop_ca_moodys
from articles.corporates.centralasia.fitch import cp_ca_fitch
from articles.corporates.centralasia.uzdaily import cp_uzdaily
from articles.corporates.centralasia.kursiv import CA_Crop_kursiv
from articles.corporates.centralasia.forbes import forbeskz_Crop

from articles.corporates.CA_ME.ebrd import ebrd
from articles.corporates.CA_ME.snp import snp_cp
from articles.corporates.CA_ME.adb import cp_adb_articles

from articles.corporates.ratingactions.moodys_ca import crop_ra_ca_moodys
from articles.corporates.ratingactions.moodys_me import crop_ra_me_moodys
from articles.corporates.ratingactions.racs_cpme_fitch import fitch_racs_mecp
from articles.corporates.ratingactions.racs_cpca_fitch import fitch_racs_cacp

#sovereigns
from articles.sovereigns.middleeast.gulfnews_sov import gulfnews_sov
from articles.sovereigns.middleeast.khaleejtimes import khaleejtimes_sov
from articles.sovereigns.middleeast.fitch import sov_fitch
from articles.sovereigns.middleeast.imf import imf_sov
from articles.sovereigns.middleeast.ifc import sov_me_ifc
from articles.sovereigns.middleeast.isdb import isdb_sov
#from articles.sovereigns.middleeast.sca import sca_sov  /need to change the rss link
from articles.sovereigns.middleeast.worldbank import me_sov_worldbank
from articles.sovereigns.middleeast.arabnews import arabnews_sov
from articles.sovereigns.middleeast.moodys import sov_me_moodys

from articles.sovereigns.centralasia.uzdaily import sov_uzdaily
from articles.sovereigns.centralasia.fitch import sov_ca_fitch
from articles.sovereigns.centralasia.kursiv import sov_kursiv
from articles.sovereigns.centralasia.imf import imf_ca_sov
from articles.sovereigns.centralasia.worldbank import ca_sov_worldbank
from articles.sovereigns.centralasia.ifc import sov_ca_ifc
from articles.sovereigns.centralasia.adb import adb_sov
from articles.sovereigns.centralasia.nurkz import nurkz_sov
from articles.sovereigns.centralasia.moodys import sov_ca_moodys

from articles.sovereigns.CA_ME.snp import snp_sov

from articles.sovereigns.ratingactions.fitch_racs_me_sov import fitch_racs_me_sov
from articles.sovereigns.ratingactions.fitch_racs_ca_sov import fitch_racs_ca_sov
from articles.sovereigns.ratingactions.moodys_me import sov_ra_me_moodys
from articles.sovereigns.ratingactions.moodys_ca import sov_ra_ca_moodys

#global
from articles.global_.moodys import global_moodys
from articles.global_.fitch import global_fitch
from articles.global_.snp import snp_global

#events
from events.adb import adb_events
from events.imf import imf_events
from events.fitch import fitch_events
from events.ifc import ifc_events
from events.snp import snp_events
from events.bloomberg import bloomberg_events
from events.moodys import moodys_events

#publications
from publications.deloitte import deloitte_publications
from publications.ebrd import ebrd_publications
from publications.goldman import goldmansachs_publications
from publications.imf import imf_weo_publications, imf_reo_publications, imf_gfsr_publications
from publications.oecd import oecd_publications
from publications.weform import weforum_publications
from publications.worldbank import worldbank_publications

#methodologies
from utils.db import save_all_methodologies

from concurrent.futures import ThreadPoolExecutor, as_completed


from pathlib import Path
import logging, sys
from logging.handlers import RotatingFileHandler

LOG_DIR = Path.home() / "news-extractor" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "runner.log"

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



extractors = [
    #banks ME news
    me_ifc,gulfnews_banks,sca_articles,isdb_banks,khaleejtimes_articles,me_fitch,fi_me_moodys,arabnews_me,snp_me,tnn_articles,

    #banks CA news
    kursiv_articles,forbeskz_banks,ca_fitch,adb_articles,fi_ca_moodys,bk_uzdaily,nurkz_bk,gazeta_bk,ca_ifc,

    #banks CA_ME news
    moodys_news,kpmg,pwc_articles,deloitte,bcg,ey_articles,snp_bk,

    #banks rating actions
    fitch_racs_ca,fitch_racs_me,fi_ra_me_moodys,fi_ra_ca_moodys,

    #corporates ME news
    gulfnews_cp,me_cp_fitch,arabnews_cp,

    #corporates CA news
    adb_cp,davaktiv,crop_ca_moodys,cp_ca_fitch,cp_uzdaily,arabianbusiness_cp,zawya_cp,CA_Crop_kursiv,forbeskz_Crop,

    #corporates CA_ME news
    ebrd,snp_cp,cp_adb_articles,

    #corporates rating actions
    crop_ra_ca_moodys,crop_ra_me_moodys,fitch_racs_mecp,fitch_racs_cacp,

    #sovereigns ME news
    gulfnews_sov,khaleejtimes_sov,sov_fitch,imf_sov,sov_me_ifc,isdb_sov,me_sov_worldbank,arabnews_sov,sov_me_moodys,

    #sovereigns CA news
    sov_ca_fitch,sov_kursiv,imf_ca_sov,ca_sov_worldbank,sov_ca_ifc,adb_sov,sov_uzdaily,nurkz_sov,sov_ca_moodys,

    #sovereigns CA_ME news
    snp_sov,

    #sovereigns rating actions
    fitch_racs_me_sov,fitch_racs_ca_sov,sov_ra_me_moodys,sov_ra_ca_moodys,

    #global news
    global_moodys,global_fitch,snp_global,

    #events
    adb_events,imf_events,fitch_events,ifc_events,snp_events,bloomberg_events,moodys_events,

    #publications
    deloitte_publications,ebrd_publications,goldmansachs_publications,imf_weo_publications,imf_reo_publications,imf_gfsr_publications,oecd_publications,weforum_publications,worldbank_publications,

    #methodologies
    save_all_methodologies,

    both_adb_articles,
]

import time, traceback

def run_extractors_concurrently():
    logger.info("=== Batch start ===")
    start = time.time()
    from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

    MAX_WORKERS = 8
    PER_BATCH_WALLCLOCK = 30 * 60  # 10 minutes safety cap

    def _wrap(extractor):
        name = extractor.__name__
        t0 = time.time()
        logger.info("[START] %s", name)
        try:
            extractor()
            logger.info("[DONE]  %s in %.2fs", name, time.time() - t0)
        except Exception as e:
            logger.error("[FAIL]  %s: %s", name, e)
            logger.debug("Traceback for %s:\n%s", name, traceback.format_exc())

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = [ex.submit(_wrap, fn) for fn in extractors]
        done, not_done = wait(futs, timeout=PER_BATCH_WALLCLOCK, return_when=ALL_COMPLETED)

        if not_done:
            for f in not_done:
                logger.warning("[TIMEBOX] An extractor exceeded %ss and will be skipped until next cycle.",
                               PER_BATCH_WALLCLOCK)

    logger.info("=== Batch end (%.2fs) ===", time.time() - start)

def run_every_hour():
    while True:
        run_extractors_concurrently()
        logger.info("Sleeping for 1 hour...")
        from time import sleep
        sleep(3600)

if __name__ == "__main__":
    run_every_hour()

    #publications = ebrd_publications() + deloitte_publications() + goldmansachs_publications() + imf_weo_publications() + imf_reo_publications() + imf_gfsr_publications() + oecd_publications() + weforum_publications() + worldbank_publications()
    #print(len(publications))
    #for publication in publications:
        #print(publication['title'])

    #articles = forbeskz_Crop()
    #print(len(articles))
    #for article in articles:
        #print(f"{article['title']}\n{article['date']}\n{article['link']}\n\n{article['source']}\n{article['keywords']}\n{article['region']}\n{article['sector']}\n\n{'-'*50}\n")


    #methodologies = save_all_methodologies()
    #print(len(methodologies))

