---
name: voice-transcribe
description: Transcribe an audio file or a WhatsApp voice note into text, tuned for Urdu, Hindi and Roman Urdu speech. Use whenever the user sends or points at a voice note, mp3, opus, m4a or any recording and asks what was said, or when a WhatsApp message has no text because it is a voice note. Uses Cartesia STT for speed, falls back to local whisper.cpp when offline.
---

# voice-transcribe

Turns speech into text. Built for Urdu and Roman Urdu, which most models handle
badly, so read the accuracy note before you trust a transcript.

## Use it

```bash
~/.claude/skills/voice-transcribe/bin/hear <file>            # any audio file
~/.claude/skills/voice-transcribe/bin/hear <file> hi         # force a language
~/.claude/skills/voice-transcribe/bin/hear --wa <message_pk> # a WhatsApp voice note
```

`--wa` looks the media path up in WhatsApp's own database, so pair it with the
`whatsapp-read` skill: that skill gives you the message pk, this one reads it out.

## How it works

1. Converts to 16 kHz mono and evens out the level, because voice notes are often
   very quiet and that alone loses whole sentences.
2. Sends it to **Cartesia STT** (`ink-whisper`). A 32 second note takes about 3
   seconds.
3. Collapses repeated words. Whisper style models loop on a word dozens of times
   at the end of a clip, and that noise is not speech.

Key comes from `CARTESIA_API_KEY` in the environment, or `~/.cartesia_key`, or
`~/Desktop/Personal/beghumchat/wabot/.env`.

Offline or no key: `STT_ENGINE=local` uses `whisper-cli` with a model from
`~/.claude/skills/voice-transcribe/models/`. It is far slower, a 32 second clip
took over two minutes, and on Roman Urdu it was noticeably worse.

## Accuracy, read this before quoting anyone

Roman Urdu spoken casually is the hardest case. Names, numbers and place names come
out wrong often. Two rules:

- **Never present a shaky transcript as if it were certain.** If it reads like
  nonsense, say the voice note was not clear rather than guessing at it.
- **Never act on money, addresses or commitments** taken from a transcript alone.
  Confirm those with the person.

Language hint matters: `ur` suits Urdu and Roman Urdu, `hi` sometimes reads
Hindi leaning speech better, `en` for English. Try another when output looks off.
