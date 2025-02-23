from flask import Blueprint, render_template
from mainApp.constants import (Information as Info, DataQueries as Query)
from utilities.sqlite_util import *
from datetime import datetime
import config
import os

bp_gui = Blueprint(
    'bp_gui',
    __name__,
    url_prefix='/gui',
    template_folder='templates',
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    static_url_path='/bp_gui/static'
)


@bp_gui.route('/test')
def test():
    return render_template('test.html')


@bp_gui.route('/')
@bp_gui.route('/home')
def index():
    """ Loading Home Page """
    return render_template('index.html', version=Info.APP_INFO['version'], author=Info.APP_INFO['author'])


@bp_gui.route('/gettingStarted')
def getting_started():
    """ Getting Started Page """
    return render_template('01GettingStarted.html', version=Info.APP_INFO['version'], author=Info.APP_INFO['author'])


@bp_gui.route('/initPurifyVerse')
def initial_purify_verses():
    """ Loading "Step 1: Initiation and Purification Verses" page """
    print(f"Database Directory: {config.DATABASE_URL}")
    verses_list = dql_fetch_all_rows(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['introductory']['getIntroductionVerseNames'])
    return render_template('02InitiationPurification.html', optionList=verses_list, version=Info.APP_INFO['version'], author=Info.APP_INFO['author'])


@bp_gui.route('/saptashatiVerses')
def saptashati_verses():
    """ Loading "Step 2: Chandi/Saptashati Path" page """
    verses_list = dql_fetch_all_rows(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['chapters']['getChapterVerseNames'])
    return render_template('03ChandiPathChapters.html', optionList=verses_list, version=Info.APP_INFO['version'], author=Info.APP_INFO['author'])


@bp_gui.route('/concludingVerses')
def concluding_verses():
    """ Loading "Step 3: Conclusion Verses" page """
    verses_list = dql_fetch_all_rows(database=config.DATABASE_URL, sql_script=Query.SELECT_QUERY['concluding']['getConcludingVerseNames'])
    return render_template('04ConcludingVerses.html', optionList=verses_list, version=Info.APP_INFO['version'], author=Info.APP_INFO['author'])


@bp_gui.route('/purpose')
def purpose():
    """ Loading "About the Website" page """
    current_year = datetime.now().year
    year_diff = current_year - Info.JOB_DETAILS['jobStartYear']
    return render_template('06PurposeOfProject.html', version=Info.APP_INFO['version'], author=Info.APP_INFO['author'], year=year_diff)


@bp_gui.route('/otherVerses')
def other_verses():
    """ Loading "Other Verses" page """
    return render_template('99UnderConstruction.html', version=Info.APP_INFO['version'], author=Info.APP_INFO['author'])
