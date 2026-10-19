"""大卫和歌利亚 — narration script and scene list (single source of truth for stories/david).

1 Samuel 17, told for children aged 3-8, about 4-5 minutes, in the narration style of SCRIPT_STYLE.md
(talk to the child, short sentences, thoughts and feelings said aloud, repetition, sound words, gentle
humour, an ending question). Same pipeline and narrator as the other films:
python3 build.py all --story david.

Speakers (narrator N from voice/tts.py; the others below):
    N = narrator   D = David (a shepherd boy)   L = Goliath   K = King Saul   E = Eliab (David's eldest
    brother)   X = Jesse (David's father)
God is never shown as a person. Goliath's defeat is shown as a fall, nothing more (no sword, no head).
"""

TITLE = "大卫和歌利亚"
SUBTITLE = "圣经绘本 · 撒母耳记上"

# speakers this story adds (same format as voice/tts.py VOICES; Kokoro v1.1-zh prompt voices: 66 is the
# highest-pitched male voice for the boy, 63 one of the lowest for the giant)
VOICES = {
    "D": {"engine": "zipvoice", "sid": 66, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 66, "speed": 0.95,
                     "text": "我是大卫，我在山坡上放羊。我的小羊又白又胖，我每天都带它们去喝水。"}},
    "L": {"engine": "zipvoice", "sid": 63, "speed": 0.85, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 63, "speed": 0.85,
                     "text": "我是非利士人的勇士，我力气很大，谁也打不过我。"}},
    "K": {"engine": "zipvoice", "sid": 100, "speed": 0.9, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 100, "speed": 0.9, "text": "我是以色列的国王，我带着军队在山上扎营。"}},
    "E": {"engine": "zipvoice", "sid": 87, "speed": 1.0, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 87, "speed": 0.9, "text": "我是家里的大哥，我在国王的军队里当兵。"}},
    "X": {"engine": "zipvoice", "sid": 71, "speed": 0.9, "fx": None, "gain_db": 0.0, "stretch_pauses": True,
          "prompt": {"engine": "kokoro", "sid": 71, "speed": 0.85, "text": "我是一个老人家，我有八个儿子，最小的那个在放羊。"}},
}
# pronunciation fixes for this script (merged into voice/lexicons.py ZV_FIX for this story only)
LEXICON = {
    "大卫": "da4 wei4", "歌利亚": "ge1 li4 ya4", "扫罗": "sao3 luo2", "以利押": "yi3 li4 ya1",
    "耶西": "ye1 xi1", "伯利恒": "bo2 li4 heng2", "非利士人": "fei1 li4 shi4 ren2", "机弦": "ji1 xian2",
    "哐当": "kuang1 dang1", "嗖": "sou1", "咚": "dong1", "转啊转": "zhuan4 a5 zhuan4",
}
NO_BREAK = ["大卫", "歌利亚", "扫罗", "以利押", "耶西", "伯利恒", "非利士", "以色列"]  # read in one breath

