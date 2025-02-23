class Information:
    APP_INFO = {
        'version': 'v.1.0.0.20250210',
        'author': 'Adhikary, Deepraj',
        'creationDate': '2024-11-23',
        'lastReleaseDate': '2024-12-29'
    }

    JOB_DETAILS = {
        'jobStartYear': 2018,
        'jobStartMonthNumber': 6
    }


class Authentication:
    EXPIRATION = {
        'inSeconds': 86400,
        'inDays': 1
    }

    API_USAGE = {
        'basic': 100
    }

    SQL_STATEMENTS = {
        'activeToken': {
            'getTokenByClientId': r"SELECT bearerToken, expirationDtTm, apiHitCount, rowId, maxApiHitsAllowed from authenticationToken where isActive = 1 and clientId = '?'",
            'getAllTokens': r"SELECT rowId, clientId, expirationDtTm from authenticationToken where isActive = 1"
        },
        'existingToken': {
            'getTokenInformationByToken': r"SELECT rowId, bearerToken, creationDtTm, expirationDtTm, lastUsedDtTm, apiHitCount, isActive, maxApiHitsAllowed from authenticationToken where bearerToken = '?'",
            'getTokenInformationByClientId': r"SELECT rowId, bearerToken, creationDtTm, expirationDtTm, lastUsedDtTm, apiHitCount, isActive, maxApiHitsAllowed from authenticationToken where clientId = '?'"
        },
        'latestToken': {
            'getLatestTokenGenerationDatetime': r"SELECT max(creationDtTm) from authenticationToken where clientId = '?'"
        },
        'insertStatements': {
            'insertNewToken': r"INSERT INTO authenticationToken (clientId, bearerToken, creationDtTm, expirationDtTm, isActive) VALUES ('@clientId', '@bearerToken', '@creationDtTm', '@expirationDtTm', @isActive)",
        },
        'updateStatements': {
            'updateTokenUsage': r"UPDATE authenticationToken set apiHitCount = @apiHitCount, lastUsedDtTm = '@lastUsedDtTm' where clientId = '@clientId' and bearerToken = '@bearerToken' and isActive = 1",
            'deactivateToken': r"UPDATE authenticationToken set isActive = 0 where clientId = '@clientId' and rowId = @rowId"
        }
    }


class Logging:
    FILE_PATH = {
        'logFilePath': r".\logs\applicationLogs.log"
    }


