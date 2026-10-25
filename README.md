# Warband Enchanting Rods

Use a higher-tier runed enchanting rod for recipes requiring a lower-tier rod
on a compatible Turtle private server. This repository contains the companion
addon, client patch builder, installer, rollback and tests.

**[Download the installation ZIP from Releases](https://github.com/pjw345/warband-enchanting-rods/releases/latest)**.
Choose `WarbandEnchantingRods-1.0.0.zip`, not GitHub's automatically generated
source ZIP: the installation package includes the matching MPQ and generated
recipe data.

## Requirements

- A server with the higher-rod validation from
  [tortoise-wow PR #68](https://github.com/pjw345/tortoise-wow/pull/68), commit
  `2721b1957f80bd13146e1ffc11b4a0eea4d15bd1`, or an equivalent implementation.
- The matching Vanilla/Turtle client data described in the release manifest.
  This patch uses the 173-field `Spell.dbc` layout and is not a WoW 3.3.5a patch.
- Windows PowerShell for the provided installer. End users do not need Python,
  Lua or StormLib to install the prepared release.

The server change and this client package are both required. Installing only the
addon cannot remove the client's exact-item cast rejection. The server continues
to validate the actual rod, skill, target and consumed reagents.

## Install

1. Extract the release ZIP outside the client folder and close WoW completely.
2. Open PowerShell in the extracted `WarbandEnchantingRods-1.0.0` folder and run,
   substituting your actual client path:

   ```powershell
   .\Install.ps1 -ClientPath 'C:\Games\TurtleWoW'
   ```

3. Start WoW and enable **Warband Enchanting Rods** on the AddOns screen.
4. Open Enchanting, select a recipe and run `/werods` to check patch status.

The installer checks file content, not machine-specific paths or timestamps.
It deliberately rejects different client files, additional MPQs and existing
destinations. A different client needs a separately generated package; do not
bypass these checks. The initial identity check hashes the original client
archives, which can take a few minutes.

**[Installation, removal and client updates](docs/INSTALL.md)**

## What is included

- `patch-Z.MPQ`: an override changing only supported runed-rod tool fields in
  the matching client's spell data.
- `WarbandEnchantingRods`: restores “Runed Copper Rod (or higher)” style
  requirements, checks carried bags and delegates crafting to the native API.
- `Install.ps1` and `manifest.json`: content checks and reversible removal.

The accepted payload preserves all 27,916 spell rows, strings and unrelated
fields. It changes 344 bytes across 172 Enchanting recipes. Consumed reagents
are unchanged. Original MPQs, executables and DLLs are not overwritten.

## Validation

On 25 October 2026, the installed patch and addon were confirmed working in
normal play for the reported Silver Rod / lower-tier enchant case. This does
not claim live coverage of every tier, trade enchanting or every negative case.

Python fixture tests cover byte preservation, unrelated tools, consumed reagents,
invalid data and generated recipe aliases. Lua 5.0 tests cover all 25 rod-tier
combinations, carried/bank-only/missing rods, native forwarding and original
client fallback. Installer fixtures cover copies with different timestamps,
same-size content changes, installation, rollback and existing/modified files.

## Build and contribute

See **[BUILD.md](docs/BUILD.md)** for tooling, dependencies and tests.
Generated game data and MPQs are release assets, not tracked source files.

The source was extracted with its three original commits from
`tools/client-enchanting-rods/` in
[tortoise-wow PR #80](https://github.com/pjw345/tortoise-wow/pull/80).
See [SOURCE.md](SOURCE.md) for provenance and the retained AGPL-3.0 license.
Server behavior remains tracked in
[tortoise-wow issue #67](https://github.com/pjw345/tortoise-wow/issues/67).
