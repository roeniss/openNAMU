from .tool.func import *

def give_user_ban_2(conn, name):
    curs = conn.cursor()

    if name and ip_or_user(name) == 0:
        curs.execute(db_change("select acl from user where id = ?"), [name])
        user = curs.fetchall()
        if not user:
            return re_error('/error/2')

        if user and user[0][0] != 'user':
            if admin_check() != 1:
                return re_error('/error/4')

    if ban_check(ip = ip_check(), tool = 'login') == 1:
        return re_error('/ban')

    if flask.request.method == 'POST':
        name = name if name else flask.request.form.get('name', 'test')

        if admin_check(1, 'ban' + ((' (' + name + ')') if name else '')) != 1:
            return re_error('/error/3')

        end = flask.request.form.get('second', '0')
        end = end if end else '0'

        if flask.request.form.get('regex', None):
            type_d = 'regex'

            try:
                re.compile(name)
            except:
                return re_error('/error/23')
        else:
            type_d = None

        ban_insert(
            name,
            end,
            flask.request.form.get('why', ''),
            flask.request.form.get('login', ''),
            ip_check(),
            type_d
        )

        return redirect('/block_log')
    else:
        if admin_check(1) != 1:
            return re_error('/error/3')

        curs.execute(db_change("select end, why from ban where block = ?"), [name])
        end = curs.fetchall()
        if end:
            main_name = name
            b_now = load_lang('release')
            now = '(' + b_now + ')'

            if end[0][0] == '':
                data = '<ul><li>' + load_lang('limitless') + '</li>'
            else:
                data = '<ul><li>' + load_lang('period') + ' : ' + end[0][0] + '</li>'

            curs.execute(db_change("select block from ban where block = ? and login = 'O'"), [name])
            if curs.fetchall():
                data += '<li>' + load_lang('login_able') + '</li>'

            if end[0][1] != '':
                data += '<li>' + load_lang('why') + ' : ' + end[0][1] + '</li></ul><hr class=\"main_hr\">'
            else:
                data += '</ul><hr class=\"main_hr\">'
        else:
            if name:
                main_name = name

                if name and re.search("^([0-9]{1,3}\.[0-9]{1,3})$", name):
                    b_now = load_lang('band_ban')
                else:
                    b_now = load_lang('ban')

                now = ' (' + b_now + ')'

                if name and ip_or_user(name) == 1:
                    plus = '<input type="checkbox" name="login"> ' + load_lang('login_able') + '<hr class=\"main_hr\">'
                else:
                    plus = ''

                name += '<hr class=\"main_hr\">'
                regex = ''
            else:
                main_name = load_lang('ban')
                name = '<input placeholder="' + load_lang('name_or_ip_or_regex') + '" name="name" type="text"><hr class=\"main_hr\">'
                regex = '<input type="checkbox" name="regex"> ' + load_lang('regex') + '<hr class=\"main_hr\">'
                plus = '<input type="checkbox" name="login"> ' + load_lang('login_able') + '<hr class=\"main_hr\">'
                now = 0
                b_now = load_lang('ban')

            time_data = [
                ['86400', load_lang('1_day')],
                ['432000‬', load_lang('5_day')],
                ['2592000', load_lang('30_day')],
                ['15552000', load_lang('180_day')],
                ['31104000‬', load_lang('360_day')],
                ['0', load_lang('limitless')]
            ]
            insert_data = ''
            for i in time_data:
                insert_data += '<a href="javascript:insert_v(\'second\', \'' + i[0] + '\')">(' + i[1] + ')</a> '

            data = name + '''
                <script>function insert_v(name, data) { document.getElementById(name).value = data; }</script>''' + insert_data + '''
                <hr class=\"main_hr\">
                <input placeholder="''' + load_lang('ban_period') + ''' (''' + load_lang('second') + ''')" name="second" id="second" type="text">
                <hr class=\"main_hr\">
                ''' + regex + '''
                <input placeholder="''' + load_lang('why') + '''" name="why" type="text">
                <hr class=\"main_hr\">
            ''' + plus

        return easy_minify(flask.render_template(skin_check(),
            imp = [main_name, wiki_set(), custom(), other2([now, 0])],
            data = '''
                <form method="post">
                    ''' + data + '''
                    <button type="submit">''' + b_now + '''</button>
                </form>
            ''',
            menu = [['manager', load_lang('return')]]
        ))   