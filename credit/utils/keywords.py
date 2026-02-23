

ME_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", "bond rating", "bond issuance", "sovereign bonds",
    "M&A", "financial institutions", "financial institution", "bank bonds", "global banks","return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks",
    "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing",
    "Non Performing", "NPAs", "credit risk", "reinsurance",
    "global banking", "insurance sector", "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI"
]

sovereign_keywords =[
    "sovereign","sovereign rating","UAE", "United Arab Emirates", "Saudi Arabia", "GCC countries", "GCC", "Kuwait", "Oman", "Bahrein", "Qatar", "Dubai", "Abu Dhabi","KSA", "saudi", 
    "Middle east", "RAK","Sharjah", "Ras Al Khamiah","Gulf Cooperation Council","Persian Gulf", "Islamic Cooperation", "Arab League","Muscat","Red Sea", "Yemen", "Jordan", 
    "MENA", "OPEC", "Organization of the Petroleum Exporting Countries", "Arabic Gulf", "Arabian Sea","UAE bank","UAE banks","banking system", "Finance system","local goverment",
]

wb_sovereign_keywords =[#removed name of countries and local governments
    "sovereign","sovereign rating","GCC countries", "GCC", "Middle east", "Gulf Cooperation Council","Persian Gulf", "Islamic Cooperation", "Arab League","Muscat","Red Sea",
    "MENA", "OPEC", "Organization of the Petroleum Exporting Countries", "Arabic Gulf", "Arabian Sea",
    
    "bank","banks","banking system", "Finance system","local goverment","economic update", "growth","reforms","economic growth","economic recovery","economic outlook",
    "economic performance","economic development","economic indicators","economic activity",
]

me_kj_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review",
    
    "bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance sector", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","financial inclusion","banking sector",
    "private sector","public sector",

    "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI","World Bank"
]

me_gf_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review",
    
    "bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "insurance sector","global banking", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","financial inclusion","banking sector",

    "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI","World Bank"
]

me_sca_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review",
    
    "bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance sector","banking regulations","open banking", "financial centre", "financial center", "anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","financial inclusion","banking sector",
    "private sector","public sector",

    "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI","World Bank"
]

me_reuters_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", "bond rating", "bond issuance", "sovereign bonds",
    "M&A", "financial institutions", "financial institution", "bank bonds", "global banks","return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks",
    "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing",
    "Non Performing", "NPAs", "credit risk", "reinsurance",
    "global banking", "insurance", "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI"
]

me_wb_KEYWORDS = [#removed World Bank
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", 
    
    "bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","financial inclusion","banking sector",
    "private sector","public sector",

    "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI",
]

me_isdb_KEYWORDS = [#removed - development bank, development banks
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", 
    
    "bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance sector", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","financial inclusion","banking sector",
    "private sector","public sector",

    "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI","World Bank"
]

