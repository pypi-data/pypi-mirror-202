# !/usr/bin/python
# -*- coding:utf-8 -*-

import json


def request_to_curl(request, debug=False, verify=False):
    """将请求对象转换为curl命令字符串

    :param request: 要转换的请求对象
    :param debug: bool，如果为True，则添加-v到curl
    :param verify: bool，如果为False，则仅为https添加-k到curl
    :return: curl命令字符串
    """
    args = ['curl', '-X', request.method, '--compressed']

    if debug:
        args.append('-v')

    if not verify and request.url.startswith('https'):
        args.append('-k')

    for k, v in sorted(request.headers.items()):
        args.append(f"-H '{k}: {v}'")

    if request.body:
        if isinstance(request.body, bytes):
            request.body = request.body.decode('utf-8')
        if request.headers.get('Content-Type') == 'application/json':
            request.body = json.dumps(request.body)
        args.append(f"-d '{request.body}'")

    args.append(request.url)

    return ' '.join(args)
