"""撒该爬上桑树 — narration script and scene list (single source of truth for stories/zacchaeus).

Luke 19:1-10, told for children aged 3-8, about 4 minutes, in the narration style of SCRIPT_STYLE.md. Small actions
and feelings are added (jumping to see over the crowd, Zacchaeus's surprise), no new plot; the story does not say
what Zacchaeus did afterwards, so the narration keeps to his promise and his changed heart. The 桑树 of the 和合本 is
a sycamore-fig (Ficus sycomorus: a wide, low-branching tree with figs on its trunk), not a mulberry: draw that. Same
pipeline as the other films: python3 build.py all --story zacchaeus.

Speakers (narrator N from voice/tts.py; the others below):
    N = narrator   Z = Jesus (the same voice as in 耶稣平静风浪 and 迷失的羊)   S = Zacchaeus   C = the crowd (a group)
Jesus is drawn as a person (his design from the earlier films), kind and calm, never comic. Owner direction: every
story looks different: Jericho is a city of palms and balsam gardens in a warm, low desert valley (date-palm green,
terracotta, sandstone gold, a hazy turquoise sky); do not reuse earlier films' towns, crowds or trees.
"""

TITLE = "撒该爬上桑树"
SUBTITLE = "圣经绘本 · 路加福音"

# speakers this story adds (same format as voice/tts.py VOICES). Pace comes from the prompt speed; keep the
# ZipVoice speed near 1.0 (a high speed with a long prompt can return an empty clip for a short line).
VOICES = {
    "Z": {"engine": "zipvoice", "sid": 98, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 98, "speed": 1.0,
                     "text": "孩子们，到我这里来。我爱你们，我会一直和你们在一起。"}},
    "S": {"engine": "zipvoice", "sid": 91, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 91, "speed": 1.1,
                     "text": "我叫撒该，我住在耶利哥。我个子很矮，可是我跑得很快。"}},
    "C": {"engine": "zipvoice", "sid": 95, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 95, "speed": 1.0, "text": "我们都住在耶利哥城里，大家都认识撒该。"}},
}
# pronunciation fixes for this script (merged into voice/lexicons.py ZV_FIX for this story only). Avoid neutral
# tones on content words: the voice reads some of them wrong (喜欢 came out like 喜喝).
LEXICON = {
    "耶稣": "ye1 su1", "撒该": "sa1 gai1", "耶利哥": "ye1 li4 ge1", "桑树": "sang1 shu4", "收税": "shou1 shui4",
    "有钱": "you3 qian2", "踮起": "dian2 qi3", "后脑勺": "hou4 nao3 shao2",
    "个子": "ge4 zi5", "矮": "ai3", "挤进去": "ji3 jin4 qu4", "经过": "jing1 guo4", "爬呀爬": "pa2 ya5 pa2",
    "清清楚楚": "qing1 qing1 chu3 chu3", "抬起头": "tai2 qi3 tou2", "下来": "xia4 lai2", "住在": "zhu4 zai4",
    "欢欢喜喜地": "huan1 huan1 xi3 xi3 de5", "接待": "jie1 dai4", "一半": "yi2 ban4", "穷人": "qiong2 ren2",
    "四倍": "si4 bei4", "还他": "huan2 ta1", "还四块": "huan2 si4 kuai4", "救恩": "jiu4 en1",
    "认识": "ren4 shi2", "躲得": "duo3 de5", "团团转": "tuan2 tuan2 zhuan4",
    "不让": "bu2 rang4", "一块钱": "yi2 kuai4 qian2", "十块钱": "shi2 kuai4 qian2", "五块": "wu3 kuai4", "跳呀跳": "tiao4 ya5 tiao4", "罗马": "luo2 ma3",
    "一堵": "yi4 du3", "管着": "guan3 zhe5", "嘿嘿": "hei1 hei1",
    "棕树": "zong1 shu4", "口袋": "kou3 dai4", "路过": "lu4 guo4", "机会": "ji1 hui4", "树枝": "shu4 zhi1",
}
NO_BREAK = ["耶稣", "撒该", "耶利哥", "罗马"]  # read in one breath (耶和华 is added for every story)

