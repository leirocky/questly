"""耶稣降生 — narration script and scene list (single source of truth for stories/nativity).

Luke 1:26-38, 2:1-20 and Matthew 2:1-11, told for children aged 3-8, about 4-5 minutes, in the narration style of
SCRIPT_STYLE.md. Herod is left out (a simplification, nothing added); the star leads the wise men only on the last stretch (Matt 2:9). Reviewed by an independent script reviewer (Bible accuracy, child clarity, pronunciation). The donkey, the camels and the stable animals
are traditional picture details only: the narration does not claim them. Same pipeline as the other films:
python3 build.py all --story nativity.

Speakers (narrator N from voice/tts.py; the others below):
    N = narrator   A = the angel (also the angel choir)   M = Mary   S = the shepherds (a group)
    W = the wise men (a group)
God the Father is never drawn; Jesus is a baby. Owner direction: every story looks different (new places, people
and palette: starry night blues, warm lamplight, the gold of the star).
"""

TITLE = "耶稣降生"
SUBTITLE = "圣经绘本 · 路加福音 · 马太福音"

# speakers this story adds (same format as voice/tts.py VOICES). Pace comes from the prompt speed; keep the
# ZipVoice speed near 1.0 (a high speed with a long prompt can return an empty clip for a short line).
VOICES = {
    "A": {"engine": "zipvoice", "sid": 89, "speed": 1.0, "fx": "divine", "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 89, "speed": 1.05,
                     "text": "不要怕！我给你们带来一个大好的消息，这是上帝要我告诉你们的。"}},
    "M": {"engine": "zipvoice", "sid": 5, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 5, "speed": 1.05,
                     "text": "我是马利亚，我住在拿撒勒。我每天都向上帝祷告，我愿意听上帝的话。"}},
    "S": {"engine": "zipvoice", "sid": 79, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 79, "speed": 1.0, "text": "我们是放羊的人，每天晚上都在野地里看守羊群。"}},
    "W": {"engine": "zipvoice", "sid": 92, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 92, "speed": 1.05, "text": "我们是从东方来的博士，我们每天晚上都在看天上的星星。"}},
}
# pronunciation fixes for this script (merged into voice/lexicons.py ZV_FIX for this story only). Avoid neutral
# tones on content words: the voice reads some of them wrong (喜欢 came out like 喜喝).
LEXICON = {
    "耶稣": "ye1 su1", "马利亚": "ma3 li4 ya4", "约瑟": "yue1 se4", "伯利恒": "bo2 li4 heng2",
    "拿撒勒": "na2 sa1 le4", "罗马": "luo2 ma3", "马槽": "ma3 cao2", "槽子": "cao2 zi5", "使女": "shi3 nv3",
    "乳香": "ru3 xiang1", "没药": "mo4 yao4", "登记": "deng1 ji4", "至高": "zhi4 gao1", "荣耀": "rong2 yao4",
    "喜悦": "xi3 yue4", "婴孩": "ying1 hai2", "牲口": "sheng1 kou3", "看守": "kan1 shou3", "博士": "bo2 shi4",
    "一闪": "yi4 shan3", "降生": "jiang4 sheng1", "老家": "lao3 jia1", "地方": "di4 fang1", "东方": "dong1 fang1",
    "消息": "xiao1 xi1", "急急忙忙": "ji2 ji2 mang2 mang2", "一路": "yi2 lu4", "屋子": "wu1 zi5",
    "亮晶晶": "liang4 jing1 jing1", "记号": "ji4 hao4", "香料": "xiang1 liao4", "贵重": "gui4 zhong4",
    "结婚": "jie2 hun1", "轮流": "lun2 liu2", "宝盒": "bao3 he2", "学问": "xue2 wen4", "四周": "si4 zhou1",
}
NO_BREAK = ["耶稣", "马利亚", "约瑟", "伯利恒", "拿撒勒", "罗马"]  # read in one breath (耶和华 is added for every story)