me_ifc_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", 
    
    "bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance sector", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","financial inclusion","banking sector",
    "private sector","public sector",

    "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI","World Bank"
]






 
CA_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", 
    
    "privatisation","bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance sector", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial services","financial system","financial technology","financial inclusion","banking sector",

    "Ministry of Investments","Money Transfers","Asia-Invest Bank", "Asian Development Bank",

    "CIS banks","National Bank of Foreign Economic Activity", "NBU", "National Bank",
    "Uzpromstroybank", "SQB", "Agrobank", "Asakabank", "Ipoteka Bank", "Kapitalbank", "Xalq Bank",
    "Qishloq Qurilish Bank", "Business Development Bank", "Hamkorbank", "Microcreditbank", "Ipak Yuli",
    "Ipak Yuli Bank", "Aloqabank","Aloqa bank", "Turonbank", "Orient Finans Bank", "Trustbank", "KDB Bank Uzbekistan",
    "KDB Bank", "Asia Alliance Bank", "Invest Finance Bank", "Davr Bank", "Ravnaq Bank", "Uzagroleasing",
    "Universal Bank", "Uzbek Leasing International", "Hi-Tech Bank", "Madad Invest Bank", "Uzagroexport Bank",
    "Ziraat Bank Uzbekistan", "Ziraat Bank", "Alfa Invest Insurance", "Euroasia Insurance", "Impex Insurance",
    "Ingo Uzbekistan Insurance", "Kafil-Sug'urta", "Mosaic", "My Insurance", "Uzbekinvest",
    "National Bank of Kazakhstan", "Halyk", "Baiterek", "Kaspi.kz", "Kaspi",
    "Kaspi Bank", "Bank CenterCredit", "Development Bank of Kazakhstan", "Otbasy Bank", "ForteBank",
    "First Heartland Jusan Bank", "Eurasian Bank", "Freedom Bank Kazakhstan", "Bereke Bank", "Bank RBK",
    "Agrarian Credit Corporation", "Citibank Kazakhstan", "Altyn Bank (China CITIC)", "Altyn Bank",
    "Home Credit Bank", "KazAgroFinance", "Shinhan Bank Kazakhstan", "Nurbank", "Damu Fund",
    "AB Bank China Kazakhstan", "Qazaq Banki", "Industrial and Commercial Bank of China (Almaty)",
    "KMF Microfinance Organization", "Kazakhstan-Ziraat International Bank", "VTB Bank Kazakhstan",
    "Al Hilal Islamic Bank", "Tengri Bank", "AsiaCredit Bank", "Capital Bank Kazakhstan",
    "Eurasian Development Bank", "KazakhExport Insurance","banking","Freedom Bank","Uzbek Industrial and Construction Bank"
]

ca_adb_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", 
    
    "privatisation","bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance sector", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","financial inclusion","banking sector",

    "CIS banks","National Bank of Foreign Economic Activity", "NBU", "National Bank",
    "Uzpromstroybank", "SQB", "Agrobank", "Asakabank", "Ipoteka Bank", "Kapitalbank", "Xalq Bank",
    "Qishloq Qurilish Bank", "Business Development Bank", "Hamkorbank", "Microcreditbank", "Ipak Yuli",
    "Ipak Yuli Bank", "Aloqabank","Aloqa bank", "Turonbank", "Orient Finans Bank", "Trustbank", "KDB Bank Uzbekistan",
    "KDB Bank", "Asia Alliance Bank", "Invest Finance Bank", "Davr Bank", "Ravnaq Bank", "Uzagroleasing",
    "Universal Bank", "Uzbek Leasing International", "Hi-Tech Bank", "Madad Invest Bank", "Uzagroexport Bank",
    "Ziraat Bank Uzbekistan", "Ziraat Bank", "Alfa Invest Insurance", "Euroasia Insurance", "Impex Insurance",
    "Ingo Uzbekistan Insurance", "Kafil-Sug'urta", "Mosaic", "My Insurance", "Uzbekinvest",
    "National Bank of Kazakhstan", "Halyk", "Baiterek", "Kaspi.kz", "Kaspi",
    "Kaspi Bank", "Bank CenterCredit", "Development Bank of Kazakhstan", "Otbasy Bank", "ForteBank",
    "First Heartland Jusan Bank", "Eurasian Bank", "Freedom Bank Kazakhstan", "Bereke Bank", "Bank RBK",
    "Agrarian Credit Corporation", "Citibank Kazakhstan", "Altyn Bank (China CITIC)", "Altyn Bank",
    "Home Credit Bank", "KazAgroFinance", "Shinhan Bank Kazakhstan", "Nurbank", "Damu Fund",
    "AB Bank China Kazakhstan", "Qazaq Banki", "Industrial and Commercial Bank of China (Almaty)",
    "KMF Microfinance Organization", "Kazakhstan-Ziraat International Bank", "VTB Bank Kazakhstan",
    "Al Hilal Islamic Bank", "Tengri Bank", "AsiaCredit Bank", "Capital Bank Kazakhstan",
    "Eurasian Development Bank", "KazakhExport Insurance","banking","Freedom Bank","Uzbek Industrial and Construction Bank"
]

