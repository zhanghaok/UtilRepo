# encoding:utf-8
import argparse
import smtplib
from email.header import Header
from email.mime.text import MIMEText


def send(args):
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "3250514239@qq.com"  # 用户名
    mail_pass = "vwmghvuwtvhbdabg"  # 授权码，注意不是邮箱登录密码，是上述设置的授权密码！！！
    sender = '3250514239@qq.com'
    receivers = ['3250514239@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    content = ''
    for arg in vars(args):
        if not arg == 'title':
            content = content + arg + ':' + str(getattr(args, arg)) + '\n\n'

    message = MIMEText(str(content), 'plain', 'utf-8')
    message['From'] = "张浩堃"
    message['To'] = "我的邮箱"

    subject = args.title

    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.set_debuglevel(1)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("================邮件发送成功================")


if __name__ == "__main__":
    # Adding necessary input arguments
    parser = argparse.ArgumentParser(description='args from command line')
    parser.add_argument('--title', default="消息通知", type=str, help='title of email')
    parser.add_argument('--type', default="success", type=str, help='type of training')
    parser.add_argument('--acc_train', default="100%", type=str, help='acc of the train')
    parser.add_argument('--acc_dev', default="100%", type=str, help='acc of the dev')
    parser.add_argument('--acc_test', default="100%", type=str, help='acc of the test')
    args = parser.parse_args()
    send(args)

    # 训练代码中的函数
    # def SendEmail(args):
    #     # 执行命令发送邮件
    #     os.system(f'python SendEmail.py --title={args.title} --type={args.type} --acc_train={args.acc_train} '
    #               f'--acc_dev={args.acc_dev} --acc_test={args.acc_test}')
