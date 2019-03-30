DISASM_SMB = smbdis.asm
SMB_O = smbdis.o
ASM_SMB = smbdis.nes
MARIO_NES = mario.nes

$(ASM_SMB) : $(SMB_O)
	ld65 -t nes --cfg-path /usr/share/cc65/cfg/ -o $(ASM_SMB) $(SMB_O)

$(SMB_O) : $(DISASM_SMB)
	ca65 $(DISASM_SMB)

play : $(ASM_SMB)
	fceux $(ASM_SMB)

gg : $(ASM_SMB)
	cmp -l $(MARIO_NES) $(ASM_SMB) | python makegg.py
