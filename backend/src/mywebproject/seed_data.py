POSTS: list[dict] = [{'slug': 'vue-3-composition-refactor',
  'title': '用 Vue 3 组合式 API 重构一个旧页面',
  'date': '2026-10-24',
  'tags': ['Vue', '前端'],
  'summary': '把一屏几百行的选项式组件拆成可读、可测的小块：记录一次真实的重构过程。',
  'content': [{'type': 'paragraph',
               'text': '最近接手了一个两年前写的后台页面。一个文件四百多行，data、computed、watch '
                       '和模板里的各种条件判断缠在一起。每次改需求都像在一团毛线里找线头。'},
              {'type': 'paragraph',
               'text': '这次我决定不着急加功能，先用 Vue 3 的组合式 API 把它拆开，顺便记录一下自己认为有效的几个步骤。'},
              {'type': 'heading', 'level': 2, 'text': '先别急着改代码'},
              {'type': 'paragraph',
               'text': '重构之前，我先在纸上列出了这个页面真正负责的事情：拉取列表、维护筛选条件、处理分页、打开编辑弹窗、提交表单。然后把它们分成三类：可以独立的状态、只依赖状态的派生数据、需要和外界交互的副作用。'},
              {'type': 'list',
               'ordered': False,
               'items': ['列出页面的核心职责，而不是先看代码结构', '找出一组总是一起变化的状态', '把可以单独测试的逻辑先抽成 composable']},
              {'type': 'heading', 'level': 2, 'text': '从 data 到 ref'},
              {'type': 'paragraph',
               'text': '选项式写法里，所有状态都挂在 this 上，很难看出哪些字段是真正相关的。改成 setup 之后，我会先按职责把状态分组，再用 ref 和 '
                       'reactive 表达它们。'},
              {'type': 'code',
               'lang': 'javascript',
               'code': "const keyword = ref('')\n"
                       'const page = ref(1)\n'
                       "const filters = reactive({ status: 'all' })\n"
                       '\n'
                       'const filteredPosts = computed(() =>\n'
                       '  posts.value.filter((post) => post.title.includes(keyword.value)),\n'
                       ')'},
              {'type': 'paragraph',
               'text': '这段代码本身不复杂，但它把“筛选条件”和“筛选结果”的关系写清楚了。后来再加搜索防抖时，我只需要动一个地方。'},
              {'type': 'heading', 'level': 2, 'text': '让副作用有名字'},
              {'type': 'paragraph',
               'text': '原来的 watch 散落在组件各处，没人知道它们之间有没有依赖。现在每个副作用都放进单独的函数，或者干脆藏进对应的 composable。'},
              {'type': 'code',
               'lang': 'javascript',
               'code': 'watch([keyword, filters], () => {\n'
                       '  page.value = 1\n'
                       '  fetchPosts()\n'
                       '})\n'
                       '\n'
                       'onMounted(fetchPosts)'},
              {'type': 'quote', 'text': '重构不是把代码换一种写法，而是把对问题的理解写进结构里。'},
              {'type': 'heading', 'level': 2, 'text': '留下可验证的边界'},
              {'type': 'paragraph',
               'text': '拆完之后，我给两个最常用的 composable '
                       '补了单元测试。它们不依赖组件，也不依赖浏览器环境，测起来很快。页面的主组件从四百多行降到了一百六十行左右，模板里终于能一眼看完。'},
              {'type': 'paragraph', 'text': '这套方法并不新鲜，但每次动手都能提醒我：先理解，再抽象，最后才是写代码。'}]},
 {'slug': 'fastapi-project-layout',
  'title': '从零搭一个 FastAPI 项目：我的目录约定',
  'date': '2026-09-18',
  'tags': ['Python', 'FastAPI', '后端'],
  'summary': '路由、配置、模型和数据库各归其位，让项目在变大之前就保持清晰。',
  'content': [{'type': 'paragraph',
               'text': '一个 FastAPI 项目在只有几个接口的时候，怎么放文件都不会太难受。真正麻烦的是三个月后回来加功能，发现路由、配置和数据库连接混在一起。'},
              {'type': 'paragraph', 'text': '下面是我目前比较顺手的一套目录约定，重点不是“标准答案”，而是让每一层都知道自己该做什么。'},
              {'type': 'heading', 'level': 2, 'text': '目录结构'},
              {'type': 'code',
               'lang': 'text',
               'code': 'backend/\n'
                       '├── src/mywebproject/\n'
                       '│   ├── api/\n'
                       '│   │   ├── router.py\n'
                       '│   │   └── health.py\n'
                       '│   ├── schema/\n'
                       '│   ├── config.py\n'
                       '│   ├── db.py\n'
                       '│   └── main.py\n'
                       '├── tests/\n'
                       '└── pyproject.toml'},
              {'type': 'paragraph',
               'text': 'api 只处理请求和响应，schema 放 Pydantic 模型，config 读取环境变量，db 管理数据库会话。main.py '
                       '负责把它们组装起来，不承载业务逻辑。'},
              {'type': 'heading', 'level': 2, 'text': '配置集中管理'},
              {'type': 'paragraph',
               'text': '用 pydantic-settings 可以把环境变量和默认值放在一个类里，还能顺便得到类型校验。启动时如果缺少 '
                       'DATABASE_URL，程序会直接报错，而不是等到第一个请求进来才发现。'},
              {'type': 'code',
               'lang': 'python',
               'code': 'class Settings(BaseSettings):\n'
                       '    model_config = SettingsConfigDict(env_file=ENV_FILE)\n'
                       '\n'
                       "    APP_NAME: str = 'mywebproject'\n"
                       '    DEBUG: bool = False\n'
                       '    DATABASE_URL: str'},
              {'type': 'heading', 'level': 2, 'text': '路由只做路由的事'},
              {'type': 'paragraph', 'text': '健康检查是最小的例子，但能说明问题：路由函数只返回 schema，不关心数据库怎么连、日志怎么写。'},
              {'type': 'code',
               'lang': 'python',
               'code': "@router.get('/health', response_model=HealthResponse)\n"
                       'def health() -> HealthResponse:\n'
                       "    return HealthResponse(status='ok')"},
              {'type': 'paragraph',
               'text': '当接口开始变多时，我会按领域拆分 APIRouter，再在总路由里统一挂载。这样新增一个模块时，不需要修改已有的业务文件。'},
              {'type': 'quote', 'text': '目录结构不会自动让代码变好，但它能让错误的位置变得显眼。'},
              {'type': 'heading', 'level': 2, 'text': '启动时做一次自检'},
              {'type': 'paragraph',
               'text': '在 lifespan 里检查数据库连接，失败就中止启动。这个习惯帮我提前发现过好几次环境变量写错的问题。配合 Docker Compose 的 '
                       'healthcheck，整个本地环境会稳定很多。'},
              {'type': 'list',
               'ordered': False,
               'items': ['配置从环境变量来，不写死在代码里', '路由、模型、数据库各自分层', '启动阶段尽早失败，别把问题留到运行时']},
              {'type': 'paragraph',
               'text': '这套结构目前支撑着这个博客的后端。等接口再多一些，也许会继续调整，但至少现在，每一次修改都还能找到应该去的地方。'}]},
 {'slug': 'docker-compose-local-stack',
  'title': '用 Docker Compose 编排一次本地全栈环境',
  'date': '2026-08-07',
  'tags': ['Docker', '运维'],
  'summary': '前端 Nginx、FastAPI 和 MySQL 一条命令启动，顺便聊聊健康检查与数据卷。',
  'content': [{'type': 'paragraph',
               'text': '本地开发最烦的事情之一，是每次拉下代码都要重新回忆一遍：数据库怎么起、环境变量放哪、前端代理指向哪个端口。用 Docker Compose '
                       '把这些约定写进文件之后，换一台机器也能一条命令启动。'},
              {'type': 'heading', 'level': 2, 'text': '三个服务，一张网'},
              {'type': 'paragraph',
               'text': '这个项目由前端、后端和 MySQL 组成。前端构建后交给 Nginx，后端用 FastAPI，数据库单独一个容器。Compose '
                       '会为它们创建同一张默认网络，服务之间直接用服务名访问。'},
              {'type': 'code',
               'lang': 'yaml',
               'code': 'services:\n'
                       '  backend:\n'
                       '    build: ./backend\n'
                       '    ports:\n'
                       "      - '8000:8000'\n"
                       '    depends_on:\n'
                       '      db:\n'
                       '        condition: service_healthy\n'
                       '\n'
                       '  db:\n'
                       '    image: mysql\n'
                       '    healthcheck:\n'
                       "      test: ['CMD-SHELL', 'mysqladmin ping -uroot "
                       '-p"$$MYSQL_ROOT_PASSWORD"\']'},
              {'type': 'paragraph',
               'text': '注意 depends_on 里的 service_healthy。只写 depends_on 只能保证容器被启动，不能保证 MySQL '
                       '已经准备好接受连接。对数据库来说，这个区别很关键。'},
              {'type': 'heading', 'level': 2, 'text': '健康检查不是装饰'},
              {'type': 'paragraph',
               'text': 'MySQL 容器启动很快，但初始化数据库往往要几秒钟。第一次跑 Compose '
                       '时，后端因为连接失败直接退出，排查了半天才发现是启动顺序问题。加上健康检查之后，后端会等数据库真正可用再启动。'},
              {'type': 'paragraph',
               'text': '健康检查命令里的美元符号需要写成两个，否则会被 Compose 提前展开。这个坑我踩过一次，现在会特意在文件里检查。'},
              {'type': 'heading', 'level': 2, 'text': '数据卷与初始化脚本'},
              {'type': 'paragraph',
               'text': '数据库数据必须放在命名卷里，否则容器一删数据就没了。初始化 SQL 则挂载到 '
                       '/docker-entrypoint-initdb.d，它只会在数据目录为空时执行一次。'},
              {'type': 'code',
               'lang': 'yaml',
               'code': 'volumes:\n'
                       '  - mysql_data:/var/lib/mysql\n'
                       '  - ./init.sql:/docker-entrypoint-initdb.d/01-init.sql:ro'},
              {'type': 'quote', 'text': '基础设施的价值，是把容易忘记的步骤变成不容忘记的约束。'},
              {'type': 'heading', 'level': 2, 'text': '别把密钥写进镜像'},
              {'type': 'paragraph',
               'text': '数据库密码、后端端口这些配置都放在 .env 里，仓库只提交 .env.example。Compose 会自动读取 '
                       '.env，但镜像本身不应该包含任何真实密钥。'},
              {'type': 'list',
               'ordered': False,
               'items': ['服务之间用服务名通信，不写 localhost',
                         '用 healthcheck 控制启动顺序',
                         '数据放命名卷，初始化脚本保持幂等',
                         '敏感配置只进 .env，不进镜像']},
              {'type': 'paragraph',
               'text': '现在我的本地启动流程只有一条 docker compose up --build。省下来的时间不多，但少了很多“这次应该没问题吧”的不确定感。'}]},
 {'slug': 'sapiens-reread',
  'title': '重读《人类简史》：故事为什么重要',
  'date': '2026-05-12',
  'tags': ['阅读', '思考'],
  'summary': '从认知革命到想象的共同体，一些关于叙事、协作与自我欺骗的笔记。',
  'content': [{'type': 'paragraph',
               'text': '第二次读《人类简史》，感受和第一次很不一样。第一次记住的是那些有趣的观点，这次更在意作者反复强调的一件事：智人之所以能统治世界，很大程度上是因为我们会讲故事。'},
              {'type': 'quote', 'text': '智人统治世界，是因为只有智人能够编织出关于虚构事物的故事。'},
              {'type': 'heading', 'level': 2, 'text': '大规模协作的起点'},
              {'type': 'paragraph',
               'text': '陌生人之间为什么能合作？因为大家相信同一套想象中的秩序。国家、货币、公司、法律，这些概念在物理世界里并不存在，却能让几百万互不相识的人按照同一套规则行动。'},
              {'type': 'paragraph',
               'text': '作者说，这不是欺骗，而是一种必要的虚构。故事让协作的半径从几十人扩大到几万人、几千万人。每次想到这一点，我都会重新审视自己每天参与的那些“理所当然”的事情。'},
              {'type': 'heading', 'level': 2, 'text': '故事也困住了我们'},
              {'type': 'paragraph',
               'text': '故事带来秩序，也带来边界。一旦某个故事被足够多的人相信，它就会变成不容置疑的现实。身处其中的人很难看到故事之外的可能。'},
              {'type': 'list',
               'ordered': False,
               'items': ['国家让陌生人愿意为彼此承担义务',
                         '货币让价值可以跨越时间和空间交换',
                         '公司让一群人为了一个不存在的实体工作',
                         '品牌让消费者为一段叙事支付溢价']},
              {'type': 'paragraph', 'text': '读到这一段时，我突然理解了为什么改变一个组织这么难。你要改变的不是流程，而是一群人共同相信的故事。'},
              {'type': 'heading', 'level': 2, 'text': '写给自己的提醒'},
              {'type': 'paragraph',
               'text': '既然秩序是想象的，那么它就不是唯一的。很多看起来坚不可摧的规则，其实只是某个时间点被共同接受的约定。这个视角既让人不安，也让人自由。'},
              {'type': 'paragraph', 'text': '我不敢说自己读懂了这本书，但它确实让我在看待日常时多了一层怀疑：这件事为什么是这样？还有没有别的可能？'},
              {'type': 'paragraph', 'text': '也许读书的意义就在这里：不是为了得到答案，而是为了多几个问题。'}]},
 {'slug': 'terminal-workflow',
  'title': '我的终端工作流：tmux、Neovim 与 fzf',
  'date': '2025-12-30',
  'tags': ['工具', '效率'],
  'summary': '一套用顺手很久的本地开发组合，以及我为什么不再频繁换工具。',
  'content': [{'type': 'paragraph',
               'text': '我曾经很喜欢折腾工具。换编辑器、换 '
                       'shell、换窗口管理器，每次都能获得一种“效率要起飞了”的错觉。后来发现，真正让工作变顺的，不是工具本身，而是固定下来的习惯。'},
              {'type': 'paragraph', 'text': '现在这套工作流已经用了两年多，几乎没变过。记录一下，也当作给未来自己的备忘。'},
              {'type': 'heading', 'level': 2, 'text': '一个会话，多个窗口'},
              {'type': 'paragraph',
               'text': 'tmux 解决的是上下文切换的问题。一个项目开一个会话，代码、日志、测试各占一个窗口。断线或者关掉终端之后，回来还能接上原来的状态。'},
              {'type': 'code',
               'lang': 'bash',
               'code': 'tmux new -s blog\n'
                       'tmux new-window -n code\n'
                       'tmux new-window -n logs\n'
                       'tmux attach -t blog'},
              {'type': 'paragraph',
               'text': '我常用的快捷键只有几个：前缀键加 c 新建窗口，加数字切换窗口，加 d 暂时离开。不需要背完整张表，够用就好。'},
              {'type': 'heading', 'level': 2, 'text': '编辑器只需要一个'},
              {'type': 'paragraph',
               'text': 'Neovim 的好处不在于快，而在于所有操作都可以用同一套肌肉记忆完成。文件跳转、搜索替换、Git 操作，都在一个界面里。'},
              {'type': 'code',
               'lang': 'lua',
               'code': "vim.keymap.set('n', '<leader>ff', '<cmd>Telescope find_files<cr>')\n"
                       "vim.keymap.set('n', '<leader>fg', '<cmd>Telescope live_grep<cr>')\n"
                       "vim.keymap.set('n', '<leader>fb', '<cmd>Telescope buffers<cr>')"},
              {'type': 'paragraph',
               'text': '我的配置原则是：只加自己每周都会用到的插件。看到别人炫酷的配置会心动，但用不上的功能最终只会变成维护成本。'},
              {'type': 'heading', 'level': 2, 'text': '模糊查找改变肌肉记忆'},
              {'type': 'paragraph',
               'text': 'fzf 最迷人的地方，是它把“记住路径”变成了“描述路径”。不用知道文件在哪一层，只要记得名字的一部分，就能在几秒内找到它。'},
              {'type': 'code',
               'lang': 'bash',
               'code': "git log --oneline | fzf --preview 'git show --stat {1}'"},
              {'type': 'paragraph', 'text': '上面这条命令几乎覆盖了我日常查看提交记录的需求。模糊查找加上预览窗口，比在网页里点来点去快很多。'},
              {'type': 'quote', 'text': '工具的上限，往往取决于你愿意花多少时间把它用顺手。'},
              {'type': 'heading', 'level': 2, 'text': '不再频繁换工具'},
              {'type': 'paragraph',
               'text': '现在的我很少主动寻找新工具了。不是失去了好奇心，而是终于承认：真正的效率来自熟练，而不是来自配置。把折腾工具的时间拿来读源码、写项目或者干脆休息，回报可能更高。'},
              {'type': 'list',
               'ordered': False,
               'items': ['固定一套顺手的快捷键', '只保留每周都会用的插件', '把配置放进版本控制，换机器五分钟恢复', '给工具留出变熟练的时间']},
              {'type': 'paragraph', 'text': '这套工作流没什么特别，但它足够安静。安静到我可以把注意力放在真正要做的事情上。'}]},
 {'slug': 'letter-to-myself',
  'title': '写给二十五岁的自己',
  'date': '2025-11-02',
  'tags': ['随笔'],
  'summary': '关于慢下来、长期主义，以及不再用效率衡量一切的一些碎碎念。',
  'content': [{'type': 'paragraph',
               'text': '二十五岁生日那天，我没有许愿，只是坐在窗边发了很久的呆。以前总觉得这个年纪应该已经想清楚很多事，真的到了才发现，不确定才是常态。'},
              {'type': 'heading', 'level': 2, 'text': '慢一点也没关系'},
              {'type': 'paragraph',
               'text': '有一段时间，我习惯用产出衡量每一天：今天写了多少代码，读了多少页书，完成了几个任务。效率很高，但人也变得很紧。'},
              {'type': 'paragraph',
               'text': '后来我开始允许自己有一些“没有产出”的时刻。散步、发呆、和朋友聊一些没有结论的话题。奇怪的是，很多卡住的问题反而在这些时候松动了。'},
              {'type': 'quote', 'text': '人生不是一场需要不断证明自己的考试，而是一段可以慢慢走的路。'},
              {'type': 'heading', 'level': 2, 'text': '把生活当成长期项目'},
              {'type': 'paragraph',
               'text': '如果把生活看成一个长期项目，很多选择的标准会变得不一样。短期看起来划算的事情，长期未必；短期看不到回报的投入，可能正在积累复利。'},
              {'type': 'list',
               'ordered': False,
               'items': ['保持阅读，但不必追求数量', '维护几段真正重要的关系', '为身体留出固定的运动时间', '做一件不为了变现的小事']},
              {'type': 'paragraph',
               'text': '我开始理解，长期主义不是咬牙坚持，而是找到一种可以持续很久的节奏。太快会耗尽，太慢会停滞，找到自己的速度比模仿别人更重要。'},
              {'type': 'heading', 'level': 2, 'text': '留一点没有用途的时间'},
              {'type': 'paragraph', 'text': '小时候画画、写字、拼模型，从来没有想过有什么用。长大后做每件事都想要一个结果，反而失去了那种单纯的快乐。'},
              {'type': 'paragraph',
               'text': '所以今年我想留一点时间给没有用途的事情。可能是重新拿起画笔，可能是学一首弹不好的曲子，也可能只是在周末骑车去一个没去过的地方。'},
              {'type': 'paragraph',
               'text': '写到这里，忽然觉得二十五岁也没那么可怕。想不清楚的事情可以继续想，走错的路也可以绕回来。只要还在认真地生活，就已经很好了。'}]}]
