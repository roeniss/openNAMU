import os
import html
import sqlite3
import threading

from .func_tool import *

# 커스텀 마크 언젠간 다시 추가 예정

conn = ''
curs = ''

def load_conn2(data):
    global conn
    global curs

    conn = data
    curs = conn.cursor()
    
def backlink_generate(data_markup, doc_data, doc_name):
    if data_markup == 'namumark':
        # Link
        link_re = re.compile(r'\[\[(?!https?:\/\/)((?:(?!\[\[|\]\]|\|).)+)(?:\]\]|\|)', re.I)
        
        data_link = link_re.findall(doc_data)
        data_link = list(set(data_link))
        
        data_link_end = {}
        data_link_end['cat'] = []
        data_link_end['file'] = []
        data_link_end['link'] = []
        
        for i in data_link:
            data_link_in = i
            if data_link_in[0] == '#':
                continue
            elif re.search(r'^(?:분류|category):', data_link_in):
                data_link_in = re.sub(r'\\(.)', '\1', data_link_in)
                data_link_end['cat'] += [re.sub(r'^분류:', 'category:', data_link_in)]
            elif re.search(r'^(?:파일|file):', data_link_in):
                data_link_in = re.sub(r'\\(.)', '\1', data_link_in)
                data_link_end['file'] += [re.sub(r'^파일:', 'file:', data_link_in)]
            else:
                data_link_in = re.sub(r'([^/])#(?:[^#]*)$', '\1', data_link_in)
                
                if data_link_in[0] == ':':
                    data_link_in = re.sub(r'^:', '', data_link_in)
                elif data_link_in[0] == '/':
                    data_link_in = doc_name + data_link_in
                elif len(data_link_in) >= 3 and data_link_in[0:3] == '../':
                    data_link_in = data_link_in[3:len(data_link_in)]
                    data_link_in = '' + \
                        re.sub('\/[^/]+$', '', doc_name) + \
                        (('/' + data_link_in) if data_link_in != '' else '') + \
                    ''

                data_link_in = re.sub(r'\\(.)', '\1', data_link_in)
                data_link_end['link'] += [data_link_in]
                
        if data_link_end != {}:
            data_link_end['cat'] = list(set(data_link_end['cat']))
            data_link_end['file'] = list(set(data_link_end['file']))
            data_link_end['link'] = list(set(data_link_end['link']))

            data_link_end_all = []
            data_link_end_all += [[doc_name, i, 'cat'] for i in data_link_end['cat']]
            data_link_end_all += [[doc_name, i, 'file'] for i in data_link_end['file']]
            data_link_end_all += [[doc_name, i, ''] for i in data_link_end['link']]
        else:
            data_link_end_all = []
            
        # Include
        include_re = re.compile(r'\[include\(((?:(?!\)\]).)+)\)\]', re.I)
        
        data_include = include_re.findall(doc_data)
        data_include = list(set(data_include))
        
        
        
        # Redirect
    else:
        data_link_end_all = []
            
    return data_link_end_all

def render_do(doc_name, doc_data, data_type, data_in):
    data_in = None if data_in == '' else data_in
    
    curs.execute(db_change('select data from other where name = "markup"'))
    rep_data = curs.fetchall()
    rep_data = rep_data[0][0] if rep_data else 'namumark'
    
    if data_type != 'backlink':
        if rep_data == 'namumark':
            data_in = (data_in + '_') if data_in else ''
            data_end = [
                '<div class="render_content" id="' + data_in + 'render_content">' + html.escape(doc_data) + '</div>', 
                '''
                    do_onmark_render(
                        test_mode = "normal", 
                        name_id = "''' + data_in + '''render_content",
                        name_include = "''' + data_in + '''",
                        name_doc = "''' + doc_name.replace('"', '//"') + '''",
                    );
                ''',
                []
            ]
        else:
            data_end = [
                doc_data, 
                '', 
                []
            ]

        if data_type == 'api_view':
            return [
                data_end[0], 
                data_end[1]
            ]
        else:
            return data_end[0] + '<script>' + data_end[1] + '</script>'
    else:
        backlink = backlink_generate(
            rep_data, 
            html.escape(doc_data), 
            doc_name
        )
        
        print(backlink)
        if backlink != []:
            curs.executemany(db_change("insert into back (link, title, type) values (?, ?, ?)"), backlink)
            curs.execute(db_change("delete from back where title = ? and type = 'no'"), [doc_name])

        conn.commit()