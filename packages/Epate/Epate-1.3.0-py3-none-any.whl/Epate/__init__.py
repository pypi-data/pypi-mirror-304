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


def coll(workid):

    result = rs.post(
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


def comment_w(workid, data):

    result = rs.post(
        "https://api.codemao.cn/creation-tools/v1/works/%d/comment" % workid,
        json=data,
    )
    global get

    def get():
        return (result.text)

    return (str(result.status_code))
