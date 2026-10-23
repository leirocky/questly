"""迷失的羊 — narration script and scene list (single source of truth for stories/lost_sheep).

Luke 15:1-7 (with Matthew 18:12-14), told for children aged 3-8, about 4 minutes, in the narration style of
SCRIPT_STYLE.md. Jesus tells the parable because the Pharisees grumble that he welcomes sinners and eats with them;
the parable itself is the heart of the film. The scribes who grumble with the Pharisees are left out (a
simplification, nothing added). Small actions are added (how the lamb wanders off, the shepherd
counting, the search over hills), no new plot. Same pipeline as the other films:
python3 build.py all --story lost_sheep.

Speakers (narrator N from voice/tts.py; the others below):
    N = narrator   Z = Jesus (the same voice as in 耶稣平静风浪)   P = the Pharisees (a group)
    H = the shepherd in Jesus's story
Jesus is drawn as a person, kind and calm, never comic. Owner direction: every story looks different. The outer
story (Jesus at a meal with tax collectors) is warm and earthy; Jesus's story is a bright spring storybook world
(mint hills, buttercups, a wide blue sky), the search turns to a lavender dusk and a silver moonlit night, and the
party is lantern-lit. Do not reuse the Nativity film's shepherds, sheep or night fields.
"""

TITLE = "迷失的羊"
SUBTITLE = "圣经绘本 · 路加福音 · 马太福音"

# speakers this story adds (same format as voice/tts.py VOICES). Pace comes from the prompt speed; keep the
# ZipVoice speed near 1.0 (a high speed with a long prompt can return an empty clip for a short line).
VOICES = {
    "Z": {"engine": "zipvoice", "sid": 98, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 98, "speed": 1.0,
                     "text": "孩子们，到我这里来。我爱你们，我会一直和你们在一起。"}},
    "P": {"engine": "zipvoice", "sid": 95, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 95, "speed": 1.0, "text": "我们是法利赛人，我们每天都很守规矩。"}},
    "H": {"engine": "zipvoice", "sid": 87, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 87, "speed": 1.05,
                     "text": "我是一个牧羊人，我有一百只羊，每一只我都很爱。"}},
}
# pronunciation fixes for this script (merged into voice/lexicons.py ZV_FIX for this story only). Avoid neutral
# tones on content words: the voice reads some of them wrong (喜欢 came out like 喜喝).
LEXICON = {
    "耶稣": "ye1 su1", "法利赛人": "fa3 li4 sai4 ren2", "牧羊人": "mu4 yang2 ren2", "收税": "shou1 shui4",
    "一百只": "yi4 bai3 zhi1", "一只": "yi4 zhi1", "两只": "liang3 zhi1", "三只": "san1 zhi1",
    "九十九只": "jiu3 shi2 jiu3 zhi1", "那一只": "na4 yi4 zhi1", "只有": "zhi3 you3", "数羊": "shu3 yang2",
    "数啊数": "shu3 a5 shu3", "吃着吃着": "chi1 zhe5 chi1 zhe5", "走着走着": "zou3 zhe5 zou3 zhe5",
    "咩": "mie1", "扛在": "kang2 zai4", "肩膀": "jian1 bang3", "欢欢喜喜": "huan1 huan1 xi3 xi3",
    "邻居": "lin2 ju1", "宝贝": "bao3 bei4", "皱着": "zhou4 zhe5", "眉头": "mei2 tou2", 
    "发抖": "fa1 dou3", "弯弯": "wan1 wan1", "翻过": "fan1 guo4", "看不起": "kan4 bu4 qi3",
    "找到": "zhao3 dao4", "庆祝": "qing4 zhu4", "一个也": "yi2 ge4 ye3", "规矩": "gui1 ju3",
    "欢欢喜喜地": "huan1 huan1 xi3 xi3 de5", "再数一遍": "zai4 shu3 yi2 bian4", "都会": "dou1 hui4", "那只": "na4 zhi1",
    "小家伙": "xiao3 jia1 huo3",
}
NO_BREAK = ["耶稣", "法利赛人", "牧羊人"]  # read in one breath (耶和华 is added for every story)

