# Install or remove Warband Enchanting Rods

Download `WarbandEnchantingRods-1.0.0.zip` from
[Releases](https://github.com/pjw345/warband-enchanting-rods/releases/latest).
The automatic GitHub source ZIP does not contain the generated client patch.

## Compatibility

The server must include
[higher-tier rod validation](https://github.com/pjw345/tortoise-wow/pull/68)
(commit `2721b1957f80bd13146e1ffc11b4a0eea4d15bd1`) or equivalent behavior.
The client package alone cannot enable that server behavior.

This release is for one exact Vanilla/Turtle client archive set. The release
manifest records the executable and all archive content hashes. In particular,
the original `Spell.dbc` SHA-256 is:

```text
fbc0a5a2e51ffe1110d0d85e9a1f885a68c4b3b2695b7e83bfc26c478af3ff6a
```

The 173-field spell layout is different from WoW 3.3.5a. A client with different
files must use a newly built package. The installer checks compatibility before
copying files; identical copies work even if their paths or timestamps differ.
Hashing the original archive set can take a few minutes.

## Installation

1. Extract the ZIP outside your client folder. Keep the extracted package for
   removal later. Close WoW completely; `/reload` cannot reload MPQ data.
2. Open PowerShell in the extracted `WarbandEnchantingRods-1.0.0` folder.
3. Run the following with your own client path:

   ```powershell
   .\Install.ps1 -ClientPath 'C:\Games\TurtleWoW'
   ```

4. Start the game and enable **Warband Enchanting Rods** on the AddOns screen.
5. Open Enchanting, select a supported recipe and run `/werods`. It should
   report an active patch; the rod requirement should say “or higher”.
6. Carry a suitable rod in your bags and the recipe's normal reagents, then
   enchant an eligible item through the normal crafting interface.

The installer refuses running/unidentifiable clients, incompatible archives,
linked destination paths and existing patch/addon destinations. It never
overwrites the client's original MPQs. Do not force installation after a failed
compatibility check.

## Removal

Close WoW, then run from the same extracted package folder:

```powershell
.\Install.ps1 -ClientPath 'C:\Games\TurtleWoW' -Remove
```

The matching patch and addon are moved into your client's
`Archive\WarbandEnchantingRods-disabled-...` directory. Original client archives
remain unchanged. If you edited the addon or added files, automatic removal
refuses to discard them; preserve your changes and move those files manually.
Restart the client to restore the original exact-rod behavior.

## Client updates

Remove this patch before updating the client. A complete `Spell.dbc` override
could mask newer spell changes. After an update, generate or obtain a matching
package instead of reusing this one.

## Test coverage and reports

Normal Silver Rod / lower-tier enchanting was confirmed in live play on
25 October 2026. All 25 tier directions and the negative cases have offline
coverage; broader live tier and trade enchanting acceptance remains open.

For problems, open an issue in
[warband-enchanting-rods](https://github.com/pjw345/warband-enchanting-rods/issues)
with the recipe, carried rod, `/werods` result and exact error. Server validation
is tracked separately in
[tortoise-wow #67](https://github.com/pjw345/tortoise-wow/issues/67).
