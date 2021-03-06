from flask import Flask, render_template
from tor.db import get_table_info, get_ga_regular, get_sc_veto, preview_sc_veto_record
app = Flask(__name__)

@app.route('/')
def welcome():
    return 'TOR app coming soon!'

#Route for GA Conventions & Declarations by language
@app.route('/<string:lang>/ga/conventions')
def ga_conventions(lang):
    table_txt = get_table_info(lang, "GA", "Conventions")
    return 'Route for GA Conventions & Declarations by language'

#Route for GA Special Sessions by language
@app.route('/<string:lang>/ga/special')
def ga_special(lang):
    table_txt = get_table_info(lang, "GA", "Special Sessions")
    return 'Route for GA Special Sessions by language'

#Route for GA Emergency Special Sessions by language
@app.route('/<string:lang>/ga/emergency')
def ga_emergency(lang):
    table_txt = get_table_info(lang, "GA", "Emergency Sessions")
    return 'Route for GA Emergency Special Sessions'

#Route for GA Regular Session by language and session
@app.route('/<string:lang>/ga/regular/<int:session>')
def ga_regular(lang, session):
    table_txt = get_table_info(lang, "GA", "Regular Sessions")
    table_records = get_ga_regular(lang, session)
    
    return render_template('/ga/regular.html', lang=lang, session=session, table_txt=table_txt, records=table_records)

#Route for SC Veteos by language
@app.route('/<string:lang>/sc/veto')
def sc_vetoes(lang):
    table_txt = get_table_info(lang, "SC", "Vetoes")
    table_records = get_sc_veto(lang)
    #return 'Route for SC vetoes'
    return render_template('/sc/veto.html', lang=lang, table_txt=table_txt, records=table_records)

#Route for SC Meetings & Outcomes by language and year
@app.route('/<string:lang>/sc/meetings/<int:year>')
def sc_meetings(lang, year):
    table_txt = get_table_info(lang, "SC", "Meetings and Outcomes")
    return 'Route for SC Meetings & Outcomes by language and year'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404 

@app.errorhandler(505)
def page_not_found(error):
    return render_template('error.html'), 505 

##################CRUD per record################

@app.route('/sc/veto/<int:row_num>')
def preview_veto(row_num):
    table_txt = get_table_info('en', "SC", "Vetoes")
    table_records = preview_sc_veto_record(row_num)
    return render_template('/sc/preview_veto.html', table_txt=table_txt, records=table_records)