# Each scene: id (stories/nativity/scenes/<id>.py), a note for illustrators and the composer, music mood,
# optional transition into the scene ("fade" default, "fadeblack", "circleopen", "dippaper" = a page-turn dip
# through the paper colour where the place changes or neighbours are drawn by different illustrators),
# optional lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 2.4,
        "note": "Title page: a little stable under a deep blue starry sky over the hills of Bethlehem, one big golden "
                "star shining down on it, warm lamplight from inside, a few sheep on the hillside.",
        "lines": [("N", "圣经绘本：耶稣降生。")],
    },
    {
        "id": "s02_question", "mood": "call",
        "note": "Opening question to the child: a modern child in a cosy living room decorating a Christmas tree "
                "(lights, a star on top), a calendar with 12月25日 circled.",
        "lines": [
            ("N", "小朋友，你过生日的时候，最开心的是什么？", 0.8),
            ("N", "圣诞节，就像是大家一起给耶稣过生日。今天，我们就来听听，耶稣是怎么出生的。"),
        ],
    },
    {
        "id": "s03_angel", "transition": "dippaper", "mood": "flee",
        "note": "Luke 1:26-38. Nazareth: a small white-washed village house; Mary, a kind young woman with a blue head "
                "cloth, sweeping / carrying a water jar; suddenly the room fills with light and the angel Gabriel "
                "stands there (a tall gentle figure of light with soft wings, not frightening); Mary startled, then "
                "calm; she bows her head and says yes.",
        "lines": [
            ("N", "很久以前，有一个小城，叫拿撒勒。城里住着一个善良的女孩，名叫马利亚。"),
            ("N", "有一天，房间里忽然亮起来了。一位天使，站在她的面前！马利亚吓了一跳。"),
            ("A", "马利亚，不要怕！上帝很爱你。你要生一个儿子，给他起名叫耶稣。他是上帝的儿子。"),
            ("M", "可是，我还没有结婚呀，怎么会有孩子呢？"),
            ("A", "这是上帝要做的事。在上帝，没有做不到的事！"),
            ("M", "我是上帝的使女。就照你说的那样吧，我愿意！"),
        ],
    },
    {
        "id": "s04_journey", "transition": "dippaper", "mood": "lots",
        "note": "Luke 2:1-5. A herald reads the Roman emperor's decree in the village square; Joseph (Mary's husband, "
                "a carpenter with a short beard) and Mary set off; a long road over hills toward Bethlehem, days "
                "passing (sun and moon); Mary visibly pregnant (Luke 2:5); a donkey is fine as a picture detail.",
        "lines": [
            ("N", "马利亚的丈夫，名叫约瑟。那时候，罗马皇帝想知道，他的国家一共有多少人。"),
            ("N", "他下了一道命令：每个人都要回到自己的老家，去登记名字。"),
            ("N", "约瑟的老家在伯利恒。所以，约瑟和马利亚也要去伯利恒。"),
            ("N", "这时候，马利亚的肚子已经大大的了。小宝宝，就快要出生了！"),
            ("N", "他们走啊走，走啊走，走了好多天。"),
        ],
    },
    {
        "id": "s05_no_room", "mood": "repent",
        "note": "Luke 2:6-7. Bethlehem at dusk, crowded streets full of travellers; the inn is full; Joseph and Mary "
                "find a humble place where animals are kept (a cave-stable with a lamp, an ox and a donkey); Mary visibly pregnant.",
        "lines": [
            ("N", "到了伯利恒，城里到处都是人，就像过年时的火车站一样挤！"),
            ("N", "客店里，已经没有地方了。"),
            ("N", "他们只好在一个放牲口的地方，住了下来。"),
        ],
    },
    {
        "id": "s06_birth", "transition": "dippaper", "mood": "belly",
        "note": "Luke 2:7. Night in the stable, warm lamplight: baby Jesus is born; Mary wraps him in cloths and lays "
                "him gently in the manger on fresh hay; Joseph watches tenderly; the ox and donkey look on; through "
                "the doorway the stars twinkle.",
        "lines": [
            ("N", "他们在伯利恒的时候，小耶稣出生了！"),
            ("N", "马利亚用布把他包起来，轻轻地放在马槽里。马槽，就是给牛和驴吃草的槽子。"),
            ("N", "小耶稣睡着了。天上的星星，一闪一闪亮晶晶。"),
        ],
    },
    {
        "id": "s07_shepherds", "transition": "dippaper", "mood": "fish",
        "note": "Luke 2:8-12. The fields outside Bethlehem at night: shepherds by a small fire with their sheep "
                "(a lamb, a sheepdog is fine), stars; suddenly an angel stands by them (may float slightly above the "
                "ground) and the glory of the Lord shines all around them; the shepherds fall back, frightened, "
                "shielding their eyes; the angel speaks kindly.",
        "lines": [
            ("N", "在伯利恒的野地里，有一群牧羊人。夜里，他们轮流守着羊群。"),
            ("N", "忽然，一位天使站在他们旁边！上帝的光，照亮了四周。牧羊人都吓坏了。"),
            ("A", "不要怕！我给你们带来一个大好消息，是给所有人的！"),
            ("A", "今天，在伯利恒，有一位救主为你们出生了！"),
            ("A", "你们会看见一个婴孩，包着布，躺在马槽里。这就是给你们的记号。"),
        ],
    },
    {
        "id": "s08_choir", "mood": "shore",
        "note": "Luke 2:13-14. The whole night sky fills with angels of light singing and praising God; the shepherds "
                "kneel in wonder; sheep look up; a glorious, joyful moment.",
        "lines": [
            ("N", "忽然，有好多好多天使出现在天上，一起赞美上帝："),
            ("A", "在至高之处，荣耀归与上帝！在地上，平安归与他所喜悦的人！"),
            ("N", "就是说：天上，要赞美上帝！地上，上帝要把平安送给他喜爱的人。"),
        ],
    },
    {
        "id": "s09_visit", "transition": "dippaper", "mood": "lesson",
        "note": "Luke 2:15-20. The angels go back to heaven; the shepherds hurry down the hill to Bethlehem with a "
                "lamb; at the stable they find Mary, Joseph and the baby in the manger; they kneel; then they go out "
                "praising God and telling everyone they meet.",
        "lines": [
            ("N", "天使们回天上去了。牧羊人你看看我，我看看你，说："),
            ("S", "我们快去伯利恒看看吧！"),
            ("N", "他们急急忙忙地跑到伯利恒。找啊找，找到了！约瑟和马利亚都在那里，小婴孩就躺在马槽里。"),
            ("N", "他就是天使说的救主，上帝派来救我们的那一位！"),
            ("N", "牧羊人好开心！他们见到人就说，把天使的话告诉大家。"),
            ("N", "听见的人，都很惊讶。马利亚呢，把这些事都记在心里，想了又想。"),
        ],
    },
    {
        "id": "s10_star", "transition": "dippaper", "mood": "nineveh",
        "note": "Matthew 2:1-2, 9. Far away in the East: wise men on a rooftop observatory with scrolls and star maps "
                "see his star rise; they set off on a long journey (camels are fine as a picture detail) across "
                "deserts and hills, nights and days (the star leads them only on the last stretch, Matt 2:9).",
        "lines": [
            ("N", "在很远很远的东方，住着几位博士。博士，就是很有学问、会研究星星的人。"),
            ("N", "有一天，他们看见天上出现了一颗特别的星星。"),
            ("W", "这颗星告诉我们，有一位王出生了。我们去拜他吧！"),
            ("N", "他们出发了。走啊走，走啊走，走了好久好久。"),
        ],
    },
    {
        "id": "s11_gifts", "mood": "worm",
        "note": "Matthew 2:9-11. The star appears again and goes ahead of them to Bethlehem, then stops over the house where little Jesus is (Matthew says a house: show a "
                "small house in Bethlehem, Jesus now a toddler on Mary's lap); the wise men kneel and worship him "
                "and open three treasures — gold, frankincense, myrrh — each shining as it is named.",
        "lines": [
            ("N", "忽然，那颗星星又出现了，在前面给他们带路！"),
            ("N", "星星一直走到伯利恒，停在了一座房子的上面。"),
            ("N", "博士们高兴极了！他们走进房子，看见了小耶稣和妈妈马利亚，就跪下来拜他。"),
            ("N", "他们打开宝盒，送上了三样礼物。黄金、乳香，还有没药。"),
            ("N", "乳香和没药，都是又香又贵重的香料。这些，都是送给王的宝贝！"),
        ],
    },
    {
        "id": "s12_end", "transition": "dippaper", "mood": "end", "tail": 5.5,   # the 2 s answer pause, the end card, a hold, the fade-out
        "note": "Ending: back to the modern child at the Christmas tree, placing a little nativity set under it; warm "
                "light; the star on the tree glows; closing question with a pause.",
        "lines": [
            ("N", "小朋友，博士们给耶稣送了礼物。可是你知道吗？耶稣，才是上帝送给全世界最好的礼物！"),
            ("N", "上帝爱我们，所以把他的儿子耶稣，送给了我们。"),
            ("N", "今年圣诞节，你想送给耶稣什么礼物呢？", 2.0),
        ],
    },
]

LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
