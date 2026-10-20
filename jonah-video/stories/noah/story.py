"""挪亚方舟 — narration script and scene list (single source of truth for stories/noah).

Genesis 6-9, told for children aged 3-8, about 5 minutes, in the narration style of SCRIPT_STYLE.md (talk to
the child, short sentences, thoughts and feelings said aloud, repetition, sound words, counting, gentle humour,
an ending question with a pause). Same pipeline as the other films: python3 build.py all --story noah.

Speakers (narrator N and God G from voice/tts.py; Noah below):
    N = narrator   G = God (a warm voice from the light, never drawn as a person)   H = Noah
Judgement is told gently: the flood covers the land; nobody is shown drowning. The raven (8:7) is left out
for length; the dove is sent three times as in 8:8-12.
"""

TITLE = "挪亚方舟"
SUBTITLE = "圣经绘本 · 创世记"

# speakers this story adds or retunes (same format as voice/tts.py VOICES). Pace comes from the prompt speed;
# keep the ZipVoice speed near 1.0 (a high speed with a long prompt can return an empty clip for a short line).
VOICES = {
    "G": {"engine": "zipvoice", "sid": 101, "speed": 1.0, "fx": "divine", "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 101, "speed": 1.0,
                     "text": "我是创造天地的上帝，我爱这世上所有的人，也爱一切的生命。"}},
    "H": {"engine": "zipvoice", "sid": 88, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 88, "speed": 1.1,
                     "text": "我是挪亚，我和我的家人住在一起，我每天都听上帝的话。"}},
}
# pronunciation fixes for this script (merged into voice/lexicons.py ZV_FIX for this story only)
LEXICON = {
    "挪亚": "nuo2 ya4", "雅弗": "ya3 fu2", "亚拉拉特": "ya4 la1 la1 te4", "方舟": "fang1 zhou1",
    "嘎吱嘎吱": "ga1 zhi1 ga1 zhi1", "叮叮当当": "ding1 ding1 dang1 dang1", "扑扑扑": "pu1 pu1 pu1",
    "蹦蹦蹦": "beng4 beng4 beng4", "滴答": "di1 da1", "哗啦啦": "hua1 la1 la1", "嗷呜": "ao2 wu1",
    "叼着": "diao1 zhe5", "落脚": "luo4 jiao3", "应许": "ying1 xu3", "一公一母": "yi4 gong1 yi4 mu3",
    "漂啊漂": "piao1 a5 piao1", "造啊造": "zao4 a5 zao4", "飞啊飞": "fei1 a5 fei1",
}
NO_BREAK = ["挪亚", "雅弗", "亚拉拉特", "方舟", "上帝"]  # read in one breath (耶和华 is added for every story)

