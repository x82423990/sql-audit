# coding=utf-8
import smtplib
from email.mime.text import MIMEText

mail_host = "smtp.qiye.aliyun.com"  # 设置服务器
mail_user = "zabbix@9ffenqigo.com"  # 用户名
mail_pass = "bycx.40450"  # 密码
# mail_user = "eatted@163.com"  # 设置服务器
# mail_host = "smtp.163.com"  # 用户名
# mail_pass = "xl50140872"  # 密码
mail_postfix = "猴嘴测试"  # 发件箱的后缀


def send_mail(to_list, personnel, sqlid, note, action_type, sqlcontent, dbname):  # to_list：收件人；sub：主题；content：邮件内容
    print("我在执行！！")
    if action_type == '--enable-check':
        title = '提交了SQL工单，编号-{}，需要您的审批！'.format(sqlid)
    elif action_type == '--enable-execute':
        title = '已执行 SQL-{}'.format(sqlid)
    else:
        title = "Unknow title"
    sqlhtml = ''
    for s in sqlcontent[0:1024].split(';'):
        if s:
            sqlhtml = sqlhtml + '<div>' + s + ';' + '</div>'
    contenthtml = "<span style='margin-right:20px'>{} {}</span> <a href='http://sql.aaa.com/sql/{}'>【查看详情】</a> <p>备注：{}</p> <p>目标数据库（线上环境）：{} </p>".format(
        personnel, title, sqlid, note, dbname)
    if len(sqlcontent) > 1024:
        sqlhtml = sqlhtml + '<div>' + '略... ...（内容比较多，可查看详情）' + '</div>'
    me = "<" + mail_user + "@" + mail_postfix + ">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(contenthtml + sqlhtml, _subtype='html', _charset='utf-8')  # 创建一个实例，这里设置为html格式邮件
    msg['Subject'] = '{} {} [{}]'.format(personnel, title, note)  # 设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        print("我开始经连接")
        s = smtplib.SMTP(host=mail_host, port=25, timeout=1)
        # s.connect(mail_host, 5)  # 连接smtp服务器
        print("我已经连接")
        # s.starttls()
        s.login(mail_user, mail_pass)  # 登陆服务器
        s.sendmail(me, to_list, msg.as_string())  # 发送邮件
        s.close()
        print("发送成功")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # ['82423990@qq.com', 'eatted@163.com'] test1 29 ba82k --enable-check UPDATE test SET count=80008 WHERE username='moca';
    to_list = ['82423990@qq.com', 'eatted@163.com']
    personnel = "test1"
    sqlid = 29
    note = "bakcipsdfsd luanqi八早"
    action_type = "--enable-check"
    sqlcontent = "UPDATE test SET count=80008 WHERE username='moca';"
    send_mail(to_list, personnel, sqlid, note, action_type, sqlcontent, "test")
