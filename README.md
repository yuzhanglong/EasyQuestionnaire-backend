# questionnaire-back

#### 此项目是问卷调查平台的后端项目 基于Python的flask框架

#### 前端项目请移步：https://github.com/yuzhanglong/questionnaire-front

##### 注意：除了问卷供填写者填写的页面(这个兼容手机端是非常有必要的)，其他的页面都不兼容移动端 O(∩_∩)O 



## 安装（开发环境）

### 进入安装目录
```
cd /安装目录
```

### clone项目

```
git clone https://github.com/yuzhanglong/questionnaire-back.git
```

### 进入程序目录
```
cd questionnaire-back
```

### 创建虚拟环境
```
virtualenv venv
```

### 进入虚拟环境
```
source venv/bin/activate
```

### 安装依赖
```
pip install -r requirements.txt
```



## 部署

##### 请参考本项目下的 [flask部署总结笔记.md]([https://github.com/yuzhanglong/questionnaire-back/blob/master/flask%E9%83%A8%E7%BD%B2%E6%80%BB%E7%BB%93%E7%AC%94%E8%AE%B0.md](https://github.com/yuzhanglong/questionnaire-back/blob/master/flask部署总结笔记.md))



## 其他

#### 当前功能：

##### 1.登录注册 邮箱验证 等用户的基本操作

##### 2.创建问卷以供填报（支持题型：单选题 多选题 填空题 下拉题）

##### 3.对你当前所拥有的问卷进行增删改  支持问卷模板一键生成问卷

##### 4.问卷发布功能（基本的发布/停止发布功能 设置问卷密码 限制ip或者设备重复访问）

##### 5.问卷数据分析 对某个问卷收集的数据进行数据可视化分析



#### 未来目标：

##### :heavy_check_mark: 二维码分享功能

##### :heavy_check_mark: 二维码海报制作功能
##### :heavy_check_mark: 问卷模板功能
##### :pushpin:添加评价题 nps题等题型
##### :heavy_check_mark:部分页面的样式调整
##### :pushpin:qq 微信分享功能
##### :pushpin:用户个人头像及其他个人信息
