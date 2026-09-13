"""All copy for the Macha recruitment PDF, English and Chinese editions.

This file is the editable source for the document's text. Layout code reads it
and never hard-codes strings, so wording can be revised without touching the
typesetting.

Editorial rules held throughout
-------------------------------
* Nothing is claimed that is not in the repository's own roadmap.
  The real cognitive core is Phase 3 and does not exist yet; the document says so.
* Minecraft is described as Test Environment 01 — the first Concrete Layer Test
  Case — never as Macha's subject or identity.
* No compensation, contract, location, hours, team size, funding, user numbers
  or shipped capability is invented. Unknown fields are marked TBD.
* No AI buzzwords. Every duty is written as an observable action.

Key terms are kept in English in the Chinese edition (Macha, Layer Protocol,
Test Environment 01, NPC, TBD) because they are the project's own vocabulary.
"""

# --------------------------------------------------------------------------
# English
# --------------------------------------------------------------------------

EN = {
    "lang_label": "EN",

    # -- 01 cover ---------------------------------------------------------
    "cover": {
        "eyebrow": "MACHA",
        "title_lines": ["FIRST WORLD", "OPERATOR"],
        "subtitle": "Minecraft Server Lead / First Player",
        "env": "Test Environment 01",
        "question_lines": [
            "\u201cFrom the player\u2019s perspective,",
            "what kind of game intelligent agent",
            "do we actually want?\u201d",
        ],
        "standfirst": (
            "Macha is an open research project building a cognitive skeleton for game NPCs "
            "that is independent of any engine and any model. Minecraft is the first world we "
            "have connected it to. Minecraft is not the project."
        ),
        "status": [
            ("STAGE", "pre-implementation · Phase 0 → 1"),
            ("NPC CAPABILITY", "not yet implemented"),
            ("COMPENSATION", "TBD"),
            ("LOCATION / HOURS", "TBD"),
        ],
    },

    # -- 02 the question --------------------------------------------------
    "question": {
        "title": "THE QUESTION",
        "sub": "Why do intelligent NPCs still feel fake?",
        "p1": (
            "A model can give an NPC more knowledge than any hand-written dialogue tree. "
            "It can answer questions, hold a persona, and speak fluently. Players still walk "
            "away saying it felt like talking to a chatbot wearing a costume."
        ),
        "p2": (
            "We are not asking how to make an NPC smarter. We are asking why more intelligence "
            "does not produce more presence."
        ),
        "belief_intro": (
            "A player starts treating an NPC as something that exists in the world at the "
            "moment they believe four things:"
        ),
        "beliefs": [
            ("01", "This NPC has its own state.",
             "It is doing something when I am not looking at it."),
            ("02", "This NPC has its own purpose.",
             "It wants something that is not me."),
            ("03", "This NPC remembers what happened.",
             "It carries the past forward instead of re-deriving it."),
            ("04", "This NPC is not generated to answer me.",
             "Its behaviour comes from being somewhere in the world."),
        ],
        "p3": (
            "None of these four are properties of intelligence. They are properties of a "
            "system that persists in a world over time. That is the gap this project exists to "
            "close — and it cannot be measured from inside the architecture."
        ),
        "closing": "Which is why the person we are looking for is a player first, and a researcher second.",
    },

    # -- 03 the role ------------------------------------------------------
    "role": {
        "title": "THE ROLE",
        "sub": "First World Operator",
        "lead": "This is not a Minecraft server administrator role.",
        "not": "NOT   server admin · operations · GM · QA tester · community moderator",
        "bridge": "It is the intersection of four jobs that do not normally live in the same person.",
        "parts": [
            ("SERVER LEAD", "Keep the test world running, reachable, and in a known state."),
            ("FIRST PLAYER", "Be the first real person inside it, for hours at a time."),
            ("WORLD OPERATOR", "Shape the conditions the agents live in, and record what you changed."),
            ("NPC EXPERIENCE RESEARCHER", "Find the moments that break the illusion, and explain why they break."),
        ],
        "honest": (
            "Today the world runs, the boundary between Macha and the world is being specified, "
            "and the agent you would be testing has not been built. You would be the first person "
            "who is not building it to stand inside it and say what is wrong with it."
        ),
        "zero_title": "THIS IS A 0 → 1 ROLE",
        "zero_body": (
            "You are not joining a finished product and executing a known procedure. Much of what "
            "defines this role does not exist yet, and you would be helping to write it:"
        ),
        "zero_items": [
            "what makes an AI NPC good",
            "what makes one read as fake",
            "which parts of a world state an agent should be able to perceive",
            "what behaviour actually counts as continuous",
            "what relationship a player should be able to form with an NPC",
        ],
        "zero_close": "None of these have an accepted answer. That is the work.",
    },

    # -- 04 what you will do ---------------------------------------------
    "work": {
        "title": "WHAT YOU WILL DO",
        "sub": "Five jobs. Only the third one is why the role exists.",
        "duties": [
            {
                "num": "01",
                "name": "RUN THE WORLD",
                "body": (
                    "Keep Test Environment 01 alive, reachable, and in a state you can describe. "
                    "Not an operations role — you keep the place habitable so the experiment can run."
                ),
                "bullets": [
                    "server maintenance and world management",
                    "basic configuration",
                    "player access for testers",
                    "a short record of what changed between sessions",
                ],
            },
            {
                "num": "02",
                "name": "BE THE FIRST PLAYER",
                "body": (
                    "Go in and live there, for hours rather than minutes. Talk to the agents, "
                    "ignore them, help them, get in their way. Play, and keep asking one question:"
                ),
                "bullets": [
                    "\u201cif I do this, what happens?\u201d",
                ],
            },
            {
                "num": "03",
                "name": "FIND THE FAKE",
                "body": (
                    "This is the job. You are not hunting for errors — you are hunting for the "
                    "specific moments that make an agent read as fake:"
                ),
                "bullets": [
                    "behaviour that does not fit the situation it is in",
                    "memory a player can tell is not real",
                    "a motive that does not hold up",
                    "behaviour disconnected from the state of the world",
                    "responses generated at the player rather than out of the world",
                    "no continuity from one encounter to the next",
                    "contradictions a person would not make",
                    "something that sounds clever but is not an agent with a stake",
                ],
                "foot": (
                    "A bug report says \u201cthe NPC did X.\u201d Your report has to say why X made it "
                    "feel like nothing was there."
                ),
            },
            {
                "num": "04",
                "name": "CREATE SITUATIONS",
                "body": "Do not wait for behaviour to appear. Build the conditions that force it:",
                "bullets": [
                    "change the agent\u2019s environment while it is not looking",
                    "create conflict between two agents",
                    "change what resources are available",
                    "disappear for a long time, then come back",
                    "give two agents a reason to know each other",
                    "watch what happens when no player is present",
                    "check how an agent reacts hours after an event, not seconds",
                ],
                "foot": "You are expected to propose your own experiments.",
            },
            {
                "num": "05",
                "name": "REPORT EXPERIENCE",
                "body": "Keep one Experience Log. One entry per moment that mattered:",
                "chain": ["SITUATION", "OBSERVATION", "PLAYER FEELING", "WHY IT FELT WRONG", "POSSIBLE CAUSE", "NEXT EXPERIMENT"],
                "foot": (
                    "No technical analysis is required. Write it the way you would describe it to "
                    "another player. Player experience first — we handle the translation into engineering."
                ),
            },
        ],
    },

    # -- 05 who we are looking for ---------------------------------------
    "fit": {
        "title": "WHO WE ARE LOOKING FOR",
        "sub": "Technical ability is not the first priority. It is not the second one either.",
        "quote": (
            "We would rather have a player who knows Minecraft deeply and knows nothing about AI, "
            "than an agent-framework expert who rarely plays. The first person will simply be "
            "better at this job."
        ),
        "spec_title": "WHAT WE WEIGHT",
        "spec": [
            ("Minecraft experience", 5),
            ("Sensitivity to NPC believability", 5),
            ("Observation and articulation", 5),
            ("Willingness to test over months", 5),
            ("Server management", 3),
            ("Java / Kotlin", 2),
            ("AI / LLM", 2),
        ],
        "profile_title": "YOU MIGHT BE THIS PERSON IF",
        "profile": [
            "you have played Minecraft for years and can still feel when something in the world is off",
            "you have opinions about how NPCs in games behave, and will defend them",
            "you notice small details other players walk past",
            "you have said \u201cthis feels wrong\u201d about a game without yet being able to explain why",
            "you are willing to go back into the same world many times",
            "you are willing to write down what happened",
            "you want to propose your own experiments",
            "you can work without being managed closely",
        ],
        "not_title": "NOT FOR YOU IF",
        "not_items": [
            "you want a normal Minecraft admin position",
            "you want to maintain a server and be done",
            "you only want to test whether features run",
            "you are not interested in watching how agents behave",
            "you do not want to write anything down",
            "\u201cwhy does an NPC read as real\u201d is not a question you care about",
        ],
    },

    # -- 06 the experiment ------------------------------------------------
    "experiment": {
        "title": "THE EXPERIMENT",
        "sub": "The role is one node in a feedback loop, and it is the node we cannot fill internally.",
        "loop_title": "THE LOOP",
        "loop": [
            ("PLAYER", "a person does something the world does not expect", False),
            ("WORLD", "the world changes state", False),
            ("NPC", "the agent reacts — or fails to", False),
            ("EXPERIENCE", "the player feels that something is wrong", True),
            ("OBSERVATION", "you record the moment, and why it broke", False),
            ("MACHA", "the architecture changes, and the loop runs again", False),
        ],
        "loop_label": "FEEDBACK",
        "right_a": (
            "EXPERIENCE is the one node the team cannot fill. The people who build the architecture "
            "are the worst possible judges of whether an agent reads as real: they already know how "
            "it works, and they cannot un-know it."
        ),
        "right_b": "Everything else in this document follows from that missing node.",
        "state_title": "WHERE THIS ACTUALLY IS",
        "state_note": "As of 2026-09, stated against the project\u2019s own roadmap.",
        "state": [
            ("Architecture and boundaries", "defined, under revision"),
            ("Layer Protocol v0", "specification in progress"),
            ("Test world", "running"),
            ("First Layer connection", "in progress"),
            ("Cognitive core (real agents)", "not built \u2014 Phase 3"),
            ("A believable agent to test", "does not exist yet"),
        ],
        "state_close": (
            "We are not going to describe this as further along than it is. If the shape of it "
            "above is not interesting to you, this is the wrong project."
        ),
        "stack_title": "WHAT MACHA IS",
        "stack": ["MACHA CORE", "LAYER PROTOCOL", "MINECRAFT LAYER", "MINECRAFT"],
        "stack_note": (
            "Minecraft is Test Environment 01 — the first Concrete Layer Test Case, not the "
            "subject of the project. Skyrim, Cyberpunk 2077, Unreal, Unity and plain simulators "
            "would each be their own Layer, built independently."
        ),
        "stack_future": "FUTURE ENVIRONMENTS — each its own Layer, later",
        "stack_rule": "Adding a Layer must never require changing Macha Core.",
    },

    # -- 07 first experiment ---------------------------------------------
    "first": {
        "title": "YOUR FIRST EXPERIMENT",
        "sub": "The task, if you get this far. This is the evaluation.",
        "task_title": "THE TASK",
        "task": [
            "Get an NPC to show that it remembers something you did yesterday — without ever telling it that it remembers.",
        ],
        "task_body": (
            "Choose the \u201csomething\u201d yourself. Yesterday, in the world, you did something in front "
            "of the agent, or out of its sight, or to something it cares about. Today you come back and "
            "let it be visible."
        ),
        "rule": "You are not allowed to say: \u201cremember when I \u2026\u201d",
        "ask_title": "WHAT WE WILL ASK YOU AFTERWARDS",
        "asks": [
            "What did you observe?",
            "Which moment made the NPC feel real to you?",
            "Which moment made it feel fake?",
            "What would you try next?",
        ],
        "why_title": "WHY THIS TASK",
        "why": (
            "It tests the thing we care about and nothing else: not memory retrieval in the abstract, "
            "but whether a player can feel that something in the world remembered them."
        ),
        "why_foot": "A good answer to question 03 is worth more to us than a good answer to question 02.",
        "no_interview": "no algorithm interview · no whiteboard · no take-home code exercise",
    },

    # -- 08 join us -------------------------------------------------------
    "join": {
        "title": "JOIN US",
        "sub": "Three steps. None of them is a technical interview.",
        "steps": [
            ("01", "INTRODUCE YOURSELF",
             "Tell us how you play. What you have built, broken, explored, or spent too long on in "
             "Minecraft. Where a game has felt fake to you. Nothing formal is required.",
             "time: none"),
            ("02", "SPEND TIME IN THE WORLD",
             "We give you access to Test Environment 01. Play it the way you would play anything. "
             "We are looking at whether you notice things, not at whether you can do something clever.",
             "time: a few sessions"),
            ("03", "RUN THE FIRST EXPERIMENT",
             "The task on the previous page. Send us your four answers.",
             "time: one experience"),
        ],
        "near_title": "WHAT YOU WOULD BE CLOSE TO",
        "near": (
            "AI agents · game AI · NPC architecture · world models · agent memory · social behaviour · "
            "player experience · environment–agent interaction"
        ),
        "tbd_title": "WHAT WE CANNOT TELL YOU YET",
        "tbd_body": (
            "This is an early-stage experimental project, not a funded company. What it becomes is "
            "partly what you make of it."
        ),
        "tbd": [
            ("Compensation", "TBD"),
            ("Contract form", "TBD"),
            ("Location", "TBD"),
            ("Hours", "TBD"),
        ],
        "apply_label": "TO APPLY",
        "apply_email": "zhaoceaser@gmail.com",
        "apply_subject": "Subject: First World Operator",
        "apply_note": "Write in English or Chinese. A short message is enough.",
        "closing": (
            "What should an intelligent game agent actually be? Nobody has a good answer yet. "
            "We are looking for the person who wants to find out."
        ),
    },

    "footer": {
        "left": "MACHA · EARLY-STAGE EXPERIMENTAL RECRUITMENT",
        "right": "REV 01 · 2026-09",
        "cover_strip": "EARLY-STAGE EXPERIMENTAL RECRUITMENT DOCUMENT · MACHA · REV 01",
    },
}


