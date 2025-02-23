import config
from utilities import (sqlite_util as sql, json_response_template as resp_json, miscellaneous as misc, custom_error as error)
from mainApp.constants import (DataQueries as Query, RegularExpressions as Regex)


def search_by_verse_name(json_data_body):
    json_response = []
    data_extract = []
    iast = ''
    english = ''
    devanagari = ''
    context = ''

    try:
        if 'verseName' in json_data_body and 'lang' in json_data_body:
            verse_name = json_data_body.get('verseName').replace('\u200c', '')
            language_search = json_data_body.get('lang')

            if language_search.lower() in ['hn', 'hi', 'hin', 'hindi'] and misc.match_regex_pattern(data_input=verse_name, pattern=Regex.PATTERNS['onlyHindi']):
                get_section_name = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['common']['getSectionByName'], data_input=verse_name)
                iast = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getIASTNameTranslationByDevanagariName'], data_input=verse_name)
                english = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getEnglishNameTranslationByDevanagariName'], data_input=verse_name)
                devanagari = verse_name
            elif language_search.lower() in ['en', 'eng', 'english'] and misc.match_regex_pattern(data_input=verse_name, pattern=Regex.PATTERNS['onlyEnglish']):
                get_id = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['common']['getIDByEnglishName'], data_input=verse_name)
                if get_id is not None:
                    get_section_name = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['common']['getSectionByID'], data_input=get_id)
                    iast = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getIASTNameTranslationByID'], data_input=get_id)
                    english = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getEnglishNameTranslationByID'], data_input=get_id)
                    devanagari = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['common']['getDevanagariNameByID'], data_input=get_id)
                else:
                    raise error.InvalidInputValues(message=f'Unable to retrieve ID for the input verseName: {verse_name}')
            else:
                error_message = "Search language could not be identified. Acceptable values are 'en' for English and 'hn' for Hindi/Sanskrit/Devanagari."
                json_response = resp_json.response_template(
                    success=False,
                    message="An exception has occurred. Please refer to the 'errorInformation' for more details.",
                    data=None,
                    error=error.InvalidInputValues(message=error_message),
                    status_code=404,
                    display_error=True
                )
                return json_response

            if get_section_name.lower() in ['intro', 'exit']:
                sql_script_to_use = Query.SELECT_QUERY['introductory']['getAllVersesByName'] if get_section_name == 'intro' else Query.SELECT_QUERY['concluding']['getAllVersesByName']
                verse_list_with_id = sql.dql_fetch_all_rows_for_one_input(
                    database=config.DATABASE_URL,
                    sql_script=sql_script_to_use,
                    data_input=devanagari,
                    return_list=False
                )

                if len(verse_list_with_id) == 0:
                    error_message = "Search is unable to find any available content in the database. Please validate the search parameters or narrow down the search parameters."
                    json_response = resp_json.response_template(
                        success=False,
                        message="An exception has occurred. Please refer to the 'errorInformation' for more details.",
                        data=None,
                        error=error.DBDataExtraction(message=error_message),
                        status_code=404,
                        display_error=True
                    )
                else:
                    for verse_data in verse_list_with_id:
                        data = resp_json.populate_json_data_extract(
                            data_id=verse_data[0],
                            verse_number=verse_data[1],
                            shloka_devanagari=verse_data[2],
                            shloka_iast=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getVerseIASTTranslationByVerseId'], data_input=verse_data[0]),
                            meaning_english=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['meanings']['getEnglishMeaningsByVerseId'], data_input=verse_data[0]),
                            meaning_hindi=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['meanings']['getHindiMeaningsByVerseId'], data_input=verse_data[0]),
                            name_devanagari=devanagari,
                            name_iast=iast,
                            name_english=english
                        )
                        data_extract.append(data)
                    json_response = resp_json.response_template(success=True, message='Search completed successfully', data=data_extract, status_code=200)
                return json_response
            elif get_section_name.lower() in ['chapter', 'main']:
                sql_script_to_use = Query.SELECT_QUERY['chapters']['getChapterVersesByName']
                verse_list_with_id = sql.dql_fetch_all_rows_for_one_input(
                    database=config.DATABASE_URL,
                    sql_script=sql_script_to_use,
                    data_input=devanagari,
                    return_list=False
                )

                if len(verse_list_with_id) == 0:
                    json_response = resp_json.response_template(
                        success=False,
                        message='Search is unable to find any available content in the database. Please validate the search parameters or narrow down the search parameters.',
                        data=None,
                        error=None,
                        status_code=404
                    )
                else:
                    for verse_data in verse_list_with_id:
                        data = resp_json.populate_json_data_extract(
                            data_id=verse_data[0],
                            verse_number=verse_data[1],
                            shloka_devanagari=verse_data[2],
                            shloka_iast=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getVerseIASTTranslationByVerseId'], data_input=verse_data[0]),
                            meaning_english=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['meanings']['getEnglishMeaningsByVerseId'], data_input=verse_data[0]),
                            meaning_hindi=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['meanings']['getHindiMeaningsByVerseId'], data_input=verse_data[0]),
                            name_devanagari=devanagari,
                            name_iast=iast,
                            name_english=english
                        )
                        data_extract.append(data)
                    json_response = resp_json.response_template(success=True, message='Search completed successfully', data=data_extract, status_code=200)
                return json_response
            else:
                json_response = resp_json.response_template(success=False, message="Search couldn't be performed.", data=None, error=None, status_code=404, display_error=True)
                return json_response
        else:
            json_response = resp_json.response_template(
                success=False,
                message="Search couldn't be performed because its missing a parameter in the input request. Request much contain 'verseName' and 'lang'.",
                data=None,
                error=None,
                status_code=404,
                display_error=False
            )
            return json_response
    except Exception as err:
        json_response = resp_json.response_template(
            success=False,
            message="An exception has occurred. Please refer to the 'errorInformation' for more details.",
            data=None,
            error=err,
            status_code=404,
            display_error=True
        )
        return json_response