# Each scene: id (stories/noah/scenes/<id>.py), a note for illustrators and the composer, music mood,
# optional transition into the scene ("fade" default, "fadeblack", "circleopen", "dippaper" = a page-turn dip
# through the paper colour where the place changes or neighbours are drawn by different illustrators),
# optional lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 1.6,
        "note": "Title page: the ark resting on a green hill after the rain, animals peeking out of the window and "
                "door (giraffe necks, an elephant trunk, birds on the roof), a rainbow behind. Book title.",
        "lines": [("N", "圣经绘本：挪亚方舟。")],
    },
    {
        "id": "s02_rain", "mood": "call",
        "note": "Opening question to the child: a little child at a window watching heavy rain (drops racing down "
                "the glass, puddles); then the rain grows huge and the page fills with it.",
        "lines": [
            ("N", "小朋友，你见过下很大很大的雨吗？哗啦啦，哗啦啦……", 0.8),
            ("N", "今天的故事里，下了一场好大好大的雨。下了多久呢？整整四十天！"),
        ],
    },
    {
        "id": "s03_world", "transition": "dippaper", "mood": "lots",
        "note": "Genesis 6:5-7, 11-12. Long ago: people quarrelling, pushing, grabbing (cartoon grumpiness, no "
                "violence shown in detail), grey clouds over the towns; God's sorrow shown as the warm light "
                "above dimming, a single falling raindrop like a tear.",
        "lines": [
            ("N", "很久很久以前，地上的人越来越坏。他们不听上帝的话，你推我，我抢你，天天吵架。"),
            ("N", "上帝看见了，心里很难过。"),
        ],
    },
    {
        "id": "s04_noah", "transition": "dippaper", "mood": "flee",
        "note": "6:8-10. One man was different: Noah, a kind grey-bearded man, with his wife, his three grown sons "
                "Shem, Ham and Japheth and their wives (a family portrait, eight people); Noah praying, helping a "
                "neighbour, walking with God (a soft golden light walking beside him).",
        "lines": [
            ("N", "可是，有一个人不一样。他的名字叫挪亚。"),
            ("N", "挪亚爱上帝，听上帝的话，每天都和上帝同行。"),
            ("N", "挪亚有三个儿子，名字叫闪、含和雅弗。"),
        ],
    },
    {
        "id": "s05_command", "transition": "dippaper", "mood": "repent",
        "note": "6:13-22. Noah alone on a hill at evening; golden light from above as God speaks (never a person); "
                "the plan of the ark appears like a glowing drawing in the sky (long box boat, three decks, a "
                "door, a window); animals in pairs drawn faintly; Noah scratches his head looking at the dry land "
                "(no sea anywhere), then nods firmly.",
        "lines": [
            ("N", "有一天，上帝对挪亚说："),
            ("G", "挪亚，地上就要发大水了。你要造一只很大很大的船，叫方舟。"),
            ("G", "你和你的家人都要进去，还要把各样的动物带进去，一公一母，两个两个地来。"),
            ("N", "挪亚心想：一只大船？可是，这里离大海好远好远啊！"),
            ("N", "可是，挪亚还是照着上帝说的，一样一样都去做了。"),
        ],
    },
    {
        "id": "s06_build", "transition": "dippaper", "mood": "worm",
        "note": "6:14-16, 22. Building: Noah and his sons saw planks (嘎吱嘎吱), hammer nails (叮叮当当), coat it "
                "with pitch; the ark grows from a keel to a huge three-deck boat with a side door and a window on "
                "top; days pass (sun and moon); a picture-book comparison of its length with a football field; "
                "finished at last, the family cheers.",
        "lines": [
            ("N", "挪亚和儿子们开始造方舟。锯木头，嘎吱嘎吱！钉钉子，叮叮当当！"),
            ("N", "方舟好长好长，比一个足球场还要长！它有三层，旁边开一个门，上面开一个窗户。"),
            ("N", "他们造啊造，造啊造，一天又一天……"),
            ("N", "终于，方舟造好了！"),
        ],
    },
    {
        "id": "s07_animals", "transition": "dippaper", "mood": "shore",
        "note": "7:2-3, 8-9, 6:21. The animals come two by two from every direction: elephants (boom boom), birds "
                "(flap flap), lions (roar), rabbits (hop hop), giraffes, zebras, sheep, cows, turtles, butterflies; "
                "a long happy queue up the ramp into the ark; Noah's family carries baskets and sacks of food "
                "aboard.",
        "lines": [
            ("N", "然后，动物们来了！"),
            ("N", "大象来了，咚，咚，咚！小鸟飞来了，扑扑扑！狮子来了，嗷呜！小兔子跳来了，蹦蹦蹦！"),
            ("N", "它们都是两个两个来的，一公一母，排着队走进方舟。"),
            ("N", "挪亚还在方舟里装满了吃的东西，有人吃的，也有动物吃的。"),
        ],
    },
    {
        "id": "s08_door", "mood": "belly",
        "note": "7:7, 13-16. Noah's family of eight walks up the ramp last; the big side door swings shut by itself "
                "with a soft golden glow around its edge (God shut it in) — a gentle 'thunk'; the first dark "
                "clouds gather.",
        "lines": [
            ("N", "挪亚一家八口人，也走进了方舟。"),
            ("N", "然后，上帝亲手把门关上了。"),
        ],
    },
    {
        "id": "s09_flood", "transition": "dippaper", "mood": "storm",
        "note": "7:10-24. Seven days later the rain begins (drip, drip... then pouring); water rises, the ark lifts "
                "and floats; rain for forty days and nights (a day counter); the water covers even the mountain "
                "tops — only the ark on a wide grey sea. Big and dramatic but never frightening; no people or "
                "animals shown in the water.",
        "lines": [
            ("N", "七天以后，下雨了。滴答，滴答……哗啦啦，哗啦啦！"),
            ("N", "大雨下了四十天四十夜。水越涨越高，越涨越高。方舟浮起来了，在水上漂啊漂。"),
            ("N", "大水盖过了最高的山。外面的一切，都不见了。"),
        ],
    },
    {
        "id": "s10_inside", "transition": "fadeblack", "mood": "belly",
        "note": "8:1. Inside the ark: cosy lamplight, animals sleeping in their stalls (the elephant's trunk "
                "curled, birds tucked in, rabbits snuggled), Noah's family eating together; rain drumming on the "
                "roof; a warm glow — God remembers them.",
        "lines": [
            ("N", "方舟里面，挪亚一家和动物们，都平平安安的。"),
            ("N", "外面风很大，雨很大。可是上帝一直记得挪亚，也记得方舟里的每一只动物。"),
        ],
    },
    {
        "id": "s11_dove", "transition": "fadeblack", "mood": "fish",
        "note": "8:1-12. The rain stops, a wind blows, the water goes down; the ark settles on the mountains of "
                "Ararat (peaks appear). Noah opens the window and sends out a white dove three times: it comes back "
                "tired; it comes back with a fresh olive leaf; it flies away and does not return.",
        "lines": [
            ("N", "后来，上帝叫风吹过大地，水慢慢地退下去了。方舟停在了亚拉拉特山上。"),
            ("N", "挪亚打开窗户，放出一只鸽子。鸽子飞啊飞，找不到落脚的地方，又飞回来了。"),
            ("N", "过了七天，挪亚又放出鸽子。到了晚上，鸽子飞回来了，嘴里叼着一片新鲜的橄榄叶！"),
            ("N", "挪亚就知道，地上的水退了！"),
            ("N", "又过了七天，挪亚再放出鸽子。这一次，鸽子再也没有回来。"),
        ],
    },
    {
        "id": "s12_out", "transition": "dippaper", "mood": "shore",
        "note": "8:15-20. God tells them to come out; the big door opens onto a fresh green world; the animals burst "
                "out happily (hopping, running, flying, the elephants spraying water); Noah's family builds a small "
                "stone altar and thanks God.",
        "lines": [
            ("N", "上帝对挪亚说："),
            ("G", "你和你的家人，还有所有的动物，都可以出来了。"),
            ("N", "门打开了！动物们一个接一个跑出来，有的跳，有的飞，有的跑，开心极了！"),
            ("N", "挪亚做的第一件事，就是筑了一座坛，感谢上帝。"),
        ],
    },
    {
        "id": "s13_rainbow", "mood": "lesson",
        "note": "8:21-9:17. God's promise: a great rainbow appears in the clouds, colour by colour as the narrator "
                "names them; Noah's family and the animals look up in wonder.",
        "lines": [
            ("G", "我要和你们立约：我再也不会用大水毁灭大地了。"),
            ("N", "上帝把一道彩虹放在云彩里。红、橙、黄、绿、青、蓝、紫，好漂亮啊！"),
            ("G", "每次看见彩虹，我就会记得我的应许。"),
        ],
    },
    {
        "id": "s14_end", "transition": "dippaper", "mood": "end",
        "note": "Ending: a child (not Noah) after a rain shower, splashing in a puddle, sees a rainbow and smiles; "
                "the ark and the animals tiny on a far hill under it; warm closing question to children.",
        "lines": [
            ("N", "小朋友，下次下完雨，看见彩虹的时候，你可以想一想："),
            ("N", "上帝说过的话，一定会做到。上帝一直记得你，就像他记得挪亚一样。"),
            ("N", "对了，方舟里那么多动物，你最喜欢哪一种呢？", 2.0),
        ],
    },
]

LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