# Each scene: id (stories/lost_sheep/scenes/<id>.py), a note for illustrators and the composer, music mood,
# optional transition into the scene ("fade" default, "fadeblack", "circleopen", "dippaper" = a page-turn dip
# through the paper colour where the place changes or neighbours are drawn by different illustrators),
# optional lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 2.4,
        "note": "Title page: a spring hillside in soft morning light, a shepherd with his crook watching a big flock; "
                "one little lamb a little apart, nibbling a flower. A new storybook look: mint green, buttercup "
                "yellow, a wide blue sky with round clouds.",
        "lines": [("N", "圣经绘本：迷失的羊。")],
    },
    {
        "id": "s02_question", "mood": "call",
        "note": "Opening question to the child: a modern child in a busy supermarket (or a park) suddenly can't see "
                "mum or dad, looks around, worried; then the parent finds them and they hug.",
        "lines": [
            ("N", "小朋友，你有没有走丢过？找不到爸爸妈妈的时候，心里是不是好着急？", 0.8),
            ("N", "今天，耶稣要讲一个故事。故事里，也有一个走丢的小家伙。"),
        ],
    },
    {
        "id": "s03_meal", "transition": "dippaper", "mood": "nineveh",
        "note": "Luke 15:1-2. A courtyard meal: Jesus at a low table with tax collectors (one with a money bag and a "
                "tax ledger) and other people nobody liked, all welcomed, laughing, sharing bread; at the edge a few "
                "Pharisees in long tasselled robes frown, arms folded, whispering to each other.",
        "lines": [
            ("N", "有一天，好多人来听耶稣讲道。"),
            ("N", "来的人里，有收税的人。他们常常多收别人的钱。"),
            ("N", "还有一些人，做过很多错事。大家都不喜欢他们。"),
            ("N", "可是耶稣很欢迎他们，还和他们一起吃饭。"),
            ("N", "旁边站着几个法利赛人。他们很守上帝的规矩，可是看不起这些人。他们皱着眉头，小声说："),
            ("P", "哼！这个人怎么和这些坏人一起吃饭呢？"),
        ],
    },
    {
        "id": "s04_story", "mood": "lesson", "tail": 2.3,   # time to fly into the page after the question
        "note": "Luke 15:3-4. Jesus turns kindly to everyone, Pharisees included, and asks his question; the scene "
                "opens into his story like a picture-book page unfolding from his hands (the spring hills).",
        "lines": [
            ("N", "耶稣听见了，就给他们讲了一个故事。"),
            ("Z", "如果你有一百只羊，丢了一只，你会怎么做呢？", 1.0),
        ],
    },
    {
        "id": "s05_flock", "transition": "dippaper", "mood": "worm",
        "note": "Jesus's story begins: the shepherd (a new design) leads a big flock over the spring hills to green "
                "grass and a stream; he knows every sheep; the little lamb is curious (a curl on its head and a tiny "
                "bell) - it sniffs flowers, chases a butterfly, hops after it over a rise, further and further; "
                "looks up: everyone is gone.",
        "lines": [
            ("N", "耶稣的故事里，有一个牧羊人。他有一百只羊，每一只他都很爱。"),
            ("N", "一百只羊，好多好多，站满了整个山坡！"),
            ("N", "每天早上，牧羊人带着羊群，到山坡上吃青草。"),
            ("N", "有一只小羊，吃着吃着，走着走着，越走越远。"),
            ("N", "它闻闻小花，追追蝴蝶。一抬头，咦？大家都不见了！"),
        ],
    },
    {
        "id": "s06_count", "mood": "lots",
        "note": "Sunset on the same hillside before heading home: the shepherd counts each sheep with his crook as it "
                "passes (numbers float up as he counts); 97, 98, 99... he counts again (comic, puzzled): still 99; "
                "one is missing. He leaves the ninety-nine together on the open hillside (Luke 15:4 旷野, Matt 18:12 "
                "山里; no sheepfold) and sets off with his crook and a lantern.",
        "lines": [
            ("N", "太阳快下山了。回家以前，牧羊人在山坡上数羊："),
            ("H", "一只，两只，三只……"),
            ("N", "数啊数，数啊数……"),
            ("H", "九十七，九十八，九十九……咦？怎么只有九十九只？我再数一遍！"),
            ("N", "数啊数……还是九十九只！少了一只小羊！"),
            ("H", "我的小羊呢？我要去找它！"),
            ("N", "牧羊人把九十九只羊留在山坡上，自己去找那一只。"),
        ],
    },
    {
        "id": "s07_alone", "mood": "fish",
        "note": "Meanwhile the little lamb alone on a rocky slope, dusk turning to night (lavender sky): the wind blows, shadows grow "
                "long, an owl hoots; the lamb trembles behind a big rock and bleats. Never too frightening.",
        "lines": [
            ("N", "这时候，小羊一个人在山上。天黑了，风呼呼地吹。"),
            ("N", "小羊好害怕，一直叫：咩——咩——"),
        ],
    },
    {
        "id": "s08_search", "transition": "dippaper", "mood": "flee",
        "note": "The search at night under a silver moon: the shepherd with his lantern climbs over high hills, along "
                "a winding path, across a little stream on stepping stones, through thorny bushes, calling; he does "
                "not give up.",
        "lines": [
            ("N", "牧羊人翻过高高的山，走过弯弯的小路，跨过一条小河。"),
            ("H", "小羊！小羊！你在哪里？"),
            ("N", "找啊找，找啊找。天越来越黑，路越来越难走。"),
            ("N", "可是牧羊人一直找，一直找，一定要找到它！"),
        ],
    },
    {
        "id": "s09_found", "mood": "shore",
        "note": "Luke 15:5. He hears a faint bleat; behind a big rock, the little lamb, cold and trembling; the "
                "shepherd kneels, not angry at all, hugs it, and joyfully lifts it onto his shoulders; the moon "
                "comes out brighter.",
        "lines": [
            ("N", "忽然，他听见了：咩——咩——"),
            ("N", "在一块大石头后面，小羊冷得发抖。找到了！"),
            ("N", "牧羊人一点也没生气。他欢欢喜喜地把小羊扛在肩膀上。"),
            ("H", "找到你了！我们回家吧！"),
        ],
    },
    {
        "id": "s10_party", "transition": "dippaper", "mood": "end",
        "note": "Luke 15:6. Back in the village at night: the shepherd, lamb on his shoulders, knocks on doors and "
                "calls his friends and neighbours; lanterns, music, everyone celebrating, the lamb in the middle "
                "nuzzling the shepherd.",
        "lines": [
            ("N", "回到家，牧羊人把朋友和邻居都请来："),
            ("H", "和我一起高兴吧！我丢的那只羊，找到了！"),
            ("N", "大家都好开心，一起唱歌，一起庆祝！"),
        ],
    },
    {
        "id": "s11_meaning", "transition": "dippaper", "mood": "repent",
        "note": "Luke 15:7, Matthew 18:14. Back at the meal: Jesus finishes his story, looking at everyone with love; "
                "the tax collectors' faces light up, warm; the Pharisees look at each other, thinking; a picture "
                "of heaven's joy: light and gentle sparkles over the courtyard. The story page folds back into Jesus's "
                "hands (mirroring s04); on the last narration line Jesus at the table with the tax collectors is shown "
                "like the shepherd with the lamb.",
        "lines": [
            ("N", "讲完故事，耶稣说："),
            ("Z", "一个做错事的人，愿意回到上帝身边，天上也会这样，欢欢喜喜地庆祝！"),
            ("N", "耶稣和这些人一起吃饭，就像牧羊人去找走丢的小羊。"),
            ("N", "在上帝眼里，每一个人都是宝贝。上帝一个也不愿意失去！"),
        ],
    },
    {
        "id": "s12_end", "transition": "dippaper", "mood": "end", "tail": 5.7,   # the 2 s answer pause, the end card, a hold, the fade-out
        "note": "Ending: the modern child from the opening at bedtime, hugging a soft toy lamb; a picture-book "
                "corner shows the shepherd carrying the lamb home under the moon; warm light; closing questions "
                "with pauses.",
        "lines": [
            ("N", "小朋友，上帝就像这个牧羊人。你，就是他的宝贝小羊。"),
            ("N", "不管你走多远，上帝都会来找你。"),
            ("N", "如果你做错了事，也不要怕。你可以对上帝说：对不起，我想回到你身边。"),
            ("N", "小朋友，如果你是那只小羊，被找到的时候，你想对牧羊人说什么呢？", 2.0),
        ],
    },
]

LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
