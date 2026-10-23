"""Re-time the chapter buttons and durations of stories/index.html from the current timelines (each chapter is a
scene start; a chapter keeps the nearest scene, within 2 s) and add the card of a new film.  Run from the repository
root after rebuilding films:  python3 jonah-video/tools/story_page.py [nativity]"""
import json, re, sys
P = 'stories/index.html'
s = open(P, encoding='utf-8').read()
def tl(name): return json.load(open(f'jonah-video/build/{name}/timeline.json'))
def mmss(t): return f"{int(t // 60)}:{int(t % 60):02d}"
def dur_cn(t): t = round(t); return f"{t // 60} 分钟" if t % 60 == 0 else f"{t // 60} 分 {t % 60} 秒"
def retime(story):
    global s
    t = tl(story); starts = [x['start'] for x in t['scenes']]
    a = s.index(f'<article class="story" id="{story}">'); b = s.index('</article>', a)
    card = s[a:b]
    def fix(m):
        old = float(m.group(1)); new = min(starts, key=lambda x: abs(x - old))
        assert abs(new - old) < 2.0, (story, old, new)
        return f'<button data-t="{new:.1f}"><time>{mmss(new)}</time>'
    card = re.sub(r'<button data-t="([\d.]+)"><time>[\d:]+</time>', fix, card)
    card = re.sub(r' · \d+ 分 \d+ 秒 · ', f' · {dur_cn(t["duration"])} · ', card)
    s = s[:a] + card + s[b:]
for st in ['david', 'noah', 'joseph', 'storm']:
    retime(st)
def add_card(story, title, ref, blurb, chapters):
    global s
    if f'id="{story}"' in s:
        return
    t = tl(story); st = {x['id']: x['start'] for x in t['scenes']}
    lis = "\n".join(f'        <li><button data-t="{st[sid]:.1f}"><time>{mmss(st[sid])}</time>{name}</button></li>' for sid, name in chapters)
    card = f'''  <article class="story" id="{story}">
    <video controls preload="metadata" playsinline poster="{story}-poster.jpg">
      <source src="../jonah-video/output/{story}_story.mp4" type="video/mp4">
      你的浏览器无法播放这个视频。
    </video>
    <div class="body">
      <h2>{title}</h2>
      <div class="meta">{ref} · {dur_cn(t["duration"])} · 中文配音与字幕 · 适合 3–8 岁</div>
      <p>{blurb}</p>
      <ul class="chapters" aria-label="章节">
{lis}
      </ul>
    </div>
  </article>

'''
    i = s.index('  <footer>')
    s = s[:i] + card + s[i:]
CARDS = {
    'nativity': ('耶稣降生', '《路加福音》1–2 章 ·《马太福音》2 章',
                 '天使对马利亚说：“你要生一个儿子，给他起名叫耶稣。”约瑟和马利亚走了好多天回到伯利恒，客店没有地方，小耶稣就躺在马槽里。\n'
                 '        天使向牧羊人报好消息，东方的博士跟着星星来献上礼物。耶稣，是上帝送给全世界最好的礼物！',
                 [('s03_angel', '天使报喜'), ('s04_journey', '回伯利恒登记'), ('s05_no_room', '客店没有地方'),
                  ('s06_birth', '小耶稣出生了'), ('s07_shepherds', '野地里的牧羊人'), ('s08_choir', '天使歌唱'),
                  ('s09_visit', '找到婴孩'), ('s10_star', '东方的星'), ('s11_gifts', '博士献礼')]),
    'lost_sheep': ('迷失的羊', '《路加福音》15 章 ·《马太福音》18 章',
                   '耶稣和收税的人一起吃饭，法利赛人不高兴。耶稣就讲了一个故事：牧羊人有一百只羊，数来数去只有九十九只！\n'
                   '        他翻山过河，找啊找，终于找到了走丢的小羊。上帝就像这个牧羊人，你就是他的宝贝小羊。',
                   [('s03_meal', '和大家一起吃饭'), ('s04_story', '耶稣讲故事'), ('s05_flock', '一百只羊'),
                    ('s06_count', '数羊'), ('s07_alone', '小羊走丢了'), ('s08_search', '找啊找'), ('s09_found', '找到了'),
                    ('s10_party', '一起庆祝'), ('s11_meaning', '天上的欢喜')]),
    'zacchaeus': ('撒该爬上桑树', '《路加福音》19 章',
                  '收税的撒该很有钱，可是大家都不喜欢他。他个子矮，挤不进人群，就跑到前面爬上了桑树。\n'
                  '        耶稣抬起头说：“撒该，快下来！今天我要住在你家里。”撒该想看看耶稣，原来耶稣也在找他！',
                  [('s03_jericho', '耶利哥城'), ('s04_crowd', '挤不进去'), ('s05_tree', '爬上桑树'), ('s06_call', '撒该，快下来'),
                   ('s07_grumble', '大家不高兴'), ('s08_promise', '撒该的决定'), ('s09_saved', '救恩到了这一家'),
                   ('s10_heart', '撒该变了')]),
}
for name in sys.argv[1:]:
    add_card(name, *CARDS[name])
open(P, 'w', encoding='utf-8').write(s)
print('ok')
