import json
import httpx
import random
import asyncio

from pathlib import Path
from loguru import logger
from graia.saya import Saya, Channel
from graia.ariadne.model import Group, Member
from graia.scheduler.timers import crontabify
from graia.ariadne.message.element import At, Plain
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import GroupMessage
from graia.scheduler.saya.schema import SchedulerSchema
from graia.saya.builtins.broadcast.schema import ListenerSchema

from config import yaml_data, group_data

from util.control import Permission, Interval
from util.sendMessage import safeSendGroupMessage


saya = Saya.current()
channel = Channel.current()


async def update_data():
    global DATA
    logger.info("正在更新词库")
    root = httpx.get(
        "https://raw.fastgit.org/Kyomotoi/AnimeThesaurus/main/data.json",
        verify=False,
    ).json()
    DATA_FILE.write_text(json.dumps(root, indent=2, ensure_ascii=False), encoding="utf-8")
    DATA = root


DATA_FILE = Path(__file__).parent.joinpath("data.json")
if not DATA_FILE.exists():
    logger.info("正在初始化词库")
    asyncio.run(update_data())

DATA = json.loads(DATA_FILE.read_text(encoding="utf-8"))


@channel.use(SchedulerSchema(crontabify("0 0 * * *")))
async def updateDict():
    await update_data()
    logger.info(f"已更新完成聊天词库，共计：{len(DATA)}条")


@channel.use(
    ListenerSchema(listening_events=[GroupMessage], decorators=[Permission.require()])
)
async def main(group: Group, member: Member, message: MessageChain):

    if (
        yaml_data["Saya"]["ChatMS"]["Disabled"]
        and group.id != yaml_data["Basic"]["Permission"]["DebugGroup"]
    ):
        return
    elif "ChatMS" in group_data[str(group.id)]["DisabledFunc"]:
        return

    if message.has(At):
        if message.getFirst(At).target == yaml_data["Basic"]["MAH"]["BotQQ"]:
            saying = message.getFirst(Plain).text
            for key in DATA:
                if key in saying:
                    await Interval.manual(member.id)
                    return await safeSendGroupMessage(
                        group, MessageChain.create([Plain(random.choice(DATA[key]))])
                    )
