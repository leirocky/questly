"""但以理和狮子坑 — narration script and scene list (single source of truth for stories/daniel).

Daniel 6, told for children aged 3-8 in plain spoken Chinese, about 5-6 minutes. The punishment of the
accusers (6:24) is told in one gentle sentence; the rest follows the text. Same pipeline and narrator as
the Jonah film: python3 build.py all --story daniel.

Speakers (voices: narrator N from voice/tts.py; the others below):
    N = narrator   D = Daniel   K = King Darius   O = the jealous officials (a group)
God is never shown as a person; the angel is shown only as light.
"""

TITLE = "但以理和狮子坑"
SUBTITLE = "圣经绘本 · 但以理书"

# speakers this story adds (same format as voice/tts.py VOICES; Kokoro v1.1-zh prompt voices)
VOICES = {
    "D": {"engine": "zipvoice", "sid": 91, "speed": 0.95, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 91, "speed": 0.9,
                     "text": "我是但以理，我每天都向上帝祷告，感谢上帝的恩典。"}},
    "K": {"engine": "zipvoice", "sid": 100, "speed": 0.9, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 100, "speed": 0.9, "text": "我是大利乌王，我管理着一个很大很大的国家。"}},
    "O": {"engine": "zipvoice", "sid": 95, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 95, "speed": 0.9, "text": "我们是国王的官员，每天都在王宫里办事。"}},
}
SCENE_FX = {("s11_morning", "D"): "cave"}      # Daniel answers from inside the den
# pronunciation fixes for this script (merged into voice/lexicons.py ZV_FIX for this story only)
LEXICON = {
    "但以理": "dan4 yi2 li3", "总管": "zong2 guan3", "耶路撒冷": "ye1 lu4 sa1 leng3", "错处": "cuo4 chu4",
    "睡不着觉": "shui4 bu5 zhao2 jiao4", "乖乖地": "guai1 guai1 de5", "平平安安地": "ping2 ping2 an1 an1 de5",
    "慢慢地": "man4 man4 de5", "都会": "dou1 hui4", "一道": "yi2 dao4",
}

