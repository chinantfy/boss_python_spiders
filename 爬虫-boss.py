#!/usr/bin/env python
# coding: utf-8

# In[23]:


# -*- coding: utf-8 -*-
"""
boss直聘爬虫
"""
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import warnings
import emoji
import re
from sqlalchemy import create_engine
import pandas as pd

warnings.filterwarnings("ignore")
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-plugins-discovery")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-service-autorun")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--password-store=basic")
chrome_options.add_argument("--no-sandbox")
# 定义chrome路径与chromedriver地址
browser = uc.Chrome(
    options=chrome_options,
    executable_path="C:\chrome_pachong1\chromedriver.exe",
    browser_executable_path="C:\chrome_pachong1\chrome.exe",
)

# 进入主页
browser.get("https://www.zhipin.com/shenzhen/")
# 打开网页后手动扫码登录
time.sleep(5)
browser.maximize_window()


def get_Job_description(xpath):
    # 一些处理规则
    xpath = xpath
    try:
        job_description = (
            browser.find_element(By.XPATH, xpath)
            .get_attribute("textContent")
            .replace("\n", "")
            .replace("                                    ", "")
            .replace("\t", "")
            .replace(" ", "")
            .replace("%", "%%")
        )
    except:
        job_description = ""
    return job_description


def change_new():
    # 切换到新标签页
    handles = browser.window_handles[-1]
    browser.switch_to.window(handles)


# engine = create_engine('mysql+pymysql://⽤户名:密码@IP地址:端⼝/数据库?charset=编 码')
engine = create_engine("mysql+pymysql://root:root@localhost:3306/chen?charset=utf8")


def db_read_table(sql):
    """
    依据sql语句读出数据
    :param sql: eg: 'select * from mydb limit 3'
    :return: pd.df
    """
    df = pd.read_sql_query(sql, engine)
    return df


def db_write_table(table_name, pd_data):
    """
    无表时自动建表，表存在就追加
    :param table_name: 'table_name'
    :param pd_data: pd.df
    :return:
    """
    # 将新建的DataFrame储存为MySQL中的数据表，不储存index列
    pd_data.to_sql(table_name, engine, index=False, if_exists="append")
    return


def db_delete_data(dele_sql):
    """
    如果有一个列表要删除，可以参考：
    for id in df_newdata.index:
        # 先删除要新增的数据
        dele_sql = f"delete from student where id={id}"
        engine.execute(dele_sql)
    :param dele_sql:
    :return:
    """
    engine.execute(dele_sql)
    return


def db_execute(sql):
    # 执行sql命令
    engine.execute(sql)
    return


def drop_emoji(text):
    text1 = emoji.demojize(text)
    text2 = re.sub(":\S+?:", " ", text1)
    return text2


# In[24]:


def get_data():
    change_new()
    # 依次爬取当前页面岗位信息
    xpath = f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li'
    tag_element = browser.find_elements(By.XPATH, xpath)
    j = 0
    for i in tag_element:
        j += 1
        # 学历要求
        job_education = get_Job_description(
            f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[{j}]/div[1]/a/div[2]/ul/li[2]'
        )
        # 薪资
        job_salary = get_Job_description(
            f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[{j}]/div[1]/a/div[2]/span'
        )
        # 福利
        job_welfare = get_Job_description(
            f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[{j}]/div[2]/div'
        )
        # 技能要求
        skills = (
            f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[{j}]/div[2]/ul/li'
        )
        tag_element = browser.find_elements(By.XPATH, skills)
        job_skill = ""
        n = 0
        for i in tag_element:
            n += 1
            job_skill += (
                get_Job_description(
                    f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[{j}]/div[2]/ul/li[{n}]'
                )
                + " "
            )
        # 点击进入详情页
        xpath = f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[{j}]/div[1]/a/div[1]/span[1]'
        tag_element = browser.find_element(By.XPATH, xpath)
        ActionChains(browser).click(tag_element).perform()
        time.sleep(10)
        change_new()

        # 获取名字
        job_name = get_Job_description(
            '//*[@id="main"]/div[1]/div/div/div[1]/div[2]/h1'
        )

        # 工作年限
        job_years = get_Job_description(
            '//*[@id="main"]/div[1]/div/div/div[1]/p/span[1]'
        )

        # 公司简介
        company_description = get_Job_description(
            '//*[@id="main"]/div[3]/div/div[2]/div[4]/div[1]/div'
        )
        company_description = drop_emoji(company_description)
        company_description = company_description.replace("'", "")
        # 工作要求
        Job_description = get_Job_description(
            '//*[@id="main"]/div[3]/div/div[2]/div[1]/div[2]'
        )
        Job_description = drop_emoji(Job_description)
        Job_description = Job_description.replace("'", "")
        # 公司名称
        company_name = get_Job_description(
            '//*[@id="main"]/div[3]/div/div[1]/div[2]/div/a[2]'
        )
        if "代招" in job_years:
            company_name = job_years
            job_years = get_Job_description(
                '//*[@id="main"]/div[1]/div/div/div[1]/p/span[2]'
            )
        else:
            pass

        # 公司所属行业
        trade_name = get_Job_description(
            '//*[@id="main"]/div[3]/div/div[1]/div[2]/p[4]/a'
        )
        # 公司规模
        company_scale = get_Job_description(
            '//*[@id="main"]/div[3]/div/div[1]/div[2]/p[3]'
        )
        if "人力资源服务许可证" in Job_description:
            Job_description = company_description
            company_description = "代招"
        else:
            pass
        # 当前网页地址
        job_url = browser.current_url
        # 插入数据库
        sql = f"insert into boss values( '{job_name}','{job_education}','{job_salary}','{job_skill}','{job_welfare}'        ,'{job_years}','{company_description}','{Job_description}','{company_name}','{trade_name}','{company_scale}','{job_url}');"
        db_execute(sql)
        browser.close()
        change_new()


# In[25]:


# 爬取数据，修改range数字控制爬取总页数，url为想要爬取的工作链接(筛选条件之后)
page = 1
for i in range(15):
    change_new()
    url = f"https://www.zhipin.com/web/geek/job?query=ETL%E5%B7%A5%E7%A8%8B%E5%B8%88&city=101280600&salary=406"
    browser.get(url)
    time.sleep(6)
    print(f"开始下载第{page}页数据")
    page += 1
    get_data()
    time.sleep(2)