ca_kzkursiv_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", 
    
    "privatisation","bond issuance", "sovereign bonds","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance sector", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial services","financial system","financial technology","financial inclusion","banking sector",
    "private sector","public sector",

    "Ministry of Investments","Money Transfers","Asia-Invest Bank", "Asian Development Bank",
    
    "CIS banks","National Bank of Foreign Economic Activity", "NBU", "National Bank",
    "Uzpromstroybank", "SQB", "Agrobank", "Asakabank", "Ipoteka Bank", "Kapitalbank", "Xalq Bank",
    "Qishloq Qurilish Bank", "Business Development Bank", "Hamkorbank", "Microcreditbank", "Ipak Yuli",
    "Ipak Yuli Bank", "Aloqabank","Aloqa bank", "Turonbank", "Orient Finans Bank", "Trustbank", "KDB Bank Uzbekistan",
    "KDB Bank", "Asia Alliance Bank", "Invest Finance Bank", "Davr Bank", "Ravnaq Bank", "Uzagroleasing",
    "Universal Bank", "Uzbek Leasing International", "Hi-Tech Bank", "Madad Invest Bank", "Uzagroexport Bank",
    "Ziraat Bank Uzbekistan", "Ziraat Bank", "Alfa Invest Insurance", "Euroasia Insurance", "Impex Insurance",
    "Ingo Uzbekistan Insurance", "Kafil-Sug'urta", "Mosaic", "My Insurance", "Uzbekinvest",
    "National Bank of Kazakhstan", "Halyk", "Baiterek", "Kaspi.kz", "Kaspi",
    "Kaspi Bank", "Bank CenterCredit", "Development Bank of Kazakhstan", "Otbasy Bank", "ForteBank",
    "First Heartland Jusan Bank", "Eurasian Bank", "Freedom Bank Kazakhstan", "Bereke Bank", "Bank RBK",
    "Agrarian Credit Corporation", "Citibank Kazakhstan", "Altyn Bank (China CITIC)", "Altyn Bank",
    "Home Credit Bank", "KazAgroFinance", "Shinhan Bank Kazakhstan", "Nurbank", "Damu Fund",
    "AB Bank China Kazakhstan", "Qazaq Banki", "Industrial and Commercial Bank of China (Almaty)",
    "KMF Microfinance Organization", "Kazakhstan-Ziraat International Bank", "VTB Bank Kazakhstan",
    "Al Hilal Islamic Bank", "Tengri Bank", "AsiaCredit Bank", "Capital Bank Kazakhstan",
    "Eurasian Development Bank", "KazakhExport Insurance","banking","Freedom Bank","Uzbek Industrial and Construction Bank"
]

