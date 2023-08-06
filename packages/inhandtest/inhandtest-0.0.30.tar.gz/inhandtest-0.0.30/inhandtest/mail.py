# -*- coding: utf-8 -*-
# @Time    : 2023/4/12 10:10:43
# @Author  : Pane Li
# @File    : mail.py
"""
mail

"""
import logging
import emails
import os


def pytest_send_report_mail(mail_to: str or list, mail_from: tuple or list, render: dict):
    """使用已配置好的邮件模板，发送邮件内容

    :param mail_to:  发送给谁
    :param mail_from: 元组($email, $password)
    :param render: 字典类型，需要将报告的内容传入 key值如下：
                             model：测试设备型号， 如VG710
                             version: 测试的版本, 如 VG7-V209bfd4(test)-2023-03-31-14-52-02.bin
                             start_time: 测试开始时间， 2023-04-12 17:33:02
                             end_time：测试结束时间，2023-04-12 17:33:02
                             host: 测试主机， 10.5.24.107
                             total: 总计执行的用例数
                             passed: 通过的用例数
                             failed：失败的用例数
                             broken：阻塞的用例数
                             skipped：跳过的用例数
                             unknown： 未知用例数
                             report_url： 报告的链接

    :return:
    """
    html_file_path = os.path.join(os.path.dirname(__file__), 'pytest_email.html')
    from emails.template import JinjaTemplate as Te

    message = emails.html(html=Te(open(html_file_path, encoding='utf-8').read()), subject=f'{render.get("model")}自动化测试',
                          mail_from=('映翰通网络测试', mail_from[0]))
    r = message.send(mail_to, smtp={'host': 'smtp.exmail.qq.com', 'port': 465, 'user': mail_from[0], 'ssl': True,
                                    'password': mail_from[1]},
                     render=render)
    assert r.status_code == 250, 'send email failed'
    logging.info(f'send {mail_to} test result success!')