# Each scene: id (stories/david/scenes/<id>.py), a note for illustrators and the composer, music mood,
# optional transition into the scene (ffmpeg xfade name, default "fade"; "fadeblack", "circleopen",
# "dippaper" = a page-turn dip through the paper colour, used where the place changes), optional
# lead_in / tail seconds, and lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title", "mood": "title", "lead_in": 1.6, "tail": 1.6,
        "note": "Title page: a shepherd boy with his sling sits on a sunny hill with his sheep; far across the valley "
                "a huge bronze helmet glints. Book title.",
        "lines": [("N", "圣经绘本：大卫和歌利亚。")],
    },
    {
        "id": "s02_afraid", "mood": "call",
        "note": "Opening question to the child: a little child in bed hiding under the blanket from thunder (a small "
                "picture-book vignette); then a crowd of soldiers peeking out, trembling, at a huge shadow.",
        "lines": [
            ("N", "小朋友，你有没有害怕过什么？比如打雷，比如黑黑的房间？", 1.0),
            ("N", "今天的故事里，有一大群人，都怕得不得了。他们怕的，是一个巨人！"),
        ],
    },
    {
        "id": "s03_valley", "transition": "dippaper", "mood": "nineveh",
        "note": "1 Samuel 17:1-3. The valley of Elah: Israel's tents and banners on the hill on the left, the "
                "Philistine camp on the hill on the right, a valley with a little brook between.",
        "lines": [
            ("N", "很久以前，以色列人和非利士人要打仗了。"),
            ("N", "以色列人站在这边的山上，非利士人站在那边的山上，中间隔着一道山谷。"),
        ],
    },
    {
        "id": "s04_giant", "mood": "storm",
        "note": "17:4-11. Goliath strides out of the Philistine camp (boom, boom, boom), huge: bronze helmet, scale "
                "armour, a shield-bearer in front of him, a spear as thick as a weaver's beam; he shouts his "
                "challenge across the valley; Israel's soldiers (and King Saul among them) shrink back, knees "
                "shaking. Big and loud but a little comic, never gory.",
        "lines": [
            ("N", "这时候，非利士人的营里，走出来一个人。咚！咚！咚！"),
            ("N", "他的名字叫歌利亚。他好高好高，差不多有篮球架那么高！"),
            ("N", "他戴着铜头盔，穿着铜盔甲，手里的枪，粗得像一根大木头。"),
            ("L", "以色列人听着！派一个人出来跟我打！他要是赢了，我们就做你们的仆人。要是我赢了，你们就做我们的仆人！"),
            ("N", "以色列人听了，吓得腿都软了。连扫罗王，也不敢出来。"),
        ],
    },
    {
        "id": "s05_forty", "mood": "lots",
        "note": "17:16. Morning and evening, forty days: the sun rises and sets over the valley again and again (a "
                "picture-book day counter), Goliath shouting each time, Israel's soldiers hiding behind shields.",
        "lines": [
            ("N", "第二天早上，歌利亚又来喊。到了晚上，他又来喊。"),
            ("N", "早上喊，晚上喊，一连喊了四十天。"),
            ("N", "可是以色列人里，一个敢出来的都没有。"),
        ],
    },
    {
        "id": "s06_shepherd", "transition": "dippaper", "mood": "flee",
        "note": "17:12-20. Bethlehem: green hills, a boy (David, about 12, ruddy, curly hair, simple tunic, shepherd's "
                "bag, staff) with his sheep; his old father Jesse at the house gives him a basket of bread and "
                "cheese; David hands the sheep to a helper and sets off at dawn.",
        "lines": [
            ("N", "在伯利恒的山坡上，有一个放羊的男孩，名叫大卫。"),
            ("N", "大卫是家里最小的孩子。他的三个哥哥，都在扫罗王的军队里。"),
            ("N", "有一天，爸爸耶西对大卫说："),
            ("X", "大卫，你带上这些饼和奶酪，去看看你的哥哥们，看他们好不好。"),
            ("N", "大卫一大早就起来，把羊交给别人看管，出发了。"),
        ],
    },
    {
        "id": "s07_camp", "transition": "dippaper", "mood": "lots",
        "note": "17:20-30. Israel's camp: David arrives with his basket and greets his brothers; Goliath's voice "
                "booms across the valley and the soldiers run; David, puzzled and brave, asks; his eldest brother "
                "Eliab, cross, scolds him; David answers simply.",
        "lines": [
            ("N", "大卫刚到军营，就听见了一个好大好大的声音。"),
            ("L", "胆小鬼们！谁敢出来跟我打？"),
            ("N", "以色列的士兵一看见歌利亚，转身就跑。"),
            ("D", "这个人是谁？他怎么敢骂永生上帝的军队呢？"),
            ("N", "大卫的大哥以利押听见了，很生气。"),
            ("E", "你来这里做什么？你的羊谁看着呢？你就是来看热闹的吧！"),
            ("D", "我又做了什么呢？我只是问问而已。"),
        ],
    },
    {
        "id": "s08_saul", "transition": "dippaper", "mood": "repent",
        "note": "17:31-37. King Saul's tent: the tall worried king on a camp stool; David stands before him; David's "
                "memories of the lion and the bear grabbing a lamb appear as picture-book thought bubbles (he "
                "rescues the lamb; no blood); Saul finally blesses him.",
        "lines": [
            ("N", "有人把大卫的话告诉了扫罗王。扫罗王就叫人把大卫带来。"),
            ("D", "王啊，大家都不用害怕。我要去跟那个巨人打！"),
            ("K", "你？你还是个孩子啊！他从年轻的时候，就是打仗的勇士了！"),
            ("D", "我替爸爸放羊的时候，有狮子来抓小羊，也有熊来抓小羊。我就去追，把小羊从它们嘴里救回来。"),
            ("D", "上帝救我脱离了狮子和熊的爪子，也一定会救我脱离这个巨人的手！"),
            ("K", "好吧，你去吧！愿上帝和你同在。"),
        ],
    },
    {
        "id": "s09_armor", "mood": "worm",
        "note": "17:38-39. Comic: Saul dresses David in his own armour; the helmet slips over his eyes, the coat of "
                "mail is far too big, the sword drags; David tries a few steps (clank, clank) and wobbles; he takes "
                "it all off and is himself again.",
        "lines": [
            ("N", "扫罗王把自己的盔甲给大卫穿上。头上戴上铜头盔，身上穿上铠甲，腰上挂上一把大刀。"),
            ("N", "大卫试着走了几步。哐当，哐当……哎呀，太重了，根本走不动！"),
            ("D", "这些我穿不惯。"),
            ("N", "大卫就把盔甲全都脱了下来。"),
        ],
    },
    {
        "id": "s10_stones", "transition": "dippaper", "mood": "shore",
        "note": "17:40. The brook in the valley: David with his staff kneels and picks five smooth stones, one by one, "
                "into his shepherd's bag; then he holds up his sling (a long strap with a pouch) and gives it a "
                "test swing.",
        "lines": [
            ("N", "大卫拿起放羊的杖，来到小溪边。"),
            ("N", "他弯下腰，挑了五块光滑的石头。一块，两块，三块，四块，五块，都放进口袋里。"),
            ("N", "他手里还拿着一样东西：甩石头用的机弦。那是一根长长的带子，能把石头甩得又快又远。"),
        ],
    },
    {
        "id": "s11_face", "mood": "storm",
        "note": "17:41-47. The valley: the giant and his shield-bearer on one side, the small boy on the other; "
                "Goliath laughs and mocks; David answers bravely, pointing up to heaven; both armies watch from the "
                "hills.",
        "lines": [
            ("N", "歌利亚看见大卫走过来，哈哈大笑。"),
            ("L", "你拿着棍子来找我，把我当成狗吗？过来，我要把你喂给天上的鸟！"),
            ("D", "你来打我，靠的是刀和枪。我来打你，靠的是万军之耶和华的名！"),
            ("D", "今天，我要让全世界的人都知道，以色列有一位上帝！打仗的输赢，全在乎上帝！"),
        ],
    },
    {
        "id": "s12_sling", "mood": "fish",
        "note": "17:48-49. The action: Goliath stomps forward; David runs toward him; a stone into the sling; spin, "
                "spin; whoosh, the stone flies; it hits Goliath's forehead (a cartoon star, no blood); the giant "
                "topples face down with a great thud and dust. Exciting, never frightening.",
        "lines": [
            ("N", "歌利亚朝大卫走过来。大卫不但没有跑，反而朝着歌利亚跑过去！"),
            ("N", "他从口袋里拿出一块石头，放在机弦上，转啊转，转啊转……"),
            ("N", "嗖！石头飞了出去，正好打中歌利亚的额头。"),
            ("N", "咚！巨人扑倒在地上，再也起不来了。"),
        ],
    },
    {
        "id": "s13_victory", "mood": "lesson",
        "note": "17:51-52. The Philistines see their champion down and run away over the hill; Israel's soldiers "
                "cheer, throwing up their arms; King Saul amazed; David looks up to heaven, thankful.",
        "lines": [
            ("N", "非利士人一看，他们最厉害的勇士倒下了，吓得转身就逃。"),
            ("N", "以色列人欢呼起来。大家都知道：是上帝帮助了大卫！"),
        ],
    },
    {
        "id": "s14_end", "transition": "dippaper", "mood": "end",
        "note": "Ending: evening on the Bethlehem hill, David sitting with his sheep, playing a little harp under the "
                "first stars; the five-stone bag beside him (four stones left). Warm closing question to children.",
        "lines": [
            ("N", "大卫并不比歌利亚高，也不比歌利亚壮。可是大卫知道，上帝比任何巨人都大。"),
            ("N", "小朋友，你心里，有没有一个让你害怕的巨人呢？", 2.0),
            ("N", "下次害怕的时候，你也可以像大卫一样，对上帝说：上帝啊，我相信你和我在一起！"),
        ],
    },
]

LEAD_IN = 0.9      # quiet before a scene's first line
LINE_GAP = 0.65    # pause after each utterance (overridable per line)
SPEAKER_GAP = 0.85  # pause when the next utterance is by a different speaker
TAIL = 1.3         # time after a scene's last line before the transition begins
XFADE = 1.0        # cross-dissolve between scenes (overlaps neighbouring scenes)