# Each scene: id (stories/zacchaeus/scenes/<id>.py), a note for illustrators and the composer, music mood,
# optional transition into the scene ("fade" default, "fadeblack", "circleopen", "dippaper" = a page-turn dip
# through the paper colour where the place changes or neighbours are drawn by different illustrators),
# optional lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 2.4,
        "note": "Title page: a big sycamore-fig tree by a dusty road in Jericho, palms behind, a little man peeking "
                "out from its leaves with a big smile; warm golden light, a hazy turquoise sky.",
        "lines": [("N", "圣经绘本：撒该爬上桑树。")],
    },
    {
        "id": "s02_question", "mood": "call", "tail": 1.8,
        "note": "Opening question to the child: a modern child at a parade or a show behind a wall of grown-ups' backs, "
                "jumping and still seeing nothing; then dad lifts the child onto his shoulders and the child beams.",
        "lines": [
            ("N", "小朋友，你有没有被前面的大人挡住，什么都看不见？", 0.8),
            ("N", "今天的故事里，有一个人也是这样。可是，他想了一个好办法！"),
        ],
    },
    {
        "id": "s03_jericho", "transition": "dippaper", "mood": "nineveh",
        "note": "Luke 19:1-2. Jericho, the city of palms: busy streets, a tax booth with coins and a ledger; Zacchaeus "
                "(a short, well-dressed man, rich robes, a bit of a show-off at first) counting a heap of coins; people "
                "pay him and walk off grumbling; when he walks down the street people step aside and look away.",
        "lines": [
            ("N", "有一天，耶稣经过一座城，叫耶利哥。"),
            ("N", "耶利哥城里，到处都是高高的棕树。"),
            ("N", "城里住着一个人，名叫撒该。撒该是收税的人。"),
            ("N", "收税的人，就是帮罗马皇帝，向大家收钱的人。"),
            ("N", "撒该管着好多收税的人。他很有钱！"),
            ("N", "可是，大家都不喜欢撒该。因为他常常多收别人的钱，放进自己的口袋。"),
            ("N", "大家看见撒该，都躲得远远的。"),
        ],
    },
    {
        "id": "s04_crowd", "mood": "lots",
        "note": "Luke 19:3. News spreads: Jesus is coming! Everyone rushes into the street; a thick crowd lines the "
                "road. Zacchaeus wants to see Jesus but he is short: he jumps (only backs of heads), stands on tiptoe, "
                "tries to squeeze in and is elbowed out; comic, never mean; he paces, thinking.",
        "lines": [
            ("N", "这一天，大家听说耶稣要来了，都跑到街上去看。"),
            ("N", "撒该也想看看，耶稣是什么样的人。"),
            ("N", "撒该心想：耶稣只是路过这里。今天要是看不见，就没有机会了！"),
            ("N", "可是，撒该的个子太矮了！他跳呀跳，看不见。他踮起脚，还是看不见！"),
            ("N", "前面的人，像一堵高高的墙。撒该只看见别人的后脑勺！"),
            ("N", "他想挤进去，大家都不让他。撒该急得团团转。"),
            ("N", "小朋友，你猜撒该想到了什么好办法？", 1.5),
        ],
    },
    {
        "id": "s05_tree", "transition": "dippaper", "mood": "flee",
        "note": "Luke 19:4. A light-bulb moment; Zacchaeus runs ahead down the road (robes hitched up, comic run) to a "
                "big sycamore-fig tree on Jesus's way and climbs it, branch by branch, and settles on a branch, peeking "
                "through the leaves: a perfect view of the road.",
        "lines": [
            ("N", "有了！撒该往前跑，跑到耶稣要经过的路上。"),
            ("N", "那里有一棵大大的桑树。树枝又低又粗，正好可以爬。"),
            ("N", "撒该爬呀爬，爬呀爬，爬上了桑树！"),
            ("S", "嘿嘿，这下看得清清楚楚了！"),
        ],
    },
    {
        "id": "s06_call", "mood": "shore",
        "note": "Luke 19:5-6. The crowd and Jesus come along the road; Jesus stops right under the tree, looks up at "
                "Zacchaeus with a warm smile and calls him by name; Zacchaeus nearly falls off the branch in surprise, "
                "then scrambles down, overjoyed, and bows to welcome Jesus.",
        "lines": [
            ("N", "耶稣走到桑树下面，停住了。他抬起头，看着撒该，说："),
            ("Z", "撒该，快下来！今天我要住在你家里。"),
            ("N", "撒该吓了一跳。"),
            ("S", "耶稣认识我？他还要到我家去？"),
            ("N", "他高兴极了，赶快爬下来，欢欢喜喜地接待耶稣。"),
        ],
    },
    {
        "id": "s07_grumble", "mood": "repent",
        "note": "Luke 19:7. The crowd watches Jesus walk off with Zacchaeus to his house; people frown, fold their arms "
                "and mutter to each other.",
        "lines": [
            ("N", "大家看见了，都不高兴，小声说："),
            ("C", "哼！耶稣怎么到坏人家里去住呢？"),
            ("N", "大家都说撒该是个坏人。可是耶稣，还是愿意到他家里去。"),
        ],
    },
    {
        "id": "s08_promise", "transition": "dippaper", "mood": "lesson",
        "note": "Luke 19:8. Zacchaeus's fine house, a meal for Jesus (and his disciples); Zacchaeus stands up, a little "
                "nervous then brave, and makes his promise; the money chests open; picture-book glosses: 'half' = ten "
                "coins split into two piles of five, one pile to the poor; 'four times' = one coin taken, four coins "
                "given back, popping out one by one.",
        "lines": [
            ("N", "在撒该家里，撒该站起来，对耶稣说："),
            ("S", "主啊，我要把我的钱，分一半给穷人！我以前多收了谁的钱，我就还他四倍！"),
            ("N", "一半，就是有十块钱，分五块给穷人！"),
            ("N", "四倍，就是多收了一块钱，要还四块钱！"),
        ],
    },
    {
        "id": "s09_saved", "mood": "end",
        "note": "Luke 19:9-10. Jesus smiles at Zacchaeus with great joy and speaks; warm light fills the house; "
                "Zacchaeus's face shines; a little picture-book echo of a shepherd carrying a lamb home (the same idea "
                "as the lost sheep: Jesus came to find the lost).",
        "lines": [
            ("N", "耶稣笑了，说："),
            ("Z", "今天，救恩到了这一家！"),
            ("N", "就是说：上帝救了撒该！撒该也是上帝家里的人。"),
            ("Z", "我来，就是要找到走丢的人，把他们救回来。"),
            ("N", "撒该想看看耶稣，原来耶稣也在找撒该！就像牧羊人，去找走丢的小羊。"),
        ],
    },
    {
        "id": "s10_heart", "transition": "dippaper", "mood": "worm",
        "note": "A gentle picture of Zacchaeus's changed heart: he gives coins to a poor widow and a beggar, pays back "
                "a farmer, and they smile back at him; children wave to him under the palms; the sycamore-fig in the "
                "evening light. (A picture of his promise, not a claim beyond the text: keep it light.)",
        "lines": [
            ("N", "撒该心里好开心！他不再只想着钱了。"),
            ("N", "因为耶稣爱他，他也开始爱别人了。"),
        ],
    },
    {
        "id": "s11_end", "transition": "dippaper", "mood": "end", "tail": 5.5,   # the 2 s answer pause, the end card, a hold, the fade-out
        "note": "Ending: the modern child from the opening, at home in the evening with dad, looking at a picture-book "
                "page of Zacchaeus in the tree (the door of their home in view, matching '到你家来'); warm light; closing question with a pause.",
        "lines": [
            ("N", "小朋友，耶稣知道撒该的名字，也知道你的名字。"),
            ("N", "不管别人喜不喜欢你，耶稣都爱你。他也想住进你的心里。"),
            ("N", "小朋友，如果耶稣今天到你家来，你想对他说什么呢？", 2.0),
        ],
    },
]

LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
