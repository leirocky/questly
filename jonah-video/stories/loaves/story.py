"""五饼二鱼 — narration script and scene list (single source of truth for stories/loaves).

John 6:1-14 with Mark 6:30-44 (and Matthew 14:21 for the women and children), told for children aged 3-8, about
4 minutes, in the narration style of SCRIPT_STYLE.md. John gives Philip, Andrew, the boy and his barley loaves, the
twelve baskets; Mark gives the setting (no time even to eat), the crowd running ahead on foot, sheep
without a shepherd, the green grass and the groups of hundreds and fifties (like garden beds, Mark 6:40 Greek); the teaching and healing
follow Luke 9:11 / Matthew 14:14; the people's reaction paraphrases John 6:14. Small actions are added (the boy hands
over his lunch, as John 6:11 implies), no new plot. Same pipeline as the other films:
python3 build.py all --story loaves.

Speakers (narrator N from voice/tts.py; the others below):
    N = narrator   Z = Jesus (the same voice as in the other Jesus films)   D = the disciples (a group, the Storm voice)
    P = Philip   A = Andrew
Jesus keeps his design from the earlier films (kind, calm, never comic); Peter, Andrew, James and John as in 耶稣平静风浪.
Owner direction: every story looks different: a lush emerald hillside above the lake in warm amber late-afternoon
light, the crowd sitting in colourful groups like flower beds on the grass (Mark 6:40), woven baskets; do not reuse
the Lost Sheep spring hills, the Storm lake shots or any earlier crowd.
"""

TITLE = "五饼二鱼"
SUBTITLE = "圣经绘本 · 约翰福音 · 马可福音"

# speakers this story adds (same format as voice/tts.py VOICES). Pace comes from the prompt speed; keep the
# ZipVoice speed near 1.0 (a high speed with a long prompt can return an empty clip for a short line).
VOICES = {
    "Z": {"engine": "zipvoice", "sid": 98, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 98, "speed": 1.0,
                     "text": "孩子们，到我这里来。我爱你们，我会一直和你们在一起。"}},
    "D": {"engine": "zipvoice", "sid": 84, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 84, "speed": 1.1, "text": "我们是打鱼的人，每天都在湖上撒网捕鱼。"}},
    "P": {"engine": "zipvoice", "sid": 79, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 79, "speed": 1.05, "text": "我叫腓力，我是耶稣的门徒，我很会算账。"}},
    "A": {"engine": "zipvoice", "sid": 88, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 88, "speed": 1.05, "text": "我叫安得烈，我以前是打鱼的，我哥哥叫彼得。"}},
}
# pronunciation fixes for this script (merged into voice/lexicons.py ZV_FIX for this story only). Avoid neutral
# tones on content words: the voice reads some of them wrong (喜欢 came out like 喜喝).
LEXICON = {
    "耶稣": "ye1 su1", "门徒": "men2 tu2", "腓力": "fei2 li4", "安得烈": "an1 de2 lie4", "大麦饼": "da4 mai4 bing3",
    "掰开": "bai1 kai1", "篮子": "lan2 zi5", "饱饱的": "bao3 bao3 de5", "剩下": "sheng4 xia4", "碎块": "sui4 kuai4",
    "浪费": "lang4 fei4", "牧人": "mu4 ren2", "治好": "zhi4 hao3", "一小口": "yi4 xiao3 kou3", "幼儿园": "you4 er2 yuan2",
    "光是": "guang1 shi4", "五千": "wu3 qian1", "五十": "wu3 shi2", "一百": "yi4 bai3", "十二": "shi2 er4",
    "教导": "jiao4 dao3", "野地": "ye3 di4", "疼爱": "teng2 ai4", "分给": "fen1 gei3", "分啊分": "fen1 a5 fen1",
    "收啊收": "shou1 a5 shou1", "一排一排": "yi4 pai2 yi4 pai2", "一组一组": "yi4 zu3 yi4 zu3", "两条": "liang3 tiao2",
    "五个饼": "wu3 ge4 bing3", "午饭": "wu3 fan4", "零食": "ling2 shi2", "分享": "fen1 xiang3", "只够": "zhi3 gou4", "牧羊人": "mu4 yang2 ren2", "咕噜咕噜": "gu1 lu1 gu1 lu1",
    "找啊找": "zhao3 a5 zhao3", "跑啊跑": "pao3 a5 pao3", "附近": "fu4 jin4", "村子": "cun1 zi5", "算了算": "suan4 le5 suan4",
    "掰着": "bai1 zhe5", "摇摇头": "yao2 yao2 tou2", "小花园": "xiao3 hua1 yuan2", "派来": "pai4 lai2",
}
NO_BREAK = ["耶稣", "腓力", "安得烈", "门徒", "牧羊人"]  # read in one breath (耶和华 is added for every story)

