smbdis.nes : smbdis.o
	ld65 -t nes --cfg-path /usr/share/cc65/cfg/ -o smbdis.nes smbdis.o

smbdis.o : smbdis.asm
	ca65 smbdis.asm

play : smbdis.nes
	fceux smbdis.nes

gg : smbdis.nes
	cmp -l mario.nes smbdis.nes | python makegg.py