def search_by_verse_id(json_data_body):
    json_response = []
    data_extract = []
    iast_name = ''
    english_name = ''
    devanagari_name = ''
    context = ''

    try:
        if 'verseId' in json_data_body and 'verseCategory' in json_data_body:
            verse_id = json_data_body.get('verseId')
            verse_category = json_data_body.get('verseCategory')

            if verse_category.lower() in ['introduction', 'start', 'intro']:
                verse_range = sql.dql_fetch_all_rows(database=config.DATABASE_URL, sql_script=Query.VERSE_MINMAX_VALUES['getIntroductionValues'], return_list=False)
                if misc.check_verse_id_in_range(verse_id, verse_range[0][0], verse_range[0][1]):
                    devanagari_name_list = sql.dql_fetch_all_rows_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['introductory']['getShlokaNameByVerseId'], data_input=verse_id, return_list=False)[0]
                    devanagari_name = f"{devanagari_name_list[0]} - {devanagari_name_list[1]}" if devanagari_name_list[1] != "" else f"{devanagari_name_list[0]}"
                    iast_name = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getIASTNameTranslationByDevanagariName'], data_input=devanagari_name_list[0])
                    english_name = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getEnglishNameTranslationByDevanagariName'], data_input=devanagari_name_list[0])
                    sql_script_to_use = Query.SELECT_QUERY['introductory']['getIntroductionVerseByVerseId']
                    verse_data = sql.dql_fetch_all_rows_for_one_input(database=config.DATABASE_URL, sql_script=sql_script_to_use, data_input=verse_id, return_list=False)[0]
                    if len(verse_data) == 0:
                        error_message = "Search is unable to find any available content in the database. Please validate the search parameters or narrow down the search parameters."
                        json_response = resp_json.response_template(
                            success=False,
                            message="An exception has occurred. Please refer to the 'errorInformation' for more details.",
                            data=None,
                            error=error.DBDataExtraction(message=error_message),
                            status_code=404,
                            display_error=True
                        )
                    else:
                        data_extract = resp_json.populate_json_data_extract(
                            data_id=verse_data[0],
                            verse_number=verse_data[1],
                            shloka_devanagari=verse_data[2],
                            shloka_iast=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getVerseIASTTranslationByVerseId'], data_input=verse_data[0]),
                            meaning_english=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['meanings']['getEnglishMeaningsByVerseId'], data_input=verse_data[0]),
                            meaning_hindi=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['meanings']['getHindiMeaningsByVerseId'], data_input=verse_data[0]),
                            name_devanagari=devanagari_name,
                            name_iast=iast_name,
                            name_english=english_name
                        )
                        json_response = resp_json.response_template(success=True, message='Search completed successfully', data=data_extract, status_code=200)
                return json_response
            elif verse_category.lower() in ['chapters', 'main', 'chapter', 'mid']:
                verse_range = sql.dql_fetch_all_rows(database=config.DATABASE_URL, sql_script=Query.VERSE_MINMAX_VALUES['getChapterValues'], return_list=False)
                if misc.check_verse_id_in_range(verse_id, verse_range[0][0], verse_range[0][1]):
                    devanagari_name_list = sql.dql_fetch_all_rows_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['chapters']['getChapterNameByVerseId'], data_input=verse_id, return_list=False)[0]
                    devanagari_name = f"{devanagari_name_list[0]} - {devanagari_name_list[1]}" if devanagari_name_list[1] != "" else f"{devanagari_name_list[0]}"
                    iast_name = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getIASTNameTranslationByDevanagariName'], data_input=devanagari_name_list[1])
                    english_name = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getEnglishNameTranslationByDevanagariName'], data_input=devanagari_name_list[1])
                    sql_script_to_use = Query.SELECT_QUERY['chapters']['getChapterVersesByVerseId']
                    verse_data = sql.dql_fetch_all_rows_for_one_input(database=config.DATABASE_URL, sql_script=sql_script_to_use, data_input=verse_id, return_list=False)[0]
                    if len(verse_data) == 0:
                        error_message = "Search is unable to find any available content in the database. Please validate the search parameters or narrow down the search parameters."
                        json_response = resp_json.response_template(
                            success=False,
                            message="An exception has occurred. Please refer to the 'errorInformation' for more details.",
                            data=None,
                            error=error.DBDataExtraction(message=error_message),
                            status_code=404,
                            display_error=True
                        )
                    else:
                        data_extract = resp_json.populate_json_data_extract(
                            data_id=verse_data[0],
                            verse_number=verse_data[1],
                            shloka_devanagari=verse_data[2],
                            shloka_iast=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getChapterVersesIASTTranslation'], data_input=verse_data[0]),
                            meaning_english=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['meanings']['getEnglishMeaningsByVerseId'], data_input=verse_data[0]),
                            meaning_hindi=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['meanings']['getHindiMeaningsByVerseId'], data_input=verse_data[0]),
                            name_devanagari=devanagari_name,
                            name_iast=iast_name,
                            name_english=english_name
                        )
                        json_response = resp_json.response_template(success=True, message='Search completed successfully', data=data_extract, status_code=200)
                return json_response
            elif verse_category.lower() in ['conclusion', 'end', 'exit', 'concluding']:
                verse_range = sql.dql_fetch_all_rows(database=config.DATABASE_URL, sql_script=Query.VERSE_MINMAX_VALUES['getConcludingValues'], return_list=False)
                if misc.check_verse_id_in_range(verse_id, verse_range[0][0], verse_range[0][1]):
                    devanagari_name_list = sql.dql_fetch_all_rows_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['concluding']['getShlokaNameByVerseId'], data_input=verse_id, return_list=False)[0]
                    devanagari_name = f"{devanagari_name_list[0]} - {devanagari_name_list[1]}" if devanagari_name_list[1] != "" else f"{devanagari_name_list[0]}"
                    iast_name = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getIASTNameTranslationByDevanagariName'], data_input=devanagari_name_list[0])
                    english_name = sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getEnglishNameTranslationByDevanagariName'], data_input=devanagari_name_list[0])
                    sql_script_to_use = Query.SELECT_QUERY['concluding']['getExitVerseByVerseId']
                    verse_data = sql.dql_fetch_all_rows_for_one_input(database=config.DATABASE_URL, sql_script=sql_script_to_use, data_input=verse_id, return_list=False)[0]
                    if len(verse_data) == 0:
                        error_message = "Search is unable to find any available content in the database. Please validate the search parameters or narrow down the search parameters."
                        json_response = resp_json.response_template(
                            success=False,
                            message="An exception has occurred. Please refer to the 'errorInformation' for more details.",
                            data=None,
                            error=error.DBDataExtraction(message=error_message),
                            status_code=404,
                            display_error=True
                        )
                    else:
                        data_extract = resp_json.populate_json_data_extract(
                            data_id=verse_data[0],
                            verse_number=verse_data[1],
                            shloka_devanagari=verse_data[2],
                            shloka_iast=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['translation']['getChapterVersesIASTTranslation'], data_input=verse_data[0]),
                            meaning_english=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['meanings']['getEnglishMeaningsByVerseId'], data_input=verse_data[0]),
                            meaning_hindi=sql.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['meanings']['getHindiMeaningsByVerseId'], data_input=verse_data[0]),
                            name_devanagari=devanagari_name,
                            name_iast=iast_name,
                            name_english=english_name
                        )
                        json_response = resp_json.response_template(success=True, message='Search completed successfully', data=data_extract, status_code=200)
                return json_response
            else:
                error_message = "Search category could not be identified. Acceptable values are introduction or chapter or conclusion."
                json_response = resp_json.response_template(
                    success=False,
                    message="An exception has occurred. Please refer to the 'errorInformation' for more details.",
                    data=None,
                    error=error.InvalidInputValues(message=error_message),
                    status_code=404,
                    display_error=True
                )
                return json_response

        else:
            error_message = "Search couldn't be performed because its missing a parameter in the input request. Request must contain 'verseId' and 'verseCategory'."
            json_response = resp_json.response_template(
                success=False,
                message="An exception has occurred. Please refer to the 'errorInformation' for more details.",
                data=None,
                error=error.InvalidRequest(message=error_message),
                status_code=404,
                display_error=True
            )
            return json_response
    except Exception as err:
        json_response = resp_json.response_template(
            success=False,
            message="An exception has occurred. Please refer to the 'errorInformation' for more details.",
            data=None,
            error=err,
            status_code=404,
            display_error=True
        )
        return json_response


