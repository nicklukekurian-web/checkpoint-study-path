---
name: "checkpoint-study-path"
description: "Use when a student wants an exam prep system for a course: a study plan doc, a mastery-gated Checkpoint Path quiz app built from their slides, and an optional cheat sheet."
---

# Checkpoint study path

Build an exam prep system from the student's own course materials. The student's slides are the source of truth for scope, notation and methods.

## 1. Gather first (ask once, with AskUserQuestion)

- Course name, professor, exam date and location.
- Exam format: number of questions, time limit, question types (multiple choice, select-all, matching, ordering, free response), and whether a cheat sheet is allowed and its size.
- Sections or chapters covered, and whether the exam is cumulative.
- Grade weights, scores so far, and the target grade.
- Materials: lecture slides, review sheets, old homework. Read every deck before planning.

## 2. Map coverage from the slides

- List each deck and the sections its title slide names.
- Note where the professor differs from the textbook (definitions, notation, algorithm variants, conventions such as whether N includes 0).
- List textbook topics the slides skip; leave them out of the quizzes and tell the student.

## 3. Study plan doc (Claude Docs)

- Lead: the exam score needed for the target grade, with the formula and a table of scenarios. Compute it by script.
- Weekly routine: short weekday sessions (recall, one problem in the exam's format, one cheat-sheet line) plus one weekly review block.
- Week-by-week timeline to the exam date, drawn as a widget.
- Coverage tracker table: section, deck, planned week, and a Stage dropdown (Not started, Learned, Recalled once, Recalled again, On sheet).
- If a cheat sheet is allowed: a space budget per chapter, drawn as a page map, plus build rules.
- Open questions to confirm at the review session.

## 4. Checkpoint Path app (published artifact)

- One checkpoint per section or slide deck, in course order. Use tracks when there is catch-up material and new material.
- Each checkpoint: 2 to 4 videos, a short lesson in the professor's notation using his examples, then 10 to 17 questions.
- Question types matching the exam: mc (default), multi {correct:[...]}, match {pairs:[[left,right]], extra:[distractors]}, order {items in correct order}. Tag questions copied from slides with the deck name.
- Explanations on every answer, plus notes on the tempting wrong options.
- Mastery: a checkpoint clears when every question has been answered correctly once; a wrong answer is requeued 3 questions later. The next checkpoint in the track then unlocks.
- Mixed review: 10 random questions from cleared checkpoints. Progress bars.
- Optional writing practice for proofs: prompt, model answer, and AI feedback through the sample capability.
- Progress in localStorage, every access wrapped in try/catch.

## 5. Optional extras

- One-page cheat sheet as a PDF at a fixed type size, following the plan's space budget.
- Master study guide PDF.
- Narrated video crash course (TTS narration, rendered frames, captions, chapters), kept under the send-size limit.

## Verification rules (never skip)

- Check every number, answer key and worked example with a script; fix anything that fails before it ships.
- Check every video link with YouTube's oEmbed endpoint via WebFetch and use the exact title and channel it returns. Never invent a link or ID. Delegate the search to a subagent when there are many.
- Test the app end to end in headless Chromium: answer every question correctly through the UI, confirm every checkpoint clears and the mixed review runs, and check there is no horizontal scroll at 400 px.
- When the student uploads new slides, realign the plan doc and the checkpoints to them and say what changed.
