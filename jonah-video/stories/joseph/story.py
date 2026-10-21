"""约瑟和彩衣 — narration script and scene list (single source of truth for stories/joseph).

Genesis 37-50, told for children aged 3-8 in one film of about 6 minutes, in the narration style of
SCRIPT_STYLE.md. The main line only: the coat, the dream, the pit, sold to Egypt, wrongly accused (Potiphar's
wife is told only as 被人冤枉), the dreams in prison and Pharaoh's dream, ruler of Egypt, the famine, the brothers
bow, Joseph forgives. Same pipeline as the other films: python3 build.py all --story joseph.

Speakers (narrator N from voice/tts.py; the others below):
    N = narrator   Y = Joseph   B = the brothers (a group)   P = Pharaoh
God does not speak in this story; his presence is shown as soft golden light. Nothing violent is shown: the
coat is torn and dirtied, the pit is dry, Jacob's grief is tears.
"""

TITLE = "约瑟和彩衣"
SUBTITLE = "圣经绘本 · 创世记"

# speakers this story adds (same format as voice/tts.py VOICES). Pace comes from the prompt speed; keep the
# ZipVoice speed near 1.0 (a high speed with a long prompt can return an empty clip for a short line).
VOICES = {
    "Y": {"engine": "zipvoice", "sid": 87, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 87, "speed": 1.1,
                     "text": "我是约瑟，我是爸爸的第十一个儿子，我最喜欢爸爸给我做的彩衣。"}},
    "B": {"engine": "zipvoice", "sid": 95, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 95, "speed": 1.0, "text": "我们是约瑟的哥哥，每天都在田野里放羊。"}},
    "P": {"engine": "zipvoice", "sid": 100, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 100, "speed": 1.0, "text": "我是埃及的法老王，我住在很大很大的王宫里。"}},
}
# pronunciation fixes for this script (merged into voice/lexicons.py ZV_FIX for this story only). Avoid
# neutral tones on content words: the voice reads some of them wrong (喜欢 came out like 喜喝).
LEXICON = {
    "约瑟": "yue1 se4", "雅各": "ya3 ge4", "法老": "fa3 lao3", "埃及": "ai1 ji2", "解梦": "jie3 meng4",
    "应验": "ying4 yan4", "麦捆": "mai4 kun3", "捆麦子": "kun3 mai4 zi5", "剥下": "bo1 xia4", "下拜": "xia4 bai4",
    "饥荒": "ji1 huang1", "骆驼": "luo4 tuo2", "冤枉": "yuan1 wang3", "监牢": "jian1 lao2", "报仇": "bao4 chou2",
    "酸溜溜": "suan1 liu1 liu1", "脏兮兮": "zang1 xi1 xi1", "漂亮": "piao4 liang4", "疼爱": "teng2 ai4",
    "仓库": "cang1 ku4", "丰收": "feng1 shou1", "金链子": "jin1 lian4 zi5", "做梦": "zuo4 meng4",
}
NO_BREAK = ["约瑟", "雅各", "法老", "埃及"]  # read in one breath (耶和华 is added for every story)

