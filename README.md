# BiliBulletScreenCrawlers  

*A bilibili bulletscreen crawiers(Cookie required)*  

Upgrade Time:2021/10/11 4:43 a.m.  

## **DISCLAIMERS**  

- **This project use MIT LICENSE,and does not involve any charging content**.  

- **The developer's development purpose of this project is only for learning and reference, not for any interest group. If anyone uses this open source project by any means to infringe upon the interests of others or the collective, the original developer will not bear any responsibility**.  

- **Although this project has designed the delayed access function, there is still certain the risk of IP blocked. The user needs to bear the risk. If there is any loss, the original developer will not bear any responsibility**.  

## QUICK-START  

1. Environment Configuration: Install python,version >= 3.0 .

2. Configure Cookies:Under the "config" folder, open the file called "user.ini" and enter your bilibili Cookie to the parameter called "cookie",this step **is required**.  
  
3. BVCode Setting:In "user.ini",enter the BV code of which the video you want to operate into the parameter called "bv".  

4. Time Setting:Since the BulletScreen datafiles given by the API which bilibili provided save as the basic unit by date,you need to enter the "start-time" in "user.ini" which you need to set in the format of "yyyy-mm-dd",this step **is required**.  

5. Run:Open the terminal in the current directory,first enter command `pip3 install -r requirements.txt` to deploy the dependent environment,then enter command `python BiliBulletScreenCrawlers.py`,and wait for the data crawling and the files generation.  

___

## **免责声明**  

- **本项目使用MIT协议，不涉及任何收费内容。**  
  
- **本项目开发者开发目的仅为学习和参考，不针对任何利益集团，若存在任何人以任何手段使用本开源项目侵害其他人或集体利益，原开发者不承担任何责任。**  

- **虽然本项目设计了延时访问功能，但仍有一定程度ip被ban的风险，使用者需要自行承担风险，如有损失，原开发者不承担任何责任。**  

## 快速上手  

1. 环境准备：安装python,版本>=3.0。

2. 配置Cookie：打开在config目录下的user.ini,在cookie参数项中输入你的哔哩哔哩Cookie，此参数项为**必填**。  

3. BV号设定：将你要操作的视频的BV号输入到user.ini的bv参数项中。  

4. 时间设定：由于弹幕获取方式以日期为基本单位，故需要在user.ini的start-date参数项中按“yyyy-mm-dd”的格式填入你设定的开始时间，此参数项为**必填**。  

5. 运行程序：在当前目录下打开终端，先使用`pip3 install -r requirements.txt`部署依赖环境，再使用`python BiliBulletScreenCrawlers.py`命令运行程序，等待数据爬取和文件生成。  

___
