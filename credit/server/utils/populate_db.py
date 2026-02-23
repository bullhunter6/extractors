"""Utility script to populate extractors into database."""
import asyncio
from server.core.database import AsyncSessionLocal, init_db
from server.models import Extractor, ExtractorCategory
from server.core.logging import get_logger

logger = get_logger(__name__)


# Define all extractors from extract.py
EXTRACTORS_CONFIG = [
    # Banks - Middle East
    ("me_ifc", "IFC Middle East", "articles.banks.middle_east.ifc", ExtractorCategory.BANKS_ME),
    ("gulfnews_banks", "Gulf News Banks", "articles.banks.middle_east.gulfnews_bk", ExtractorCategory.BANKS_ME),
    ("sca_articles", "SCA Articles", "articles.banks.middle_east.sca", ExtractorCategory.BANKS_ME),
    ("isdb_banks", "IsDB Banks", "articles.banks.middle_east.isdb", ExtractorCategory.BANKS_ME),
    ("khaleejtimes_articles", "Khaleej Times", "articles.banks.middle_east.khaleejtimes", ExtractorCategory.BANKS_ME),
    ("me_fitch", "Fitch Middle East", "articles.banks.middle_east.fitch", ExtractorCategory.BANKS_ME),
    ("fi_me_moodys", "Moody's Middle East FI", "articles.banks.middle_east.moodys", ExtractorCategory.BANKS_ME),
    ("arabnews_me", "Arab News ME", "articles.banks.middle_east.arabnews", ExtractorCategory.BANKS_ME),
    ("snp_me", "S&P Middle East", "articles.banks.middle_east.snp", ExtractorCategory.BANKS_ME),
    ("tnn_articles", "TNN Articles", "articles.banks.middle_east.tnn", ExtractorCategory.BANKS_ME),
    
    # Banks - Central Asia
    ("kursiv_articles", "Kursiv Articles", "articles.banks.central_asia.kursiv", ExtractorCategory.BANKS_CA),
    ("forbeskz_banks", "Forbes KZ Banks", "articles.banks.central_asia.forbes", ExtractorCategory.BANKS_CA),
    ("ca_fitch", "Fitch Central Asia", "articles.banks.central_asia.fitch", ExtractorCategory.BANKS_CA),
    ("adb_articles", "ADB Articles", "articles.banks.central_asia.adb", ExtractorCategory.BANKS_CA),
    ("fi_ca_moodys", "Moody's Central Asia FI", "articles.banks.central_asia.moodys", ExtractorCategory.BANKS_CA),
    ("bk_uzdaily", "Uzdaily Banks", "articles.banks.central_asia.uzdaily", ExtractorCategory.BANKS_CA),
    ("nurkz_bk", "Nur.kz Banks", "articles.banks.central_asia.nurkz", ExtractorCategory.BANKS_CA),
    ("gazeta_bk", "Gazeta Banks", "articles.banks.central_asia.gazeta", ExtractorCategory.BANKS_CA),
    ("ca_ifc", "IFC Central Asia", "articles.banks.central_asia.ifc", ExtractorCategory.BANKS_CA),
    
    # Banks - CA/ME Combined
    ("moodys_news", "Moody's News", "articles.banks.CA_ME.moodys", ExtractorCategory.BANKS_CA_ME),
    ("kpmg", "KPMG", "articles.banks.CA_ME.kpmg", ExtractorCategory.BANKS_CA_ME),
    ("pwc_articles", "PwC Articles", "articles.banks.CA_ME.pwc", ExtractorCategory.BANKS_CA_ME),
    ("deloitte", "Deloitte", "articles.banks.CA_ME.deloitte", ExtractorCategory.BANKS_CA_ME),
    ("bcg", "BCG", "articles.banks.CA_ME.bcg", ExtractorCategory.BANKS_CA_ME),
    ("ey_articles", "EY Articles", "articles.banks.CA_ME.ey", ExtractorCategory.BANKS_CA_ME),
    ("snp_bk", "S&P Banks", "articles.banks.CA_ME.snp", ExtractorCategory.BANKS_CA_ME),
    ("both_adb_articles", "ADB Both Regions", "articles.banks.CA_ME.adb", ExtractorCategory.BANKS_CA_ME),
    
    # Banks - Rating Actions
    ("fitch_racs_ca", "Fitch Rating Actions CA", "articles.banks.ratingactions.fitch_racs_ca", ExtractorCategory.BANKS_RATING),
    ("fitch_racs_me", "Fitch Rating Actions ME", "articles.banks.ratingactions.fitch_racs_me", ExtractorCategory.BANKS_RATING),
    ("fi_ra_me_moodys", "Moody's Rating Actions ME FI", "articles.banks.ratingactions.moodys_me", ExtractorCategory.BANKS_RATING),
    ("fi_ra_ca_moodys", "Moody's Rating Actions CA FI", "articles.banks.ratingactions.moodys_ca", ExtractorCategory.BANKS_RATING),
    
    # Corporates - Middle East
    ("gulfnews_cp", "Gulf News Corporates", "articles.corporates.middleeast.gulfnews_cp", ExtractorCategory.CORPORATES_ME),
    ("me_cp_fitch", "Fitch ME Corporates", "articles.corporates.middleeast.fitch", ExtractorCategory.CORPORATES_ME),
    ("arabnews_cp", "Arab News Corporates", "articles.corporates.middleeast.arabnews", ExtractorCategory.CORPORATES_ME),
    ("arabianbusiness_cp", "Arabian Business CP", "articles.corporates.middleeast.arabianbusiness", ExtractorCategory.CORPORATES_ME),
    ("zawya_cp", "Zawya Corporates", "articles.corporates.middleeast.zawya", ExtractorCategory.CORPORATES_ME),
    
    # Corporates - Central Asia
    ("adb_cp", "ADB Corporates", "articles.corporates.centralasia.adb_cp", ExtractorCategory.CORPORATES_CA),
    ("davaktiv", "Davaktiv", "articles.corporates.centralasia.davaktiv", ExtractorCategory.CORPORATES_CA),
    ("crop_ca_moodys", "Moody's CA Corporates", "articles.corporates.centralasia.moodys", ExtractorCategory.CORPORATES_CA),
    ("cp_ca_fitch", "Fitch CA Corporates", "articles.corporates.centralasia.fitch", ExtractorCategory.CORPORATES_CA),
    ("cp_uzdaily", "Uzdaily Corporates", "articles.corporates.centralasia.uzdaily", ExtractorCategory.CORPORATES_CA),
    ("CA_Crop_kursiv", "Kursiv Corporates", "articles.corporates.centralasia.kursiv", ExtractorCategory.CORPORATES_CA),
    ("forbeskz_Crop", "Forbes KZ Corporates", "articles.corporates.centralasia.forbes", ExtractorCategory.CORPORATES_CA),
    
    # Corporates - CA/ME Combined
    ("ebrd", "EBRD", "articles.corporates.CA_ME.ebrd", ExtractorCategory.CORPORATES_CA_ME),
    ("snp_cp", "S&P Corporates", "articles.corporates.CA_ME.snp", ExtractorCategory.CORPORATES_CA_ME),
    ("cp_adb_articles", "ADB Corporates Both", "articles.corporates.CA_ME.adb", ExtractorCategory.CORPORATES_CA_ME),
    
    # Corporates - Rating Actions
    ("crop_ra_ca_moodys", "Moody's Rating Actions CA Corp", "articles.corporates.ratingactions.moodys_ca", ExtractorCategory.CORPORATES_RATING),
    ("crop_ra_me_moodys", "Moody's Rating Actions ME Corp", "articles.corporates.ratingactions.moodys_me", ExtractorCategory.CORPORATES_RATING),
    ("fitch_racs_mecp", "Fitch Rating Actions ME Corp", "articles.corporates.ratingactions.racs_cpme_fitch", ExtractorCategory.CORPORATES_RATING),
    ("fitch_racs_cacp", "Fitch Rating Actions CA Corp", "articles.corporates.ratingactions.racs_cpca_fitch", ExtractorCategory.CORPORATES_RATING),
    
    # Sovereigns - Middle East
    ("gulfnews_sov", "Gulf News Sovereigns", "articles.sovereigns.middleeast.gulfnews_sov", ExtractorCategory.SOVEREIGNS_ME),
    ("khaleejtimes_sov", "Khaleej Times Sovereigns", "articles.sovereigns.middleeast.khaleejtimes", ExtractorCategory.SOVEREIGNS_ME),
    ("sov_fitch", "Fitch Sovereigns", "articles.sovereigns.middleeast.fitch", ExtractorCategory.SOVEREIGNS_ME),
    ("imf_sov", "IMF Sovereigns", "articles.sovereigns.middleeast.imf", ExtractorCategory.SOVEREIGNS_ME),
    ("sov_me_ifc", "IFC ME Sovereigns", "articles.sovereigns.middleeast.ifc", ExtractorCategory.SOVEREIGNS_ME),
    ("isdb_sov", "IsDB Sovereigns", "articles.sovereigns.middleeast.isdb", ExtractorCategory.SOVEREIGNS_ME),
    ("me_sov_worldbank", "World Bank ME Sovereigns", "articles.sovereigns.middleeast.worldbank", ExtractorCategory.SOVEREIGNS_ME),
    ("arabnews_sov", "Arab News Sovereigns", "articles.sovereigns.middleeast.arabnews", ExtractorCategory.SOVEREIGNS_ME),
    ("sov_me_moodys", "Moody's ME Sovereigns", "articles.sovereigns.middleeast.moodys", ExtractorCategory.SOVEREIGNS_ME),
    
    # Sovereigns - Central Asia
    ("sov_ca_fitch", "Fitch CA Sovereigns", "articles.sovereigns.centralasia.fitch", ExtractorCategory.SOVEREIGNS_CA),
    ("sov_kursiv", "Kursiv Sovereigns", "articles.sovereigns.centralasia.kursiv", ExtractorCategory.SOVEREIGNS_CA),
    ("imf_ca_sov", "IMF CA Sovereigns", "articles.sovereigns.centralasia.imf", ExtractorCategory.SOVEREIGNS_CA),
    ("ca_sov_worldbank", "World Bank CA Sovereigns", "articles.sovereigns.centralasia.worldbank", ExtractorCategory.SOVEREIGNS_CA),
    ("sov_ca_ifc", "IFC CA Sovereigns", "articles.sovereigns.centralasia.ifc", ExtractorCategory.SOVEREIGNS_CA),
    ("adb_sov", "ADB Sovereigns", "articles.sovereigns.centralasia.adb", ExtractorCategory.SOVEREIGNS_CA),
    ("sov_uzdaily", "Uzdaily Sovereigns", "articles.sovereigns.centralasia.uzdaily", ExtractorCategory.SOVEREIGNS_CA),
    ("nurkz_sov", "Nur.kz Sovereigns", "articles.sovereigns.centralasia.nurkz", ExtractorCategory.SOVEREIGNS_CA),
    ("sov_ca_moodys", "Moody's CA Sovereigns", "articles.sovereigns.centralasia.moodys", ExtractorCategory.SOVEREIGNS_CA),
    
    # Sovereigns - CA/ME Combined
    ("snp_sov", "S&P Sovereigns", "articles.sovereigns.CA_ME.snp", ExtractorCategory.SOVEREIGNS_CA_ME),
    
    # Sovereigns - Rating Actions
    ("fitch_racs_me_sov", "Fitch Rating Actions ME Sov", "articles.sovereigns.ratingactions.fitch_racs_me_sov", ExtractorCategory.SOVEREIGNS_RATING),
    ("fitch_racs_ca_sov", "Fitch Rating Actions CA Sov", "articles.sovereigns.ratingactions.fitch_racs_ca_sov", ExtractorCategory.SOVEREIGNS_RATING),
    ("sov_ra_me_moodys", "Moody's Rating Actions ME Sov", "articles.sovereigns.ratingactions.moodys_me", ExtractorCategory.SOVEREIGNS_RATING),
    ("sov_ra_ca_moodys", "Moody's Rating Actions CA Sov", "articles.sovereigns.ratingactions.moodys_ca", ExtractorCategory.SOVEREIGNS_RATING),
    
    # Global
    ("global_moodys", "Moody's Global", "articles.global_.moodys", ExtractorCategory.GLOBAL),
    ("global_fitch", "Fitch Global", "articles.global_.fitch", ExtractorCategory.GLOBAL),
    ("snp_global", "S&P Global", "articles.global_.snp", ExtractorCategory.GLOBAL),
    
    # Events
    ("adb_events", "ADB Events", "events.adb", ExtractorCategory.EVENTS),
    ("imf_events", "IMF Events", "events.imf", ExtractorCategory.EVENTS),
    ("fitch_events", "Fitch Events", "events.fitch", ExtractorCategory.EVENTS),
    ("ifc_events", "IFC Events", "events.ifc", ExtractorCategory.EVENTS),
    ("snp_events", "S&P Events", "events.snp", ExtractorCategory.EVENTS),
    ("bloomberg_events", "Bloomberg Events", "events.bloomberg", ExtractorCategory.EVENTS),
    ("moodys_events", "Moody's Events", "events.moodys", ExtractorCategory.EVENTS),
    
    # Publications
    ("deloitte_publications", "Deloitte Publications", "publications.deloitte", ExtractorCategory.PUBLICATIONS),
    ("ebrd_publications", "EBRD Publications", "publications.ebrd", ExtractorCategory.PUBLICATIONS),
    ("goldmansachs_publications", "Goldman Sachs Publications", "publications.goldman", ExtractorCategory.PUBLICATIONS),
    ("imf_weo_publications", "IMF WEO Publications", "publications.imf", ExtractorCategory.PUBLICATIONS),
    ("imf_reo_publications", "IMF REO Publications", "publications.imf", ExtractorCategory.PUBLICATIONS),
    ("imf_gfsr_publications", "IMF GFSR Publications", "publications.imf", ExtractorCategory.PUBLICATIONS),
    ("oecd_publications", "OECD Publications", "publications.oecd", ExtractorCategory.PUBLICATIONS),
    ("weforum_publications", "WEForum Publications", "publications.weform", ExtractorCategory.PUBLICATIONS),
    ("worldbank_publications", "World Bank Publications", "publications.worldbank", ExtractorCategory.PUBLICATIONS),
    
    # Methodologies
    ("save_all_methodologies", "Save All Methodologies", "utils.db", ExtractorCategory.METHODOLOGIES),
]


async def populate_extractors():
    """Populate database with all extractors."""
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # Check if already populated
        from sqlalchemy import select, func
        count = await db.execute(select(func.count()).select_from(Extractor))
        if count.scalar() > 0:
            logger.info("Database already populated, skipping")
            return
        
        logger.info(f"Populating {len(EXTRACTORS_CONFIG)} extractors")
        
        for func_name, display_name, module_path, category in EXTRACTORS_CONFIG:
            extractor = Extractor(
                name=func_name,
                display_name=display_name,
                module_path=module_path,
                function_name=func_name,
                category=category,
                enabled=True,
                schedule_interval_minutes=60,  # Default 1 hour
                description=f"{display_name} extractor for {category.value}"
            )
            db.add(extractor)
        
        await db.commit()
        logger.info("Database populated successfully")


if __name__ == "__main__":
    asyncio.run(populate_extractors())