# Each scene: id (stories/joseph/scenes/<id>.py), a note for illustrators and the composer, music mood,
# optional transition into the scene ("fade" default, "fadeblack", "circleopen", "dippaper" = a page-turn dip
# through the paper colour where the place changes or neighbours are drawn by different illustrators),
# optional lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 1.6,
        "note": "Title page: young Joseph in his bright many-coloured coat on a green hill with sheep, his eleven "
                "brothers far off; a sheaf of wheat in the corner. Book title.",
        "lines": [("N", "圣经绘本：约瑟和彩衣。")],
    },
    {
        "id": "s02_question", "mood": "call",
        "note": "Opening question to the child: two siblings squabbling over a toy, then one sulking with arms "
                "crossed (a picture-book vignette, a modern child, not Joseph).",
        "lines": [
            ("N", "小朋友，你有没有被哥哥姐姐欺负过？你有没有生过别人的气，很久很久都不想原谅他？", 0.8),
            ("N", "今天的故事里，有一个人被他的哥哥们欺负得好惨。可是后来，他做了一件很了不起的事。"),
        ],
    },
    {
        "id": "s03_coat", "transition": "dippaper", "mood": "flee",
        "note": "Genesis 37:2-4. Canaan, tents and flocks: old Jacob with his twelve sons (a family portrait, "
                "Joseph about 17, the youngest Benjamin a small boy); Jacob gives Joseph a beautiful coat of many "
                "colours (bands appear colour by colour as they are named); the ten older brothers frown, jealous.",
        "lines": [
            ("N", "很久以前，有一个爸爸，名字叫雅各。他有十二个儿子。"),
            ("N", "雅各最疼爱的，是第十一个儿子，约瑟。"),
            ("N", "他给约瑟做了一件彩色的衣服。红的、黄的、蓝的、绿的，好漂亮！"),
            ("N", "哥哥们看见了，心里酸溜溜的："),
            ("B", "凭什么只给他做？"),
        ],
    },
    {
        "id": "s04_dream", "mood": "lots",
        "note": "37:5-8. Night, Joseph asleep; a dream bubble: sheaves of wheat in a field, Joseph's sheaf stands "
                "up and the brothers' sheaves gather round and bow to it; morning, Joseph tells his brothers "
                "excitedly; they cross their arms, angrier.",
        "lines": [
            ("N", "有一天晚上，约瑟做了一个梦。"),
            ("Y", "我梦见我们在田里捆麦子。我的那一捆站了起来，你们的麦捆都围过来，向我的麦捆下拜！"),
            ("N", "哥哥们听了，更生气了。"),
            ("B", "难道你还想做王，管我们吗？"),
        ],
    },
    {
        "id": "s05_pit", "transition": "dippaper", "mood": "storm",
        "note": "37:12-24. Joseph walks across the hills in his bright coat to find his brothers with the flocks; "
                "they see him far off and plot; they pull off his coat and put him into a dry, empty pit (no "
                "water); Joseph calls from the bottom. Sad and tense, never violent.",
        "lines": [
            ("N", "有一天，爸爸叫约瑟去看看在远处放羊的哥哥们。"),
            ("N", "哥哥们远远看见约瑟走来，就说："),
            ("B", "看，那个做梦的来了！"),
            ("N", "他们剥下约瑟的彩衣，把他丢进一个干枯的坑里。坑里一滴水也没有。"),
            ("Y", "哥哥！放我出去！"),
        ],
    },
    {
        "id": "s06_sold", "mood": "fish",
        "note": "37:25-28. A caravan of camels with traders comes along the road (spices and bundles); the brothers "
                "pull Joseph up and sell him for twenty pieces of silver (coins counted); the caravan leads Joseph "
                "away toward Egypt, getting smaller.",
        "lines": [
            ("N", "这时候，来了一队骆驼。那是去埃及做生意的商人。"),
            ("N", "哥哥们把约瑟拉上来，用二十块银子把他卖了。"),
            ("N", "约瑟被带到了很远很远的埃及。"),
        ],
    },
    {
        "id": "s07_jacob", "transition": "dippaper", "mood": "belly",
        "note": "37:31-35. At home: the brothers show old Jacob the torn, dirty coat; Jacob thinks a wild animal took "
                "Joseph and weeps for a long time, holding the coat (tears, no blood shown).",
        "lines": [
            ("N", "哥哥们把彩衣弄得又破又脏，拿回家给爸爸看。"),
            ("N", "雅各以为约瑟被野兽吃掉了，伤心得哭了很久很久。"),
        ],
    },
    {
        "id": "s08_egypt", "transition": "dippaper", "mood": "repent",
        "note": "39. Egypt: pyramids, palms, the Nile; Joseph as a servant in a rich Egyptian house working hard, his "
                "master smiling and handing him keys; then (gently) Joseph led to prison by guards; soft golden "
                "light stays with him in both places.",
        "lines": [
            ("N", "在埃及，约瑟做了奴隶。可是，上帝和约瑟同在。"),
            ("N", "约瑟做事很认真，主人很信任他，让他管理全家的事。"),
            ("N", "后来，约瑟被人冤枉，关进了监牢。可是在监牢里，上帝还是和约瑟同在。"),
        ],
    },
    {
        "id": "s09_prison", "mood": "belly",
        "note": "40. The prison: Joseph kind to two prisoners (the king's cupbearer and baker), who look puzzled about "
                "their dreams (dream bubbles: a vine with grapes, baskets of bread); Joseph points up to heaven.",
        "lines": [
            ("N", "在监牢里，有两个人做了奇怪的梦。约瑟帮他们解梦，他说的都应验了。"),
            ("Y", "能解梦的不是我，是上帝。"),
        ],
    },
    {
        "id": "s10_pharaoh", "transition": "dippaper", "mood": "nineveh",
        "note": "41:1-36. Pharaoh's palace; Pharaoh's dream bubble: seven fat cows by the Nile, then seven thin cows "
                "come and eat them up (comic, not scary); wise men shrug; Joseph is brought in (shaved, clean robe) "
                "and explains: seven good years (golden wheat), seven hungry years (dry land); store the grain.",
        "lines": [
            ("N", "过了两年，埃及的法老王做了一个奇怪的梦。七头肥肥的牛，被七头瘦瘦的牛吃掉了！"),
            ("N", "没有人能解这个梦。这时候，有人想起了约瑟。"),
            ("Y", "上帝告诉你，会有七年大丰收，接着是七年大饥荒。要趁丰收的时候，把粮食存起来。"),
        ],
    },
    {
        "id": "s11_ruler", "mood": "lesson",
        "note": "41:37-49. Pharaoh puts his ring on Joseph's hand, a gold chain round his neck, fine linen clothes; "
                "Joseph rides in a chariot as people bow; during the good years the storehouses fill up, the "
                "grain heaps grow like mountains.",
        "lines": [
            ("P", "上帝和你同在，没有人比你更聪明。我要让你管理全埃及！"),
            ("N", "约瑟穿上了漂亮的衣服，戴上了金链子，坐上了大马车。"),
            ("N", "七年丰收的时候，约瑟把粮食存进仓库。粮食堆得像山一样高！"),
        ],
    },
    {
        "id": "s12_brothers", "transition": "dippaper", "mood": "worm",
        "note": "42:1-9. The famine (dry fields everywhere); the ten brothers travel to Egypt with donkeys to buy "
                "grain; in Joseph's hall they bow low before him; they do not recognise the Egyptian ruler, but "
                "Joseph recognises them; a picture-book callback: the sheaves bowing from the dream.",
        "lines": [
            ("N", "后来，饥荒来了。约瑟的哥哥们没有粮食吃，就来到埃及买粮。"),
            ("N", "他们向约瑟跪下下拜，可是，他们认不出约瑟。"),
            ("N", "小朋友，你还记得约瑟的梦吗？哥哥们的麦捆向他下拜，现在真的发生了！"),
        ],
    },
    {
        "id": "s13_forgive", "mood": "end",
        "note": "45, 46, 50:20. Joseph cannot hold back his tears and tells them who he is; the brothers are "
                "frightened; Joseph comforts them and hugs them; then old Jacob arrives in Egypt and hugs Joseph — "
                "the whole family together again.",
        "lines": [
            ("N", "约瑟再也忍不住了，大哭起来，说："),
            ("Y", "我就是约瑟，你们的弟弟啊！"),
            ("N", "哥哥们吓坏了，他们怕约瑟会报仇。"),
            ("Y", "不要害怕。你们本来想害我，可是上帝把它变成了好事，救了许多人的性命。"),
            ("N", "约瑟抱住哥哥们，原谅了他们。后来，爸爸雅各也来了。一家人，又在一起了！"),
        ],
    },
    {
        "id": "s14_end", "transition": "dippaper", "mood": "end",
        "note": "Ending: the two siblings from the opening make up and share the toy; Joseph's family together in a "
                "warm picture-book corner; golden light; closing question to children with a pause.",
        "lines": [
            ("N", "约瑟被卖，被冤枉，被关进监牢，可是他从来没有离开上帝，上帝也从来没有离开他。"),
            ("N", "小朋友，如果有人对你不好，你愿意原谅他吗？", 2.0),
            ("N", "上帝可以把不好的事，变成好事。我们也可以像约瑟一样，学会原谅。"),
        ],
    },
]

LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
