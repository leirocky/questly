"""约拿的故事 — narration script and scene list (single source of truth).

Text follows the Book of Jonah (chapters 1-4, 和合本 wording where practical),
retold in simple words for children. Every line becomes one TTS clip and one
subtitle, so keep each line short enough for a single subtitle row (<= 24 汉字).

Speakers map to voices in ``voice/tts.py``:
    N = narrator, G = God (deep, with a soft echo), J = Jonah.
"""

TITLE = "约拿的故事"
SUBTITLE = "圣经绘本 · 约拿书"

# Each scene: id (matches art/scenes/<id>.py), a short English note for the
# illustrators and composer, music mood, optional transition into the scene
# (ffmpeg xfade name, default "fade"), and its lines: (speaker, text[, pause_after_s]).
SCENES = [
    {
        "id": "s01_title",
        "note": "Title page: calm sea at dawn, the great fish's back and a small ship; book title.",
        "mood": "title",
        "lead_in": 1.6,
        "tail": 1.4,
        "lines": [("N", "圣经绘本：约拿的故事。")],
    },
    {
        "id": "s02_call",
        "note": "Jonah 1:1-2. Jonah at his hillside home; warm light from heaven; God calls him.",
        "mood": "call",
        "lines": [
            ("N", "很久以前，有一位先知，名叫约拿。"),
            ("N", "上帝对他说："),
            ("G", "约拿，起来，到尼尼微大城去！"),
            ("G", "那里的人做了许多坏事，你要去警告他们。"),
        ],
    },
    {
        "id": "s03_flee",
        "note": "Jonah 1:3. Jonah runs the other way to the port of Joppa and boards a ship to Tarshish.",
        "mood": "flee",
        "lines": [
            ("N", "可是约拿不想去。"),
            ("N", "他跑到海边的约帕，坐上一条开往他施的船，"),
            ("N", "想要躲开上帝。"),
        ],
    },
    {
        "id": "s04_storm",
        "note": "Jonah 1:4-5. Huge storm; sailors throw cargo overboard; Jonah sleeps below deck.",
        "mood": "storm",
        "lines": [
            ("N", "上帝让海上刮起狂风大浪，"),
            ("N", "船几乎要被打破了！"),
            ("N", "水手们吓坏了，忙着把货物扔进海里。"),
            ("N", "约拿却躺在船舱底下，呼呼大睡。"),
        ],
    },
    {
        "id": "s05_lots",
        "note": "Jonah 1:6-12. Captain wakes Jonah; sailors cast lots; the lot falls on Jonah; he confesses.",
        "mood": "lots",
        "lines": [
            ("N", "船长叫醒了他。水手们抽签，"),
            ("N", "签落在了约拿身上。"),
            ("J", "是我得罪了上帝。把我抛进海里吧，"),
            ("J", "海就会平静下来。"),
        ],
    },
    {
        "id": "s06_fish",
        "note": "Jonah 1:15-17. Jonah thrown into the sea; the sea becomes calm; a great fish swallows him.",
        "mood": "fish",
        "lines": [
            ("N", "水手们把约拿抛进海里，海立刻平静了。"),
            ("N", "上帝安排了一条大鱼，"),
            ("N", "一口就把约拿吞了下去！"),
        ],
    },
    {
        "id": "s07_belly",
        "note": "Jonah 1:17-2:9. Inside the fish for three days and nights; Jonah prays in the dark.",
        "mood": "belly",
        "transition": "fadeblack",
        "lines": [
            ("N", "约拿在大鱼的腹中，过了三天三夜。"),
            ("N", "他在黑暗中向上帝祷告："),
            ("J", "我在患难中求告你，你就应允我。"),
            ("J", "救恩属于耶和华！"),
        ],
    },
    {
        "id": "s08_shore",
        "note": "Jonah 2:10. God speaks to the fish; it spits Jonah out onto dry land.",
        "mood": "shore",
        "transition": "circleopen",
        "lines": [
            ("N", "上帝吩咐大鱼，大鱼就把约拿吐到了陆地上。"),
        ],
    },
    {
        "id": "s09_nineveh",
        "note": "Jonah 3:1-4. God calls a second time; Jonah obeys, walks into the great city and preaches.",
        "mood": "nineveh",
        "lines": [
            ("N", "上帝再次呼召约拿，这一次，他听话了。"),
            ("N", "他走进尼尼微城，大声呼喊："),
            ("J", "再过四十天，尼尼微就要倾覆了！"),
        ],
    },
    {
        "id": "s10_repent",
        "note": "Jonah 3:5-10. The people and the king believe God, wear sackcloth and fast; God has mercy.",
        "mood": "repent",
        "lines": [
            ("N", "尼尼微人相信了上帝。从国王到百姓，"),
            ("N", "都穿上麻衣，禁食悔改。"),
            ("N", "上帝看见他们离开恶道，就怜悯他们，"),
            ("N", "没有降下灾祸。"),
        ],
    },
    {
        "id": "s11_vine",
        "note": "Jonah 4:1-8. Jonah sulks east of the city; God grows a castor-oil plant for shade, "
        "then a worm kills it; hot east wind and sun make Jonah faint.",
        "mood": "vine",
        "lines": [
            ("N", "约拿却很生气，坐在城外，看城会怎样。"),
            ("N", "上帝让一棵蓖麻长起来，为他遮阴，"),
            ("N", "约拿非常喜乐。"),
            ("N", "第二天，一条虫子咬了蓖麻，蓖麻枯干了。"),
            ("N", "烈日当头，热风吹来，约拿热得发昏。"),
        ],
    },
    {
        "id": "s12_lesson",
        "note": "Jonah 4:10-11. God gently speaks to Jonah about the plant and the great city.",
        "mood": "lesson",
        "lines": [
            ("G", "约拿，这棵蓖麻不是你栽种的，"),
            ("G", "你尚且这样爱惜它。"),
            ("G", "尼尼微有十二万多不能分辨左右手的人，"),
            ("G", "还有许多牲畜，我怎能不爱惜呢？"),
        ],
    },
    {
        "id": "s13_end",
        "note": "Closing page: God's love wider than the sea; sunset over sea and city; 'The End'.",
        "mood": "end",
        "tail": 3.2,
        "lines": [
            ("N", "上帝的爱，比海更宽，比天更高。"),
            ("N", "他愿意给每一个人，重新开始的机会。"),
        ],
    },
]

# Timing defaults (seconds).
LEAD_IN = 0.6      # silence at the start of a scene before its first line
LINE_GAP = 0.3    # pause after each line (overridable per line)
TAIL = 0.85        # time after a scene's last line before the transition begins
XFADE = 0.8        # cross-dissolve between scenes (overlaps neighbouring scenes)