def update_verse_meaning(json_data_body):
    try:
        if len(json_data_body) != 0:
            if 'action' in json_data_body and 'dataInput' in json_data_body:
                action = json_data_body.get('action')
                if action.upper() == 'U':
                    data_input = json_data_body.get('dataInput')
                    if len(data_input) > 0:
                        if data_input and len(data_input) > 1:
                            for data_item in data_input:
                                member_id = data_item['id']
                                meaning_lang = data_item['meaningLanguage']
                                meaning_description = data_item['meaningDescription']

                                if meaning_lang in ['en', 'english', 'eng'] and (meaning_description is not None and meaning_description is not ""):
                                    update_query = Query.UPDATE_QUERY['setMeaning']['forEnglish'].replace('?meaning', meaning_description).replace('?id', str(member_id))
                                    sql.dml_execute_script(database=config.DATABASE_URL, sql_script=update_query)
                                elif meaning_lang in ['hn', 'hindi', 'hin'] and (meaning_description is not None and meaning_description is not ""):
                                    update_query = Query.UPDATE_QUERY['setMeaning']['forHindi'].replace('?meaning', meaning_description).replace('?id', str(member_id))
                                    sql.dml_execute_script(database=config.DATABASE_URL, sql_script=update_query)
                                else:
                                    raise error.InvalidInputValues("Input language doesn't fall in the standard options. Applicable values: en/hn")
                        elif 'id' in data_input[0] and 'meaningLanguage' in data_input[0] and 'meaningDescription' in data_input[0] and len(data_input) == 1:
                            member_id = data_input[0]['id']
                            meaning_lang = data_input[0]['meaningLanguage']
                            meaning_description = data_input[0]['meaningDescription']
                            if meaning_lang in ['en', 'english', 'eng'] and (meaning_description is not None and meaning_description is not ""):
                                update_query = Query.UPDATE_QUERY['setMeaning']['forEnglish'].replace('?meaning', meaning_description).replace('?id', str(member_id))
                                sql.dml_execute_script(database=config.DATABASE_URL, sql_script=update_query)
                            elif meaning_lang in ['hn', 'hindi', 'hin'] and (meaning_description is not None and meaning_description is not ""):
                                update_query = Query.UPDATE_QUERY['setMeaning']['forHindi'].replace('?meaning', meaning_description).replace('?id', str(member_id))
                                sql.dml_execute_script(database=config.DATABASE_URL, sql_script=update_query)
                            else:
                                raise error.InvalidInputValues("Input language doesn't fall in the standard options. Applicable values: en/hn")
                        else:
                            raise error.InvalidRequest("Mandatory input parameters are missing. Update couldn't be performed.")
                    else:
                        raise error.InputMissing("Data input is missing. Update could not be performed.")
                else:
                    raise error.InvalidInputValues("The operation you are trying to perform is not applicable.")
            else:
                raise error.InvalidRequest("Action or dataInput is missing. UPDATE operation cannot be performed.")
        else:
            raise error.InputMissing("There is no input request provided.")
        json_response = resp_json.response_template(
            success=True,
            message="Data updated successfully.",
            data=None
        )
        return json_response
    except Exception as err:
        json_response = resp_json.response_template(
            success=False,
            message="An exception has occurred. Please refer to the 'errorInformation' for more details.",
            data=None,
            error=err,
            status_code=404,
            display_error=True
        )
        return json_response

