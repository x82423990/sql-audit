# coding=utf-8
from celery import task
import smtplib
from email.mime.text import MIMEText

# mail_host = "smtp.qiye.aliyun.com"  # 设置服务器
# mail_user = "zabbix@9ffenqigo.com"  # 用户名
# mail_pass = "bycx.40450"  # 密码
mail_postfix = "猴嘴测试"  # 发件箱的后缀
mail_host = "smtp.163.com"
mail_user = "eatted@163.com"
mail_pass = "xl50140872"


def send_mail(to_list, personnel, sqlid, note, action_type, sqlcontent, dbname,
              max_rows):  # to_list：收件人；sub：主题；content：邮件内容
    contenthtml = ''
    sqlhtml = ''
    ("task在执行")
    subject = ""
    ("to_list, personnel, sqlid, note, action_type, sqlcontent, dbname,  max_rows", to_list, personnel, sqlid,
          note, action_type, sqlcontent, dbname,
          max_rows)
    if action_type == '--enable-check':
        ("--enable-check")
        subject = "工单审核提醒"
        title = '提交了工单 SQL-{}'.format(sqlid)
        for s in sqlcontent[0:1024].split(';'):
            if s:
                sqlhtml = sqlhtml + '<div>' + s + ';' + '</div>'
        contenthtml = "<span style='margin-right:20px'>{} {}</span> " \
                      "<a href='http://120.79.128.26:8888/#/workOrders/sqlOrder/'>【查看详情】</a>" \
                      " <p>备注：{}</p> <p>目标数据库（线上环境）：{} </p><p>SQL语句：{}行;" \
                      "</p><p>SQL语句： </p>" \
            .format(
            personnel, title, note, dbname, max_rows)
        if len(sqlcontent) > 1024:
            sqlhtml = sqlhtml + '<div>' + '略... ...（内容比较多，可查看详情）' + '</div>'
    elif action_type == 'approve':
        subject = "工单执行提醒"
        title = '你的工单{}已经审批通过.'.format(sqlid)
        contenthtml += title

    me = "<" + mail_user + "@" + mail_postfix + ">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
    # me = "<"'hulala'+'@'+'DbApprove.com'">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(contenthtml + sqlhtml, _subtype='html', _charset='utf-8')  # 创建一个实例，这里设置为html格式邮件
    # msg['Subject'] = '{} {} [{}]'.format(personnel, title, note)  # 设置主题
    msg['Subject'] = '{}]'.format(subject)
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        ("start connect")
        s = smtplib.SMTP_SSL(host=mail_host, port=994, timeout=1)
        # s.starttls()
        s.login(mail_user, mail_pass)  # 登陆服务器
        ('to_list', to_list)
        s.sendmail(me, to_list, msg.as_string())  # 发送邮件
        s.close()
        return True
    except Exception as e:
        (e)
        return False


if __name__ == '__main__':
    # ['82423990@qq.com', 'eatted@163.com'] test1 29 ba82k --enable-check UPDATE test SET count=80008 WHERE username='moca';
    to_list = ['eatted@163.com']
    personnel = "test1"
    sqlid = 29
    note = "bakcipsdfsd luanqi八早"
    action_type = "--enable-check"
    max_rows = 100
    sqlcontent = "UPDATE test SET count=80008 WHERE username='moca';"
    send_mail(to_list, personnel, sqlid, note, action_type, sqlcontent, "test", max_rows)
