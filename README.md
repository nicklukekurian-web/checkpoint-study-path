# Checkpoint Study Path

A [Claude](https://claude.ai) skill that turns your own course slides into an exam prep system:

1. **A study plan doc.** It computes the exam score you need for your target grade, lays out a week-by-week timeline, and includes a coverage tracker.
2. **A Checkpoint Path quiz app.** It's mastery-gated: one checkpoint per lecture deck, each with a short lesson and 10-17 questions. A checkpoint clears only when every question has been answered correctly once, and missed questions come back a few questions later.
3. **An optional cheat sheet** with a per-chapter space budget, if your exam allows one.

Everything is built from *your* slides, so the scope, notation and methods match what your professor actually teaches.

## How it works

| Step | What happens |
|---|---|
| Gather | Claude asks once for the exam date, format, question types, grade weights and your materials |
| Map coverage | It reads every deck, notes where the professor differs from the textbook, and lists topics the slides skip |
| Plan doc | Required-score formula and scenario table, weekly routine, timeline, coverage tracker |
| Checkpoint Path | Mastery-gated quiz app with exam-matching question types (multiple choice, select-all, matching, ordering) |
| Verify | Answer keys are checked by script, video links are checked against YouTube's oEmbed endpoint, and the app is tested end to end in a headless browser |

### Quiz app features

- Checkpoints unlock in course order
- Wrong answers are requeued 3 questions later
- Mixed review draws 10 random questions from cleared checkpoints
- Explanations on every answer, including notes on the tempting wrong options
- Progress saved in the browser (localStorage)
- Optional writing practice for proofs

## Install

This is a skill for Claude. It needs Claude's document and artifact tools (Claude Docs, published artifacts, the file and shell tools), so it won't run as a standalone script.

1. Download or clone this repo.
2. Add the `skills/checkpoint-study-path/` folder as a skill in Claude (Settings, then Capabilities/Skills, then upload the folder or its `SKILL.md`; the exact menu names may differ by plan and app version).
3. In a chat, say "use the checkpoint-study-path skill for [course]" and attach your slides, or type `/checkpoint-study-path`.

## Using it responsibly

- **Use your own materials.** The quizzes are generated from the slides you give it. Don't publish a generated checkpoint that copies your professor's lecture examples or slides unless your school's policy and your professor allow it.
- **Check the output.** The skill verifies answer keys by script, but you should still spot-check against your slides and textbook before an exam.
- **It's a study aid, not a shortcut.** Mastery gating only works if you try each question before reading the explanation.

## Repo layout

```
checkpoint-study-path/
├── README.md
├── LICENSE
└── skills/
    └── checkpoint-study-path/
        └── SKILL.md
```

## Contributing

Ideas welcome: new question types, other subjects, better pacing rules. Open an issue or a PR.

## License

MIT. See [LICENSE](LICENSE).
