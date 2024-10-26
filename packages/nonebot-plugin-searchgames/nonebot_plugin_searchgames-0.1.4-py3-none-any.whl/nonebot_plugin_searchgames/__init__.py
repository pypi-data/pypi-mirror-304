import requests
from nonebot.plugin import PluginMetadata
import json
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent,MessageSegment,PrivateMessageEvent,bot,event
from pathlib import Path
from nonebot import require
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import template_to_pic
from datetime import datetime


__plugin_meta__ = PluginMetadata(
    name="游戏信息查询",
    description="查询steam和ns平台的游戏信息",
    usage=
    """
    输入 搜游戏 +游戏名 查找steam平台的游戏信息
    输入 搜ns +游戏名 查找ns平台的游戏信息
    """,
    type="application",
    supported_adapters={"~onebot.v11"},
    homepage="https://github.com/NYAGO666/nonebot-plugin-Searchgame",
)

cx = on_command("搜游戏 ",aliases={"查游戏"})
ns = on_command("搜ns ",aliases={"查ns"})
# 导入模版路径
current_dir = Path(__file__).resolve().parent
template_path = current_dir / "templates" 
template_name = "steam游戏查询.html"
template_name1 = "steam免费游戏.html"
template_name2 = "switch游戏查询.html"

@cx.handle()
async def _(event:GroupMessageEvent):
    gamename = event.get_plaintext().strip().removeprefix('搜游戏').strip()

    url = f"https://api.xiaoheihe.cn/game/search/?os_type=web&version=999.0.0&q={gamename}"
    response = requests.get(url).text
    data = json.loads(response)

    if not gamename:
        await cx.finish("请输入游戏名")
    
    if "result" in data and "games" in data["result"] and len(data["result"]["games"]) > 0:
        first_game = data["result"]["games"][0]
        platform = first_game.get("platforms", "")
        
        if "steam" in platform: 
            gameinfo = {}
            
            if first_game.get("is_free"):
                gameinfo = {
                    "appid": str(first_game["steam_appid"]),
                    "链接": f"https://store.steampowered.com/app/{str(first_game['steam_appid'])}",
                    "原价": "免费开玩",
                    "标题": first_game["name"],
                    "图片": first_game["image"],
                    "平台": platform,
                    "当前在线人数":first_game["online_player"],
                }
                output = await template_to_pic(
                    template_path=template_path,
                    template_name=template_name1,
                    templates=gameinfo,
                )
                await cx.send("正在搜索中，请稍等...")
                await cx.finish(MessageSegment.image(output))
            else:
                if "price" in first_game and first_game["price"]:
                    price_info = first_game["price"]
                    original = price_info["initial"]
                    current = price_info["current"]
                    
                    if original != current:
                        discount = price_info["discount"]
                        lowest_state = "是史低哦" if price_info["is_lowest"] == 1 else "不是史低哦"
                        newlowest = "是新史低!!" if price_info.get("new_lowest", "") == 1 else " "
                        deadline = price_info.get("deadline_date", "无截止日期信息")
                    else:
                        discount = "没在打折喔"
                        lowest_state = newlowest = deadline = " "
                    
                    gameinfo = {
                        "appid": str(first_game["steam_appid"]),
                        "链接": f"https://store.steampowered.com/app/{str(first_game['steam_appid'])}",
                        "原价": original,
                        "当前价": current,
                        "折扣比": discount,
                        "是否史低": lowest_state,
                        "是否新史低": newlowest,
                        "截止日期": deadline,
                        "平史低价": str(price_info.get("lowest_price", "无平史低价格信息")),
                        "标题": first_game["name"],
                        "图片": first_game["image"],
                        "平台": platform,
                        "当前在线人数":first_game["online_player"],
                    }
                output = await template_to_pic(
                    template_path=template_path,
                    template_name=template_name,
                    templates=gameinfo,
                )
                await cx.send("正在搜索中，请稍等...")
                await cx.finish(MessageSegment.image(output))

            #可以选择文字发送
            #     message = [
            #         MessageSegment.text(f"标题: {gameinfo['标题']}\n"),
            #         MessageSegment.text(f"平台: {gameinfo['平台']}\n"),
            #         MessageSegment.image(file=gameinfo['图片']),
            #         MessageSegment.text(f"原价: {gameinfo['原价']}\n"),
            #         MessageSegment.text(f"当前价: {gameinfo['当前价']}\n"),
            #         MessageSegment.text(f"折扣比: {gameinfo['折扣比']}\n"),
            #         MessageSegment.text(f"是否史低: {gameinfo['是否史低']}\n"),
            #         MessageSegment.text(f"是否新史低: {gameinfo['是否新史低']}\n"),
            #         MessageSegment.text(f"截止日期: {gameinfo['截止日期']}\n"),
            #         MessageSegment.text(f"平史低价: {gameinfo['平史低价']}\n"),
            #         MessageSegment.text(f"链接: {gameinfo['链接']}\n"),
            #         MessageSegment.text(f"当前在线人数: {gameinfo['当前在线人数']}")
            #     ]
            # await cx.finish(message)
        else:
            await cx.send("该游戏或许不在steam平台？")
    else:
        await cx.send("没有找到该游戏")