ca_uzkursiv_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology",
    "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "credit rating scale",
    "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria",
    "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review",
    "bond rating", "bond issuance", "sovereign bonds", "M&A", "banks", "bank", "financial institutions", "financial institution", "bank bonds", "global banks",
    "global banking", "CIS banks", "insurance sector", "National Bank of Foreign Economic Activity", "NBU", "National Bank",
    "Uzpromstroybank", "SQB", "Agrobank", "Asakabank", "Ipoteka Bank", "Kapitalbank", "Xalq Bank",
    "Qishloq Qurilish Bank", "Business Development Bank", "Hamkorbank", "Microcreditbank", "Ipak Yuli",
    "Ipak Yuli Bank", "Aloqabank", "Aloqa Bank" , "Turonbank", "Orient Finans Bank", "Trustbank", "KDB Bank Uzbekistan",
    "KDB Bank", "Asia Alliance Bank", "Invest Finance Bank", "Davr Bank", "Ravnaq Bank", "Uzagroleasing",
    "Universal Bank", "Uzbek Leasing International", "Hi-Tech Bank", "Madad Invest Bank", "Uzagroexport Bank",
    "Ziraat Bank Uzbekistan", "Ziraat Bank", "Alfa Invest Insurance", "Euroasia Insurance", "Impex Insurance",
    "Ingo Uzbekistan Insurance", "Kafil-Sug'urta", "Mosaic", "My Insurance", "Uzbekinvest",
    "National Bank of Kazakhstan", "Halyk", "Baiterek", "Kaspi.kz", "Kaspi",
    "Kaspi Bank", "Bank CenterCredit", "Development Bank of Kazakhstan", "Otbasy Bank", "ForteBank",
    "First Heartland Jusan Bank", "Eurasian Bank", "Freedom Bank Kazakhstan", "Bereke Bank", "Bank RBK",
    "Agrarian Credit Corporation", "Citibank Kazakhstan", "Altyn Bank (China CITIC)", "Altyn Bank",
    "Home Credit Bank", "KazAgroFinance", "Shinhan Bank Kazakhstan", "Nurbank", "Damu Fund",
    "AB Bank China Kazakhstan", "Qazaq Banki", "Industrial and Commercial Bank of China (Almaty)",
    "KMF Microfinance Organization", "Kazakhstan-Ziraat International Bank", "VTB Bank Kazakhstan",
    "Al Hilal Islamic Bank", "Tengri Bank", "AsiaCredit Bank", "Capital Bank Kazakhstan",
    "Eurasian Development Bank", "KazakhExport Insurance","banking","Freedom Bank"
]

ca_wb_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", 
    
    "privatisation","bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance sector", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","financial inclusion","banking sector",
    "private sector","public sector",
    
    "CIS banks","National Bank of Foreign Economic Activity", "NBU", "National Bank",
    "Uzpromstroybank", "SQB", "Agrobank", "Asakabank", "Ipoteka Bank", "Kapitalbank", "Xalq Bank",
    "Qishloq Qurilish Bank", "Business Development Bank", "Hamkorbank", "Microcreditbank", "Ipak Yuli",
    "Ipak Yuli Bank", "Aloqabank","Aloqa bank", "Turonbank", "Orient Finans Bank", "Trustbank", "KDB Bank Uzbekistan",
    "KDB Bank", "Asia Alliance Bank", "Invest Finance Bank", "Davr Bank", "Ravnaq Bank", "Uzagroleasing",
    "Universal Bank", "Uzbek Leasing International", "Hi-Tech Bank", "Madad Invest Bank", "Uzagroexport Bank",
    "Ziraat Bank Uzbekistan", "Ziraat Bank", "Alfa Invest Insurance", "Euroasia Insurance", "Impex Insurance",
    "Ingo Uzbekistan Insurance", "Kafil-Sug'urta", "Mosaic", "My Insurance", "Uzbekinvest",
    "National Bank of Kazakhstan", "Halyk", "Baiterek", "Kaspi.kz", "Kaspi",
    "Kaspi Bank", "Bank CenterCredit", "Development Bank of Kazakhstan", "Otbasy Bank", "ForteBank",
    "First Heartland Jusan Bank", "Eurasian Bank", "Freedom Bank Kazakhstan", "Bereke Bank", "Bank RBK",
    "Agrarian Credit Corporation", "Citibank Kazakhstan", "Altyn Bank (China CITIC)", "Altyn Bank",
    "Home Credit Bank", "KazAgroFinance", "Shinhan Bank Kazakhstan", "Nurbank", "Damu Fund",
    "AB Bank China Kazakhstan", "Qazaq Banki", "Industrial and Commercial Bank of China (Almaty)",
    "KMF Microfinance Organization", "Kazakhstan-Ziraat International Bank", "VTB Bank Kazakhstan",
    "Al Hilal Islamic Bank", "Tengri Bank", "AsiaCredit Bank", "Capital Bank Kazakhstan",
    "Eurasian Development Bank", "KazakhExport Insurance","banking","Freedom Bank","Uzbek Industrial and Construction Bank"
]

