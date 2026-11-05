<div align="center">

<img src="assets/banner.png" alt="Checkpoint Study Path: Your slides in. A game plan out." width="100%">

<h1>
  <img src="assets/flag.gif" height="40" alt="">
  Checkpoint Study Path
  <img src="assets/hero.gif" height="40" alt="">
</h1>

**Your slides in. A game plan out.** 🎮📚

An exam-prep skill for [Claude](https://claude.ai). Give it your lecture slides and it builds you<br>
a study plan, a level-by-level quiz path you clear one checkpoint at a time, and an optional cheat sheet.

<br>

<img src="https://img.shields.io/badge/Claude-Skill-FFA300?style=for-the-badge&labelColor=1D2B53" alt="Claude Skill">
<img src="https://img.shields.io/badge/license-MIT-00E436?style=for-the-badge&labelColor=1D2B53" alt="MIT license">
<img src="https://img.shields.io/badge/made%20for-students-29ADFF?style=for-the-badge&labelColor=1D2B53" alt="Made for students">
<img src="https://img.shields.io/badge/vibe-8--bit-FF77A8?style=for-the-badge&labelColor=1D2B53" alt="8-bit">
<a href="https://github.com/nicklukekurian-web/checkpoint-study-path/stargazers"><img src="https://img.shields.io/github/stars/nicklukekurian-web/checkpoint-study-path?style=for-the-badge&color=FFEC27&labelColor=1D2B53" alt="Stars"></a>

[🕹️ Install](#%EF%B8%8F-install) · [🗺️ How it works](#%EF%B8%8F-how-it-works) · [🏁 The Checkpoint Path](#-the-checkpoint-path) · [🎒 What you get](#-what-you-get) · [💬 Prompts](#-example-prompts) · [❓ FAQ](#-faq)

</div>

<img src="assets/divider.png" width="100%" alt="">

## 🕹️ Install

> **You need:** a Claude **Pro, Max, Team or Enterprise** plan, with **Code execution and file creation** turned on in **Settings → Capabilities**.

1. ⬇️ **Download** [`checkpoint-study-path.zip`](https://github.com/nicklukekurian-web/checkpoint-study-path/raw/main/dist/checkpoint-study-path.zip). Don't unzip it.
2. ⚙️ In Claude, open **Settings → Capabilities**, scroll to **Skills**, click **Upload skill** and pick the zip.
3. ✅ Make sure the skill's toggle is **on**.
4. 🚀 Start a new chat, attach your slides and say:

```text
Use the checkpoint-study-path skill for my Discrete Math final on Dec 12.
```

<!-- VIDEO: on github.com, edit this file, delete the demo.gif line below, and drag assets/checkpoint-study-path.mp4 into this spot to get the video player with sound. -->
<div align="center">
<img src="assets/demo.gif" alt="30-second 8-bit demo: drop in slides, get a plan, clear checkpoints, ace the exam" width="100%">
</div>

Re-reading slides *feels* like studying, but nothing sticks, and a week before the exam you still can't tell what you actually know. This skill turns the slides you already have into a game you play every day until the test.

- 📥 **It starts from *your* slides.** Claude reads every deck first, so the notation, examples and scope match what your professor actually teaches, not some random textbook.
- 🧮 **You get a real plan.** It works out the score you need on the final for the grade you want, then lays out every day until the exam.
- 🏁 **You clear checkpoints, not chapters.** One checkpoint per lecture deck. It only clears when you've answered *every* question right at least once.
- 🔁 **Missed questions come back.** Get one wrong and it returns three questions later, so you can't skip past what you don't know.
- 🧪 **Claude checks its own work.** Answer keys are verified by script, video links are checked, and the quiz app is tested end to end before you ever see it.

<img src="assets/divider.png" width="100%" alt="">

## 🗺️ How it works

<img src="assets/how-it-works.png" alt="Four steps: slides in, game plan, checkpoints, exam ready" width="100%">

| 🎮 | Step | What happens |
|:-:|---|---|
| <img src="assets/icons/slides.png" width="24" height="28" alt=""> | **1. Slides in** | Claude asks once for your exam date, format, question types, grade weights and materials. Then it reads every deck and maps which sections each one covers, flags where your professor differs from the textbook, and lists topics the slides skip (so they stay out of your quizzes). |
| <img src="assets/icons/doc.png" width="26" height="28" alt=""> | **2. Game plan** | A study plan doc: the score you need (formula + scenario table, computed by script), a weekly routine, a week-by-week timeline and a coverage tracker. |
| <img src="assets/icons/flag.png" width="26" height="28" alt=""> | **3. Checkpoints** | A quiz app published as a Claude artifact: one checkpoint per deck, in course order, each with short videos, a mini-lesson in your professor's notation, then 10–17 questions. |
| <img src="assets/icons/trophy.png" width="28" height="28" alt=""> | **4. Exam ready** | Mixed review keeps old checkpoints fresh, and an optional one-page cheat sheet follows a space budget per chapter. |

<img src="assets/divider.png" width="100%" alt="">

## 🏁 The Checkpoint Path

<img src="assets/mastery-loop.png" alt="Mastery loop: answer, wrong answers requeue 3 later, all right once clears the checkpoint and unlocks the next" width="100%">

<table>
<tr>
<td width="50%" valign="top">

### 🔓 Mastery gating
- A checkpoint clears only when **every** question has been answered correctly once.
- A wrong answer is **requeued 3 questions later**.
- Clearing a checkpoint **unlocks the next one** on the track.
- Catch-up material and new material can run as **separate tracks**.

</td>
<td width="50%" valign="top">

### 🎲 Mixed review
- **10 random questions** pulled from every checkpoint you've cleared.
- **Progress bars** for each checkpoint and the whole path.
- Progress is **saved in your browser**, so you can come back tomorrow.
- Optional **proof-writing practice** with a model answer and AI feedback.

</td>
</tr>
</table>

**Question types that match your real exam:**

| 🔘 Multiple choice | ☑️ Select all | 🔗 Match | 🔢 Order |
|:-:|:-:|:-:|:-:|
| one right answer | every correct option | pair left with right, plus distractors | put the steps in sequence |

Every answer comes with an explanation, **plus a note on why the tempting wrong option is wrong**. Questions taken straight from your slides are tagged with the deck they came from.

<img src="assets/divider.png" width="100%" alt="">

## 🎒 What you get

| 🎒 | Output | Inside |
|:-:|---|---|
| <img src="assets/icons/doc.png" width="26" height="28" alt=""> | **Study plan doc** | Score-needed formula and scenarios · weekly routine · timeline widget · coverage tracker with a stage dropdown (*Not started → Learned → Recalled once → Recalled again → On sheet*) · cheat-sheet space budget · open questions for the review session |
| <img src="assets/icons/flag-gold.png" width="26" height="28" alt=""> | **Checkpoint Path app** | Mastery-gated checkpoints · videos + mini-lessons · exam-style questions · mixed review · saved progress |
| <img src="assets/icons/card.png" width="41" height="28" alt=""> | **Cheat sheet** *(optional)* | One page, fixed type size, built from the plan's per-chapter space budget |
| <img src="assets/icons/book.png" width="36" height="28" alt=""> | **Extras** *(optional)* | Master study guide PDF · narrated video crash course with captions and chapters |

<details>
<summary>📸 <b>Peek at the storyboard</b> (8-bit illustrations from the demo video)</summary>
<br>
<img src="assets/storyboard.png" alt="Storyboard: chat with slides, study plan, a checkpoint question, mixed review" width="100%">
</details>

<img src="assets/divider.png" width="100%" alt="">

## 🛡️ Built-in checks

The skill tells Claude to **never skip** these:

| ✔️ | Check |
|:-:|---|
| <img src="assets/icons/check.png" width="26" height="22" alt=""> | Every number, answer key and worked example is checked **with a script**, and anything that fails is fixed before it ships. |
| <img src="assets/icons/check.png" width="26" height="22" alt=""> | Every video link is checked against **YouTube's oEmbed endpoint**, and its exact title and channel are used. No invented links. |
| <img src="assets/icons/check.png" width="26" height="22" alt=""> | The app is tested **end to end in a headless browser**: every question answered through the UI, every checkpoint cleared, mixed review run, no sideways scrolling at phone width. |
| <img src="assets/icons/check.png" width="26" height="22" alt=""> | When you upload new slides, the plan and checkpoints are **realigned** and Claude tells you what changed. |

<img src="assets/divider.png" width="100%" alt="">

## 💬 Example prompts

```text
Use the checkpoint-study-path skill for my Discrete Math final on Dec 12. Slides attached.
```
```text
The exam is 40 multiple choice + 2 proofs and I get a one-page cheat sheet. Build the path.
```
```text
I just uploaded Deck 7. Realign my plan and checkpoints.
```
```text
Make me the cheat sheet now.
```

> 💡 **Tip:** Answer each question *before* you read the explanation. Mastery gating only works if you actually try.

<img src="assets/divider.png" width="100%" alt="">

## ❓ FAQ

<details>
<summary><b>Does it work for any class?</b></summary>
<br>
It's built around lecture slides, so any course with slides or notes works. It shines when questions have clear right answers (math, CS, the sciences).
</details>

<details>
<summary><b>Is it free?</b></summary>
<br>
The skill is free and MIT-licensed. Skills in Claude need a Pro, Max, Team or Enterprise plan.
</details>

<details>
<summary><b>Where does my stuff end up?</b></summary>
<br>
The plan doc and the quiz app are artifacts in <i>your</i> Claude account. They stay private until you choose to share them.
</details>

<details>
<summary><b>Claude didn't use the skill. What now?</b></summary>
<br>
Check that the toggle is on under <b>Settings → Capabilities → Skills</b>, then name it in your message: <i>"Use the checkpoint-study-path skill for…"</i>
</details>

<details>
<summary><b>On a Team or Enterprise plan?</b></summary>
<br>
On Enterprise, an owner has to turn on code execution and Skills in admin settings first. Skills you upload are private to your own account.
</details>

<img src="assets/divider.png" width="100%" alt="">

## 🤝 Use it responsibly

- 📄 **Use your own materials.** Don't publish a generated checkpoint that copies your professor's slides or examples unless your school's policy and your professor allow it.
- 🔍 **Spot-check before the exam.** The skill verifies its answer keys, but compare against your slides and textbook too.
- 🧠 **It's a study aid, not a shortcut.** The point is that *you* can answer every question.

## 📁 Repo layout

```
checkpoint-study-path/
├── README.md
├── LICENSE
├── dist/
│   └── checkpoint-study-path.zip     ← upload this to Claude
├── skills/
│   └── checkpoint-study-path/
│       └── SKILL.md                  ← the skill itself
├── assets/                           ← banner, diagrams, icons, demo video
└── tools/
    └── pixel-video/                  ← Python that draws the art + video
```

🎨 Every image and the demo video are drawn in code: Python + Pillow for the pixels, numpy for the chiptune. See [`tools/pixel-video`](tools/pixel-video).

## 🌟 Contributing

Ideas welcome: new question types, other subjects, better pacing rules. Open an issue or a PR. If the skill helped you clear a checkpoint, a ⭐ helps other students find it.

## 📜 License & credits

MIT. See [LICENSE](LICENSE).<br>
Fonts: [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) by CodeMan38 and [Silkscreen](https://fonts.google.com/specimen/Silkscreen) by Jason Kottke, both under the SIL Open Font License. Palette inspired by the PICO-8 fantasy console.

<div align="center">
<br>
<img src="assets/star.gif" height="28" alt=""> &nbsp; Built by <a href="https://github.com/nicklukekurian-web">@nicklukekurian-web</a> &nbsp; <img src="assets/star.gif" height="28" alt="">
<br><br>
<img src="assets/divider.png" width="100%" alt="">
</div>
