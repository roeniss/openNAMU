from .tool.func import *

def topic_change_2(conn, topic_num):
    curs = conn.cursor()

    if admin_check(None) != 1:
        return re_error('/error/3')

    ip = ip_check()
    time = get_time()
    topic_num = str(topic_num)

    curs.execute(db_change("select title, sub from rd where code = ?"), [topic_num])
    rd_d = curs.fetchall()
    if not rd_d:
        return redirect('/')

    if flask.request.method == 'POST':
        admin_check(None, 'move_topic (code ' + topic_num + ')')

        curs.execute(db_change("select id from topic where code = ? order by id + 0 desc limit 1"), [topic_num])
        topic_check = curs.fetchall()
        if topic_check:
            title_d = flask.request.form.get('title', 'test')
            sub_d = flask.request.form.get('sub', 'test')

            curs.execute(db_change("update rd set title = ?, sub = ? where code = ?"), [
                title_d,
                sub_d,
                topic_num
            ])

            curs.execute(db_change("insert into topic (id, data, date, ip, top, code) values (?, ?, ?, ?, '1', ?)"), [
                str(int(topic_check[0][0]) + 1),
                'change name to ' + sub_d + '(' + title_d + ')',
                time,
                ip,
                topic_num
            ])

            rd_plus(topic_num, time)

        return redirect('/thread/' + topic_num)
    else:
        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('topic_setting'), wiki_set(), custom(), other2([0, 0])],
            data = '''
                <form method="post">
                    ''' + load_lang('document_name') + '''
                    <hr class=\"main_hr\">
                    <input value="''' + rd_d[0][0] + '''" name="title" type="text">
                    <hr class=\"main_hr\">
                    ''' + load_lang('discussion_name') + '''
                    <hr class=\"main_hr\">
                    <input value="''' + rd_d[0][1] + '''" name="sub" type="text">
                    <hr class=\"main_hr\">
                    <button type="submit">''' + load_lang('save') + '''</button>
                </form>
            ''',
            menu = [['thread/' + topic_num + '/tool', load_lang('return')]]
        ))
