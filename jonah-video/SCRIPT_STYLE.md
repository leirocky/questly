# Narration style for the Bible picture-book films (ages 3–8)

Owner direction (2026-10-19): write like the Minno kids' Bible content for young children (e.g. Phil
Vischer's *Laugh and Grow Bible for Kids*: short, funny, gospel-centred five-minute stories told
straight to the child). Nothing similar exists in Chinese, so we make it. Take the *approach*, never the
text: every line is written fresh from the Bible passage.

## Rules
1. **Talk to the child.** The narrator is a friendly storyteller sitting next to them: 你、小朋友、我们.
   Open with one question from the child's own life (你有没有被人冤枉过？), then start the story.
2. **Short sentences.** One idea per sentence, usually ≤ 15 characters, at most ~20. This also keeps
   subtitles to one chunk and helps the TTS.
3. **Say what people think.** Inner thoughts as speech: 国王心想：嗯，这个人真不错！ Feelings get names
   a child knows (害怕、难过、着急、心里酸溜溜的), so hard words (嫉妒) come with a feeling.
4. **Repetition and rhythm.** Doubled verbs (找啊找，找啊找……), a refrain that comes back
   (但以理还是照样祷告), lists of three.
5. **Sound and action words** the narrator can perform: 咚！哗啦！嗷呜！ Check each with the TTS.
6. **Gentle humour** from the situation, the villains' clumsiness, the animals, everyday comparisons
   (狮子的嘴有多大？能装下一个西瓜！). Never joke about God, prayer or someone's suffering.
7. **Pictures a child knows.** Measure with their world: 比两层楼还高、走路要走三天、像幼儿园那么多人.
8. **Few names, said often.** Introduce one at a time; repeat the name instead of 他 when it could be
   unclear. Every name goes into the story's NO_BREAK list.
9. **Faithful to the passage.** Add expressions, thoughts and small actions, never new plot. Hard parts
   (punishment, death) in one calm sentence.
10. **Ending:** one sentence about who God is in this story, then one or two questions for the child,
    each followed by a pause (pause_after_s ~2 s) so a parent can talk with them.
11. **Length:** 3–5 minutes (about 450–750 characters of narration).

## Example (Daniel 6 opening)
Before (first films):
> 很久很久以前，有一个人，名叫但以理。他是以色列人，住在很远的巴比伦。
> 大利乌王管理着一个很大的国家。他派了一百二十个官员，又派了三个总管，来管理这些官员。

After:
> 小朋友，你有没有被人冤枉过？今天的故事里，有一个人就碰到了这样的事。
> 他的名字叫但以理。
> 但以理住在巴比伦。那是一座好大好大的城。
> 这里的国王叫大利乌。国王的事情太多了，忙都忙不过来！
> 所以，他找了一百二十个官员来帮忙，又找了三个总管，来管这些官员。
> 但以理就是三个总管里的一个。他做事特别认真，从来不说谎，也从来不偷懒。
> 国王心想：嗯，这个人真不错！我要让他来管整个国家！
> 可是，别的官员听了，心里酸溜溜的。
> 官员：凭什么是他？
> 他们天天盯着但以理，想抓他的错。盯啊盯，盯啊盯……一个错也抓不到！
> 官员：等等！他每天都向他的上帝祷告……有了！
