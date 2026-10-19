"""约拿的故事 (v2) — narration script and scene list (single source of truth).

The Book of Jonah, chapters 1-4, told for children aged 3-8 at a natural storytelling pace, in
plain spoken Chinese (reviewed for Bible accuracy, child-friendliness and TTS pronunciation).
Jonah's two wishes to die (4:3, 4:8-9) are softened for young children; one line of historical
background (Nineveh was Israel's enemy) is added; everything else follows the text.

Each line is ONE utterance by one speaker and is synthesised in one piece, so
prosody and pauses stay natural. Subtitles are cut from it automatically at
punctuation and timed from the recognised speech (voice/tts.py).

Speakers (voices in voice/tts.py):
    N = narrator   G = God (never shown as a person)   J = Jonah
    C = the ship's captain   S = the sailors   K = the king of Nineveh
"""

TITLE = "约拿的故事"
SUBTITLE = "圣经绘本 · 约拿书"
NO_BREAK = ["约拿", "尼尼微", "他施", "约帕", "以色列"]   # names read in one breath (voice/tts.py retakes a line that pauses inside one)

# Each scene: id (art/scenes/<id>.py), a note for illustrators and the composer,
# music mood, optional transition into the scene (ffmpeg xfade name, default
# "fade"), optional lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 1.6,
        "note": "Title page: calm sea at dawn, the great fish arching out of the water, a small ship; book title.",
        "lines": [("N", "圣经绘本：约拿的故事。")],
    },
    {
        "id": "s02_call", "mood": "call",
        "note": "Jonah 1:1-2. Jonah's hillside village in Israel; God's warm light from heaven; Nineveh far away "
                "to the east in a vision bubble (a fierce enemy city).",
        "lines": [
            ("N", "很久很久以前，在以色列，有一个先知，名叫约拿。"),
            ("N", "先知，就是替上帝传话的人。"),
            ("N", "有一天，上帝对约拿说："),
            ("G", "约拿，你起来，到尼尼微那座大城去。"),
            ("G", "城里的人做了许多坏事，我都看见了。你要去大声警告他们。"),
            ("N", "尼尼微在很远的东方。那里的人很凶，是以色列人的敌人。"),
        ],
    },
    {
        "id": "s03_flee", "mood": "flee",
        "note": "Jonah 1:3. Jonah turns away from the road to Nineveh (east) and runs west to the port of Joppa; "
                "pays the fare; boards a ship for Tarshish.",
        "lines": [
            ("N", "可是，约拿不愿意去。他转过身，朝着相反的方向跑走了。"),
            ("N", "约拿为什么不想去呢？故事的后面，我们就会知道。"),
            ("N", "他一路跑到海边的约帕城，找到一条要开往他施的船。他施在很远很远的西边。"),
            ("N", "约拿付了船钱，上了船，想要逃到远方，躲开上帝。"),
        ],
    },
    {
        "id": "s04_storm", "mood": "storm",
        "note": "Jonah 1:4-5. The storm; the sailors cry to their own gods and throw cargo overboard; Jonah asleep "
                "below deck.",
        "lines": [
            ("N", "但是，人怎么能躲开上帝呢？船开出去不久，上帝就让海上刮起了狂风。"),
            ("N", "大浪一个接着一个打过来，船摇来摇去，好像就要被打碎了。"),
            ("N", "水手们都吓坏了，每个人都向自己拜的神求救。他们把船上的货物扔进海里，想让船轻一些。"),
            ("N", "这时候，约拿在哪里呢？原来，他早已下到船舱底下，躺在那里，呼呼大睡。"),
        ],
    },
    {
        "id": "s05_captain", "mood": "lots",
        "note": "Jonah 1:6. In the hold: the captain shakes Jonah awake and urges him to call on his god.",
        "lines": [
            ("N", "船长找到了约拿，把他摇醒，说："),
            ("C", "快醒醒！风浪这么大，你怎么还在睡觉？"),
            ("C", "快起来，求你的神救救我们吧！也许你的神会可怜我们，让我们活下来。"),
        ],
    },
    {
        "id": "s06_lots", "mood": "lots",
        "note": "Jonah 1:7-10. On deck in the storm: the sailors cast lots; the lot falls on Jonah; they question him; "
                "he answers; they are terrified.",
        "lines": [
            ("N", "水手们彼此商量说："),
            ("S", "来，我们来抽签，看看是哪个人惹来了这场大风暴！"),
            ("N", "他们就抽签。结果，抽中的正是约拿！水手们赶紧问他："),
            ("S", "请你告诉我们，你是做什么的？你从哪里来？你是哪国人？"),
            ("J", "我是希伯来人。我敬拜耶和华，天上的上帝。大海和陆地，都是他造的。"),
            ("N", "耶和华，就是上帝的名字。约拿还告诉他们，他正在逃跑，想要躲开耶和华。水手们听了，更加害怕了，说："),
            ("S", "你怎么能做这样的事呢？"),
        ],
    },
    {
        "id": "s07_confess", "mood": "lots",
        "note": "Jonah 1:11-12. The sea grows wilder; the sailors ask what to do; Jonah tells them to throw him in.",
        "lines": [
            ("N", "海浪越来越大，越来越凶。水手们问约拿："),
            ("S", "我们该拿你怎么办，海才会平静下来呢？"),
            ("J", "你们把我抬起来，扔进海里吧，海就会平静下来。"),
            ("J", "我知道，这场大风浪，都是因为我。"),
        ],
    },
    {
        "id": "s08_row", "mood": "storm",
        "note": "Jonah 1:13-14. The sailors row with all their strength toward land but cannot; they pray to the LORD, "
                "Jonah's God, and own that he has done as he pleased.",
        "lines": [
            ("N", "水手们不忍心把约拿扔下去。他们拼命划桨，想让船回到岸边。"),
            ("N", "但是，海浪越翻越高。他们怎么用力划桨，都没有办法回到岸边。"),
            ("N", "水手们只好向约拿的上帝耶和华祷告："),
            ("S", "耶和华啊，我们实在没有办法了。求你不要因为这个人惩罚我们，也不要怪我们害了他。"),
            ("S", "因为这一切，都是你照着自己的心意做的。"),
        ],
    },
    {
        "id": "s09_overboard", "mood": "fish",
        "note": "Jonah 1:15-16. They throw Jonah into the sea; at once the sea is calm; the sailors fear the LORD, "
                "offer a sacrifice and make vows.",
        "lines": [
            ("N", "于是，他们把约拿抬起来，扔进了大海。"),
            ("N", "一下子，海就平静了。风停了，浪也静了。", 1.2),
            ("N", "水手们看见了，心里对耶和华又敬又怕。他们向耶和华献上祭物，还许下了诺言。"),
        ],
    },
    {
        "id": "s10_swallow", "mood": "fish",
        "note": "Jonah 1:17. Underwater: Jonah sinks; the great fish God prepared swims up and swallows him.",
        "lines": [
            ("N", "约拿往下沉，一直往下沉。"),
            ("N", "可是，上帝早就为约拿安排好了一条大鱼。"),
            ("N", "大鱼游过来，张开大嘴，一口就把约拿吞了下去！", 1.2),
        ],
    },
    {
        "id": "s11_belly", "mood": "belly", "transition": "fadeblack",
        "note": "Jonah 1:17-2:2. Inside the fish, dark and wet — but Jonah is alive; three days and three nights; "
                "he prays.",
        "lines": [
            ("N", "大鱼的肚子里又黑又湿。可是别怕，约拿还活着！"),
            ("N", "约拿在大鱼的肚子里，过了三天三夜。他在那里，向上帝祷告："),
            ("J", "我遇到危险，向你求救，你就回答了我。"),
            ("J", "我从很深很深的地方呼喊，你就听见了我的声音。"),
        ],
    },
    {
        "id": "s12_deep", "mood": "belly",
        "note": "Jonah 2:3-9. The prayer's pictures: thrown into the deep, waters around, seaweed around his head, down "
                "to the roots of the undersea mountains; when he was about to give up he remembered the LORD; God "
                "brings him up; thanks and vows; 'Salvation belongs to the LORD'.",
        "lines": [
            ("J", "你把我丢进深海，大水包围着我，海草缠在我的头上。"),
            ("J", "我一直往下沉，沉到了海底大山的脚下。"),
            ("J", "我快要支持不住的时候，就想起了耶和华。我的祷告，一直达到了你的面前。"),
            ("J", "你把我从深坑里，救了上来！"),
            ("J", "我要大声感谢你。我答应你的事，一定会做到。救恩属于耶和华！"),
        ],
    },
    {
        "id": "s13_shore", "mood": "shore", "transition": "circleopen",
        "note": "Jonah 2:10. God speaks to the fish; it swims to the shore and spits Jonah out onto dry land; Jonah "
                "is safe in the sunshine.",
        "lines": [
            ("N", "上帝吩咐那条大鱼。大鱼就游到岸边，张开大嘴，把约拿吐到了陆地上。"),
            ("N", "约拿浑身湿漉漉的，可是他又看见了太阳。他得救了！"),
        ],
    },
    {
        "id": "s14_again", "mood": "call",
        "note": "Jonah 3:1-3a. God speaks to Jonah a second time (echoing the first call); this time Jonah obeys.",
        "lines": [
            ("N", "上帝第二次对约拿说："),
            ("G", "约拿，你起来，到尼尼微那座大城去，把我告诉你的话，说给城里的人听。"),
            ("N", "这一次，约拿听话了。他起来，照着上帝的吩咐，往尼尼微去。"),
        ],
    },
    {
        "id": "s15_city", "mood": "nineveh",
        "note": "Jonah 3:3b-4. Nineveh is huge — three days' walk; Jonah walks a day into the city crying out.",
        "lines": [
            ("N", "尼尼微是一座非常非常大的城，要走整整三天，才能走遍整座城。"),
            ("N", "约拿进了城，走了一天的路，一边走，一边大声喊："),
            ("J", "再过四十天，尼尼微就要毁灭了！", 1.2),
        ],
    },
    {
        "id": "s16_believe", "mood": "repent",
        "note": "Jonah 3:5. Surprise: the people believe God; they fast and put on sackcloth, grown-ups and children.",
        "lines": [
            ("N", "你猜怎么样？尼尼微的人听了，竟然都相信了上帝！"),
            ("N", "他们禁食，就是不吃饭。大人小孩都换上粗粗的麻布衣服，向上帝认错，表示愿意改。"),
        ],
    },
    {
        "id": "s17_king", "mood": "repent",
        "note": "Jonah 3:6-9. The king rises from his throne, lays aside his robe, puts on sackcloth and sits in ashes; "
                "his decree: no food or water for people or animals, all in sackcloth, crying to God, turning from "
                "evil and violence.",
        "lines": [
            ("N", "国王听说了，也从宝座上站起来，脱下漂亮的王袍，换上粗麻布衣服，坐在灰堆里，表示真心认错。"),
            ("N", "国王又派人在全城宣告："),
            ("K", "所有的人和牛羊，都不可以吃，也不可以喝。"),
            ("K", "人和牛羊，都要穿上麻布衣服，诚心向上帝呼求。"),
            ("K", "每个人都要改掉坏行为，不再欺负别人。说不定上帝会可怜我们，我们就能活下来！"),
        ],
    },
    {
        "id": "s18_mercy", "mood": "repent",
        "note": "Jonah 3:10. God sees they really turned from their evil ways and has mercy; the city is not "
                "destroyed (golden light over the city, joy).",
        "lines": [
            ("N", "上帝看见他们真的改掉了坏行为，就可怜他们，没有毁灭这座城。"),
            ("N", "整座尼尼微城，都得到了平安！"),
        ],
    },
    {
        "id": "s19_angry", "mood": "vine",
        "note": "Jonah 4:1-4. Everyone rejoices except Jonah, who is very angry; he says this is why he fled — he "
                "knew God is kind and relents from the disaster he announced; the narrator explains; God asks: is "
                "it right for you to be angry?",
        "lines": [
            ("N", "大家都很高兴，只有约拿一点儿也不高兴。他非常生气，对上帝说："),
            ("J", "耶和华啊，我早就知道会这样！所以我才急忙逃到他施去。"),
            ("J", "因为我知道，你又慈爱，又宽容，不轻易生气。你说要降下的灾祸，只要人一认错，你就不忍心降下来。"),
            ("N", "原来，约拿早就知道上帝会可怜尼尼微人。可是他不愿意上帝饶恕他们，所以当初才逃跑了。"),
            ("N", "于是，上帝问约拿："),
            ("G", "约拿，你这样生气，对吗？"),
        ],
    },
    {
        "id": "s20_booth", "mood": "vine",
        "note": "Jonah 4:5. Jonah leaves the city, sits on its east side, builds a little booth and waits to see "
                "what will happen to the city.",
        "lines": [
            ("N", "约拿没有回答。他出了城，坐在城的东边，为自己搭了一座小棚子。"),
            ("N", "他坐在棚子下面的阴凉里，要看看这座城到底会怎么样。"),
        ],
    },
    {
        "id": "s21_vine", "mood": "vine",
        "note": "Jonah 4:6. God appoints a castor-oil plant; overnight it grows tall; its big leaves shade Jonah like "
                "a green umbrella; Jonah is very glad.",
        "lines": [
            ("N", "上帝安排了一棵蓖麻。一夜之间，蓖麻就长起来了，又高又大。"),
            ("N", "它宽宽的叶子，像一把绿色的大伞，替约拿挡住了火辣辣的太阳。"),
            ("N", "这下，约拿非常非常高兴！"),
        ],
    },
    {
        "id": "s22_worm", "mood": "worm",
        "note": "Jonah 4:7-9. At dawn God appoints a little worm that bites the plant; it withers. Then a hot dry "
                "east wind and the sun on Jonah's head; he is faint and upset. God asks; Jonah answers angrily.",
        "lines": [
            ("N", "第二天天刚亮，上帝又安排了一条小虫子。小虫子咬了蓖麻，蓖麻就枯死了。"),
            ("N", "太阳出来以后，上帝安排了又热又干的东风。太阳晒在约拿的头上，约拿热极了，头都发昏了，又难过又生气。"),
            ("N", "上帝又问约拿："),
            ("G", "约拿，你因为这棵蓖麻生气，对吗？"),
            ("J", "对！我就是生气！我气极了！"),
        ],
    },
    {
        "id": "s23_lesson", "mood": "lesson",
        "note": "Jonah 4:10-11. God speaks gently: Jonah cared for a plant he did not make grow; how much more should "
                "God care for the great city of 120,000 people who cannot tell right from wrong, and many animals.",
        "lines": [
            ("G", "约拿，这棵蓖麻不是你栽种的，也不是你让它长大的。"),
            ("G", "它一夜长起来，一夜又枯死了，你都这么心疼它。"),
            ("G", "尼尼微这座大城里，有十二万多人，就像分不清左右手的小孩子，不知道什么是对，什么是错。"),
            ("G", "还有许多牛羊。我怎么能不心疼他们呢？"),
        ],
    },
    {
        "id": "s24_end", "mood": "end", "tail": 3.4,
        "note": "Closing at sunset: the Bible ends on God's question — how would you answer? God's love is wider than "
                "the sea and higher than the sky, for Israel and Nineveh, Jonah and you and me; second chances; "
                "love even people we don't like; 'The End'.",
        "lines": [
            ("N", "约拿是怎么回答的呢？圣经没有告诉我们。"),
            ("N", "如果你是约拿，你会怎么回答上帝呢？", 2.5),
            ("N", "上帝的爱，比大海还要宽，比天空还要高。他爱以色列人，也爱尼尼微人；他爱约拿，也爱你和我。"),
            ("N", "我们做错了事，只要回到上帝身边，他总会给我们重新开始的机会。"),
            ("N", "上帝也希望我们像他一样，爱惜身边的每一个人，连我们不喜欢的人也一样。"),
        ],
    },
]

# Timing defaults (seconds): natural storytelling pauses.
LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
