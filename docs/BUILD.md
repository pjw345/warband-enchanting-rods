# Build a package for a matching client

End users should download a prepared release. These steps are for maintainers
generating a package from their own compatible client data.

## Design

Wrath 3.3.5 has spell tool categories; the Vanilla/Turtle 173-field spell layout
does not. The builder selects only Enchanting skill-line 333 spells and clears
known runed-rod tool fields. All other fields, strings, skills, native formats,
ordinary reagents and unrelated tools are preserved and audited byte by byte.
The addon restores the rod display and carried-bag check, then calls native
`DoCraft` with its original arguments. The server remains authoritative.

## Dependencies

- Python 3.10+ and `mpyq==0.2.5` (`python -m pip install -r requirements.txt`).
- Official [StormLib](https://github.com/ladislav-zezula/StormLib), v9.25 commit
  `28c9b4be3f23c6b3a5ff55cacac7dbe5b9cdc4fc`, built as a shared library.
- Lua 5.0.3 for the client-runtime tests; Windows PowerShell for installer tests.

The published MPQ was packed and read back with the Linux StormLib shared
library. For that workflow, generate a candidate on the client machine, copy
the candidate to the Linux build host for packing, then copy it back for the
independent client-side audit. Paths below are examples; use an output folder
outside the installed client. The builder rejects existing destinations.

## Generate and verify

Remove this patch from the input client first. Do not generate from an already
patched spell table, and do not change installed client files while it runs.

```text
python build_patch.py --client C:/Games/TurtleWoW --output C:/Build/rod-candidate
```

Pack the copied candidate on the StormLib build host:

```text
python pack_mpq.py --stormlib /path/to/libstorm.so --candidate /path/to/rod-candidate
```

Return the packed `Data/patch-Z.MPQ` and updated `manifest.json` to the original
candidate folder, then independently verify it against the original client:

```text
python finalize_release.py --candidate C:/Build/rod-candidate
```

This audit checks every output byte and generated recipe alias, a classic MPQ
header and an independent `mpyq` extraction. It never installs the candidate.

```text
python -m unittest discover -s . -p test_patch.py -v
/path/to/lua-5.0.3/bin/lua test_rods.lua . /path/to/rod-candidate/Interface/AddOns/WarbandEnchantingRods/Recipes.lua
```

On Windows, test the real prepared payload against isolated fake client files:

```powershell
.\test_installer.ps1 -Candidate 'C:\Build\rod-candidate'
```

Package only the allowlisted installer, manifest, MPQ, addon, documentation and
license. Raw DBCs and development receipts stay outside the ZIP:

```text
python package_release.py --candidate C:/Build/rod-candidate --output C:/Build/WarbandEnchantingRods-1.0.0.zip
```

The packager strips the local client path and writes an adjacent SHA-256
checksum file. A rebuilt package needs its own live startup/enchanting checks;
the accepted release does not establish compatibility with another client.
