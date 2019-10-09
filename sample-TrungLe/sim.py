# Author: Trung Le
# Supported instrs: 
# addi, sub, beq, ori, sw



def sim(program):
    finished = False      # Is the simulation finished? 
    PC = 0                # Program Counter
    register = [0] * 32   # Let's initialize 32 empty registers
    mem = [0] * 12288     # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
                          # But my machine has 16GB of RAM, its ok :)
    DIC = 0               # Dynamic Instr Count
    high = register[30]
    low = register[31]
    while(not(finished)):
        if PC == len(program) - 4: 
            finished = True
        fetch = program[PC]
        DIC += 1
        #print(hex(int(fetch,2)), PC)
        if fetch[0:6] == '000000' and fetch[21:32] == '00000100000': # ADD
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] + register[t]

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100001': # ADDU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] + register[t]

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100011': # SUBU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] - register[t]

        elif fetch[0:6] == '001001': # ADDIU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] + imm

        elif fetch[0:6] == '001000': # ADDI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            register[t] = register[s] + imm
            
        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100010': # SUB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] - register[t]

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000011000': # MULT
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            low = register[s] * register[t]
            
        elif fetch[0:6] == '000000' and fetch[21:32] == '00000011001': # MULTU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            low = register[s] * register[t]
           
        elif fetch[0:6] == '000000' and fetch[21:32] == '00000010000': # MFHI
            PC += 4
            d = int(fetch[16:21],2)
            register[d] = high

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000010010': # MFLO
            PC += 4
            d = int(fetch[16:21],2)
            register[d] = low

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000011010': # DIV
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            low = register[s] / register[t]
            high = register[s] % register[t]
            
        elif fetch[0:6] == '000000' and fetch[21:32] == '00000011011': # DIVU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            low = register[s] / register[t]
            high = register[s] % register[t]
            
        elif fetch[0:6] == '000100':  # BEQ
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            # Compare the registers and decide if jumping or not
            if register[s] == register[t]:
                PC += imm*4
        
        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100100': # AND
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = (register[s] & register[t])
        
        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100101': # OR
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] | register[t]

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100111': # NOR
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = ~(register[s] | register[t])

        elif fetch[0:6] == '000000' and fetch[26:32] == '100110': # XOR
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] ^ register[t]

        elif fetch[0:6] == '001100': # ANDI
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] & imm
            
        elif fetch[0:6] == '001101':   # ORI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] | imm

        elif fetch[0:6] == '001110': # XORI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] ^ imm

        elif fetch[0:6] == '000000' and fetch[26:32] == '000000': # SLL
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            h = int(fetch[21:26],2)
            register[d] = register[t] << h   

        elif fetch[0:6] == '000000' and fetch[26:32] == '000010': # SRL
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            h = int(fetch[21:26],2)
            register[d] = register[t] >> h

        elif fetch[0:6] == '000000' and fetch[26:32] == '000011': # SRA
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            h = int(fetch[21:26],2)
            register[d] = register[t] >> h

        elif fetch[0:6] == '000000' and fetch[26:32] == '000100': # SLLV
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[t] << register[s]

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000000110': # SRLV
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[t] >> register[s]

        elif fetch[0:6] == '000000' and fetch[26:32] == '000111': # SRAV
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[t] >> register[s]

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000101010': # SLT
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            if register[s] < register[t]:
                register[d] = 1
            else:
                register[d] = 0

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000101011': # SLTU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            if register[s] < register[t]:
                register[d] = 1
            else:
                register[d] = 0

        elif fetch[0:6] == '001010': # SLTI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            if register[s] < imm:
                register[t] = 1
            else:
                register[t] = 0

        elif fetch[0:6] == '001011': # SLTIU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            if register[s] < imm:
                register[t] = 1
            else:
                register[t] = 0
        
        elif fetch[0:6] == '001111': # LUI
            PC += 4
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = imm << 16

        elif fetch[0:6] == '100000': # LB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            register[t] = mem[offset]

        elif fetch[0:6] == '100100': # LBU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = int(fetch[16:],2)
            offset = offset + register[s]
            andbyte = 0xFF
            register[t] = (mem[offset]  & andbyte)

        elif fetch[0:6] == '100001': # LH
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            register[t] = mem[offset]

        elif fetch[0:6] == '100101': # LHU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = int(fetch[16:],2)
            offset = offset + register[s]
            andbyte = 0xFFFF
            register[t] = (mem[offset]  & andbyte)

        elif fetch[0:6] == '100011': # LW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            register[t] = mem[offset]

        elif fetch[0:6] == '101000': # SB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            mem[offset] = register[t]

        elif fetch[0:6] == '101001': # SH
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            mem[offset] = register[t]

        elif fetch[0:6] == '101011':  # SW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            mem[offset] = register[t]

        else:
            # This is not implemented on purpose
            print('Not implemented')

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***')
    print('Registers $8 - $23 ', register[6:24])
    print('Dynamic Instr Count ', DIC)
    print('Memory contents 0x2000 - 0x2050 ', mem[8192:8272])




def main():
    file = open('prog.asm')
    program = []
    for line in file:
        
        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)
        if line[0] == '\n':
            continue
        line = line.replace('\n','')
        instr = line[2:]
        instr = int(instr,16)
        instr = format(instr,'032b')
        program.append(instr)       # since PC increment by 4 every cycle,
        program.append(0)           # let's align the program code by every
        program.append(0)           # 4 lines
        program.append(0)

    # We SHALL start the simulation! 
    sim(program)     

if __name__ == '__main__':
    main()
