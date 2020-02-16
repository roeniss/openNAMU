from .tool.func import *

def api_skin_info_2(conn, name):
    curs = conn.cursor()

    if name == '':
        name = skin_check()
    else:
        name = './views/' + name + '/index.html'

    if not flask.request.args.get('all', None):
        json_address = re.sub("(((?!\.|\/).)+)\.html$", "info.json", name)
        try:
            json_data = json.loads(open(json_address).read())
        except:
            json_data = None

        if json_data:
            return flask.jsonify(json_data)
        else:
            return flask.jsonify({}), 404
    else:
        a_data = {}
        d_link_data = {
            "ACME" : "https://raw.githubusercontent.com/openNAMU/openNAMU-Skin-ACME/master/info.json",
            "Liberty" : "https://raw.githubusercontent.com/openNAMU/openNAMU-Skin-Liberty/master/info.json",
            "Before Namu" : "https://raw.githubusercontent.com/openNAMU/openNAMU-Skin-Before_Namu/master/info.json"
        }

        for i in load_skin(skin_check(1), 1):
            json_address = re.sub("(((?!\.|\/).)+)\.html$", "info.json", './views/' + i + '/index.html')
            try:
                json_data = json.loads(open(json_address).read())
            except:
                json_data = None

            if json_data:
                if i == skin_check(1):
                    json_data = {**json_data, **{ "main" : "true" }}

                if "info_link" in json_data:
                    info_link = json_data["info_link"]
                    get_num = 1
                elif json_data["name"] in d_link_data:
                    info_link = d_link_data[json_data["name"]]
                    get_num = 1
                else:
                    get_num = 0

                if get_num == 1:
                    get_data = urllib.request.urlopen(info_link)
                    if get_data and get_data.getcode() == 200:
                        try:
                            get_data = json.loads(get_data.read().decode())
                            if "skin_ver" in get_data:
                                json_data = {**json_data, **{ "lastest_version" : {
                                    "skin_ver" : json_data["skin_ver"]
                                }}}
                        except:
                            pass

                a_data = {**a_data, **{ i : json_data }}

        return flask.jsonify(a_data)