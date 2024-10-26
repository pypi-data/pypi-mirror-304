<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-searchgame

_✨ 简单查询steam和switch游戏平台的游戏信息 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-template.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-template">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-template.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>


## 📖 介绍

萌新第一次发布的插件，别笑我qwq
目前只支持查询steam和switch游戏平台的游戏信息，后续会添加更多平台。
游戏数据源来自小黑盒JUMP

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-searchgame

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-searchgame
</details>

<details>
<summary>conda</summary>

    conda install nonebot-plugin-searchgame
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebo_plugin_searchgames"]

</details>



## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 查游戏（搜游戏) | 所有人 | 否 | 群聊 | 加上游戏名即可查询 |
| 查ns（搜ns）| 所有人 | 否 | 群聊 | 加上游戏名即可查询 |
### 效果图
<a href="./LICENSE">
    <img src="./img/steam.png" alt="license">
</a>
<a href="./LICENSE">
    <img src="./img/ns.png" alt="license">
</a>