# --------------------------------------------------------------------------
# Chinese
# --------------------------------------------------------------------------

ZH = {
    "lang_label": "中文",

    "cover": {
        "eyebrow": "MACHA",
        "title_lines": ["FIRST WORLD", "OPERATOR"],
        "title_cn": "第一位世界运营者",
        "subtitle": "Minecraft 服务器主理 / 第一位玩家",
        "env": "Test Environment 01",
        "question_lines": [
            "「从玩家的视角出发，",
            "我们到底需要一个什么样的",
            "游戏智能体？」",
        ],
        "standfirst": (
            "Macha 是一个开放研究项目，目标是构建一套不依赖任何引擎、不依赖任何模型的游戏 NPC 认知骨架。"
            "Minecraft 是我们接入的第一个世界。但 Minecraft 不是这个项目本身。"
        ),
        "status": [
            ("阶段", "尚未进入实现 · Phase 0 → 1"),
            ("NPC 能力", "尚未实现"),
            ("报酬", "TBD"),
            ("地点 / 工时", "TBD"),
        ],
    },

    "question": {
        "title": "THE QUESTION",
        "sub": "为什么足够聪明的 NPC，依然让人觉得是假的？",
        "p1": (
            "大模型可以让一个 NPC 拥有远超手写对话树的知识量。它能回答问题、能维持人设、说话也很流畅。"
            "但玩家离开之后，说的仍然是：像是在和一个穿着戏服的聊天机器人对话。"
        ),
        "p2": "我们要问的不是「怎样让 NPC 更聪明」，而是「为什么更多的智能，换不来更多的存在感」。",
        "belief_intro": "玩家开始把一个 NPC 当成世界里真实存在的东西，是在他相信下面四件事的那一刻：",
        "beliefs": [
            ("01", "这个 NPC 有自己的状态。", "我不看它的时候，它也在做它自己的事。"),
            ("02", "这个 NPC 有自己的目的。", "它想要的东西不是我。"),
            ("03", "这个 NPC 记得发生过什么。", "它把过去带着走，而不是每次重新推一遍。"),
            ("04", "这个 NPC 不是在回应我。", "它的行为来自它身处世界之中，而不是为了回答我而生成。"),
        ],
        "p3": (
            "这四件事没有一件属于「智能」。它们属于一个「在时间里、在世界里持续存在」的系统。"
            "这正是本项目要填的缺口——而它无法从架构内部被测量出来。"
        ),
        "closing": "所以我们找的第一个人，首先是一个玩家，其次才是一个研究者。",
    },

    "role": {
        "title": "THE ROLE",
        "sub": "First World Operator",
        "lead": "这不是一个 Minecraft 服务器管理员岗位。",
        "not": "不属于   服务器运维 · 运营 · GM · QA 测试 · 社区版主",
        "bridge": "它是四种通常不会出现在同一个人身上的角色交叉：",
        "parts": [
            ("SERVER LEAD", "让测试世界持续运行、可进入、状态清楚。"),
            ("FIRST PLAYER", "成为第一个真正进去生活的人，一次待上几个小时。"),
            ("WORLD OPERATOR", "塑造智能体所处环境的条件，并记录你改了什么。"),
            ("NPC EXPERIENCE RESEARCHER", "找到那个让幻觉破裂的瞬间，并说清它为什么破裂。"),
        ],
        "honest": (
            "现状是：世界已经能跑起来，Macha 与世界之间的边界正在被定义，而你要测试的那个智能体还没有被做出来。"
            "你将是第一个「不是造它的人」却站进里面、并且指出它哪里不对的人。"
        ),
        "zero_title": "这是一个 0 → 1 的角色",
        "zero_body": "你不是加入一个已经完成的产品、然后执行既定流程。这个角色的很多定义目前还不存在，你会参与把它写出来：",
        "zero_items": [
            "什么样的 AI NPC 算好",
            "什么样的 NPC 是假的",
            "世界的哪些状态应该被智能体感知到",
            "什么样的行为才算真正具有连续性",
            "玩家和一个 AI NPC 之间应该形成什么关系",
        ],
        "zero_close": "这些问题目前都没有公认答案。这就是这份工作。",
    },

    "work": {
        "title": "WHAT YOU WILL DO",
        "sub": "五件事。其中只有第三件是设这个岗位的理由。",
        "duties": [
            {
                "num": "01",
                "name": "RUN THE WORLD",
                "body": "让 Test Environment 01 活着、进得去、并且处于一个你能描述的状态。这不是运维岗——你是在保持这个地方可居住，好让实验能跑。",
                "bullets": [
                    "服务器维护与世界管理",
                    "基础配置",
                    "为测试者开放访问",
                    "简单记录每次测试之间改了什么",
                ],
            },
            {
                "num": "02",
                "name": "BE THE FIRST PLAYER",
                "body": "进去，住在里面，待上几个小时而不是几分钟。和智能体说话、无视它们、帮它们、挡它们的路。然后反复问自己同一个问题：",
                "bullets": ["「如果我这样做，它会怎样？」"],
            },
            {
                "num": "03",
                "name": "FIND THE FAKE",
                "body": "这是这份工作的核心。你要找的不是错误，而是那些让一个智能体「读起来就是假的」的具体瞬间：",
                "bullets": [
                    "行为与它所处的情境对不上",
                    "玩家一眼能看出不真实的记忆",
                    "动机站不住",
                    "行为与世界当前状态脱节",
                    "只是为了回应玩家而生成的回答",
                    "从一次相遇带到下一次之间的连续性断裂",
                    "一个真人不会犯的前后矛盾",
                    "听起来很聪明，但背后不是一个有立场的存在",
                ],
                "foot": "Bug 报告会写「NPC 做了 X」。你的报告要写清：为什么 X 让人感觉那里根本什么都没有。",
            },
            {
                "num": "04",
                "name": "CREATE SITUATIONS",
                "body": "不要等行为自己出现。主动构造能逼出行为的条件：",
                "bullets": [
                    "在智能体看不到的时候改变它的环境",
                    "让两个智能体之间产生冲突",
                    "改变可获取的资源",
                    "长时间不出现，然后再回来",
                    "给两个智能体一个认识彼此的理由",
                    "观察玩家不在场时会发生什么",
                    "观察一件事发生数小时之后，它如何反应",
                ],
                "foot": "你可以自己提出实验。我们期待你这么做。",
            },
            {
                "num": "05",
                "name": "REPORT EXPERIENCE",
                "body": "维护一份 Experience Log。每一个值得记录的瞬间写一条：",
                "chain": ["SITUATION", "OBSERVATION", "PLAYER FEELING", "WHY IT FELT WRONG", "POSSIBLE CAUSE", "NEXT EXPERIMENT"],
                "foot": "不需要技术分析。就按你会怎么讲给另一个玩家听来写。玩家体验优先——翻译成工程语言是我们的事。",
            },
        ],
    },

    "fit": {
        "title": "WHO WE ARE LOOKING FOR",
        "sub": "技术能力不是第一优先级，也不是第二优先级。",
        "quote": (
            "我们宁愿要一个非常懂 Minecraft、但完全不懂 AI 的玩家，"
            "也不要一个非常懂 Agent 框架、但几乎不玩游戏的专家。前一种人做这件事会更好。"
        ),
        "spec_title": "我们看重的权重",
        "spec": [
            ("Minecraft 经验", 5),
            ("对 NPC 可信度的敏感度", 5),
            ("观察与表达能力", 5),
            ("长期测试的意愿", 5),
            ("服务器管理", 3),
            ("Java / Kotlin", 2),
            ("AI / LLM", 2),
        ],
        "profile_title": "你可能是这个人，如果",
        "profile": [
            "你玩了很多年 Minecraft，并且仍然能感觉到世界里某处不对",
            "你对游戏里的 NPC 行为有自己的判断，并且愿意为它辩护",
            "你会注意到别的玩家走过去的那些小细节",
            "你曾经说过「这个感觉不对」，但当时还说不清为什么",
            "你愿意反复进入同一个世界很多次",
            "你愿意把发生过的事情写下来",
            "你想提出自己的实验",
            "你不需要被紧密管理也能工作",
        ],
        "not_title": "NOT FOR YOU IF",
        "not_items": [
            "你想找一个普通的 Minecraft 管理岗",
            "你只想把服务器维护好然后收工",
            "你只想测试功能有没有跑起来",
            "你对观察智能体的行为没有兴趣",
            "你不愿意写任何东西",
            "「为什么一个 NPC 会让人相信它存在」不是你在意的问题",
        ],
    },

    "experiment": {
        "title": "THE EXPERIMENT",
        "sub": "这个岗位是一条反馈回路上的一个节点，而且是我们在内部补不上的那个节点。",
        "loop_title": "THE LOOP",
        "loop": [
            ("PLAYER", "一个人做了一件世界没预料到的事", False),
            ("WORLD", "世界状态发生改变", False),
            ("NPC", "智能体做出反应——或者反应失败", False),
            ("EXPERIENCE", "玩家感觉到有什么不对", True),
            ("OBSERVATION", "你把这个瞬间、以及它为什么破裂，记录下来", False),
            ("MACHA", "架构发生改变，回路重新跑一遍", False),
        ],
        "loop_label": "FEEDBACK",
        "right_a": (
            "EXPERIENCE 是团队内部补不上的那个节点。造架构的人，恰恰是最不适合判断「它读起来真不真」的人："
            "他们知道它是怎么运作的，而且无法把这件事忘掉。"
        ),
        "right_b": "这份文档里其余的一切，都是从这一个缺失的节点推出来的。",
        "state_title": "目前的真实状态",
        "state_note": "截至 2026-09，按项目自己的 roadmap 口径。",
        "state": [
            ("架构与边界", "已定义，正在修订"),
            ("Layer Protocol v0", "规格撰写中"),
            ("测试世界", "已可运行"),
            ("第一个 Layer 接入", "进行中"),
            ("认知核心（真正的智能体）", "尚未构建 —— Phase 3"),
            ("一个可信的、可供测试的智能体", "目前不存在"),
        ],
        "state_close": "我们不会把它说得比实际更成熟。如果上面这个形状对你不构成吸引力，那这个项目就不适合你。",
        "stack_title": "MACHA 是什么",
        "stack": ["MACHA CORE", "LAYER PROTOCOL", "MINECRAFT LAYER", "MINECRAFT"],
        "stack_note": (
            "Minecraft 是 Test Environment 01——第一个具体的 Layer 测试用例，而不是这个项目的主题。"
            "Skyrim、Cyberpunk 2077、Unreal、Unity 以及纯模拟环境，将来都会各自对应一个独立的 Layer。"
        ),
        "stack_future": "未来的环境 —— 各自独立成 Layer，之后再做",
        "stack_rule": "新增一个 Layer，永远不应要求改动 Macha Core。",
    },

    "first": {
        "title": "YOUR FIRST EXPERIMENT",
        "sub": "如果你走到了这一步。这就是全部考核。",
        "task_title": "任务",
        "task": ["让一个 NPC 表现出它记得你昨天做过的一件事——而你始终不能告诉它它记得。"],
        "task_body": (
            "「那件事」由你自己选。昨天，在世界里，你当着它的面做了一件事，或者背着它做了一件事，"
            "或者动了它在意的东西。今天你回来，让它变得可见。"
        ),
        "rule": "你不允许说：「你还记得我上次……」",
        "ask_title": "之后我们会问你",
        "asks": [
            "你观察到了什么？",
            "哪一个瞬间让你觉得这个 NPC 是真的？",
            "哪一个瞬间让你觉得它是假的？",
            "你下一次会怎么设计实验？",
        ],
        "why_title": "为什么要设这个任务",
        "why": "它只测我们在意的那一件事：不是抽象的「记忆召回」，而是玩家能不能感觉到，世界里的某个东西记住了他。",
        "why_foot": "第 03 题答得好，对我们来说比第 02 题答得好更有价值。",
        "no_interview": "没有算法面试 · 没有白板题 · 没有回家作业式的代码题",
    },

    "join": {
        "title": "JOIN US",
        "sub": "三步。没有一步是技术面试。",
        "steps": [
            ("01", "自我介绍一下",
             "讲讲你是怎么玩游戏的。你在 Minecraft 里造过什么、弄坏过什么、探索过什么，或者在哪件事上花了过多的时间。"
             "以及在哪个游戏里，你感觉到过「假」。不需要任何正式格式。",
             "耗时：无"),
            ("02", "进世界里待一会儿",
             "我们给你 Test Environment 01 的访问权限。像玩任何东西一样去玩它。我们看的是你有没有注意到东西，"
             "而不是你能不能做出什么聪明操作。",
             "耗时：几次游玩"),
            ("03", "跑第一个实验",
             "上一页那个任务。把你的四个回答发给我们。",
             "耗时：一次体验"),
        ],
        "near_title": "你会接触到",
        "near": "AI agents · game AI · NPC 架构 · world models · agent memory · 社会行为 · 玩家体验 · 环境与智能体的交互",
        "tbd_title": "目前我们还不能告诉你的",
        "tbd_body": "这是一个早期实验项目，不是一家已融资的公司。它会变成什么，有一部分取决于你把它做成什么。",
        "tbd": [
            ("报酬", "TBD"),
            ("合同形式", "TBD"),
            ("地点", "TBD"),
            ("工作时间", "TBD"),
        ],
        "apply_label": "申请方式",
        "apply_email": "zhaoceaser@gmail.com",
        "apply_subject": "邮件标题：First World Operator",
        "apply_note": "中文或英文都可以。一段简短的话就够了。",
        "closing": "一个游戏智能体到底应该是什么？目前没有人有好的答案。我们在找那个想把它找出来的人。",
    },

    "footer": {
        "left": "MACHA · 早期实验性招募文档",
        "right": "REV 01 · 2026-09",
        "cover_strip": "早期实验性招募文档 · MACHA · REV 01",
    },
}

CONTENT = {"en": EN, "zh": ZH}
