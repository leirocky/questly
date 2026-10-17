"""约拿的故事 (v2) — narration script and scene list (single source of truth).

The Book of Jonah, chapters 1-4, told for children aged 3-8 at a natural storytelling pace.
Wording follows the 和合本 where practical, in plain words. Jonah's two wishes to die
(4:3, 4:8-9) are softened for young children; everything else follows the text.

Each line is ONE utterance by one speaker and is synthesised in one piece, so
prosody and pauses stay natural. Subtitles are cut from it automatically at
punctuation and timed from the recognised speech (voice/tts.py).

Speakers (voices in voice/tts.py):
    N = narrator   G = God (never shown as a person)   J = Jonah
    C = the ship's captain   S = the sailors   K = the king of Nineveh
"""

TITLE = "约拿的故事"
SUBTITLE = "圣经绘本 · 约拿书"

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
                "to the east in a vision bubble.",
        "lines": [
            ("N", "很久很久以前，在以色列，有一位先知，名叫约拿。"),
            ("N", "先知，就是替上帝传话的人。"),
            ("N", "有一天，上帝对约拿说："),
            ("G", "约拿，你起来，往尼尼微那座大城去，向城里的人大声呼喊。因为他们做了许多坏事，他们的恶行已经达到我的面前。"),
        ],
    },
    {
        "id": "s03_flee", "mood": "flee",
        "note": "Jonah 1:3. Jonah turns away from the road to Nineveh (east) and runs west to the port of Joppa; "
                "pays the fare; boards a ship for Tarshish.",
        "lines": [
            ("N", "可是，约拿不愿意去。他转过身，朝着相反的方向跑走了。"),
            ("N", "他一路跑到海边的约帕城，找到一条要开往他施的船。他施在很远很远的西边。"),
            ("N", "约拿付了船钱，上了船，想要逃到远方，躲开上帝。"),
        ],
    },
    {
        "id": "s04_storm", "mood": "storm",
        "note": "Jonah 1:4-5. The storm; sailors cry to their gods and throw cargo overboard; Jonah asleep below deck.",
        "lines": [
            ("N", "可是，人怎么能躲开上帝呢？船开到海上，上帝就让海上刮起了狂风。"),
            ("N", "大浪一个接着一个打过来，船摇来摇去，好像就要被打碎了。"),
            ("N", "水手们都吓坏了，各人向自己的神哀求。他们把船上的货物扔进海里，想让船轻一些。"),
            ("N", "这时候，约拿在哪里呢？原来，他早已下到船舱底下，躺在那里，沉沉地睡着了。"),
        ],
    },
    {
        "id": "s05_captain", "mood": "lots",
        "note": "Jonah 1:6. In the hold: the captain shakes Jonah awake and pleads with him to pray.",
        "lines": [
            ("N", "船长找到了约拿，把他摇醒，说："),
            ("C", "你这个睡觉的人哪，怎么还睡得着呢？快起来，求告你的上帝吧！也许上帝会顾念我们，我们就不会死了。"),
        ],
    },
    {
        "id": "s06_lots", "mood": "lots",
        "note": "Jonah 1:7-10. On deck in the storm: the sailors cast lots; the lot falls on Jonah; they question him; "
                "he answers; they are terrified.",
        "lines": [
            ("N", "水手们彼此商量说："),
            ("S", "来，我们来抽签，看看这场灾祸是因为谁而来的。"),
            ("N", "他们就抽签，签落在了约拿身上。"),
            ("S", "请你告诉我们，你是做什么的？你从哪里来？你是哪国人？"),
            ("J", "我是希伯来人。我敬畏耶和华，他是天上的上帝，是创造大海和陆地的那一位。"),
            ("N", "约拿还告诉他们，自己正在逃避上帝。水手们听了，更加害怕，说："),
            ("S", "你怎么做出这样的事来呢？"),
        ],
    },
    {
        "id": "s07_confess", "mood": "lots",
        "note": "Jonah 1:11-12. The sea grows wilder; the sailors ask what to do; Jonah tells them to throw him in.",
        "lines": [
            ("N", "海浪越来越大，越来越凶。水手们问约拿："),
            ("S", "我们该怎么处置你，才能让海平静下来呢？"),
            ("J", "你们把我抬起来，抛进海里，海就会平静下来。我知道，你们遇到这场大风浪，都是因为我的缘故。"),
        ],
    },
    {
        "id": "s08_row", "mood": "storm",
        "note": "Jonah 1:13-14. The sailors row with all their strength toward land but cannot; they pray to the LORD.",
        "lines": [
            ("N", "可是，水手们不忍心这样做。他们拼命地划桨，想把船划回岸边。"),
            ("N", "可是风浪越来越大，他们怎么划，也划不回去。"),
            ("N", "水手们只好向耶和华祷告："),
            ("S", "耶和华啊，求你不要因为这个人的性命，使我们死亡。"),
        ],
    },
    {
        "id": "s09_overboard", "mood": "fish",
        "note": "Jonah 1:15-16. They throw Jonah into the sea; at once the sea is calm; the sailors fear the LORD, "
                "offer a sacrifice and make vows.",
        "lines": [
            ("N", "于是，他们把约拿抬起来，抛进了大海。"),
            ("N", "海立刻就平静了。风停了，浪也静了。"),
            ("N", "水手们看见了，就非常敬畏耶和华。他们向耶和华献上祭物，并且许了愿。"),
        ],
    },
    {
        "id": "s10_swallow", "mood": "fish",
        "note": "Jonah 1:17. Underwater: Jonah sinks; the great fish God prepared swims up and swallows him.",
        "lines": [
            ("N", "约拿往下沉，一直往下沉。"),
            ("N", "这时候，上帝早已安排了一条大鱼。"),
            ("N", "大鱼游过来，张开大嘴，一口就把约拿吞了下去！"),
        ],
    },
    {
        "id": "s11_belly", "mood": "belly", "transition": "fadeblack",
        "note": "Jonah 1:17-2:2. Inside the fish, dark; three days and three nights; Jonah begins to pray.",
        "lines": [
            ("N", "约拿在大鱼的腹中，过了三天三夜。"),
            ("N", "那里又黑又湿，什么也看不见。约拿就在大鱼的腹中，向上帝祷告。"),
            ("J", "我在患难中求告你，你就应允我。我从深处呼求，你就俯听我的声音。"),
        ],
    },
    {
        "id": "s12_deep", "mood": "belly",
        "note": "Jonah 2:3-9. The prayer's pictures: thrown into the deep, waters all around, seaweed around his head, "
                "down to the roots of the mountains — then God lifts his life up; thankfulness; 'Salvation belongs "
                "to the LORD'.",
        "lines": [
            ("J", "你把我投下深海，大水环绕我，海草缠绕我的头。"),
            ("J", "我沉到了山根底下，可是你把我的性命，从深坑里救了出来。"),
            ("J", "我要用感谢的声音向你献祭。我所许的愿，我一定要还。救恩属于耶和华！"),
        ],
    },
    {
        "id": "s13_shore", "mood": "shore", "transition": "circleopen",
        "note": "Jonah 2:10. God speaks to the fish; it swims to the shore and spits Jonah out onto dry land.",
        "lines": [
            ("N", "上帝吩咐那条大鱼。大鱼就游到岸边，把约拿吐到了陆地上。"),
        ],
    },
    {
        "id": "s14_again", "mood": "call",
        "note": "Jonah 3:1-3a. God speaks to Jonah a second time; this time Jonah obeys and sets off east.",
        "lines": [
            ("N", "上帝第二次对约拿说："),
            ("G", "你起来，往尼尼微那座大城去，向城里的人宣告我吩咐你的话。"),
            ("N", "这一次，约拿听话了。他起来，照着上帝的吩咐，往尼尼微去。"),
        ],
    },
    {
        "id": "s15_city", "mood": "nineveh",
        "note": "Jonah 3:3b-4. Nineveh is huge — three days' walk across; Jonah walks a day into the city crying out.",
        "lines": [
            ("N", "尼尼微是一座非常大的城。从城的这一头走到那一头，要走整整三天。"),
            ("N", "约拿进了城，走了一天的路，一边走，一边大声呼喊："),
            ("J", "再过四十天，尼尼微就要倾覆了！"),
        ],
    },
    {
        "id": "s16_believe", "mood": "repent",
        "note": "Jonah 3:5. The people believe God, proclaim a fast and put on sackcloth, from the greatest to the least.",
        "lines": [
            ("N", "尼尼微的人听见了，就相信了上帝。"),
            ("N", "他们宣告禁食，从最大的到最小的，都穿上了粗糙的麻衣，表示自己悔改。"),
        ],
    },
    {
        "id": "s17_king", "mood": "repent",
        "note": "Jonah 3:6-9. The king rises from his throne, lays aside his robe, puts on sackcloth and sits in ashes; "
                "his decree: no food or water for people or animals, all in sackcloth, crying to God, turning from evil.",
        "lines": [
            ("N", "这个消息传到了尼尼微王那里。国王从宝座上起来，脱下华丽的朝服，穿上麻衣，坐在炉灰中。"),
            ("N", "国王又派人在全城宣告："),
            ("K", "人和牲畜，牛群羊群，什么都不可以吃，也不可以喝水。人和牲畜都要披上麻衣，切切地求告上帝。"),
            ("K", "各人都要离开自己的恶行，不再欺负别人。也许上帝会怜悯我们，不再发怒，我们就不会灭亡了。"),
        ],
    },
    {
        "id": "s18_mercy", "mood": "repent",
        "note": "Jonah 3:10. God sees how they turned from their evil ways and has mercy; the threatened disaster "
                "does not come (golden light over the city).",
        "lines": [
            ("N", "上帝看见他们所做的，看见他们真的离开了恶道，就怜悯他们，没有把灾祸降给他们。"),
        ],
    },
    {
        "id": "s19_angry", "mood": "vine",
        "note": "Jonah 4:1-4. Jonah is very displeased and angry; he complains to God: this is why he fled — he knew "
                "God is gracious and merciful; God asks: is it right for you to be angry?",
        "lines": [
            ("N", "尼尼微得救了，约拿却很不高兴，甚至非常生气。他向上帝祷告说："),
            ("J", "耶和华啊，我还在家乡的时候，不就是这么说的吗？所以，我才急忙逃往他施。"),
            ("J", "因为我知道，你是有恩典、有怜悯的上帝，不轻易发怒，有丰盛的慈爱，总是不忍心降下灾祸。"),
            ("N", "约拿又难过，又生气。上帝问他："),
            ("G", "约拿，你这样发怒，合理吗？"),
        ],
    },
    {
        "id": "s20_booth", "mood": "vine",
        "note": "Jonah 4:5. Jonah leaves the city, sits on its east side, builds a little booth and waits to see "
                "what will happen to the city.",
        "lines": [
            ("N", "约拿没有回答。他出了城，坐在城的东边，为自己搭了一座小棚子。"),
            ("N", "他坐在棚子的阴凉底下，要看看这座城到底会怎么样。"),
        ],
    },
    {
        "id": "s21_vine", "mood": "vine",
        "note": "Jonah 4:6. God appoints a castor-oil plant; overnight it grows tall and shades Jonah's head; "
                "Jonah is very glad.",
        "lines": [
            ("N", "上帝安排了一棵蓖麻。一夜之间，蓖麻长得又高又大，宽大的叶子遮住了约拿的头，替他挡住炎热的太阳。"),
            ("N", "约拿因为这棵蓖麻，非常非常地喜乐。"),
        ],
    },
    {
        "id": "s22_worm", "mood": "worm",
        "note": "Jonah 4:7-9. At dawn God appoints a worm that attacks the plant; it withers. Then a scorching east "
                "wind and the sun on Jonah's head; he is faint. God asks; Jonah answers angrily.",
        "lines": [
            ("N", "第二天黎明，上帝又安排了一条虫子。虫子咬了蓖麻，蓖麻就枯干了。"),
            ("N", "太阳出来以后，上帝安排了炎热的东风。太阳晒在约拿的头上，约拿热得发昏，又难过又生气。"),
            ("G", "你因为这棵蓖麻发怒，合理吗？"),
            ("J", "合理！我生气极了！"),
        ],
    },
    {
        "id": "s23_lesson", "mood": "lesson",
        "note": "Jonah 4:10-11. God speaks gently about the plant and the great city with its 120,000 people who "
                "cannot tell right from left, and many animals.",
        "lines": [
            ("G", "约拿，这棵蓖麻不是你栽种的，也不是你使它长大的。它一夜长起来，一夜又干死了，你尚且爱惜它。"),
            ("G", "何况尼尼微这座大城，城里有十二万多不能分辨左右手的人，还有许多牲畜，我怎能不爱惜他们呢？"),
        ],
    },
    {
        "id": "s24_end", "mood": "end", "tail": 3.4,
        "note": "Closing page at sunset: God's love is wider than the sea and higher than the sky; he loves Israel and "
                "Nineveh, Jonah and you and me; 'The End'.",
        "lines": [
            ("N", "上帝的爱，比大海还要宽，比天空还要高。"),
            ("N", "他爱以色列人，也爱尼尼微人；他爱约拿，也爱你和我。"),
            ("N", "只要我们愿意回到他身边，他总是愿意给我们重新开始的机会。"),
        ],
    },
]

# Timing defaults (seconds): natural storytelling pauses.
LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
