# Source and provenance

This standalone project was extracted using `git subtree split` from
`tools/client-enchanting-rods/` in
https://github.com/pjw345/tortoise-wow at commit
`1dd1ec07` (branch `codex/enchanting-rod-client-patch`, PR #80).
Its three original source commits are retained, with their subtree commit IDs.
The AGPL-3.0 license from that repository is retained in `LICENSE` and applies
to this project's source. Generated game-data release assets are not covered by
an additional ownership claim from this project.

The client compatibility work complements server commit
`2721b1957f80bd13146e1ffc11b4a0eea4d15bd1` in
https://github.com/pjw345/tortoise-wow/pull/68. This repository does not contain
a replacement server implementation or a complete game client.

Generated MPQs, DBCs, recipe tables and installation packages are kept out of
Git. Release ZIPs include the exact generated patch and matching recipe table,
installer, manifest, source link and removal instructions.
