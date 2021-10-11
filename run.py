if __name__ == '__main__':
    # 定义测试集
    allure_list = '--allure_features=Home,Personal'
    args = ['-s', '-q', '--alluredir', xml_report_path, allure_list]
    log.info('执行用例集为：%s' % allure_list)
    self_args = sys.argv[1:]
    pytest.main(args)
    cmd = 'allure generate %s -o %s' % (xml_report_path, html_report_path)

    try:
        shell.invoke(cmd)
    except:
        log.error('执行用例失败，请检查环境配置')
        raise

    try:
        mail = Email.SendMail()
        mail.sendMail()
    except:
        log.error('发送邮件失败，请检查邮件配置')
        raise
