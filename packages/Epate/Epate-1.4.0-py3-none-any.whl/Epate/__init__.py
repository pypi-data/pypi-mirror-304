import requests

rs = requests.session()


def login(username, password):
    login_data = {
        "identity": username,
        "password": password,
        "pid": "65edCTyg",
        "agreement_ids": [-1]
    }
    result = rs.post(url='https://api.codemao.cn/tiger/v3/web/accounts/login',
                     json=login_data)

    code = str(result.status_code)
    global get

    def get():
        return (result.text)

    return (code)


def logout():

    result = rs.post('https://api.codemao.cn/tiger/v3/web/accounts/loginout')
    global get

    def get():
        return (result.text)

    return (str(result.status_code))


def usrinfo(kind, inputstr, inputint: int):
    if kind == 'nick':

        change = {'nickname': inputstr}
        result = rs.patch("/tiger/v3/web/accounts/info", data=change)

    if kind == 'full':

        change = {'fullname': inputstr}
        result = rs.patch("/tiger/v3/web/accounts/info", data=change)

    if kind == 'desc':

        change = {'description': inputstr}
        result = rs.patch("/tiger/v3/web/accounts/info", data=change)

    if kind == 'sex':

        change = {'sex': inputint}
        result = rs.patch("/tiger/v3/web/accounts/info", data=change)

    if kind == 'birth':

        change = {'birthday	': inputint}
        result = rs.patch("/tiger/v3/web/accounts/info", data=change)

    if kind == 'avat':

        change = {'avatar_url': inputstr}
        result = rs.patch("/tiger/v3/web/accounts/info", data=change)
    global get

    def get():
        return (result.text)

    return (str(result.status_code))


def psc(old_password, new_password):

    change = {
        'old_password': old_password,
        'password': new_password,
        'confirm_password': new_password
    }
    result = rs.patch(
        "/tiger/v3/web/accounts/info",
        data=change,
    )

    global get

    def get():
        return (result.text)

    return (str(result.status_code))


def like(workid):

    result = rs.post(
        "https://api.codemao.cn/nemo/v2/works/" + workid + "/like", )
    global get

    def get():
        return (result.text)

    return (str(result.status_code))

def dislike(workid):

    result = rs.delete(
        "https://api.codemao.cn/nemo/v2/works/" + workid + "/like", )
    global get

    def get():
        return (result.text)

    return (str(result.status_code))


def coll(workid):

    result = rs.post(
        "https://api.codemao.cn/nemo/v2/works/" + workid + "/collection", )
    global get

    def get():
        return (result.text)

    return (str(result.status_code))

def discoll(workid):

    result = rs.delete(
        "https://api.codemao.cn/nemo/v2/works/" + workid + "/collection", )
    global get

    def get():
        return (result.text)

    return (str(result.status_code))

def fork(workid):

    result = rs.post(
        "https://api.codemao.cn/nemo/v2/works/" + workid + "/fork", )
    global get

    def get():
        return (result.text)

    return (str(result.status_code))


def follow(userid):

    result = rs.post(
        "https://api.codemao.cn/nemo/v2/user/" + userid + "/follow", )
    global get

    def get():
        return (result.text)

    return (str(result.status_code))

class comment():
    def work(workid, data):
        rldata = {"emoji_content":"","content":data}

        result = rs.post(
            "https://api.codemao.cn/creation-tools/v1/works/%d/comment" % workid,
            json=rldata,
        )
        global get

        def get():
            return (result.text)

        return (str(result.status_code))
    def post(postid, data):
        rldata = {"content":data}
        result = rs.post(
            "https://api.codemao.cn/web/forums/posts/%d/replies" % postid,
            json=rldata,
        )
        global get

        def get():
            return (result.text)

        return (str(result.status_code))

class report():
    def work(workid:str,reason:str,describe:str):
        data = {"work_id":workid,"report_reason":reason,"report_describe":describe}
        result = rs.post(url='https://api.codemao.cn/nemo/v2/report/work',
                        json=data)

        code = str(result.status_code)
        global get

        def get():
            return (result.text)

        return (code)
    def post(postid:str,reasonid:str,describe:str):
        data = {"post_id":postid,"reason_id":reasonid,"description":describe}
        result = rs.post(url='https://api.codemao.cn/web/reports/posts',
                        json=data)

        code = str(result.status_code)
        global get

        def get():
            return (result.text)

        return (code)
