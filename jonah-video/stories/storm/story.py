"""耶稣平静风浪 — narration script and scene list (single source of truth for stories/storm).

Mark 4:35-41 with its setting (the disciples who were fishermen, Mark 1/3; the mustard seed told that same day, 4:30-32; arriving on the far shore, 5:1), told for children aged 3-8, about 4 minutes, in the narration style of SCRIPT_STYLE.md. Same
pipeline as the other films: python3 build.py all --story storm.

Speakers (narrator N from voice/tts.py; the others below):
    N = narrator   Z = Jesus   M = the disciples (a group)
Jesus is drawn as a person (the Son of God among his friends): kind, calm, never comic. Owner direction: every
story should look different — new boat, new lake, new palette; do not reuse the Jonah film's ship or storm art.
"""

TITLE = "耶稣平静风浪"
SUBTITLE = "圣经绘本 · 马可福音"

# speakers this story adds (same format as voice/tts.py VOICES). Pace comes from the prompt speed; keep the
# ZipVoice speed near 1.0 (a high speed with a long prompt can return an empty clip for a short line).
VOICES = {
    "Z": {"engine": "zipvoice", "sid": 98, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 98, "speed": 1.0,
                     "text": "孩子们，到我这里来。我爱你们，我会一直和你们在一起。"}},
    "M": {"engine": "zipvoice", "sid": 84, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 84, "speed": 1.1, "text": "我们是打鱼的人，每天都在湖上撒网捕鱼。"}},
}
# pronunciation fixes for this script (merged into voice/lexicons.py ZV_FIX for this story only). Avoid neutral
# tones on content words: the voice reads some of them wrong (喜欢 came out like 喜喝).
LEXICON = {
    "耶稣": "ye1 su1", "加利利": "jia1 li4 li4", "门徒": "men2 tu2", "船尾": "chuan2 wei3", "枕着": "zhen3 zhe5",
    "舀水": "yao3 shui3", "淹死": "yan1 si3", "敬畏": "jing4 wei4", "渡到": "du4 dao4", "呼呼": "hu1 hu1",
    "哗啦": "hua1 la1", "哐哐": "kuang1 kuang1", "摇啊摇": "yao2 a5 yao2", "住了吧": "zhu4 le5 ba5",
    "静了吧": "jing4 le5 ba5", "打鱼": "da3 yu2", "芥菜种": "jie4 cai4 zhong3", "彼得": "bi3 de2",
    "安得烈": "an1 de2 lie4", "雅各": "ya3 ge4", "约翰": "yue1 han4", "撒网": "sa1 wang3", "枝子": "zhi1 zi5",
    "做窝": "zuo4 wo1", "长啊长": "zhang3 a5 zhang3", "亮晶晶": "liang4 jing1 jing1",
}
NO_BREAK = ["耶稣", "加利利", "门徒", "彼得", "安得烈", "雅各", "约翰", "芥菜种"]  # read in one breath (耶和华 is added for every story)
TONE_WATCH = "长"   # 长 (grow) must stay zhang3, not drift to chang2