class DataQueries:
    SELECT_QUERY = {
        'common': {
            'getTestQuery': r"SELECT * FROM typeInfo",
            'getSectionByName': r"SELECT whenToRead FROM stotraSuktaMantraInfo where name like '?%'",
            'getSectionByID': r"SELECT whenToRead FROM stotraSuktaMantraInfo where ssmid like '?%'",
            'getIDByEnglishName': r"SELECT MIN(ssmid) from nameTransliteration where iastTranslation like '%?%' or enTranslation like '%?%'",
            'getDevanagariNameByID': r"SELECT distinct name from stotraSuktaMantraInfo where ssmid = ?",
        },
        'introductory': {
            'getAllVersesByName': r"SELECT d.vrID, d.verseNo, d.completeVerse FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.name like '?%' ORDER BY d.vrID ASC",
            'getAllIntroductionVerses': r"SELECT d.completeVerse, d.verseNo, d.vrID FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.whenToRead = 'Intro' ORDER BY d.vrID ASC",
            'getIntroductionVerseNames': r"SELECT DISTINCT name FROM stotraSuktaMantraInfo WHERE whenToRead = 'Intro' ORDER BY orderId ASC",
            'getIntroductionVerseByVerseId': r"SELECT d.vrID, d.verseNo, d.completeVerse FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where d.vrID = ? and s.whenToRead = 'Intro' ORDER BY d.vrID ASC",
            'getShlokaNameByVerseId': r"select ssmi.name, ssmi.classification from stotraSuktaMantraInfo ssmi inner join deviSaptashatiOtherVerses dsov on dsov.ssmID = ssmi.ssmId where dsov.vrID in (?)",
        },
        'chapters': {
            'getChapterVerseNames': r"SELECT DISTINCT name FROM stotraSuktaMantraInfo WHERE whenToRead = 'Main' ORDER BY orderId ASC",
            'getChapterVersesByName': r"select d.rowID, d.verseNo, d.chapterVerse from stotraSuktaMantraInfo s inner join deviSaptashatiChapters d on d.ssmID = s.ssmId where s.name like '?%' or s.classification like '?%' order by d.rowID asc",
            'getChapterVersesByVerseId': r"select d.rowID, d.verseNo, d.chapterVerse from stotraSuktaMantraInfo s inner join deviSaptashatiChapters d on d.ssmID = s.ssmId where s.whenToRead = 'Main' and d.rowID = ? or s.classification like '?%' order by d.rowID asc",
            'getAllChapterVerses': r"select d.chapterVerse, d.verseNo, d.rowID from stotraSuktaMantraInfo s inner join deviSaptashatiChapters d on d.ssmID = s.ssmId where s.whenToRead = 'Main' order by d.rowID asc",
            'getChapterNameByVerseId': r"select cni2.charitraName, cni.chapterName from stotraSuktaMantraInfo ssmi inner join deviSaptashatiChapters dsc on dsc.ssmID = ssmi.ssmId inner join chapterNameInfo cni on cni.chapterNo = dsc.chapterNo inner join charitraNameInfo cni2 on cni2.charitraNo = dsc.charitraNo where dsc.rowID in (?)",
        },
        'concluding': {
            'getAllVersesByName': r"SELECT d.vrID, d.verseNo, d.completeVerse FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.name like '?%' ORDER BY d.vrID ASC",
            'getConcludingVerseNames': r"SELECT DISTINCT name FROM stotraSuktaMantraInfo WHERE whenToRead = 'Exit' ORDER BY orderId ASC",
            'getExitVerseByVerseId': r"SELECT d.vrID, d.verseNo, d.completeVerse  FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where d.vrID = ? and s.whenToRead = 'Exit' ORDER BY d.vrID ASC",
            'getAllConcludingVerses': r"SELECT d.completeVerse, d.verseNo, d.vrID FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.whenToRead = 'Exit' ORDER BY d.vrID ASC",
            'getShlokaNameByVerseId': r"select ssmi.name, ssmi.classification from stotraSuktaMantraInfo ssmi inner join deviSaptashatiOtherVerses dsov on dsov.ssmID = ssmi.ssmId where dsov.vrID in (?)",
        },
        'meanings': {
            'getEnglishMeaningsByVerseId': r"SELECT englishMeaning FROM shlokaTransLiterationMeaning where vrID = '?'",
            'getHindiMeaningsByVerseId': r"SELECT devanagariMeaning FROM shlokaTransLiterationMeaning where vrID = '?'",
            'getChapterVersesMeanings': r"SELECT englishMeaning, devanagariMeaning FROM chaptersShlokaTransLiterationMeaning where rowID = '?'",
        },
        'translation': {
            'getVerseIASTTranslationByVerseId': r"SELECT latinTranslation FROM shlokaTransLiterationMeaning where vrID = '?'",
            'getChapterVersesIASTTranslation': r"SELECT latinTranslation FROM chaptersShlokaTransLiterationMeaning where rowID = '?'",
            'getIASTTranslatedChapterName': r"select chapterNameIAST from chapterNameInfo where chapterName like '%?%'",
            'getIASTTranslatedCharitraName': r"Select cni2.charitraNameIAST from chapterNameInfo cni inner join chapterCharitraMapping ccm on ccm.chapterNo = cni.chapterNo inner join charitraNameInfo cni2 on cni2.charitraNo = ccm.charitraNo where cni.chapterName like '%?%'",
            'getDevanagariVerseNameByIASTName': r"SELECT DISTINCT name from stotraSuktaMantraInfo ssmi INNER JOIN chapterNameInfo cni on cni.chapterName = ssmi.name where cni.chapterNameEn like '%?%'",
            'getIASTNameTranslationByID': r"SELECT iastTranslation from nameTransliteration where ssmid = ?",
            'getEnglishNameTranslationByID': r"SELECT enTranslation from nameTransliteration where ssmid = ?",
            'getIASTNameTranslationByDevanagariName': r"SELECT iastTranslation from nameTransliteration nt INNER JOIN stotraSuktaMantraInfo ssm on ssm.ssmid = nt.ssmid where ssm.name like '%?%'",
            'getEnglishNameTranslationByDevanagariName': r"SELECT enTranslation from nameTransliteration nt INNER JOIN stotraSuktaMantraInfo ssm on ssm.ssmid = nt.ssmid where ssm.name like '%?%'",
        },
        'orderInformation': {
            'getVerseOrderIdByName': r"SELECT distinct readingOrderId from stotraSuktaMantraInfo where name like '%?%'",
            'getVerseTypeByName': r"SELECT DISTINCT whenToRead from stotraSuktaMantraInfo where name like '%?%'",
            'getEnglishVerseTypeByName': r"SELECT DISTINCT whenToRead from stotraSuktaMantraInfo ssmi INNER JOIN chapterNameInfo cni on cni.chapterName = ssmi.name where cni.chapterNameEn like '%?%'",
        },
    }

    VERSE_MINMAX_VALUES = {
        'getIntroductionValues': r"SELECT MIN(d.vrID), MAX(d.vrID) FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.whenToRead = 'Intro' ORDER BY d.vrID ASC",
        'getChapterValues': r"select MIN(d.rowID), MAX(d.rowID) from stotraSuktaMantraInfo s inner join deviSaptashatiChapters d on d.ssmID = s.ssmId where s.whenToRead = 'Main' order by d.rowID asc",
        'getConcludingValues': r"SELECT MIN(d.vrID), MAX(d.vrID) FROM stotraSuktaMantraInfo s INNER JOIN deviSaptashatiOtherVerses d on d.ssmID = s.ssmId where s.whenToRead = 'Exit' ORDER BY d.vrID ASC",
    }

    INSERT_QUERY = {
        'insertVerse': '',
    }

    UPDATE_QUERY = {
        'setMeaning': {
            'forEnglish': "UPDATE shlokaTransLiterationMeaning set englishMeaning = '?meaning' where stsId = ?id",
            'forHindi': "UPDATE shlokaTransLiterationMeaning set devanagariMeaning = '?meaning' where stsId = ?id"
        }
    }


class RegularExpressions:
    PATTERNS = {
        "onlyEnglish": r"[A-Za-z\s.,!?]+",
        "onlyHindi": r"[\u0900-\u097F\s]+",
        "bothEnglishAndHindi": r"([A-Za-z\s.,!?]+|[\u0900-\u097F\s]+)"
    }
