## 部署 ABot

### 环境要求

- 为必须
  - 为可选

> 如未特殊说明，均已最新版为准

- [Python](https://www.python.org/) `3.9`
- [Poetry](https://python-poetry.org/)
- [Mirai HTTP API](https://github.com/project-mirai/mirai-api-http) `^2.3` （后文简写为 MAH）
  - [Netease Cloud Music Api](https://github.com/Binaryify/NeteaseCloudMusicApi) `如果你需要点歌姬功能的话需要自行搭建`
  - [QQ Music API](https://github.com/Rain120/qq-music-api) `如果你需要点歌姬功能的话需要自行搭建`

### 安装

> 首先你需要将 [MAH v2](https://github.com/project-mirai/mirai-api-http) 配置完成，你的配置文件应该长这样：
>
> ```yaml
> adapters:
>   - http
>   - ws
> debug: false
> enableVerify: true
> verifyKey: xxxxxx # 记住这里填写的 key
> singleMode: false
> cacheSize: 4096
> adapterSettings:
>   http:
>     host: localhost
>     port: 8066
>     cors: [*]
>   ws:
>     host: localhost
>     port: 8066 # 此端口请与 http 端口保持一致
>     reservedSyncId: -1
> ```

1. 克隆 ABot 到本地
   ```shell
   git clone https://github.com/djkcyl/ABot-Graia
   ```
2. 下载 ABot 所需字体资源 [ABot Font](https://github.com/djkcyl/ABot-Resource/releases/tag/Font) 并解压至 ABot 根目录

3. 创建虚拟容器
   ```shell
   poetry env use 3.9
   ```
4. 使用虚拟容器安装依赖 `本步骤可能需要执行5分钟到5小时，请耐心等待（`
   ```shell
   poetry install
   ```
5. 修改 ABot 配置文件 `config/config.exp.yaml` 后**并重命名**为 `config/config.yaml`
6. 启动 ABot
   ```shell
   poetry run python main.py
   ```

> 你可能还需要执行下面这条命令才能正常使用某些功能
>
> ```shell
> npx playwright install-deps
> ```

> 你也可能在执行 `poetry install` 的时候出现装不上 `graiax-silkcoder` 的情况，请自行解决编译环境问题

> 你也可能没有安装 `poetry` ，没关系，你可以使用 `pip install -r requirements.txt` 来安装依赖。但请注意这样很容易导致依赖错误，所以请尽可能使用类似 `poetry` 或 `vnev` 之类的虚拟环境！

如果你是 Windows 系统且你并不想自己配置 Python 环境，可以使用 [ABot WindowsRuntime](https://github.com/djkcyl/ABot-Resource/releases/tag/Windows-Runtime)

**尽情享用吧~**

## 保持在后台运行

### **Windows**

> ~~Windows 系统也需要问吗？彳亍~~<br>
> 按下最小化即可。<br> > ~~为什么会有人这个也要教啊（恼）~~<br>

### **Linux**

> **Centos**
>
> ```shell
> yum install screen
> screen -R ABot
> ...
> ```
>
> 其他发行版怎么用请查阅[此处](https://zhuanlan.zhihu.com/p/26683968)
