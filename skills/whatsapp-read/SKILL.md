---
name: whatsapp-read
description: Read WhatsApp Desktop messages, chats, reactions and media straight from the local database on macOS. Use whenever the user asks what someone said on WhatsApp, what a chat contains, who reacted to what, what is unanswered, or wants a message found or quoted. Read only, needs no window focus, and never sends anything.
---

# whatsapp-read

Reads WhatsApp Desktop's own SQLite store on macOS. Nothing is sent, no window is
brought forward, and WhatsApp keeps running while you read.

Database:
`~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite`

**Always open it read only**, otherwise you risk corrupting a live Core Data store:
```bash
DB="$HOME/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite"
sqlite3 "file:${DB}?mode=ro" "..."
```

## Ready made commands

```bash
~/.claude/skills/whatsapp-read/bin/wa chats            # recent chats with ids
~/.claude/skills/whatsapp-read/bin/wa find "luqmaan"   # find a chat by name
~/.claude/skills/whatsapp-read/bin/wa read <session> [n]   # last n messages
~/.claude/skills/whatsapp-read/bin/wa unread <session>     # what came after our last reply
~/.claude/skills/whatsapp-read/bin/wa reactions <session>  # who reacted with what
~/.claude/skills/whatsapp-read/bin/wa media <message_pk>   # path of an image, voice or doc
```

## Schema, the parts that matter

- `ZWACHATSESSION` one row per chat. `Z_PK` is the session id, `ZPARTNERNAME` the
  display name, `ZCONTACTJID` the address. Group jids end `@g.us`, one to one are
  `@lid` on newer builds and `@s.whatsapp.net` on older ones.
- `ZWAMESSAGE` one row per message. `ZCHATSESSION` links to the chat, `ZISFROMME`
  is 1 for our own, `ZTEXT` is the body, `ZSTANZAID` is the id WhatsApp itself uses.
- Timestamps are Apple epoch: `datetime(ZMESSAGEDATE+978307200,'unixepoch','localtime')`.
- `ZMESSAGETYPE`: 0 text, 1 image, 2 video, 3 voice or audio, 7 link, 8 document,
  11 gif, 13 and 15 sticker, 14 deleted, 10 call, 59 and 66 are system rows with
  nothing to read.
- In groups the sender is `ZWAGROUPMEMBER` joined on `ZGROUPMEMBER`, name in
  `ZCONTACTNAME`, address in `ZMEMBERJID`.
- Media lives under `~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/Message/`
  plus `ZWAMEDIAITEM.ZMEDIALOCALPATH`.

## Reactions are hidden in a protobuf blob

They are not a table. `ZWAMESSAGEINFO.ZRECEIPTINFO` is a protobuf blob, and field 7
holds the reaction list. Inside each entry: field 1 the reaction stanza id, field 2
the reactor's jid, field 3 the emoji, field 4 the time.
`bin/wa reactions` already parses this, do not go hunting for it again.

## Reading voice notes

A voice note (`ZMESSAGETYPE=3`) has no text. Transcribe it with the
`voice-transcribe` skill before answering anything about it. Never guess what a
voice note said, and if the transcript comes out garbled say so plainly.

## Care

- Read only. Writing a row into this database does **not** send anything: there is
  no outbox table, and the actual sending happens inside WhatsApp over an encrypted
  socket with the Signal session state kept in a separate `Axolotl.sqlite`.
- Chats can contain private matters. Quote only what the user asked about.