# Each scene: id (stories/daniel/scenes/<id>.py), a note for illustrators and the composer, music mood,
# optional transition into the scene (ffmpeg xfade name, default "fade"; "fadeblack", "circleopen"),
# optional lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 1.6,
        "note": "Title page: a friendly lion resting at the mouth of a stone den at dawn, golden light; book title.",
        "lines": [("N", "圣经绘本：但以理和狮子坑。")],
    },
    {
        "id": "s02_daniel", "mood": "call",
        "note": "Daniel 6:1-3. Babylon under King Darius: a great city; Daniel, a kind grown man in a blue robe, "
                "works faithfully in the palace; the king smiles at him.",
        "lines": [
            ("N", "很久很久以前，有一个人，名叫但以理。他是以色列人，住在很远的巴比伦。"),
            ("N", "但以理很爱上帝，每天都向上帝祷告。"),
            ("N", "大利乌王管理着一个很大的国家。他派了一百二十个官员，又派了三个总管，来管理这些官员。"),
            ("N", "但以理就是三个总管中的一个。他做事又认真，又诚实，国王很喜欢他，想让他管理整个国家。"),
        ],
    },
    {
        "id": "s03_jealous", "mood": "lots",
        "note": "Daniel 6:4-5. The other officials whisper behind pillars, jealous; they search Daniel's work "
                "(scrolls, ledgers) but find nothing wrong.",
        "lines": [
            ("N", "可是，别的官员心里很不高兴。他们嫉妒但以理，想找他的错处。"),
            ("N", "他们找啊找，可是一点错处也找不到，因为但以理又忠心，又诚实。"),
            ("O", "我们找不到他的错。除非，在他敬拜上帝的事上想办法！"),
        ],
    },
    {
        "id": "s04_trick", "mood": "nineveh",
        "note": "Daniel 6:6-9. The officials bow before the king's throne and flatter him; a decree scroll; the king "
                "signs it with his seal (he does not see the trap).",
        "lines": [
            ("N", "于是，这些官员一起去见国王，说："),
            ("O", "王啊，愿你万岁！请你下一道命令：三十天之内，谁都不可以向别的神或者别的人祷告，只能向王祈求。"),
            ("O", "谁要是不听，就把他扔进狮子坑里！"),
            ("N", "国王没有想到这是一个圈套，就在命令上签了名。按照国家的规矩，国王签了名的命令，谁也不能改。"),
        ],
    },
    {
        "id": "s05_prays", "transition": "dippaper", "mood": "repent",
        "note": "Daniel 6:10. Daniel reads the decree on the city wall, goes home, climbs to his upstairs room, opens "
                "the window toward Jerusalem (west, far away) and kneels to pray and give thanks, as always.",
        "lines": [
            ("N", "但以理知道了这道命令。可是他没有害怕，也没有躲起来。"),
            ("N", "他知道这样做会有危险，可是他更相信上帝。"),
            ("N", "他回到家，上了楼，打开朝着耶路撒冷的窗户。"),
            ("N", "他像平常一样，一天三次，跪下来向上帝祷告，感谢上帝。"),
        ],
    },
    {
        "id": "s06_caught", "mood": "lots",
        "note": "Daniel 6:11-13. The officials peek from the street below the open window, point, then hurry to the "
                "king to accuse Daniel.",
        "lines": [
            ("N", "那些官员早就躲在外面偷看。"),
            ("O", "看！他在向他的上帝祷告！"),
            ("N", "他们急忙跑去告诉国王："),
            ("O", "王啊，但以理不听你的命令，他一天三次向他的上帝祷告！"),
        ],
    },
    {
        "id": "s07_king_sad", "mood": "repent",
        "note": "Daniel 6:14-15. The king, very sad, paces and thinks how to save Daniel until sunset (sky turns "
                "orange); the officials remind him the law cannot be changed.",
        "lines": [
            ("N", "国王听了，非常难过。他很喜欢但以理，想尽办法要救他，一直想到太阳下山。"),
            ("N", "可是那些官员又来说："),
            ("O", "王啊，你知道，你签了名的命令，是不能改的。"),
        ],
    },
    {
        "id": "s08_den", "transition": "dippaper", "mood": "storm",
        "note": "Daniel 6:16-17. Evening: soldiers lead Daniel (calm, not hurt) to the den and lower him in; the king "
                "speaks to him; a big round stone rolled over the opening and sealed with the king's seal.",
        "lines": [
            ("N", "国王只好下令，把但以理带来，放进狮子坑里。狮子坑很深，里面住着好多大狮子。"),
            ("K", "但以理，你一直敬拜的上帝，一定会救你！"),
            ("N", "人们搬来一块大石头，堵住坑口。国王用自己的印，在石头上封了印，谁也不能打开。"),
        ],
    },
    {
        "id": "s09_night", "transition": "dippaper", "mood": "belly",
        "note": "Daniel 6:18. Night in the palace: the king alone in his bedroom, food untouched, musicians sent away, "
                "awake by the window looking at the moon toward the den.",
        "lines": [
            ("N", "那天晚上，国王回到宫里。他不吃饭，也不要人奏乐，整夜都睡不着觉。"),
            ("N", "他走来走去，一会儿看看窗外，一会儿又叹一口气。他一直在想：但以理怎么样了？"),
        ],
    },
    {
        "id": "s10_angel", "transition": "fadeblack", "mood": "fish",
        "note": "Daniel 6:22. Inside the dim den: big lions circle; then God's angel comes as bright warm light (no "
                "human figure needed: light with soft wing shapes); the lions lie down gently like big sleepy cats; "
                "Daniel sits safe among them.",
        "lines": [
            ("N", "狮子坑里黑黑的。大狮子们慢慢地走过来，围在但以理身边。"),
            ("N", "可是，上帝派了天使来，封住了狮子的口。"),
            ("N", "狮子们一个个乖乖地趴下来，一口也没有咬但以理。"),
            ("N", "但以理在上帝的保护中，平平安安地过了一夜。"),
        ],
    },
    {
        "id": "s11_morning", "transition": "fadeblack", "mood": "call",
        "note": "Daniel 6:19-22. Dawn: the king runs to the den, the stone is moved aside a little, he calls down "
                "anxiously; Daniel's voice answers from below (we see his happy face looking up from the den).",
        "lines": [
            ("N", "第二天天刚亮，国王就急忙跑到狮子坑边，大声喊："),
            ("K", "但以理！永生上帝的仆人但以理！你的上帝救了你吗？"),
            ("N", "坑里传来但以理的声音："),
            ("D", "王啊，愿你万岁！我的上帝派天使封住了狮子的口，狮子没有伤害我。"),
            ("D", "因为在上帝面前，我是无罪的；在王面前，我也没有做错事。"),
        ],
    },
    {
        "id": "s12_rescue", "transition": "dippaper", "mood": "shore",
        "note": "Daniel 6:23-24. Ropes pull Daniel up into the sunshine; the king hugs him; not a scratch on him. One "
                "gentle line: the bad officials were punished (show them led away by guards, nothing scary).",
        "lines": [
            ("N", "国王高兴极了，马上叫人把但以理从坑里拉上来。"),
            ("N", "大家看了又看，但以理身上一点伤也没有，因为他信靠他的上帝。"),
            ("N", "那些想害但以理的官员，后来自己受到了惩罚。"),
        ],
    },
    {
        "id": "s13_decree", "mood": "lesson",
        "note": "Daniel 6:25-28. The king on his throne writes a letter; messengers carry it on horses to every land; "
                "people of many nations read it; Daniel serves happily.",
        "lines": [
            ("N", "后来，大利乌王写信给全国各地的人，说："),
            ("K", "你们都要敬畏但以理的上帝！他是永远活着的上帝。他会拯救人，他救了但以理，脱离狮子的口。"),
            ("N", "从那以后，但以理一直平平安安，做事都很顺利。"),
        ],
    },
    {
        "id": "s14_end", "transition": "dippaper", "mood": "end",
        "note": "Ending: evening, Daniel kneels at his open window again, the friendly lion from the title dozing in a "
                "picture-book corner; warm closing message to children.",
        "lines": [
            ("N", "但以理不管遇到什么事，都一直向上帝祷告。"),
            ("N", "小朋友，遇到害怕的事情，我们也可以像但以理一样，向上帝祷告。"),
            ("N", "不管在哪里，上帝都会听我们的祷告，和我们在一起。"),
        ],
    },
]

LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
