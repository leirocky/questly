"""耶稣降生 — narration script and scene list (single source of truth for stories/nativity).

Luke 1:26-38, 2:1-20 and Matthew 2:1-11, told for children aged 3-8, about 4-5 minutes, in the narration style of
SCRIPT_STYLE.md. Herod is left out (a simplification, nothing added). The donkey, the camels and the stable animals
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
          "prompt": {"engine": "kokoro", "sid": 79, "speed": 1.1, "text": "我们是放羊的人，每天晚上都在野地里看守羊群。"}},
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
}
NO_BREAK = ["耶稣", "马利亚", "约瑟", "伯利恒", "拿撒勒", "罗马"]  # read in one breath (耶和华 is added for every story)

# Each scene: id (stories/nativity/scenes/<id>.py), a note for illustrators and the composer, music mood,
# optional transition into the scene ("fade" default, "fadeblack", "circleopen", "dippaper" = a page-turn dip
# through the paper colour where the place changes or neighbours are drawn by different illustrators),
# optional lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 1.6,
        "note": "Title page: a little stable under a deep blue starry sky over the hills of Bethlehem, one big golden "
                "star shining down on it, warm lamplight from inside, a few sheep on the hillside.",
        "lines": [("N", "圣经绘本：耶稣降生。")],
    },
    {
        "id": "s02_question", "mood": "call",
        "note": "Opening question to the child: a modern child in a cosy living room decorating a Christmas tree "
                "(lights, a star on top), a calendar with 12月25日 circled.",
        "lines": [
            ("N", "小朋友，你最喜欢哪个节日？是不是圣诞节？", 0.8),
            ("N", "圣诞节，就是庆祝耶稣生日的日子。今天，我们就来听听，耶稣是怎么出生的。"),
        ],
    },
    {
        "id": "s03_angel", "transition": "dippaper", "mood": "flee",
        "note": "Luke 1:26-38. Nazareth: a small white-washed village house; Mary, a kind young woman with a blue head "
                "cloth, sweeping / carrying a water jar; suddenly the room fills with light and the angel Gabriel "
                "stands there (a tall gentle figure of light with soft wings, not frightening); Mary startled, then "
                "calm; she bows her head and says yes.",
        "lines": [
            ("N", "很久以前，在一个叫拿撒勒的小村子里，住着一个善良的女孩，名叫马利亚。"),
            ("N", "有一天，房间里忽然亮起来了。一位天使，站在她的面前！"),
            ("A", "马利亚，不要怕！上帝很爱你。你要生一个儿子，给他起名叫耶稣。他是上帝的儿子。"),
            ("M", "我是上帝的使女，我愿意照你说的去做。"),
        ],
    },
    {
        "id": "s04_journey", "transition": "dippaper", "mood": "lots",
        "note": "Luke 2:1-5. A herald reads the Roman emperor's decree in the village square; Joseph (Mary's husband, "
                "a carpenter with a short beard) and Mary set off; a long road over hills toward Bethlehem, days "
                "passing (sun and moon); Mary riding a donkey is fine as a picture detail.",
        "lines": [
            ("N", "马利亚的丈夫，名叫约瑟。那时候，罗马皇帝下了一道命令：每个人都要回到自己的老家去登记名字。"),
            ("N", "约瑟和马利亚，就要去伯利恒。他们走啊走，走啊走，走了好多天。"),
        ],
    },
    {
        "id": "s05_no_room", "mood": "repent",
        "note": "Luke 2:6-7. Bethlehem at dusk, crowded streets full of travellers; the inn is full; Joseph and Mary "
                "find a humble place where animals are kept (a cave-stable with a lamp, an ox and a donkey).",
        "lines": [
            ("N", "到了伯利恒，城里的人好多好多。客店里，已经没有地方了。"),
            ("N", "他们只好在一个放牲口的地方，住了下来。"),
        ],
    },
    {
        "id": "s06_birth", "transition": "dippaper", "mood": "belly",
        "note": "Luke 2:7. Night in the stable, warm lamplight: baby Jesus is born; Mary wraps him in cloths and lays "
                "him gently in the manger on fresh hay; Joseph watches tenderly; the ox and donkey look on; through "
                "the doorway the stars twinkle.",
        "lines": [
            ("N", "就在那天晚上，小耶稣出生了！"),
            ("N", "马利亚用布把他包起来，轻轻地放在马槽里。马槽，就是给牛和驴吃草的槽子。"),
            ("N", "小耶稣睡着了。星星在天上，一闪，一闪。"),
        ],
    },
    {
        "id": "s07_shepherds", "transition": "dippaper", "mood": "fish",
        "note": "Luke 2:8-12. The fields outside Bethlehem at night: shepherds by a small fire with their sheep "
                "(a lamb, a sheepdog is fine), stars; suddenly a great light and an angel appear in the sky; the "
                "shepherds fall back, frightened, shielding their eyes; the angel speaks kindly.",
        "lines": [
            ("N", "在伯利恒的野地里，有一群牧羊人。夜里，他们在看守着羊群。"),
            ("N", "忽然，天上大放光明，一位天使出现了！牧羊人都吓坏了。"),
            ("A", "不要怕！我报给你们大喜的消息。今天，在伯利恒，救主为你们出生了，他就是耶稣！"),
            ("A", "你们会看见一个婴孩，包着布，躺在马槽里。"),
        ],
    },
    {
        "id": "s08_choir", "mood": "shore",
        "note": "Luke 2:13-14. The whole night sky fills with angels of light singing and praising God; the shepherds "
                "kneel in wonder; sheep look up; a glorious, joyful moment.",
        "lines": [
            ("N", "忽然，有好多好多天使出现在天上，一起赞美上帝："),
            ("A", "在至高之处，荣耀归与上帝！在地上，平安归与他所喜悦的人！"),
        ],
    },
    {
        "id": "s09_visit", "transition": "dippaper", "mood": "lesson",
        "note": "Luke 2:15-20. The angels go back to heaven; the shepherds hurry down the hill to Bethlehem with a "
                "lamb; at the stable they find Mary, Joseph and the baby in the manger; they kneel; then they go out "
                "praising God and telling everyone they meet.",
        "lines": [
            ("N", "天使们回天上去了。牧羊人彼此说："),
            ("S", "我们快去伯利恒看看吧！"),
            ("N", "他们急急忙忙地跑去，真的找到了马利亚、约瑟，还有躺在马槽里的小婴孩。"),
            ("N", "牧羊人好开心。他们一路走，一路赞美上帝，把这个好消息告诉每一个人。"),
        ],
    },
    {
        "id": "s10_star", "transition": "dippaper", "mood": "nineveh",
        "note": "Matthew 2:1-2, 9. Far away in the East: wise men on a rooftop observatory with scrolls and star maps "
                "see a new, very bright star; they set off on a long journey (camels are fine as a picture detail), "
                "following the star across deserts and hills, nights and days.",
        "lines": [
            ("N", "在很远很远的东方，有几位博士，看见天上出现了一颗特别亮的星星。"),
            ("W", "这颗星告诉我们，有一位王出生了。我们去拜他吧！"),
            ("N", "他们跟着星星，走啊走，走了好久好久。"),
        ],
    },
    {
        "id": "s11_gifts", "mood": "worm",
        "note": "Matthew 2:9-11. The star stops over the house where little Jesus is (Matthew says a house: show a "
                "small house in Bethlehem, Jesus now a toddler on Mary's lap); the wise men kneel and worship him "
                "and open three treasures — gold, frankincense, myrrh — each shining as it is named.",
        "lines": [
            ("N", "星星停在了小耶稣住的地方。博士们好高兴，走进屋子，跪下来拜他。"),
            ("N", "他们送上了三样礼物：黄金、乳香，还有没药。"),
        ],
    },
    {
        "id": "s12_end", "transition": "dippaper", "mood": "end",
        "note": "Ending: back to the modern child at the Christmas tree, placing a little nativity set under it; warm "
                "light; the star on the tree glows; closing question with a pause.",
        "lines": [
            ("N", "小朋友，耶稣出生，是上帝送给全世界最好的礼物。"),
            ("N", "上帝爱你，所以把他的儿子耶稣送给了我们。"),
            ("N", "今年圣诞节，你想送给耶稣什么礼物呢？", 2.0),
        ],
    },
]

LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