ca_fitch_KEYWORDS = [
    "S&P Global", "Moody's", "credit rating agency", "rating methodology",
    "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "credit rating scale",
    "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria",
    "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review",
    "bond rating", "bond issuance", "sovereign bonds", "M&A",
    "banks", "bank", "financial institutions", "financial institution", "bank bonds", "global banks",
    "global banking", "CIS banks", "insurance", "National Bank of Foreign Economic Activity", "NBU", "National Bank",
    "Uzpromstroybank", "SQB", "Agrobank", "Asakabank", "Ipoteka Bank", "Kapitalbank", "Xalq Bank",
    "Qishloq Qurilish Bank", "Business Development Bank", "Hamkorbank", "Microcreditbank", "Ipak Yuli",
    "Ipak Yuli Bank", "Aloqabank","Aloqa bank", "Turonbank", "Orient Finans Bank", "Trustbank", "KDB Bank Uzbekistan",
    "KDB Bank", "Asia Alliance Bank", "Invest Finance Bank", "Davr Bank", "Ravnaq Bank", "Uzagroleasing",
    "Universal Bank", "Uzbek Leasing International", "Hi-Tech Bank", "Madad Invest Bank", "Uzagroexport Bank",
    "Ziraat Bank Uzbekistan", "Ziraat Bank", "Alfa Invest Insurance", "Euroasia Insurance", "Impex Insurance",
    "Ingo Uzbekistan Insurance", "Kafil-Sug'urta", "Mosaic", "My Insurance", "Uzbekinvest",
    "National Bank of Kazakhstan", "Halyk", "Baiterek", "Kaspi.kz", "Kaspi",
    "Kaspi Bank", "Bank CenterCredit", "Development Bank of Kazakhstan", "Otbasy Bank", "ForteBank",
    "First Heartland Jusan Bank", "Eurasian Bank", "Freedom Bank Kazakhstan", "Bereke Bank", "Bank RBK",
    "Agrarian Credit Corporation", "Citibank Kazakhstan", "Altyn Bank (China CITIC)", "Altyn Bank",
    "Home Credit Bank", "KazAgroFinance", "Shinhan Bank Kazakhstan", "Nurbank", "Damu Fund",
    "AB Bank China Kazakhstan", "Qazaq Banki", "Industrial and Commercial Bank of China (Almaty)",
    "KMF Microfinance Organization", "Kazakhstan-Ziraat International Bank", "VTB Bank Kazakhstan",
    "Al Hilal Islamic Bank", "Tengri Bank", "AsiaCredit Bank", "Capital Bank Kazakhstan",
    "Eurasian Development Bank", "KazakhExport Insurance","World Bank","banking","Freedom Bank"
]











COMMON_KEYWORDS = [
    "Fitch Ratings","Moody's", "credit rating", "credit rating agency", "rating methodology",
    "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "credit rating scale",
    "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria",
    "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review",
    "banks", "bank", "financial institutions", "financial institution", "insurance", "bond issuance",
    "sovereign bonds", "M&A", "bank bonds", "global banks", "global banking", "banking system", "Finance system", "Basel", "banking regulations","banking","NPLs","Non-Performing",
    "Non Performing", "NPAs", "credit risk", "reinsurance",
]
 
MIDDLEEAST_COUNTRY_KEYWORDS = ["UAE", "United Arab Emirates", "Saudi Arabia", "GCC countries", "GCC", "Kuwait", "Oman", "Bahrein", "Qatar", "Dubai", "Abu Dhabi","KSA", "saudi", "Middle east", "RAK","Sharjah", "Ras Al Khamiah","Gulf Cooperation Council",
                               "Persian Gulf", "Islamic Cooperation", "Arab League","Muscat","Red Sea", "Yemen", "Jordan", "MENA", "OPEC", "Organization of the Petroleum Exporting Countries", "Arabic Gulf", "Arabian Sea"]

