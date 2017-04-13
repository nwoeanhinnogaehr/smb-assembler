# smb-assembler

This is a collection of scripts for messing around with the code of Nintendo's Super Mario Bros.

Anything not listed under sources/thanks below is released into the public domain and you can use it however you want.

## usage

Requires [cc65](http://cc65.github.io/cc65/) to assemble.

Modify `smbdis.asm`, then run `make play` (assumes fceux as an emulator, edit the makefile to change it).

Run `make gg` to get a list of Game Genie codes which you can enter into a real console to achieve the same modification.

`SMBRE.DIS` is provided as an alternate disassembly for reference purposes. It does not currently assemble.

## sources/thanks

- mario.nes is copyright Nintendo, view at your own risk.
- gamegenie.py by Jarhmander, from https://github.com/Jarhmander/gamegenie (MIT license)
- smbdis.asm by doppelganger, downloaded from romhacking.net
- SMBRE.DIS by F.H, downloaded from romhacking.net