# Each scene: id (stories/loaves/scenes/<id>.py), a note for illustrators and the composer, music mood,
# optional transition into the scene ("fade" default, "fadeblack", "circleopen", "dippaper" = a page-turn dip
# through the paper colour where the place changes or neighbours are drawn by different illustrators),
# optional lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 2.8,
        "note": "Title page: a grassy hillside above the lake in warm late-afternoon light, a small boy with a little "
                "basket (five round loaves, two small fish peeking out), woven baskets, the lake glinting far below.",
        "lines": [("N", "圣经绘本：五饼二鱼。")],
    },
    {
        "id": "s02_question", "mood": "call", "tail": 1.8,
        "note": "Opening question to the child: a modern child at a picnic or a school lunch opens a lunchbox; a friend "
                "beside them has nothing; the child hesitates, then shares half; both smile.",
        "lines": [
            ("N", "小朋友，你有没有把好吃的，分给好朋友？", 0.8),
            ("N", "今天的故事里，有一个小男孩，他只带了一点点饭。可是，耶稣用这一点点饭，让好多好多人都吃饱了！"),
        ],
    },
    {
        "id": "s03_crowd", "transition": "dippaper", "mood": "lots", "tail": 2.0,
        "note": "Mark 6:30-34. Jesus and the twelve, tired, crowded by people coming and going; they push off in a boat "
                "for a quiet place across the lake; but people see them and run along the shore from all the towns "
                "and get there first; Jesus steps out, sees the huge crowd, and his face fills with love; he teaches "
                "them and heals the sick (a man walks without his crutch, a child's fever gone).",
        "lines": [
            ("N", "耶稣有十二个好朋友，叫做门徒。"),
            ("N", "有一天，耶稣和门徒们好忙好忙，连吃饭的时间都没有。耶稣说："),
            ("Z", "我们到安静的地方，去休息一下吧。"),
            ("N", "他们坐船，到湖的那一边去。可是，好多人看见了。大家沿着湖边，跑啊跑，跑啊跑……比船还先到了！"),
            ("N", "耶稣下了船，看见这么多人，心里好疼爱他们。他们就像一群没有牧羊人的羊，不知道该往哪里去。"),
            ("N", "耶稣就给大家讲上帝的事，还把生病的人都治好了。"),
        ],
    },
    {
        "id": "s04_evening", "mood": "nineveh",
        "note": "Mark 6:35-37, John 6:5-7. The sun sinks; the disciples come to Jesus, worried; Jesus says they should "
                "feed them; he turns to Philip, who counts in the air and on his fingers, shaking his head: impossible.",
        "lines": [
            ("N", "天快黑了。大家的肚子，咕噜咕噜叫。门徒们来对耶稣说："),
            ("D", "这里什么吃的都没有，天也晚了。让大家到附近的村子里，自己买东西吃吧！"),
            ("Z", "你们给他们吃吧。"),
            ("N", "门徒们吓了一跳。耶稣又问腓力："),
            ("Z", "我们到哪里买饼，给这些人吃呢？"),
            ("N", "耶稣这样问，是要看看腓力怎么想。其实，耶稣自己早就知道要怎么做了。"),
            ("N", "腓力掰着手指算了算，摇摇头说："),
            ("P", "就算花好多好多钱买饼，也不够每个人吃一小口啊！"),
        ],
    },
    {
        "id": "s05_boy", "transition": "dippaper", "mood": "worm", "tail": 2.3,
        "note": "John 6:8-9. Andrew brings a small boy with a little basket: five round barley loaves and two small "
                "dried fish; Andrew holds them up, doubtful, looking at the huge crowd; the boy looks up at Jesus and "
                "gives him his lunch with both hands.",
        "lines": [
            ("Z", "你们有多少饼？去看看吧。"),
            ("N", "门徒们找啊找，找啊找……这时候，彼得的兄弟安得烈，带来一个小男孩。安得烈说："),
            ("A", "这里有个小孩子，带着五个大麦饼、两条小鱼。可是，这么多人，这一点点怎么够呢？"),
            ("N", "五个饼，两条鱼，只够一个小男孩吃。可是，小男孩把他带的饭，交给了耶稣。"),
        ],
    },
    {
        "id": "s06_sit", "transition": "dippaper", "mood": "shore", "tail": 2.5,
        "note": "Mark 6:39-40, John 6:10, Matthew 14:21. Jesus has everyone sit down on the green grass; the crowd "
                "settles in neat colourful groups, like little gardens seen from above (groups of a hundred and of "
                "fifty); a picture-book count: 5000 men plus mothers and children; the whole hillside full.",
        "lines": [
            ("N", "耶稣对门徒说："),
            ("Z", "叫大家都坐下来吧。"),
            ("N", "那里有好多青草。大家一排一排、一组一组地坐下。有的一百个人一组，有的五十个人一组。"),
            ("N", "从高处看，一组一组的人，就像一块一块的小花园。"),
            ("N", "光是男人，就有五千个！还有好多妈妈和小朋友。整个山坡，都坐满了人！"),
        ],
    },
    {
        "id": "s07_bless", "mood": "end", "tail": 2.8,
        "note": "John 6:11, Mark 6:41. Jesus takes the five loaves and two fish, looks up to heaven and gives thanks "
                "(light only, God never drawn); he breaks the bread and hands it to the disciples, who carry it to "
                "the groups; the bread and fish in each disciple's hands never run out.",
        "lines": [
            ("N", "耶稣拿起五个饼和两条鱼，抬头望着天，感谢上帝。", 1.4),
            ("N", "然后，他把饼掰开，递给门徒，门徒再分给大家。鱼也是这样。"),
            ("N", "分啊分，分啊分……饼一直分不完！鱼也一直分不完！大家想吃多少，就吃多少。"),
        ],
    },
    {
        "id": "s08_baskets", "transition": "dippaper", "mood": "lesson", "tail": 2.0,
        "note": "John 6:12-13. Everyone has eaten their fill, children patting full tummies; Jesus tells the "
                "disciples to gather the leftovers so nothing is wasted; the twelve go round with baskets: twelve "
                "baskets full, more than the five loaves they started with; the boy's eyes go wide, then he smiles.",
        "lines": [
            ("N", "每个人都吃得饱饱的。耶稣对门徒说："),
            ("Z", "把剩下的碎块收起来，一点也不要浪费。"),
            ("N", "门徒们去收，收啊收，收啊收……装满了十二个篮子！比原来的五个饼，还多得多！"),
            ("N", "大家都好惊讶：五个饼、两条鱼，怎么能让这么多人吃饱呢？"),
            ("N", "大家都说：耶稣一定是上帝派来的！小男孩看着满满的篮子，笑了。"),
        ],
    },
    {
        "id": "s09_end", "transition": "dippaper", "mood": "end", "tail": 5.7,   # the 2 s answer pause, the end card, a hold, the fade-out
        "note": "Ending: the modern child from the opening, sharing their lunch with the friend again, now with a happy "
                "glow; a picture-book corner shows the boy giving his basket to Jesus; warm light; closing question "
                "with a pause.",
        "lines": [
            ("N", "小朋友，五个饼、两条鱼，看起来只有一点点。可是在耶稣手里，一点点也能变成好多好多！"),
            ("N", "耶稣看见大家饿了，就疼爱他们、照顾他们。耶稣也知道你需要什么，他也会照顾你。"),
            ("N", "小朋友，你有什么好东西，可以分给别人呢？", 2.0),
        ],
    },
]

LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