CENTRALASIA_COUNTRY_KEYWORDS = ["Uzbekistan", "Kazakhstan", "Asia and Pacific", "Central Asia","Azerbaijan","Armenia","Turkmenistan","Kyrgyzstan","Tajikistan","Silk Road","Caspian Sea","Eurasia", "Post-Soviet States","Tashkent","Almaty",
                                "Samarkand","Economic Cooperation Organization","Silk Route"]

MIDDLEEAST_RARE_KEYWORDS = ["First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI","World Bank"
    ]

CENTERALASIA_RARE_KEYWORDS = ["CIS banks", "National Bank of Foreign Economic Activity", "NBU",
    "Uzpromstroybank", "SQB", "Agrobank", "Asakabank", "Ipoteka Bank", "Kapitalbank", "Xalq Bank",
    "Qishloq Qurilish Bank", "Business Development Bank", "Hamkorbank", "Microcreditbank", "Ipak Yuli",
    "Ipak Yuli Bank", "Aloqabank","Aloqa bank", "Turonbank", "Orient Finans Bank", "Trustbank", "KDB Bank Uzbekistan",
    "KDB Bank", "Asia Alliance Bank", "Invest Finance Bank", "Davr Bank", "Ravnaq Bank", "Uzagroleasing",
    "Universal Bank", "Uzbek Leasing International", "Hi-Tech Bank", "Madad Invest Bank", "Uzagroexport Bank",
    "Ziraat Bank Uzbekistan", "Ziraat Bank", "Alfa Invest Insurance", "Euroasia Insurance", "Impex Insurance",
    "Ingo Uzbekistan Insurance", "Kafil-Sug'urta", "Mosaic", "My Insurance", "Uzbekinvest",
    "National Bank of Kazakhstan", "Halyk", "Baiterek", "Kaspi.kz", "Kaspi",
    "Kaspi Bank", "Bank CenterCredit", "Development Bank of Kazakhstan", "Otbasy Bank", "ForteBank",
    "First Heartland Jusan Bank", "Eurasian Bank", "Freedom Bank Kazakhstan", "Bereke Bank", "Bank RBK",
    "Agrarian Credit Corporation", "Citibank Kazakhstan", "Altyn Bank (China CITIC)", "Altyn Bank",
    "Home Credit Bank", "KazAgroFinance", "Shinhan Bank Kazakhstan", "Nurbank", "Damu Fund",
    "AB Bank China Kazakhstan", "Qazaq Banki", "Industrial and Commercial Bank of China (Almaty)",
    "KMF Microfinance Organization", "Kazakhstan-Ziraat International Bank", "VTB Bank Kazakhstan",
    "Al Hilal Islamic Bank", "Tengri Bank", "AsiaCredit Bank", "Capital Bank Kazakhstan","Asian Development Bank","ADB",
    "Eurasian Development Bank", "KazakhExport Insurance"]

REGIONAL_KEYWORDS = {
    "MiddleEast": MIDDLEEAST_COUNTRY_KEYWORDS,
    "CentralAsia": CENTRALASIA_COUNTRY_KEYWORDS,
}

RARE_KEYWORDS = {
    "MiddleEast": MIDDLEEAST_RARE_KEYWORDS,
    "CentralAsia": CENTERALASIA_RARE_KEYWORDS,
}