# Each scene: id (stories/storm/scenes/<id>.py), a note for illustrators and the composer, music mood,
# optional transition into the scene ("fade" default, "fadeblack", "circleopen", "dippaper" = a page-turn dip
# through the paper colour where the place changes or neighbours are drawn by different illustrators),
# optional lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 1.6,
        "note": "Title page: a small wooden fishing boat with a square sail on a calm lake at sunset, Jesus and his "
                "friends in it; far away dark clouds gather over the hills. A new look: violet-gold evening light.",
        "lines": [("N", "圣经绘本：耶稣平静风浪。")],
    },
    {
        "id": "s02_wind", "mood": "call",
        "note": "Opening question to the child: a modern child at home at night, the wind howling outside, the window "
                "rattling, curtains flapping; the child hugs a pillow.",
        "lines": [
            ("N", "小朋友，你遇到过很大很大的风吗？风呼呼地吹，窗户哐哐地响，你会不会害怕？", 0.8),
            ("N", "今天的故事里，有一群人在船上，遇到了好大好大的风浪。"),
        ],
    },
    {
        "id": "s03_friends", "transition": "dippaper", "mood": "flee",
        "note": "Mark 1:16-20, 3:13-19. The Sea of Galilee at morning: Jesus walking with his twelve friends along the "
                "shore; four fishermen (Peter, Andrew, James, John) casting and hauling nets from their boats, fish "
                "flapping; they know the lake well: a picture-book map-like vignette of the lake with fish spots and a "
                "little wind sign.",
        "lines": [
            ("N", "耶稣有十二个好朋友，叫做门徒。"),
            ("N", "他们当中，有好几个是打鱼的。彼得、安得烈、雅各和约翰，以前每天都在加利利湖上撒网捕鱼。"),
            ("N", "他们最熟悉这个湖了。哪里鱼多，什么时候起风，他们都知道。"),
        ],
    },
    {
        "id": "s04_shore", "mood": "nineveh",
        "note": "Mark 4:1-2. The lakeshore: green hills, a fishing village, nets drying; a big crowd gathers; Jesus "
                "sits in a boat just off the shore and teaches (gestures, children listening at the front).",
        "lines": [
            ("N", "有一天，耶稣在加利利湖边，教导很多很多人。人太多了，耶稣就坐在船上讲故事。"),
            ("N", "大家都安安静静地听，连小孩子也听得好认真。"),
        ],
    },
    {
        "id": "s05_seed", "transition": "dippaper", "mood": "worm",
        "note": "Mark 4:30-32. Jesus's story of the mustard seed shown as a picture-book page: a tiny seed in a hand, "
                "planted in the earth, rain and sun, a sprout that grows and grows into a big bushy tree, little birds "
                "flying in to build nests in its branches; back to the listeners nodding and smiling.",
        "lines": [
            ("N", "那天，耶稣给大家讲了一个小小种子的故事。"),
            ("Z", "芥菜种是最小最小的种子。可是种在地里，它会长啊长，长得比所有的菜都大，连小鸟都可以在它的枝子上做窝。"),
            ("N", "大家听了，都点点头，笑了。"),
        ],
    },
    {
        "id": "s06_evening", "transition": "dippaper", "mood": "lesson",
        "note": "Mark 4:35-36. Sunset over the lake (violet-gold); the crowd starts to go home; Jesus, tired, turns to his "
                "disciples and points across the lake; they ready the boat.",
        "lines": [
            ("N", "天快黑了。耶稣对门徒说："),
            ("Z", "我们渡到湖的那一边去吧。"),
        ],
    },
    {
        "id": "s07_sleep", "mood": "belly",
        "note": "4:36-38. The disciples push off and row/sail out onto the calm evening lake (the crowd waving, small "
                "lanterns); Jesus, tired after a long day, lies down at the back of the boat with his head on a "
                "cushion and falls asleep; the boat rocks gently, first stars.",
        "lines": [
            ("N", "门徒们把船划开了。耶稣累了一整天，就在船尾，枕着枕头睡着了。"),
            ("N", "还有别的小船，也跟着他们一起出发。"),
            ("N", "小船在湖上轻轻地摇啊摇，摇啊摇。星星一颗一颗地亮起来了。"),
        ],
    },
    {
        "id": "s08_storm", "transition": "fadeblack", "mood": "storm",
        "note": "4:37. Suddenly a great wind: clouds race, the sail snaps, the lake turns into big waves; waves splash "
                "into the boat and the water inside rises. Big and dramatic but never frightening for small "
                "children; a new storm look (cold blue-grey with white foam), not the Jonah storm.",
        "lines": [
            ("N", "忽然，起了一阵大风。呼——呼——！乌云跑过来，把月亮都遮住了。"),
            ("N", "浪一个接一个打进船里，哗啦！哗啦！船里的水越来越多。"),
        ],
    },
    {
        "id": "s09_scared", "mood": "lots",
        "note": "The disciples, many of them fishermen, are terrified; they bail water with buckets and bowls but the "
                "water keeps coming; one clings to the mast, one holds the sail rope.",
        "lines": [
            ("N", "门徒们吓坏了。他们好多人是打鱼的，可是从来没见过这么大的风浪！"),
            ("M", "抓紧！快把水舀出去！"),
            ("N", "他们拼命地舀水，可是水越舀越多。小船摇来摇去，好像就要沉下去了。"),
        ],
    },
    {
        "id": "s10_wake", "mood": "fish",
        "note": "4:38. Jesus still asleep, peaceful, at the stern in the middle of the storm (a calm little bubble of "
                "warm light around him); the disciples crowd round and shake him awake.",
        "lines": [
            ("N", "可是，耶稣还在睡觉。门徒们赶快叫醒他："),
            ("M", "老师！老师！我们快要淹死了，你不管吗？"),
        ],
    },
    {
        "id": "s11_calm", "mood": "shore",
        "note": "4:39. Jesus wakes, stands up in the boat and speaks to the wind and the sea with a raised hand; at once "
                "the wind stops, the waves flatten, the clouds open, the moon and stars come out: a great calm.",
        "lines": [
            ("N", "耶稣醒了，站起来，对着风和海说："),
            ("Z", "住了吧！静了吧！"),
            ("N", "风立刻停了，湖面变得平平静静的，一点浪也没有了。月亮出来了，星星又亮了。"),
        ],
    },
    {
        "id": "s12_question", "mood": "repent",
        "note": "4:40. On the calm moonlit lake Jesus turns to his wet, astonished disciples and gently asks them.",
        "lines": [
            ("N", "耶稣转过身来，温柔地问门徒："),
            ("Z", "你们为什么这样害怕呢？你们还没有信心吗？"),
        ],
    },
    {
        "id": "s13_who", "mood": "lesson",
        "note": "4:41. The disciples look at each other in wonder and awe, whispering; the calm lake shines; the boat "
                "glides on toward the far shore at dawn.",
        "lines": [
            ("N", "门徒们又惊讶，又敬畏，彼此说："),
            ("M", "这到底是谁？连风和海都听他的话！"),
            ("N", "这一天，门徒们才知道，耶稣不只是他们的好老师。"),
        ],
    },
    {
        "id": "s14_arrive", "mood": "end",
        "note": "Mark 5:1. Morning: the little boat arrives safely on the far shore; the sun rises, the water sparkles; "
                "the disciples step out, still looking back at Jesus and whispering, wondering.",
        "lines": [
            ("N", "第二天早上，小船平平安安地到了湖的那一边。太阳出来了，湖水亮晶晶的。"),
            ("N", "门徒们一边走下船，一边还在想：耶稣，到底是谁呢？"),
        ],
    },
    {
        "id": "s15_end", "transition": "dippaper", "mood": "end",
        "note": "Ending: the modern child from the opening, the wind still blowing outside, folds her hands and prays; "
                "the room grows warm and calm; a picture-book corner shows Jesus in the boat on the calm lake; "
                "closing questions to children with pauses.",
        "lines": [
            ("N", "小朋友，你知道他是谁吗？", 1.5),
            ("N", "他就是耶稣，上帝的儿子。连风和海，都听耶稣的话。"),
            ("N", "下次你害怕的时候，记得耶稣就在你身边。你可以向他祷告。"),
            ("N", "小朋友，你害怕的时候，想对耶稣说什么呢？", 2.0),
        ],
    },
]

LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