@ns.handle()
async def search_ns_game(event: GroupMessageEvent):
    input = event.get_plaintext().strip().removeprefix('搜ns').strip()
    
    if not input:
        await ns.send("请提供游戏名称!")
        return
    try:
        url = f'https://switch.jumpvg.com/jump/searchGame/list/v2?type=1&searchName={input}'
        response = requests.get(url)
        data = response.json()

        name = data["data"]["gameList"][0]['name']
        id = data["data"]["gameList"][0]['oldGameId']

        url_game = f"https://switch.jumpvg.com/jump/game/detail?id={id}"
        res = requests.get(url_game)
        data_game = res.json()
        
        game_name = data_game["data"]["jumpGame"]["name"]
        game_tag = ', '.join(data_game["data"]["jumpGame"]["categories"])
        game_language_qu = data_game["data"]["jumpGameExt"]["gameExtItems"][0]["value"]
        game_img = data_game["data"]["jumpGame"]["banner"]
        game_size = data_game["data"]["jumpGameExt"]["gameExtItems"][1]["value"]
        game_player = data_game["data"]["jumpGameExt"]["gameExtItems"][2]["value"]
        game_originPrice = data_game["data"]["jumpGame"].get("originPrice", None)
        if game_originPrice is not None:
            game_originPrice /= 100.0
        game_lowestPrice = data_game["data"]["jumpGame"].get("lowestPrice", None)
        if game_lowestPrice is not None:
            game_lowestPrice /= 100.0
        game_priceCountry = data_game["data"]["jumpGame"]["priceCountry"]
        game_cloud = data_game["data"]["jumpGameExt"]["gameExtItems"][8]["value"]
        game_riqi = data_game["data"]["jumpGame"]["pubDate"]
        riqi = game_riqi / 1000.0
        dt_object = datetime.fromtimestamp(riqi)
        game_riqi = dt_object.strftime('%Y-%m-%d')

        # DLC
        dlc_info = []
        for dlc in data_game["data"]["dlcList"]:
            dlc_name = dlc.get("name", "未知")
            dlc_price = dlc.get("price", None)
            if dlc_price is not None:
                dlc_price /= 100.0
            dlc_info.append(f"{dlc_name}:{dlc_price}¥")
            
        message = (f"游戏名：{game_name}\n"
                    f"标签：{game_tag}\n"
                    f"图片url：{game_img}\n"
                    f"中文支持：{game_language_qu}\n"
                    f"容量：{game_size}\n"
                    f"游戏人数：{game_player}\n"
                    f"支持云存档：{game_cloud}\n"
                    f"原价：{game_originPrice or '无'}¥, 史低({game_priceCountry}区): {game_lowestPrice or '无'}¥\n"
                    f"DLC(仅展示前3个)：\n" + "\n".join(dlc_info[:3]))
        
        gameinfo = {"标题": game_name, 
                    "图片": game_img, 
                    "原价": f"{game_originPrice or '无'}",
                    "史低区":game_priceCountry,
                    "史低": f"{game_lowestPrice or '无'}",
                    "标签": game_tag,
                    "中文支持": game_language_qu,
                    "容量": game_size,
                    "支持云存档": game_cloud,
                    "游戏人数": game_player,
                    "DLC": f"{('<br>'.join(dlc_info[:3])) or '无'}",
                    "发售日期": game_riqi,
                    }
        output = await template_to_pic(
            template_path=template_path,
            template_name=template_name2,
            templates=gameinfo,
        )
        #可以选择文字发送
        #await ns.send(message)
        await ns.send("正在搜索中，请稍等...")
        await ns.finish(MessageSegment.image(output))
    except Exception as e:
        await ns.send(f"发生错误")
        print(e)