CP_MIDDLEEAST_KEYWORDS = [
    "corporate rating", "corporate bonds", "debt capital market", "corporate sukuk", "Sukuk issuance", 
    "bond issuance", "green bonds", "Abu Dhabi National Energy Company", "TAQA", "National Central Cooling", 
    "Vista Global Holding", "ABU DHABI FUTURE ENERGY COMPANY", "Masdar", "DP WORLD", "Shelf Drilling Holdings", 
    "Fertiglobe", "Abu Dhabi Ports Company", "AD Ports Group", "Senaat", "EQUATE Sukuk", "Kuwait Projects", 
    "Damac", "Emaar", "Emirates Telecommunications Group Company", "Etisalat", "Aldar", "ADNOC", "Mamoura", 
    "Abu Dhabi Developmental Holding Company", "DUBAI AEROSPACE ENTERPRISE", "Majid Al Futtaim", "ACWA", 
    "EMIRATES SEMB CORP WATER AND POWER COMPANY", "EWEC", "Oztel", "RUWAIS", "SWEIHAN", "Abu Dhabi Crude Oil Pipeline", 
    "ADCOP", "Dae Funding", "Five Holdings", "Dubai Electricity and Water Authority", "DEWA", "Arada Developments", 
    "Ittihad International Investment", "DIFC Investments", "Emirates Strategic Investment Company", 
    "Private Department", "Taghleef Industries Holdco", "Taghleef Industries Topco", "Vantage Drilling International", 
    "Emirates Airline", "Telford Offshore", "Aerotranscargo FZE", "Brooge Petroleum and Gas Investment Company FZC", 
    "Telford Finco", "ACWA Power Capital Management", "2Rivers DMCC", "Eros Media World", "MRV Holding", 
    "Habtoor International", "A D N H Catering", "Abu Dhabi Aviation", "Abu Dhabi National for Building Materials", 
    "Abu Dhabi National Hotels", "Abu Dhabi National Oil Company For Distribution", "Abu Dhabi Ship Building", 
    "ADNOC Drilling Company", "ADNOC Gas", "ADNOC Logistics & Services", "Agility Global", "Agthia Group", 
    "Air Arabia", "AL KHALEEJ Investment", "Al Seer Marine Supplies & Equipment Company", "Alef Education Holding", 
    "Alpha Dhabi Holding", "Americana Restaurants International", "APEX INVESTMENT", "Aram Group", "Aramex", 
    "Borouge", "BURJEEL HOLDINGS", "Dana Gas", "Depa", "Deyaar Development", "Drake & Scull International", 
    "Dubai Investments", "Dubai Taxi Company", "E7 Group", "Easy Lease Motorcycle Rental", "Emaar Development", 
    "Emirates Central Cooling Systems Corporation", "Emirates Driving Company", "Emirates Integrated Telecommunications Company", 
    "Emirates Reem Investments", "EMSTEEL BUILDING MATERIALS", "ESG EMIRATES STALLIONS GROUP", "ESHRAQ INVESTMENTS", 
    "FOODCO NATIONAL FOODSTUFF", "Fujairah Building Industries", "Fujairah Cement Industries", "Ghitha Holding", 
    "Gulf Cement Co", "Gulf Medical Projects Company", "Gulf Navigation Holding", "Gulf Pharmaceutical Industries", 
    "HILY HOLDING", "International Holding Company", "Manazel", "MBME GROUP", "Modon Holding", "National Cement Co", 
    "National Corporation for Tourism & Hotels", "NATIONAL MARINE DREDGING COMPANY", "NMDC Energy", "Orascom Construction", 
    "PALMS SPORTS", "Parkin Company", "PHOENIX GROUP", "Presight AI Holding", "Pure Health Holding", "RAK Ceramics", 
    "RAK Properties", "Ras Al Khaimah Co for White Cement & Construction Materials", "Salik Company", 
    "Sharjah Cement and Industrial Development Company", "SPACE42", "Spinneys 1961 Holding", "Taaleem Holdings", 
    "Tecom Group", "Union Properties"
]

CP_CENTRALASIA_KEYWORDS = [
    "corporate rating", "corporate bonds", "standalone credit profile", "issuer default rating", 
    "recovery rating", "recovery percentage", "government related entity", "corporate family rating", 
    "Navoi Mining and Metallurgical", "Navoi Mining and Metallurgy", "Navoiyuran", 
    "Almalyk Mining and Metallurgical", "Almalyk Mining and Metallurgy", "Almalyk MMC", 
    "Uzbek Metallurgical", "Uzbek Metallurgy", "Uzmetkombinat", "Uzbekneftegaz", "Uztransgaz", 
    "Hududgazta'minot", "Hududgaz", "UzGasTrade", "National Electric Grid of Uzbekistan", 
    "National Electric Grids of Uzbekistan", "Thermal Power Plants", "Regional Electrical Power Networks", 
    "Uzbekgeofizika", "Uzkimyosanoat", "Navoiyazot", "Navoi-Azot", "Navoiazot", 
    "Uzbek Railways", "Oʻzbekiston temir yoʻllari", "O'zbekiston Temir Yollari", 
    "Uzbekiston Temir Yollari", "Ozbekiston Temir Yollari", "Uzbekistan Railways", 
    "Uzbekistan Airways", "Uzbekistan Airports", "Toshshahartransxizmat", "UzAuto", 
    "Uz Auto", "Uzautosanoat", "Uzauto-sanoat", "Uzbektelecom", "Uzbek telecom", 
    "Uztelecom", "O'zbekiston pochtasi", "UzPost", "Uzbekistan Post", "Uzbekcoal", 
    "Artel Electronics", "Dehkanabad Potash Plant", "Dekhkanabad plant of potassium", 
    "Toshkent Metallurgiya Zavodi", "Tashkent Metallurgical Plant", "Tashkent Metallurgy Plant", 
    "SamAuto", "Samarqand Avtomobil zavodi", "SamAvto", "Akfa Aluminium", "Enter Engineering", 
    "Saneg", "Sanoat Energetika Guruhi", "Fargonaazot", "Farg'onaazot", "Hududiy Elektr Tarmoqla", 
    "Uzsungwoo", "QuvasoyCement", "Quvasoy Cement", "Kuvasaycement", "POSCO International Textile", 
    "Promxim Impex", "Kazakhstan Housing Company", "Samruk-Energy", "Samruk-Energo", 
    "Samruk Energy", "Samruk Energo", "Ekibastuz GRES-1", "Ekibastuz GRES 1", 
    "Samruk-Kazyna Construction", "Samruk Kazyna Construction", "Kazpost", "QazPost", 
    "Kazakhtelecom", "Kcell", "Kazakhstan Electricity Grid Operating Company", "KEGOC", 
    "KazMunayGas", "KazTransOil", "Astana Gas", "Astanagas", "Astana-Gas", "QazaqGaz", 
    "Intergas Central Asia", "KazTransGas", "Kazatomprom", "Kazakhstan Temir Zholy", 
    "Qazaqstan Temır Joly", "Kaztemirtrans", "Tengizchevroil", "Eurasian Resources Group", 
    "BI Group", "Kazakhstan Utility Systems", "Mangistau Regional Electricity Network", 
    "Food Contract Corp", "Food Contract Corporation", "TransteleCom", "Kaz Minerals", 
    "Kazakhmys", "BI Development", "Alma Telecommunications", "Batys transit", 
    "KazMunaiGas", "Kaztemirtrans", "Integra Construction"
]

CP_COMMON_KEYWORDS =[ "Fitch Ratings","Moody's", "credit rating", "credit rating agency", "rating methodology",
    "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "credit rating scale",
    "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria",
    "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", "bond issuance",
    "sovereign bonds", "M&A", "credit risk", "assigns", "withdraws", "affirms", "upgrades", "downgrades", "guarantee", "guaranty", "guaranteed", "secured", "unsecured"]

CP_RARE_KEYWORDS = {
    "MiddleEast": CP_MIDDLEEAST_KEYWORDS,
    "CentralAsia": CP_CENTRALASIA_KEYWORDS,
}







