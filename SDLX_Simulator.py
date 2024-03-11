import tkinter as tk
from tkinter import *
from tkinter import CENTER, messagebox
import csv

import pandas as pd
import numpy as np

# root=tk.Tk()

# root.geometry("800x500")
# root.mainloop()


class MyGUI:

    def __init__(self):

        self.root = tk.Tk()

        self.label = tk.Label(
            self.root, text="SDLX Simulator", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)

        self.textbox = tk.Text(self.root, height=5, font=('Arial', 16))
        # self.textbox.set("Hellooo")
        # text = tk.StringVar()
        # text.set("This is the default text")
        # self.textbox.Entry(self.root, textvariable=text)
        self.textbox.pack(padx=10, pady=10)

        # text = tk.StringVar()
        # text.set("This is the default text")
        # textBox = tk.Entry(self.root, textvariable = text, font=('Arial', 16))
        # # self.textbox.pack(padx=10, pady=10)
        
        # textBox.pack()



        # self.button = tk.Button(self.root, text= "Start!", font=('Arial', 18), command=self.print)
        self.button = tk.Button(self.root, text="Run!", font=('Arial', 18), command=self.mainFunc)
        self.button.pack(padx=10, pady=10)

        self.root.mainloop()

    # def twos_comp(val, bits):
    #     # """compute the 2's complement of int value val"""
    #     if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
    #         val = val - (1 << bits)        # compute negative value
    #     return val  
    
    def mainFunc(self):

        # making reg file (initialize all values in registers to 0)
        Register_no = []
        Register_value_d = []
        Register_value_b = []
        reg_file_dictionary = {"Register" : Register_no, "Decimal" : Register_value_d, "Binary" : Register_value_b}

        for i in range(32):
            Register_no.append(f"R{i}")

        for i in range(32):
            Register_value_d.append(0)
            

        for i in range(32):
            Register_value_b.append('0b{:032b}'.format(Register_value_d[i]%(1<<32)))

        Reg_file = pd.DataFrame(reg_file_dictionary)

        # making memory (initializing all values to 0)
        memory_adress = []
        memory_value_d = []
        memory_value_b = []
        memory_dictionary = {"Memory Adress": memory_adress, "Decimal": memory_value_d, "Binary": memory_value_b}

        for i in range(0,37,4):
            memory_adress.append('0x{:08x}'.format(i))
            
        for i in range(10):
            memory_value_d.append(0)

        for i in range(10):
            memory_value_b.append('0b{:032b}'.format(memory_value_d[i]%(1<<32)))
        
        Memory = pd.DataFrame(memory_dictionary)

        PC=0

        flag=0

        new_PC=0

        data = pd.read_csv('t1.csv', dtype=str)
        array = data.to_numpy()
        array.reshape(-1,1)
        result =array.flatten()
        result

        Instruction_array=result

        # Instruction_array = ["00000100101001010000000000000101", "00000100101001010000000000000100", "01100100000001010000000000000100", "01011000000000110000000000000100", "01000100101011010000000011111111", "01001000000010100000000000000111"]
        # Instruction_array = ["00000100101001010000000000000100", "01100100000001010000000000000100", "01011000000000110000000000000100", "01000100101011010000000011111111", "01001000000010100000000000000111"]
        
        while(PC<len(Instruction_array)):
            instruction = Instruction_array[PC]
            if (instruction[:6] == '000000'): #R Type Instructions
                
                RS1 = instruction[6:11]
                RS2 = instruction[11:16]
                RD = instruction[16:21]
                    
                if (instruction[-6:] == '000000'): #ADD Instruction
                    answer = Register_value_d[int(RS1,2)]+Register_value_d[int(RS2,2)]
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
                if (instruction[-6:] == '000001'): #SUB Instruction
                    answer = Register_value_d[int(RS1,2)]-Register_value_d[int(RS2,2)]
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
                if (instruction[-6:] == '000010'): #AND Instruction
                    answer = Register_value_d[int(RS1,2)]&Register_value_d[int(RS2,2)]
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                
                
                if (instruction[-6:] == '000011'): #OR Instruction
                    answer = Register_value_d[int(RS1,2)]|Register_value_d[int(RS2,2)]
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
                if (instruction[-6:] == '000100'): #XOR Instruction
                    answer = Register_value_d[int(RS1,2)]^Register_value_d[int(RS2,2)]
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                
                if (instruction[-6:] == '000101'): #SLL Instruction
                    answer = Register_value_d[int(RS1,2)]<<Register_value_d[int(RS2,2)]
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
                if (instruction[-6:] == '000110'): #SRL Instruction
                    answer = Register_value_d[int(RS1,2)]>>Register_value_d[int(RS2,2)]
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
            
                
                if (instruction[-6:] == '001000'): #SLT Instruction
                    if (Register_value_d[int(RS1,2)]<Register_value_d[int(RS2,2)]):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                
                if (instruction[-6:] == '001001'): #SGT Instruction
                    if (Register_value_d[int(RS1,2)]>Register_value_d[int(RS2,2)]):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
                if (instruction[-6:] == '001010'): #SLE Instruction
                    if (Register_value_d[int(RS1,2)]<=Register_value_d[int(RS2,2)]):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
                if (instruction[-6:] == '001011'): #SGE Instruction
                    if (Register_value_d[int(RS1,2)]>=Register_value_d[int(RS2,2)]):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
                if (instruction[-6:] == '001100'): #ULT Instruction
                    
                    a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
                    b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2) 
                    if (a<b):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
                if (instruction[-6:] == '001101'): #UGT Instruction
                    
                    a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
                    b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2) 
                    if (a>b):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
                if (instruction[-6:] == '001110'): #ULE Instruction
                    
                    a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
                    b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2) 
                    if (a<=b):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
                if (instruction[-6:] == '001111'): #UGE Instruction
                    
                    a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
                    b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2) 
                    if (a>=b):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                    
                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    
            else:
                if (instruction[:6] == '000001'): #ADDI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    answer = Register_value_d[int(RS1,2)] + IMM_value
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '000010'): #SUBI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    answer = Register_value_d[int(RS1,2)] - IMM_value
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '000011'): #ORI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    answer = Register_value_d[int(RS1,2)] | IMM_value
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                
                if (instruction[:6] == '000100'): #ANDI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    answer = Register_value_d[int(RS1,2)] & IMM_value
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '000101'): #XORI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    answer = Register_value_d[int(RS1,2)] ^ IMM_value
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '000110'): #SLLI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    answer = Register_value_d[int(RS1,2)] << IMM_value
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '000111'): #SRLI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    answer = Register_value_d[int(RS1,2)] >> IMM_value
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                
                if (instruction[:6] == '001001'): #SLTI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    if (Register_value_d[int(RS1,2)] < IMM_value):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '001010'): #SGTI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    if (Register_value_d[int(RS1,2)] > IMM_value):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
            

                if (instruction[:6] == '001011'): #SLEI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    if (Register_value_d[int(RS1,2)] <= IMM_value):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '001100'): #SGEI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    if (Register_value_d[int(RS1,2)] >= IMM_value):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '001101'): #ULTI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2) 
                    if (Register_value_d[int(RS1,2)] < IMM_UNS):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '001110'): #UGTI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2) 
                    if (Register_value_d[int(RS1,2)] > IMM_UNS):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                
                if (instruction[:6] == '001111'): #ULEI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2) 
                    if (Register_value_d[int(RS1,2)] <= IMM_UNS):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '010000'): #UGEI
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2) 
                    if (Register_value_d[int(RS1,2)] >= IMM_UNS):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                
                if (instruction[:6] == '010001'): #LHI (to be completed)
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2) 
                    if (Register_value_d[int(RS1,2)] <= IMM_UNS):
                        answer = (2**32)-1
                    else:
                        answer = 0
                    Register_value_d[int(RD,2)] = answer
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0



                if (instruction[:6] == '010010'): #LB
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    adress = Register_value_d[int(RS1,2)]+IMM_value
                    mem_line = (adress//4)*4
                    within_adress = adress-mem_line
                    #string = Memory.iloc[mem_line/4]["Binary"][2:34]
                    string = memory_value_b[adress//4]
                    print(string)
                    value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+8+2]
                    value_required = twos_comp(int(value_required_bin_string,2), len(value_required_bin_string))
                    Register_value_d[int(RD,2)] = value_required
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '010011'): #LBU
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    adress = Register_value_d[int(RS1,2)]+IMM_value
                    mem_line = (adress//4)*4
                    within_adress = adress-mem_line
                    #string = Memory.iloc[mem_line/4]["Binary"][2:34]
                    string = memory_value_b[adress//4]
                    value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+8+2]
                    value_required = int(value_required_bin_string,2)
                    Register_value_d[int(RD,2)] = value_required
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                
                if (instruction[:6] == '010100'): #LH
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    adress = Register_value_d[int(RS1,2)]+IMM_value
                    mem_line = (adress//4)*4
                    within_adress = adress-mem_line
                    #string = Memory.iloc[mem_line/4]["Binary"][2:34]
                    string = memory_value_b[adress//4]
                    if (within_adress == 1 | within_adress == 3):
                        print("Memory not accessable")
                    value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+16+2]
                    value_required = twos_comp(int(value_required_bin_string,2), len(value_required_bin_string))
                    Register_value_d[int(RD,2)] = value_required
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '010101'): #LHU
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    adress = Register_value_d[int(RS1,2)]+IMM_value
                    mem_line = (adress//4)*4
                    within_adress = adress-mem_line
                    #string = Memory.iloc[mem_line/4]["Binary"][2:34]
                    string = memory_value_b[adress//4]
                    if (within_adress == 1 | within_adress == 3):
                        print("Memory not accessable")
                    value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+16+2]
                    value_required = int(value_required_bin_string,2)
                    Register_value_d[int(RD,2)] = value_required
                    Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '010110'): #LW (Loads the whole 4 bytes; Load byte and Load byte unsigned is litte more complicated)
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    adress = Register_value_d[int(RS1,2)]+IMM_value
                    #value_required_bin_string = Memory.iloc[adress/4]["Binary"][2:34]
                    value_required_bin_string = memory_value_b[adress//4]
                    value_required = int(value_required_bin_string,2)
                    Register_value_d[int(RD,2)] = value_required
                    Register_value_b[int(RD,2)] = value_required_bin_string

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                    #mem_adress = '0x{:08x}'.format(adress)
                    #value = Memory[Memory["Memory Adress"] == mem_adress]["Decimal"].iloc[0]
                    #Register_value_d[int(RD,2)] = value
                    #Register_value_b[int(RD,2)] = '0b{:032b}'.format(value%(1<<32))
                
                if (instruction[:6] == '010111'): #SB
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    adress = Register_value_d[int(RS1,2)]+IMM_value
                    mem_line = (adress//4)*4
                    within_adress = adress-mem_line
                    #string = Reg_file.iloc[int(RD,2)]["Binary"][2:34]
                    string = Register_value_b[int(RD,2)]
                    value_required_bin_string = string[-8:]

                    if (within_adress == 0):
                        req_string = value_required_bin_string+'{:024}'.format(0)
                    if (within_adress == 1):
                        req_string = '{:008}'.format(0)+value_required_bin_string+'{:016}'.format(0)
                    if (within_adress == 2):
                        req_string = '{:016}'.format(0)+value_required_bin_string+'{:008}'.format(0)
                    if (within_adress == 3):
                        req_string = '{:024}'.format(0)+value_required_bin_string

                    req_value = twos_comp(int(req_string,2), len(req_string))

                    memory_value_d[(adress//4)] = req_value
                    memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0
                
                if (instruction[:6] == '011000'): #SH
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    adress = Register_value_d[int(RS1,2)]+IMM_value
                    mem_line = (adress//4)*4
                    within_adress = adress-mem_line
                    #string = Reg_file.iloc[int(RD,2)]["Binary"][2:34]
                    string = Register_value_b[int(RD,2)]
                    value_required_bin_string = string[-16:]

                    if (within_adress == 1 | within_adress == 3):
                        print("Memory not accessable")

                    if (within_adress == 0):
                        req_string = value_required_bin_string+'{:024}'.format(0)

                    if (within_adress == 2):
                        req_string = '{:016}'.format(0)+value_required_bin_string+'{:008}'.format(0)


                    req_value = twos_comp(int(req_string,2), len(req_string))

                    memory_value_d[(adress//4)] = req_value
                    memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0

                if (instruction[:6] == '011001'): #SW
                    RS1 = instruction[6:11]
                    RD = instruction[11:16]
                    IMM = instruction[16:32]
                    IMM_value = twos_comp(int(IMM,2), len(IMM))
                    adress = Register_value_d[int(RS1,2)]+IMM_value
                    mem_line = (adress//4)*4
                    within_adress = adress-mem_line
                    string = Register_value_b[int(RD,2)]


                    if (within_adress == 1 | within_adress == 3 | within_adress ==2):
                        print("Memory not accessable")

                    if (within_adress == 0):
                        req_string = string


                    req_value = twos_comp(int(req_string,2), len(req_string))
                    

                    memory_value_d[adress//4] = req_value
                    memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

                    if (flag == 0):
                        PC +=1
                    else:
                        PC = new_PC
                        flag = 0


                if (instruction[:6] == '011010'): #BEQZ
                    RS1 = instruction[6:11]
                    SO_string = instruction[16:32]
                    SO_value = twos_comp(int(SO_string,2), len(SO_string))
                    
                    if (Register_value_d[int(RS1,2)] == 0):
                        new_PC = PC+SO_value
                        flag = 1
                        PC += 1
                    else:
                        PC += 1
                
                if (instruction[:6] == '011011'): #BNEZ
                    RS1 = instruction[6:11]
                    SO_string = instruction[16:32]
                    SO_value = twos_comp(int(SO_string,2), len(SO_string))
                    
                    if (Register_value_d[int(RS1,2)] != 0):
                        new_PC = PC+SO_value
                        flag = 1
                        PC += 1
                    else:
                        PC += 1
                        
                if (instruction[:6] == '011100'): #JR
                    RS1 = instruction[6:11]
                    SO_string = instruction[16:32]
                    SO_value = twos_comp(int(SO_string,2), len(SO_string))
                    new_PC = Register_value_d[int(RS1,2)]/4 + SO_value
                    PC += 1
                    flag = 1
                    
                if (instruction[:6] == '011101'): #JALR
                    RS1 = instruction[6:11]
                    SO_string = instruction[16:32]
                    SO_value = twos_comp(int(SO_string,2), len(SO_string))
                    Register_value_d[31] = PC+2
                    Register_value_b[31] = '0b{:032b}'.format((PC+2)%(1<<32))
                    new_PC = Register_value_d[int(RS1,2)]/4 + SO_value
                    PC += 1
                    flag = 1
                    
                if (instruction[:6] == '011110'): #J
                    SO_string = instruction[6:32]
                    SO_value = twos_comp(int(SO_string,2), len(SO_string))
                    new_PC = PC + SO_value
                    PC += 1
                    flag = 1
                    
                if (instruction[:6] == '011111'): #JAL
                    SO_string = instruction[6:32]
                    SO_value = twos_comp(int(SO_string,2), len(SO_string))
                    Register_value_d[31] = PC+2
                    Register_value_b[31] = '0b{:032b}'.format((PC+2)%(1<<32))
                    new_PC = PC + SO_value
                    PC += 1
                    flag = 1

        Reg_file = pd.DataFrame(reg_file_dictionary)
        Memory = pd.DataFrame(memory_dictionary)

        # print(Reg_file)
        # print(Memory)

        # def show_dict(self, d):
        #     for k, v in d.items():
        #         self.text.insert(tk.END, "key = {}, val = {}\n".format(k, v))

        # self.show_dict(Reg_file)
        # self.show_dict(Memory)

        # window = tk.Tk()
        # for x in range(2):
        #     for y in range(3):
        #         frameGrid = tk.Frame(
        #         master=window,
        #         relief=tk.FLAT,
        #         borderwidth=2
        #         )
        #         frameGrid.grid(row=x, column=y)
        #         labelGrid = tk.Label(master=frameGrid, text=f"Row No. {x}\nColumn No. {y}")
        #         labelGrid.pack()
        window = tk.Tk()
        # for x in range():
        #     for y in range(3):
        i=0
        j=0
        # for k, v in Reg_file.items():
        #     # print(f"{k}, {v}")
        #     frameGrid = tk.Frame(
        #     master=window,
        #     relief=tk.FLAT,
        #     borderwidth=2
        #     )
        #     frameGrid.grid(row=0, column=0)
        #     labelGrid = tk.Label(master=frameGrid, text=f"{k}{v}")
        #     # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
        #     labelGrid.pack()
        #     # i=i+1
        #     # j=j+1

        for k, v in Reg_file.items():
            frameGrid = tk.Frame(
            master=window,
            relief=tk.FLAT,
            borderwidth=10
            )
            frameGrid.grid(row=0,column=j)
            labelGrid = tk.Label(master=frameGrid, text=f"{k}")
            # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
            labelGrid.pack()
            i=i+1
            j=j+1

        l=0
        m=0

        for k, v in Reg_file.items():
            # print(f"{k}, {v}")
            # print(k)
            frameGrid = tk.Frame(
            master=window,
            relief=tk.FLAT,
            borderwidth=10
            )
            frameGrid.grid(row=1,column=m)
            labelGrid = tk.Label(master=frameGrid, text=f"{v}")
            # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
            labelGrid.pack()
            l=l+1
            m=m+1


        ##################################################

        window2 = tk.Tk()
            # for x in range():
            #     for y in range(3):
        p=0
        q=0
            # for k, v in Reg_file.items():
            #     # print(f"{k}, {v}")
            #     frameGrid = tk.Frame(
            #     master=window,
            #     relief=tk.FLAT,
            #     borderwidth=2
            #     )
            #     frameGrid.grid(row=0, column=0)
            #     labelGrid = tk.Label(master=frameGrid, text=f"{k}{v}")
            #     # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
            #     labelGrid.pack()
            #     # i=i+1
            #     # j=j+1

        for k, v in Memory.items():
            frameGrid = tk.Frame(
            master=window2,
            relief=tk.FLAT,
            borderwidth=10
            )
            frameGrid.grid(row=0,column=q)
            labelGrid = tk.Label(master=frameGrid, text=f"{k}")
                        # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
            labelGrid.pack()
            p=p+1
            q=q+1    

        t=0
        f=0

        for k, v in Memory.items():
                # print(f"{k}, {v}")
                # print(k)
            frameGrid = tk.Frame(
                master=window2,
                relief=tk.FLAT,
                borderwidth=10
                )
            frameGrid.grid(row=1,column=f)
            labelGrid = tk.Label(master=frameGrid, text=f"{v}")
            # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
            labelGrid.pack()
            t=t+1
            f=f+1

        # for k, v in Memory.items():
        #     label=tk.Label(window2, text=f"{v}\n")
        #     label.pack()
        
        window3 = tk.Tk()
        # label=tk.Label(window3, text=f"PC Value: {PC+1}", font=('Arial', 14))
        label=tk.Label(window3, text=f"PC Value: {PC+1}")
        label.pack()

        # window9=tk.Tk()

        # for k, v in Memory.items():
        #     label=tk.Label(window9, text=f"{v}")
        #     label.pack()

        # print(Reg_file['Register'], Reg_file['Decimal'])
        # print(Reg_file['Decimal'])

        # for label, content in Reg_file.items():
        #     print(f'label: {label}')
        #     print(f'content: {content}', sep=' ')
            # print(f"{k}, {v}")
            # print(k)
            # frameGrid = tk.Frame(
            # master=window,
            # relief=tk.FLAT,
            # borderwidth=2
            # )
            # frameGrid.grid(row=1, column=2)
            # labelGrid = tk.Label(master=frameGrid, text=f"{k}")
            # # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
            # labelGrid.pack()
            # i=i+1
            # j=j+1

def twos_comp(val, bits):
        # """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val  

MyGUI()



##########################################################################################################################################




# import tkinter as tk
# from tkinter import *
# from tkinter import CENTER, messagebox

# import pandas as pd
# import numpy as np

# # root=tk.Tk()

# # root.geometry("800x500")
# # root.mainloop()


# class MyGUI:

#     def __init__(self):

#         self.root = tk.Tk()

#         self.label = tk.Label(
#             self.root, text="SDLX Simulator", font=('Arial', 18))
#         self.label.pack(padx=10, pady=10)

#         self.textbox = tk.Text(self.root, height=5, font=('Arial', 16))
#         self.textbox.pack(padx=10, pady=10)

#         # self.button = tk.Button(self.root, text= "Start!", font=('Arial', 18), command=self.print)
#         self.button = tk.Button(self.root, text="Start!", font=('Arial', 18))
#         self.button.pack(padx=10, pady=10)

#         self.root.mainloop()

#     def twos_comp(val, bits):
#         # """compute the 2's complement of int value val"""
#         if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
#             val = val - (1 << bits)        # compute negative value
#         return val  
    
#     # making reg file (initialize all values in registers to 0)
#     Register_no = []
#     Register_value_d = []
#     Register_value_b = []
#     reg_file_dictionary = {"Register" : Register_no, "Decimal" : Register_value_d, "Binary" : Register_value_b}

#     for i in range(32):
#         Register_no.append(f"R{i}")

#     for i in range(32):
#         Register_value_d.append(0)
        

#     for i in range(32):
#         Register_value_b.append('0b{:032b}'.format(Register_value_d[i]%(1<<32)))

#     Reg_file = pd.DataFrame(reg_file_dictionary)

#     # making memory (initializing all values to 0)
#     memory_adress = []
#     memory_value_d = []
#     memory_value_b = []
#     memory_dictionary = {"Memory Adress": memory_adress, "Decimal": memory_value_d, "Binary": memory_value_b}

#     for i in range(0,37,4):
#         memory_adress.append('0x{:08x}'.format(i))
        
#     for i in range(10):
#         memory_value_d.append(0)

#     for i in range(10):
#         memory_value_b.append('0b{:032b}'.format(memory_value_d[i]%(1<<32)))
    
#     Memory = pd.DataFrame(memory_dictionary)

#     PC=0

#     flag=0

#     new_PC=0

#     Instruction_array = ["00000100101001010000000000000101", "00000100101001010000000000000100", "01100100000001010000000000000100", "01011000000000110000000000000100", "01000100101011010000000011111111", "01001000000010100000000000000111"]
    
#     while(PC<len(Instruction_array)):
#         instruction = Instruction_array[PC]
#         if (instruction[:6] == '000000'): #R Type Instructions
            
#             RS1 = instruction[6:11]
#             RS2 = instruction[11:16]
#             RD = instruction[16:21]
                
#             if (instruction[-6:] == '000000'): #ADD Instruction
#                 answer = Register_value_d[int(RS1,2)]+Register_value_d[int(RS2,2)]
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#             if (instruction[-6:] == '000001'): #SUB Instruction
#                 answer = Register_value_d[int(RS1,2)]-Register_value_d[int(RS2,2)]
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#             if (instruction[-6:] == '000010'): #AND Instruction
#                 answer = Register_value_d[int(RS1,2)]&Register_value_d[int(RS2,2)]
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
            
            
#             if (instruction[-6:] == '000011'): #OR Instruction
#                 answer = Register_value_d[int(RS1,2)]|Register_value_d[int(RS2,2)]
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#             if (instruction[-6:] == '000100'): #XOR Instruction
#                 answer = Register_value_d[int(RS1,2)]^Register_value_d[int(RS2,2)]
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
            
#             if (instruction[-6:] == '000101'): #SLL Instruction
#                 answer = Register_value_d[int(RS1,2)]<<Register_value_d[int(RS2,2)]
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#             if (instruction[-6:] == '000110'): #SRL Instruction
#                 answer = Register_value_d[int(RS1,2)]>>Register_value_d[int(RS2,2)]
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
        
            
#             if (instruction[-6:] == '001000'): #SLT Instruction
#                 if (Register_value_d[int(RS1,2)]<Register_value_d[int(RS2,2)]):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
            
#             if (instruction[-6:] == '001001'): #SGT Instruction
#                 if (Register_value_d[int(RS1,2)]>Register_value_d[int(RS2,2)]):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#             if (instruction[-6:] == '001010'): #SLE Instruction
#                 if (Register_value_d[int(RS1,2)]<=Register_value_d[int(RS2,2)]):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#             if (instruction[-6:] == '001011'): #SGE Instruction
#                 if (Register_value_d[int(RS1,2)]>=Register_value_d[int(RS2,2)]):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#             if (instruction[-6:] == '001100'): #ULT Instruction
                
#                 a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
#                 b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2) 
#                 if (a<b):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#             if (instruction[-6:] == '001101'): #UGT Instruction
                
#                 a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
#                 b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2) 
#                 if (a>b):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#             if (instruction[-6:] == '001110'): #ULE Instruction
                
#                 a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
#                 b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2) 
#                 if (a<=b):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#             if (instruction[-6:] == '001111'): #UGE Instruction
                
#                 a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
#                 b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2) 
#                 if (a>=b):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))
                
#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
                
#         else:
#             if (instruction[:6] == '000001'): #ADDI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 answer = Register_value_d[int(RS1,2)] + IMM_value
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '000010'): #SUBI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 answer = Register_value_d[int(RS1,2)] - IMM_value
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '000011'): #ORI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 answer = Register_value_d[int(RS1,2)] | IMM_value
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
            
#             if (instruction[:6] == '000100'): #ANDI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 answer = Register_value_d[int(RS1,2)] & IMM_value
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '000101'): #XORI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 answer = Register_value_d[int(RS1,2)] ^ IMM_value
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '000110'): #SLLI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 answer = Register_value_d[int(RS1,2)] << IMM_value
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '000111'): #SRLI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 answer = Register_value_d[int(RS1,2)] >> IMM_value
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
            
#             if (instruction[:6] == '001001'): #SLTI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 if (Register_value_d[int(RS1,2)] < IMM_value):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '001010'): #SGTI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 if (Register_value_d[int(RS1,2)] > IMM_value):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
        

#             if (instruction[:6] == '001011'): #SLEI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 if (Register_value_d[int(RS1,2)] <= IMM_value):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '001100'): #SGEI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 if (Register_value_d[int(RS1,2)] >= IMM_value):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '001101'): #ULTI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2) 
#                 if (Register_value_d[int(RS1,2)] < IMM_UNS):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '001110'): #UGTI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2) 
#                 if (Register_value_d[int(RS1,2)] > IMM_UNS):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
            
#             if (instruction[:6] == '001111'): #ULEI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2) 
#                 if (Register_value_d[int(RS1,2)] <= IMM_UNS):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '010000'): #UGEI
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2) 
#                 if (Register_value_d[int(RS1,2)] >= IMM_UNS):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

            
#             if (instruction[:6] == '010001'): #LHI (to be completed)
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2) 
#                 if (Register_value_d[int(RS1,2)] <= IMM_UNS):
#                     answer = (2**32)-1
#                 else:
#                     answer = 0
#                 Register_value_d[int(RD,2)] = answer
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0



#             if (instruction[:6] == '010010'): #LB
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 adress = Register_value_d[int(RS1,2)]+IMM_value
#                 mem_line = (adress//4)*4
#                 within_adress = adress-mem_line
#                 #string = Memory.iloc[mem_line/4]["Binary"][2:34]
#                 string = memory_value_b[adress//4]
#                 print(string)
#                 value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+8+2]
#                 value_required = twos_comp(int(value_required_bin_string,2), len(value_required_bin_string))
#                 Register_value_d[int(RD,2)] = value_required
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '010011'): #LBU
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 adress = Register_value_d[int(RS1,2)]+IMM_value
#                 mem_line = (adress//4)*4
#                 within_adress = adress-mem_line
#                 #string = Memory.iloc[mem_line/4]["Binary"][2:34]
#                 string = memory_value_b[adress//4]
#                 value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+8+2]
#                 value_required = int(value_required_bin_string,2)
#                 Register_value_d[int(RD,2)] = value_required
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
            
#             if (instruction[:6] == '010100'): #LH
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 adress = Register_value_d[int(RS1,2)]+IMM_value
#                 mem_line = (adress//4)*4
#                 within_adress = adress-mem_line
#                 #string = Memory.iloc[mem_line/4]["Binary"][2:34]
#                 string = memory_value_b[adress//4]
#                 if (within_adress == 1 | within_adress == 3):
#                     print("Memory not accessable")
#                 value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+16+2]
#                 value_required = twos_comp(int(value_required_bin_string,2), len(value_required_bin_string))
#                 Register_value_d[int(RD,2)] = value_required
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '010101'): #LHU
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 adress = Register_value_d[int(RS1,2)]+IMM_value
#                 mem_line = (adress//4)*4
#                 within_adress = adress-mem_line
#                 #string = Memory.iloc[mem_line/4]["Binary"][2:34]
#                 string = memory_value_b[adress//4]
#                 if (within_adress == 1 | within_adress == 3):
#                     print("Memory not accessable")
#                 value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+16+2]
#                 value_required = int(value_required_bin_string,2)
#                 Register_value_d[int(RD,2)] = value_required
#                 Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '010110'): #LW (Loads the whole 4 bytes; Load byte and Load byte unsigned is litte more complicated)
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 adress = Register_value_d[int(RS1,2)]+IMM_value
#                 #value_required_bin_string = Memory.iloc[adress/4]["Binary"][2:34]
#                 value_required_bin_string = memory_value_b[adress//4]
#                 value_required = int(value_required_bin_string,2)
#                 Register_value_d[int(RD,2)] = value_required
#                 Register_value_b[int(RD,2)] = value_required_bin_string

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
#                 #mem_adress = '0x{:08x}'.format(adress)
#                 #value = Memory[Memory["Memory Adress"] == mem_adress]["Decimal"].iloc[0]
#                 #Register_value_d[int(RD,2)] = value
#                 #Register_value_b[int(RD,2)] = '0b{:032b}'.format(value%(1<<32))
            
#             if (instruction[:6] == '010111'): #SB
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 adress = Register_value_d[int(RS1,2)]+IMM_value
#                 mem_line = (adress//4)*4
#                 within_adress = adress-mem_line
#                 #string = Reg_file.iloc[int(RD,2)]["Binary"][2:34]
#                 string = Register_value_b[int(RD,2)]
#                 value_required_bin_string = string[-8:]

#                 if (within_adress == 0):
#                     req_string = value_required_bin_string+'{:024}'.format(0)
#                 if (within_adress == 1):
#                     req_string = '{:008}'.format(0)+value_required_bin_string+'{:016}'.format(0)
#                 if (within_adress == 2):
#                     req_string = '{:016}'.format(0)+value_required_bin_string+'{:008}'.format(0)
#                 if (within_adress == 3):
#                     req_string = '{:024}'.format(0)+value_required_bin_string

#                 req_value = twos_comp(int(req_string,2), len(req_string))

#                 memory_value_d[(adress//4)] = req_value
#                 memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0
            
#             if (instruction[:6] == '011000'): #SH
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 adress = Register_value_d[int(RS1,2)]+IMM_value
#                 mem_line = (adress//4)*4
#                 within_adress = adress-mem_line
#                 #string = Reg_file.iloc[int(RD,2)]["Binary"][2:34]
#                 string = Register_value_b[int(RD,2)]
#                 value_required_bin_string = string[-16:]

#                 if (within_adress == 1 | within_adress == 3):
#                     print("Memory not accessable")

#                 if (within_adress == 0):
#                     req_string = value_required_bin_string+'{:024}'.format(0)

#                 if (within_adress == 2):
#                     req_string = '{:016}'.format(0)+value_required_bin_string+'{:008}'.format(0)


#                 req_value = twos_comp(int(req_string,2), len(req_string))

#                 memory_value_d[(adress//4)] = req_value
#                 memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0

#             if (instruction[:6] == '011001'): #SW
#                 RS1 = instruction[6:11]
#                 RD = instruction[11:16]
#                 IMM = instruction[16:32]
#                 IMM_value = twos_comp(int(IMM,2), len(IMM))
#                 adress = Register_value_d[int(RS1,2)]+IMM_value
#                 mem_line = (adress//4)*4
#                 within_adress = adress-mem_line
#                 string = Register_value_b[int(RD,2)]


#                 if (within_adress == 1 | within_adress == 3 | within_adress ==2):
#                     print("Memory not accessable")

#                 if (within_adress == 0):
#                     req_string = string


#                 req_value = twos_comp(int(req_string,2), len(req_string))
                

#                 memory_value_d[adress//4] = req_value
#                 memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

#                 if (flag == 0):
#                     PC +=1
#                 else:
#                     PC = new_PC
#                     flag = 0


#             if (instruction[:6] == '011010'): #BEQZ
#                 RS1 = instruction[6:11]
#                 SO_string = instruction[16:32]
#                 SO_value = twos_comp(int(SO_string,2), len(SO_string))
                
#                 if (Register_value_d[int(RS1,2)] == 0):
#                     new_PC = PC+SO_value
#                     flag = 1
#                     PC += 1
#                 else:
#                     PC += 1
            
#             if (instruction[:6] == '011011'): #BNEZ
#                 RS1 = instruction[6:11]
#                 SO_string = instruction[16:32]
#                 SO_value = twos_comp(int(SO_string,2), len(SO_string))
                
#                 if (Register_value_d[int(RS1,2)] != 0):
#                     new_PC = PC+SO_value
#                     flag = 1
#                     PC += 1
#                 else:
#                     PC += 1
                    
#             if (instruction[:6] == '011100'): #JR
#                 RS1 = instruction[6:11]
#                 SO_string = instruction[16:32]
#                 SO_value = twos_comp(int(SO_string,2), len(SO_string))
#                 new_PC = Register_value_d[int(RS1,2)]/4 + SO_value
#                 PC += 1
#                 flag = 1
                
#             if (instruction[:6] == '011101'): #JALR
#                 RS1 = instruction[6:11]
#                 SO_string = instruction[16:32]
#                 SO_value = twos_comp(int(SO_string,2), len(SO_string))
#                 Register_value_d[31] = PC+2
#                 Register_value_b[31] = '0b{:032b}'.format((PC+2)%(1<<32))
#                 new_PC = Register_value_d[int(RS1,2)]/4 + SO_value
#                 PC += 1
#                 flag = 1
                
#             if (instruction[:6] == '011110'): #J
#                 SO_string = instruction[6:32]
#                 SO_value = twos_comp(int(SO_string,2), len(SO_string))
#                 new_PC = PC + SO_value
#                 PC += 1
#                 flag = 1
                
#             if (instruction[:6] == '011111'): #JAL
#                 SO_string = instruction[6:32]
#                 SO_value = twos_comp(int(SO_string,2), len(SO_string))
#                 Register_value_d[31] = PC+2
#                 Register_value_b[31] = '0b{:032b}'.format((PC+2)%(1<<32))
#                 new_PC = PC + SO_value
#                 PC += 1
#                 flag = 1

#     Reg_file = pd.DataFrame(reg_file_dictionary)
#     Memory = pd.DataFrame(memory_dictionary)

#     # print(Reg_file)
#     # print(Memory)

#     # def show_dict(self, d):
#     #     for k, v in d.items():
#     #         self.text.insert(tk.END, "key = {}, val = {}\n".format(k, v))

#     # self.show_dict(Reg_file)
#     # self.show_dict(Memory)

#     # window = tk.Tk()
#     # for x in range(2):
#     #     for y in range(3):
#     #         frameGrid = tk.Frame(
#     #         master=window,
#     #         relief=tk.FLAT,
#     #         borderwidth=2
#     #         )
#     #         frameGrid.grid(row=x, column=y)
#     #         labelGrid = tk.Label(master=frameGrid, text=f"Row No. {x}\nColumn No. {y}")
#     #         labelGrid.pack()
#     window = tk.Tk()
#     # for x in range():
#     #     for y in range(3):
#     i=0
#     j=0
#     # for k, v in Reg_file.items():
#     #     # print(f"{k}, {v}")
#     #     frameGrid = tk.Frame(
#     #     master=window,
#     #     relief=tk.FLAT,
#     #     borderwidth=2
#     #     )
#     #     frameGrid.grid(row=0, column=0)
#     #     labelGrid = tk.Label(master=frameGrid, text=f"{k}{v}")
#     #     # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
#     #     labelGrid.pack()
#     #     # i=i+1
#     #     # j=j+1

#     for k, v in Reg_file.items():
#         frameGrid = tk.Frame(
#         master=window,
#         relief=tk.FLAT,
#         borderwidth=10
#         )
#         frameGrid.grid(row=0,column=j)
#         labelGrid = tk.Label(master=frameGrid, text=f"{k}")
#         # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
#         labelGrid.pack()
#         i=i+1
#         j=j+1

#     l=0
#     m=0

#     for k, v in Reg_file.items():
#         # print(f"{k}, {v}")
#         # print(k)
#         frameGrid = tk.Frame(
#         master=window,
#         relief=tk.FLAT,
#         borderwidth=10
#         )
#         frameGrid.grid(row=1,column=m)
#         labelGrid = tk.Label(master=frameGrid, text=f"{v}")
#         # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
#         labelGrid.pack()
#         l=l+1
#         m=m+1


#     ##################################################

#     window2 = tk.Tk()
#         # for x in range():
#         #     for y in range(3):
#     p=0
#     q=0
#         # for k, v in Reg_file.items():
#         #     # print(f"{k}, {v}")
#         #     frameGrid = tk.Frame(
#         #     master=window,
#         #     relief=tk.FLAT,
#         #     borderwidth=2
#         #     )
#         #     frameGrid.grid(row=0, column=0)
#         #     labelGrid = tk.Label(master=frameGrid, text=f"{k}{v}")
#         #     # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
#         #     labelGrid.pack()
#         #     # i=i+1
#         #     # j=j+1

#     for k, v in Memory.items():
#         frameGrid = tk.Frame(
#         master=window2,
#         relief=tk.FLAT,
#         borderwidth=10
#         )
#         frameGrid.grid(row=0,column=q)
#         labelGrid = tk.Label(master=frameGrid, text=f"{k}")
#                     # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
#         labelGrid.pack()
#         p=p+1
#         q=q+1    

#     t=0
#     f=0

#     for k, v in Memory.items():
#             # print(f"{k}, {v}")
#             # print(k)
#         frameGrid = tk.Frame(
#             master=window2,
#             relief=tk.FLAT,
#             borderwidth=10
#             )
#         frameGrid.grid(row=1,column=f)
#         labelGrid = tk.Label(master=frameGrid, text=f"{v}")
#         # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
#         labelGrid.pack()
#         t=t+1
#         f=f+1




#     # print(Reg_file['Register'], Reg_file['Decimal'])
#     # print(Reg_file['Decimal'])

#     # for label, content in Reg_file.items():
#     #     print(f'label: {label}')
#     #     print(f'content: {content}', sep=' ')
#         # print(f"{k}, {v}")
#         # print(k)
#         # frameGrid = tk.Frame(
#         # master=window,
#         # relief=tk.FLAT,
#         # borderwidth=2
#         # )
#         # frameGrid.grid(row=1, column=2)
#         # labelGrid = tk.Label(master=frameGrid, text=f"{k}")
#         # # labelGrid = tk.Label(master=frameGrid, text="key = {}, val = {}\n".format(k, v))
#         # labelGrid.pack()
#         # i=i+1
#         # j=j+1

# MyGUI()

##########################################################################################################################################################


# # Import the required libraries
# from tkinter import *
# from tkinter import ttk

# # Create an instance of tkinter frame
# win = Tk()

# # Set the size of the tkinter window
# win.geometry("700x350")
# s = ttk.Style()
# s.theme_use('clam')

# # Add a Treeview widget
# tree = ttk.Treeview(win, column=("c1", "c2", "c3"), show='headings', height=5)
# tree.column("# 1", anchor=CENTER)
# tree.heading("# 1", text="ID")
# tree.column("# 2", anchor=CENTER)
# tree.heading("# 2", text="FName")
# tree.column("# 3", anchor=CENTER)
# tree.heading("# 3", text="LName")

# # Insert the data in Treeview widget
# tree.insert('', 'end', text="1", values=('1', 'Joe', 'Nash'))
# tree.insert('', 'end', text="2", values=('2', 'Emily', 'Mackmohan'))
# tree.insert('', 'end', text="3", values=('3', 'Estilla', 'Roffe'))
# tree.insert('', 'end', text="4", values=('4', 'Percy', 'Andrews'))
# tree.insert('', 'end', text="5", values=('5', 'Stephan', 'Heyward'))

# tree.pack()

# win.mainloop()
    
    
# import tkinter as tk
# class Application(tk.Frame):
#     def __init__(self, master):
#         tk.Frame.__init__(self, master)
#         self.text = tk.Text(master)        
#         self.text.pack()
#     def show_dict(self, d):
#         for k, v in d.items():
#             self.text.insert(tk.END, "key = {}, val = {}\n".format(k, v))
     
# root = tk.Tk()
# app = Application(root)
# app.show_dict({'Username': 0, 'Username2': 2})
# app.mainloop()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#     Register_no = []
#     Register_value_d = []
#     Register_value_b = []
#     reg_file_dictionary = {"Register": Register_no,
#         "Decimal": Register_value_d, "Binary": Register_value_b}

#     for i in range(32):
#         Register_no.append(f"R{i}")

#     for i in range(32):
#         Register_value_d.append(0)

#     for i in range(32):
#         Register_value_b.append('0b{:032b}'.format(
#             Register_value_d[i] % (1 << 32)))

#     Reg_file = pd.DataFrame(reg_file_dictionary)

#      # making memory (initializing all values to 0)
#     memory_adress = []
#     memory_value_d = []
#     memory_value_b = []
#     memory_dictionary = {"Memory Adress": memory_adress,
#                          "Decimal": memory_value_d, "Binary": memory_value_b}

#     for i in range(0, 37, 4):
#         memory_adress.append('0x{:08x}'.format(i))

#     for i in range(10):
#         memory_value_d.append(0)

#     for i in range(10):
#         memory_value_b.append('0b{:032b}'.format(
#             memory_value_d[i] % (1 << 32)))

#     Memory = pd.DataFrame(memory_dictionary)

#     Instruction_array = ["00000100101001010000000000000101", "00000100101001010000000000000100", "01100100000001010000000000000100",
#                          "01011000000000110000000000000100", "01000100101011010000000011111111", "01001000000010100000000000000111"]

#     PC = 0

#     flag = 0

#     new_PC = 0

#    while (PC < len(Instruction_array)):
#     instruction = Instruction_array[PC]
#         if (instruction[:6] == '000000'):  # R Type Instructions

#                 RS1 = instruction[6:11]
#                 RS2 = instruction[11:16]
#                 RD = instruction[16:21]

#                 if (instruction[-6:] == '000000'):  # ADD Instruction
#                     answer = Register_value_d[int(
#                         RS1, 2)]+Register_value_d[int(RS2, 2)]
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '000001'):  # SUB Instruction
#                     answer = Register_value_d[int(
#                         RS1, 2)]-Register_value_d[int(RS2, 2)]
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '000010'):  # AND Instruction
#                     answer = Register_value_d[int(
#                         RS1, 2)] & Register_value_d[int(RS2, 2)]
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '000011'):  # OR Instruction
#                     answer = Register_value_d[int(
#                         RS1, 2)] | Register_value_d[int(RS2, 2)]
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '000100'):  # XOR Instruction
#                     answer = Register_value_d[int(
#                         RS1, 2)] ^ Register_value_d[int(RS2, 2)]
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '000101'):  # SLL Instruction
#                     answer = Register_value_d[int(
#                         RS1, 2)] << Register_value_d[int(RS2, 2)]
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '000110'):  # SRL Instruction
#                     answer = Register_value_d[int(
#                         RS1, 2)] >> Register_value_d[int(RS2, 2)]
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '001000'):  # SLT Instruction
#                     if (Register_value_d[int(RS1, 2)] < Register_value_d[int(RS2, 2)]):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '001001'):  # SGT Instruction
#                     if (Register_value_d[int(RS1, 2)] > Register_value_d[int(RS2, 2)]):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '001010'):  # SLE Instruction
#                     if (Register_value_d[int(RS1, 2)] <= Register_value_d[int(RS2, 2)]):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '001011'):  # SGE Instruction
#                     if (Register_value_d[int(RS1, 2)] >= Register_value_d[int(RS2, 2)]):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '001100'):  # ULT Instruction

#                     a = int('0b{:032b}'.format(
#                         Register_value_d[int(RS1, 2)] % (1 << 32)), 2)
#                     b = int('0b{:032b}'.format(
#                         Register_value_d[int(RS2, 2)] % (1 << 32)), 2)
#                     if (a < b):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '001101'):  # UGT Instruction

#                     a = int('0b{:032b}'.format(
#                         Register_value_d[int(RS1, 2)] % (1 << 32)), 2)
#                     b = int('0b{:032b}'.format(
#                         Register_value_d[int(RS2, 2)] % (1 << 32)), 2)
#                     if (a > b):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '001110'):  # ULE Instruction

#                     a = int('0b{:032b}'.format(
#                         Register_value_d[int(RS1, 2)] % (1 << 32)), 2)
#                     b = int('0b{:032b}'.format(
#                         Register_value_d[int(RS2, 2)] % (1 << 32)), 2)
#                     if (a <= b):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[-6:] == '001111'):  # UGE Instruction

#                     a = int('0b{:032b}'.format(
#                         Register_value_d[int(RS1, 2)] % (1 << 32)), 2)
#                     b = int('0b{:032b}'.format(
#                         Register_value_d[int(RS2, 2)] % (1 << 32)), 2)
#                     if (a >= b):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#             else:
#                 if (instruction[:6] == '000001'):  # ADDI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     answer = Register_value_d[int(RS1, 2)] + IMM_value
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '000010'):  # SUBI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     answer = Register_value_d[int(RS1, 2)] - IMM_value
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '000011'):  # ORI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     answer = Register_value_d[int(RS1, 2)] | IMM_value
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '000100'):  # ANDI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     answer = Register_value_d[int(RS1, 2)] & IMM_value
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '000101'):  # XORI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     answer = Register_value_d[int(RS1, 2)] ^ IMM_value
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '000110'):  # SLLI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     answer = Register_value_d[int(RS1, 2)] << IMM_value
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '000111'):  # SRLI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     answer = Register_value_d[int(RS1, 2)] >> IMM_value
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '001001'):  # SLTI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     if (Register_value_d[int(RS1, 2)] < IMM_value):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '001010'):  # SGTI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     if (Register_value_d[int(RS1, 2)] > IMM_value):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '001011'):  # SLEI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     if (Register_value_d[int(RS1, 2)] <= IMM_value):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '001100'):  # SGEI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     if (Register_value_d[int(RS1, 2)] >= IMM_value):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '001101'):  # ULTI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_UNS = int('0b{:032b}'.format(
#                         int(IMM, 2) % (1 << 32)), 2)
#                     if (Register_value_d[int(RS1, 2)] < IMM_UNS):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '001110'):  # UGTI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_UNS = int('0b{:032b}'.format(
#                         int(IMM, 2) % (1 << 32)), 2)
#                     if (Register_value_d[int(RS1, 2)] > IMM_UNS):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '001111'):  # ULEI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_UNS = int('0b{:032b}'.format(
#                         int(IMM, 2) % (1 << 32)), 2)
#                     if (Register_value_d[int(RS1, 2)] <= IMM_UNS):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '010000'):  # UGEI
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_UNS = int('0b{:032b}'.format(
#                         int(IMM, 2) % (1 << 32)), 2)
#                     if (Register_value_d[int(RS1, 2)] >= IMM_UNS):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '010001'):  # LHI (to be completed)
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_UNS = int('0b{:032b}'.format(
#                         int(IMM, 2) % (1 << 32)), 2)
#                     if (Register_value_d[int(RS1, 2)] <= IMM_UNS):
#                         answer = (2**32)-1
#                     else:
#                         answer = 0
#                     Register_value_d[int(RD, 2)] = answer
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         answer % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '010010'):  # LB
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     adress = Register_value_d[int(RS1, 2)]+IMM_value
#                     mem_line = (adress//4)*4
#                     within_adress = adress-mem_line
#                     # string = Memory.iloc[mem_line/4]["Binary"][2:34]
#                     string = memory_value_b[adress//4]
#                     print(string)
#                     value_required_bin_string = string[2 +
#                                                        8*(within_adress):8*(within_adress)+8+2]
#                     value_required = twos_comp(
#                         int(value_required_bin_string, 2), len(value_required_bin_string))
#                     Register_value_d[int(RD, 2)] = value_required
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         (value_required) % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '010011'):  # LBU
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     adress = Register_value_d[int(RS1, 2)]+IMM_value
#                     mem_line = (adress//4)*4
#                     within_adress = adress-mem_line
#                     # string = Memory.iloc[mem_line/4]["Binary"][2:34]
#                     string = memory_value_b[adress//4]
#                     value_required_bin_string = string[2 +
#                                                        8*(within_adress):8*(within_adress)+8+2]
#                     value_required = int(value_required_bin_string, 2)
#                     Register_value_d[int(RD, 2)] = value_required
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         (value_required) % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '010100'):  # LH
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     adress = Register_value_d[int(RS1, 2)]+IMM_value
#                     mem_line = (adress//4)*4
#                     within_adress = adress-mem_line
#                     # string = Memory.iloc[mem_line/4]["Binary"][2:34]
#                     string = memory_value_b[adress//4]
#                     if (within_adress == 1 | within_adress == 3):
#                         print("Memory not accessable")
#                     value_required_bin_string = string[2+8 *
#                                                        (within_adress):8*(within_adress)+16+2]
#                     value_required = twos_comp(
#                         int(value_required_bin_string, 2), len(value_required_bin_string))
#                     Register_value_d[int(RD, 2)] = value_required
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         (value_required) % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '010101'):  # LHU
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     adress = Register_value_d[int(RS1, 2)]+IMM_value
#                     mem_line = (adress//4)*4
#                     within_adress = adress-mem_line
#                     # string = Memory.iloc[mem_line/4]["Binary"][2:34]
#                     string = memory_value_b[adress//4]
#                     if (within_adress == 1 | within_adress == 3):
#                         print("Memory not accessable")
#                     value_required_bin_string = string[2+8 *
#                                                        (within_adress):8*(within_adress)+16+2]
#                     value_required = int(value_required_bin_string, 2)
#                     Register_value_d[int(RD, 2)] = value_required
#                     Register_value_b[int(RD, 2)] = '0b{:032b}'.format(
#                         (value_required) % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 # LW (Loads the whole 4 bytes; Load byte and Load byte unsigned is litte more complicated)
#                 if (instruction[:6] == '010110'):
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     adress = Register_value_d[int(RS1, 2)]+IMM_value
#                     # value_required_bin_string = Memory.iloc[adress/4]["Binary"][2:34]
#                     value_required_bin_string = memory_value_b[adress//4]
#                     value_required = int(value_required_bin_string, 2)
#                     Register_value_d[int(RD, 2)] = value_required
#                     Register_value_b[int(RD, 2)] = value_required_bin_string

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0
#                     # mem_adress = '0x{:08x}'.format(adress)
#                     # value = Memory[Memory["Memory Adress"] == mem_adress]["Decimal"].iloc[0]
#                     # Register_value_d[int(RD,2)] = value
#                     # Register_value_b[int(RD,2)] = '0b{:032b}'.format(value%(1<<32))

#                 if (instruction[:6] == '010111'):  # SB
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     adress = Register_value_d[int(RS1, 2)]+IMM_value
#                     mem_line = (adress//4)*4
#                     within_adress = adress-mem_line
#                     # string = Reg_file.iloc[int(RD,2)]["Binary"][2:34]
#                     string = Register_value_b[int(RD, 2)]
#                     value_required_bin_string = string[-8:]

#                     if (within_adress == 0):
#                         req_string = value_required_bin_string + \
#                             '{:024}'.format(0)
#                     if (within_adress == 1):
#                         req_string = '{:008}'.format(
#                             0)+value_required_bin_string+'{:016}'.format(0)
#                     if (within_adress == 2):
#                         req_string = '{:016}'.format(
#                             0)+value_required_bin_string+'{:008}'.format(0)
#                     if (within_adress == 3):
#                         req_string = '{:024}'.format(
#                             0)+value_required_bin_string

#                     req_value = twos_comp(int(req_string, 2), len(req_string))

#                     memory_value_d[(adress//4)] = req_value
#                     memory_value_b[(
#                         adress//4)] = '0b{:032b}'.format((req_value) % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '011000'):  # SH
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     adress = Register_value_d[int(RS1, 2)]+IMM_value
#                     mem_line = (adress//4)*4
#                     within_adress = adress-mem_line
#                     # string = Reg_file.iloc[int(RD,2)]["Binary"][2:34]
#                     string = Register_value_b[int(RD, 2)]
#                     value_required_bin_string = string[-16:]

#                     if (within_adress == 1 | within_adress == 3):
#                         print("Memory not accessable")

#                     if (within_adress == 0):
#                         req_string = value_required_bin_string + \
#                             '{:024}'.format(0)

#                     if (within_adress == 2):
#                         req_string = '{:016}'.format(
#                             0)+value_required_bin_string+'{:008}'.format(0)

#                     req_value = twos_comp(int(req_string, 2), len(req_string))

#                     memory_value_d[(adress//4)] = req_value
#                     memory_value_b[(
#                         adress//4)] = '0b{:032b}'.format((req_value) % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '011001'):  # SW
#                     RS1 = instruction[6:11]
#                     RD = instruction[11:16]
#                     IMM = instruction[16:32]
#                     IMM_value = twos_comp(int(IMM, 2), len(IMM))
#                     adress = Register_value_d[int(RS1, 2)]+IMM_value
#                     mem_line = (adress//4)*4
#                     within_adress = adress-mem_line
#                     string = Register_value_b[int(RD, 2)]

#                     if (within_adress == 1 | within_adress == 3 | within_adress == 2):
#                         print("Memory not accessable")

#                     if (within_adress == 0):
#                         req_string = string

#                     req_value = twos_comp(int(req_string, 2), len(req_string))

#                     memory_value_d[adress//4] = req_value
#                     memory_value_b[(
#                         adress//4)] = '0b{:032b}'.format((req_value) % (1 << 32))

#                     if (flag == 0):
#                         PC += 1
#                     else:
#                         PC = new_PC
#                         flag = 0

#                 if (instruction[:6] == '011010'):  # BEQZ
#                     RS1 = instruction[6:11]
#                     SO_string = instruction[16:32]
#                     SO_value = twos_comp(int(SO_string, 2), len(SO_string))

#                     if (Register_value_d[int(RS1, 2)] == 0):
#                         new_PC = PC+SO_value
#                         flag = 1
#                         PC += 1
#                     else:
#                         PC += 1

#                 if (instruction[:6] == '011011'):  # BNEZ
#                     RS1 = instruction[6:11]
#                     SO_string = instruction[16:32]
#                     SO_value = twos_comp(int(SO_string, 2), len(SO_string))

#                     if (Register_value_d[int(RS1, 2)] != 0):
#                         new_PC = PC+SO_value
#                         flag = 1
#                         PC += 1
#                     else:
#                         PC += 1

#                 if (instruction[:6] == '011100'):  # JR
#                     RS1 = instruction[6:11]
#                     SO_string = instruction[16:32]
#                     SO_value = twos_comp(int(SO_string, 2), len(SO_string))
#                     new_PC = Register_value_d[int(RS1, 2)]/4 + SO_value
#                     PC += 1
#                     flag = 1

#                 if (instruction[:6] == '011101'):  # JALR
#                     RS1 = instruction[6:11]
#                     SO_string = instruction[16:32]
#                     SO_value = twos_comp(int(SO_string, 2), len(SO_string))
#                     Register_value_d[31] = PC+2
#                     Register_value_b[31] = '0b{:032b}'.format(
#                         (PC+2) % (1 << 32))
#                     new_PC = Register_value_d[int(RS1, 2)]/4 + SO_value
#                     PC += 1
#                     flag = 1

#                 if (instruction[:6] == '011110'):  # J
#                     SO_string = instruction[6:32]
#                     SO_value = twos_comp(int(SO_string, 2), len(SO_string))
#                     new_PC = PC + SO_value
#                     PC += 1
#                     flag = 1

#                 if (instruction[:6] == '011111'):  # JAL
#                     SO_string = instruction[6:32]
#                     SO_value = twos_comp(int(SO_string, 2), len(SO_string))
#                     Register_value_d[31] = PC+2
#                     Register_value_b[31] = '0b{:032b}'.format(
#                         (PC+2) % (1 << 32))
#                     new_PC = PC + SO_value
#                     PC += 1
#                     flag = 1

#         print(Reg_file)
#         print(Memory)





    # def func(self):
        # print("Hello World!")
        # making reg file (initialize all values in registers to 0)
        # Register_no = []
        # Register_value_d = []
        # Register_value_b = []
        # reg_file_dictionary = {"Register" : Register_no, "Decimal" : Register_value_d, "Binary" : Register_value_b}

        # for i in range(32):
        #     Register_no.append(f"R{i}")

        # for i in range(32):
        #     Register_value_d.append(0)

        # for i in range(32):
        #     Register_value_b.append('0b{:032b}'.format(Register_value_d[i]%(1<<32)))

        # Reg_file = pd.DataFrame(reg_file_dictionary)

        # # making memory (initializing all values to 0)
        # memory_adress = []
        # memory_value_d = []
        # memory_value_b = []
        # memory_dictionary = {"Memory Adress": memory_adress, "Decimal": memory_value_d, "Binary": memory_value_b}

        # for i in range(0,37,4):
        #     memory_adress.append('0x{:08x}'.format(i))

        # for i in range(10):
        #     memory_value_d.append(0)

        # for i in range(10):
        #     memory_value_b.append('0b{:032b}'.format(memory_value_d[i]%(1<<32)))

        # Memory = pd.DataFrame(memory_dictionary)

        # Instruction_array = ["00000100101001010000000000000101", "00000100101001010000000000000100", "01100100000001010000000000000100", "01011000000000110000000000000100", "01000100101011010000000011111111", "01001000000010100000000000000111"]

        # PC=0

        # flag=0

        # new_PC=0

        # while(PC<len(Instruction_array)):
        #     instruction = Instruction_array[PC]
        #     if (instruction[:6] == '000000'): #R Type Instructions

        #         RS1 = instruction[6:11]
        #         RS2 = instruction[11:16]
        #         RD = instruction[16:21]

        #         if (instruction[-6:] == '000000'): #ADD Instruction
        #             answer = Register_value_d[int(RS1,2)]+Register_value_d[int(RS2,2)]
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '000001'): #SUB Instruction
        #             answer = Register_value_d[int(RS1,2)]-Register_value_d[int(RS2,2)]
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '000010'): #AND Instruction
        #             answer = Register_value_d[int(RS1,2)]&Register_value_d[int(RS2,2)]
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '000011'): #OR Instruction
        #             answer = Register_value_d[int(RS1,2)]|Register_value_d[int(RS2,2)]
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '000100'): #XOR Instruction
        #             answer = Register_value_d[int(RS1,2)]^Register_value_d[int(RS2,2)]
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '000101'): #SLL Instruction
        #             answer = Register_value_d[int(RS1,2)]<<Register_value_d[int(RS2,2)]
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '000110'): #SRL Instruction
        #             answer = Register_value_d[int(RS1,2)]>>Register_value_d[int(RS2,2)]
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '001000'): #SLT Instruction
        #             if (Register_value_d[int(RS1,2)]<Register_value_d[int(RS2,2)]):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '001001'): #SGT Instruction
        #             if (Register_value_d[int(RS1,2)]>Register_value_d[int(RS2,2)]):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '001010'): #SLE Instruction
        #             if (Register_value_d[int(RS1,2)]<=Register_value_d[int(RS2,2)]):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '001011'): #SGE Instruction
        #             if (Register_value_d[int(RS1,2)]>=Register_value_d[int(RS2,2)]):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '001100'): #ULT Instruction

        #             a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
        #             b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2)
        #             if (a<b):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '001101'): #UGT Instruction

        #             a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
        #             b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2)
        #             if (a>b):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '001110'): #ULE Instruction

        #             a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
        #             b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2)
        #             if (a<=b):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[-6:] == '001111'): #UGE Instruction

        #             a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
        #             b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2)
        #             if (a>=b):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #     else:
        #         if (instruction[:6] == '000001'): #ADDI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             answer = Register_value_d[int(RS1,2)] + IMM_value
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '000010'): #SUBI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             answer = Register_value_d[int(RS1,2)] - IMM_value
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '000011'): #ORI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             answer = Register_value_d[int(RS1,2)] | IMM_value
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '000100'): #ANDI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             answer = Register_value_d[int(RS1,2)] & IMM_value
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '000101'): #XORI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             answer = Register_value_d[int(RS1,2)] ^ IMM_value
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '000110'): #SLLI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             answer = Register_value_d[int(RS1,2)] << IMM_value
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '000111'): #SRLI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             answer = Register_value_d[int(RS1,2)] >> IMM_value
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '001001'): #SLTI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             if (Register_value_d[int(RS1,2)] < IMM_value):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '001010'): #SGTI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             if (Register_value_d[int(RS1,2)] > IMM_value):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '001011'): #SLEI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             if (Register_value_d[int(RS1,2)] <= IMM_value):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '001100'): #SGEI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             if (Register_value_d[int(RS1,2)] >= IMM_value):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '001101'): #ULTI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2)
        #             if (Register_value_d[int(RS1,2)] < IMM_UNS):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '001110'): #UGTI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2)
        #             if (Register_value_d[int(RS1,2)] > IMM_UNS):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '001111'): #ULEI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2)
        #             if (Register_value_d[int(RS1,2)] <= IMM_UNS):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '010000'): #UGEI
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2)
        #             if (Register_value_d[int(RS1,2)] >= IMM_UNS):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '010001'): #LHI (to be completed)
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2)
        #             if (Register_value_d[int(RS1,2)] <= IMM_UNS):
        #                 answer = (2**32)-1
        #             else:
        #                 answer = 0
        #             Register_value_d[int(RD,2)] = answer
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '010010'): #LB
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             adress = Register_value_d[int(RS1,2)]+IMM_value
        #             mem_line = (adress//4)*4
        #             within_adress = adress-mem_line
        #             #string = Memory.iloc[mem_line/4]["Binary"][2:34]
        #             string = memory_value_b[adress//4]
        #             print(string)
        #             value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+8+2]
        #             value_required = twos_comp(int(value_required_bin_string,2), len(value_required_bin_string))
        #             Register_value_d[int(RD,2)] = value_required
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '010011'): #LBU
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             adress = Register_value_d[int(RS1,2)]+IMM_value
        #             mem_line = (adress//4)*4
        #             within_adress = adress-mem_line
        #             #string = Memory.iloc[mem_line/4]["Binary"][2:34]
        #             string = memory_value_b[adress//4]
        #             value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+8+2]
        #             value_required = int(value_required_bin_string,2)
        #             Register_value_d[int(RD,2)] = value_required
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '010100'): #LH
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             adress = Register_value_d[int(RS1,2)]+IMM_value
        #             mem_line = (adress//4)*4
        #             within_adress = adress-mem_line
        #             #string = Memory.iloc[mem_line/4]["Binary"][2:34]
        #             string = memory_value_b[adress//4]
        #             if (within_adress == 1 | within_adress == 3):
        #                 print("Memory not accessable")
        #             value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+16+2]
        #             value_required = twos_comp(int(value_required_bin_string,2), len(value_required_bin_string))
        #             Register_value_d[int(RD,2)] = value_required
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '010101'): #LHU
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             adress = Register_value_d[int(RS1,2)]+IMM_value
        #             mem_line = (adress//4)*4
        #             within_adress = adress-mem_line
        #             #string = Memory.iloc[mem_line/4]["Binary"][2:34]
        #             string = memory_value_b[adress//4]
        #             if (within_adress == 1 | within_adress == 3):
        #                 print("Memory not accessable")
        #             value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+16+2]
        #             value_required = int(value_required_bin_string,2)
        #             Register_value_d[int(RD,2)] = value_required
        #             Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '010110'): #LW (Loads the whole 4 bytes; Load byte and Load byte unsigned is litte more complicated)
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             adress = Register_value_d[int(RS1,2)]+IMM_value
        #             #value_required_bin_string = Memory.iloc[adress/4]["Binary"][2:34]
        #             value_required_bin_string = memory_value_b[adress//4]
        #             value_required = int(value_required_bin_string,2)
        #             Register_value_d[int(RD,2)] = value_required
        #             Register_value_b[int(RD,2)] = value_required_bin_string

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0
        #             #mem_adress = '0x{:08x}'.format(adress)
        #             #value = Memory[Memory["Memory Adress"] == mem_adress]["Decimal"].iloc[0]
        #             #Register_value_d[int(RD,2)] = value
        #             #Register_value_b[int(RD,2)] = '0b{:032b}'.format(value%(1<<32))

        #         if (instruction[:6] == '010111'): #SB
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             adress = Register_value_d[int(RS1,2)]+IMM_value
        #             mem_line = (adress//4)*4
        #             within_adress = adress-mem_line
        #             #string = Reg_file.iloc[int(RD,2)]["Binary"][2:34]
        #             string = Register_value_b[int(RD,2)]
        #             value_required_bin_string = string[-8:]

        #             if (within_adress == 0):
        #                 req_string = value_required_bin_string+'{:024}'.format(0)
        #             if (within_adress == 1):
        #                 req_string = '{:008}'.format(0)+value_required_bin_string+'{:016}'.format(0)
        #             if (within_adress == 2):
        #                 req_string = '{:016}'.format(0)+value_required_bin_string+'{:008}'.format(0)
        #             if (within_adress == 3):
        #                 req_string = '{:024}'.format(0)+value_required_bin_string

        #             req_value = twos_comp(int(req_string,2), len(req_string))

        #             memory_value_d[(adress//4)] = req_value
        #             memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '011000'): #SH
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             adress = Register_value_d[int(RS1,2)]+IMM_value
        #             mem_line = (adress//4)*4
        #             within_adress = adress-mem_line
        #             #string = Reg_file.iloc[int(RD,2)]["Binary"][2:34]
        #             string = Register_value_b[int(RD,2)]
        #             value_required_bin_string = string[-16:]

        #             if (within_adress == 1 | within_adress == 3):
        #                 print("Memory not accessable")

        #             if (within_adress == 0):
        #                 req_string = value_required_bin_string+'{:024}'.format(0)

        #             if (within_adress == 2):
        #                 req_string = '{:016}'.format(0)+value_required_bin_string+'{:008}'.format(0)

        #             req_value = twos_comp(int(req_string,2), len(req_string))

        #             memory_value_d[(adress//4)] = req_value
        #             memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '011001'): #SW
        #             RS1 = instruction[6:11]
        #             RD = instruction[11:16]
        #             IMM = instruction[16:32]
        #             IMM_value = twos_comp(int(IMM,2), len(IMM))
        #             adress = Register_value_d[int(RS1,2)]+IMM_value
        #             mem_line = (adress//4)*4
        #             within_adress = adress-mem_line
        #             string = Register_value_b[int(RD,2)]

        #             if (within_adress == 1 | within_adress == 3 | within_adress ==2):
        #                 print("Memory not accessable")

        #             if (within_adress == 0):
        #                 req_string = string

        #             req_value = twos_comp(int(req_string,2), len(req_string))

        #             memory_value_d[adress//4] = req_value
        #             memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

        #             if (flag == 0):
        #                 PC +=1
        #             else:
        #                 PC = new_PC
        #                 flag = 0

        #         if (instruction[:6] == '011010'): #BEQZ
        #             RS1 = instruction[6:11]
        #             SO_string = instruction[16:32]
        #             SO_value = twos_comp(int(SO_string,2), len(SO_string))

        #             if (Register_value_d[int(RS1,2)] == 0):
        #                 new_PC = PC+SO_value
        #                 flag = 1
        #                 PC += 1
        #             else:
        #                 PC += 1

        #         if (instruction[:6] == '011011'): #BNEZ
        #             RS1 = instruction[6:11]
        #             SO_string = instruction[16:32]
        #             SO_value = twos_comp(int(SO_string,2), len(SO_string))

        #             if (Register_value_d[int(RS1,2)] != 0):
        #                 new_PC = PC+SO_value
        #                 flag = 1
        #                 PC += 1
        #             else:
        #                 PC += 1

        #         if (instruction[:6] == '011100'): #JR
        #             RS1 = instruction[6:11]
        #             SO_string = instruction[16:32]
        #             SO_value = twos_comp(int(SO_string,2), len(SO_string))
        #             new_PC = Register_value_d[int(RS1,2)]/4 + SO_value
        #             PC += 1
        #             flag = 1

        #         if (instruction[:6] == '011101'): #JALR
        #             RS1 = instruction[6:11]
        #             SO_string = instruction[16:32]
        #             SO_value = twos_comp(int(SO_string,2), len(SO_string))
        #             Register_value_d[31] = PC+2
        #             Register_value_b[31] = '0b{:032b}'.format((PC+2)%(1<<32))
        #             new_PC = Register_value_d[int(RS1,2)]/4 + SO_value
        #             PC += 1
        #             flag = 1

        #         if (instruction[:6] == '011110'): #J
        #             SO_string = instruction[6:32]
        #             SO_value = twos_comp(int(SO_string,2), len(SO_string))
        #             new_PC = PC + SO_value
        #             PC += 1
        #             flag = 1

        #         if (instruction[:6] == '011111'): #JAL
        #             SO_string = instruction[6:32]
        #             SO_value = twos_comp(int(SO_string,2), len(SO_string))
        #             Register_value_d[31] = PC+2
        #             Register_value_b[31] = '0b{:032b}'.format((PC+2)%(1<<32))
        #             new_PC = PC + SO_value
        #             PC += 1
        #             flag = 1

        # print(Reg_file)
        # print(Memory)
        # self.textbox=tk.Text(self.root, height=5, font=('Arial', 16))
        # self.textbox.pack(padx=10, pady=10)

    # def print(self):
    #     # print(self.textbox.get('1.0', tk.END))
    #     messagebox.showinfo(title="Message", message=self.textbox.get('1.0', tk.END))
        # messagebox.showinfo(title="Message", message=self.Reg_file)
        # print(Reg_file)

# MyGUI()


# def twos_comp(val, bits):
#     """compute the 2's complement of int value val"""
#     if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
#         val = val - (1 << bits)        # compute negative value
#     return val


# MyGUI()


# # making reg file (initialize all values in registers to 0)
# Register_no = []
# Register_value_d = []
# Register_value_b = []
# reg_file_dictionary = {"Register" : Register_no, "Decimal" : Register_value_d, "Binary" : Register_value_b}

# for i in range(32):
#     Register_no.append(f"R{i}")

# for i in range(32):
#     Register_value_d.append(0)


# for i in range(32):
#     Register_value_b.append('0b{:032b}'.format(Register_value_d[i]%(1<<32)))

# # making memory (initializing all values to 0)
# memory_adress = []
# memory_value_d = []
# memory_value_b = []
# memory_dictionary = {"Memory Adress": memory_adress, "Decimal": memory_value_d, "Binary": memory_value_b}

# for i in range(0,37,4):
#     memory_adress.append('0x{:08x}'.format(i))

# for i in range(10):
#     memory_value_d.append(0)

# for i in range(10):
#     memory_value_b.append('0b{:032b}'.format(memory_value_d[i]%(1<<32)))

# Instruction_array = ["00000100101001010000000000000101", "00000100101001010000000000000100", "01100100000001010000000000000100", "01011000000000110000000000000100", "01000100101011010000000011111111", "01001000000010100000000000000111"]

# while(PC<len(Instruction_array)):
#     instruction = Instruction_array[PC]
#     if (instruction[:6] == '000000'): #R Type Instructions

#         RS1 = instruction[6:11]
#         RS2 = instruction[11:16]
#         RD = instruction[16:21]

#         if (instruction[-6:] == '000000'): #ADD Instruction
#             answer = Register_value_d[int(RS1,2)]+Register_value_d[int(RS2,2)]
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '000001'): #SUB Instruction
#             answer = Register_value_d[int(RS1,2)]-Register_value_d[int(RS2,2)]
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '000010'): #AND Instruction
#             answer = Register_value_d[int(RS1,2)]&Register_value_d[int(RS2,2)]
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0


#         if (instruction[-6:] == '000011'): #OR Instruction
#             answer = Register_value_d[int(RS1,2)]|Register_value_d[int(RS2,2)]
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '000100'): #XOR Instruction
#             answer = Register_value_d[int(RS1,2)]^Register_value_d[int(RS2,2)]
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '000101'): #SLL Instruction
#             answer = Register_value_d[int(RS1,2)]<<Register_value_d[int(RS2,2)]
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '000110'): #SRL Instruction
#             answer = Register_value_d[int(RS1,2)]>>Register_value_d[int(RS2,2)]
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0


#         if (instruction[-6:] == '001000'): #SLT Instruction
#             if (Register_value_d[int(RS1,2)]<Register_value_d[int(RS2,2)]):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '001001'): #SGT Instruction
#             if (Register_value_d[int(RS1,2)]>Register_value_d[int(RS2,2)]):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '001010'): #SLE Instruction
#             if (Register_value_d[int(RS1,2)]<=Register_value_d[int(RS2,2)]):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '001011'): #SGE Instruction
#             if (Register_value_d[int(RS1,2)]>=Register_value_d[int(RS2,2)]):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '001100'): #ULT Instruction

#             a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
#             b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2)
#             if (a<b):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '001101'): #UGT Instruction

#             a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
#             b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2)
#             if (a>b):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '001110'): #ULE Instruction

#             a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
#             b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2)
#             if (a<=b):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[-6:] == '001111'): #UGE Instruction

#             a = int('0b{:032b}'.format(Register_value_d[int(RS1,2)]%(1<<32)),2)
#             b = int('0b{:032b}'.format(Register_value_d[int(RS2,2)]%(1<<32)),2)
#             if (a>=b):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#     else:
#         if (instruction[:6] == '000001'): #ADDI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             answer = Register_value_d[int(RS1,2)] + IMM_value
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '000010'): #SUBI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             answer = Register_value_d[int(RS1,2)] - IMM_value
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '000011'): #ORI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             answer = Register_value_d[int(RS1,2)] | IMM_value
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '000100'): #ANDI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             answer = Register_value_d[int(RS1,2)] & IMM_value
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '000101'): #XORI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             answer = Register_value_d[int(RS1,2)] ^ IMM_value
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '000110'): #SLLI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             answer = Register_value_d[int(RS1,2)] << IMM_value
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '000111'): #SRLI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             answer = Register_value_d[int(RS1,2)] >> IMM_value
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '001001'): #SLTI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             if (Register_value_d[int(RS1,2)] < IMM_value):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '001010'): #SGTI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             if (Register_value_d[int(RS1,2)] > IMM_value):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0


#         if (instruction[:6] == '001011'): #SLEI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             if (Register_value_d[int(RS1,2)] <= IMM_value):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '001100'): #SGEI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             if (Register_value_d[int(RS1,2)] >= IMM_value):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '001101'): #ULTI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2)
#             if (Register_value_d[int(RS1,2)] < IMM_UNS):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '001110'): #UGTI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2)
#             if (Register_value_d[int(RS1,2)] > IMM_UNS):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '001111'): #ULEI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2)
#             if (Register_value_d[int(RS1,2)] <= IMM_UNS):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '010000'): #UGEI
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2)
#             if (Register_value_d[int(RS1,2)] >= IMM_UNS):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0


#         if (instruction[:6] == '010001'): #LHI (to be completed)
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_UNS = int('0b{:032b}'.format(int(IMM,2)%(1<<32)),2)
#             if (Register_value_d[int(RS1,2)] <= IMM_UNS):
#                 answer = (2**32)-1
#             else:
#                 answer = 0
#             Register_value_d[int(RD,2)] = answer
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format(answer%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0


#         if (instruction[:6] == '010010'): #LB
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             adress = Register_value_d[int(RS1,2)]+IMM_value
#             mem_line = (adress//4)*4
#             within_adress = adress-mem_line
#             #string = Memory.iloc[mem_line/4]["Binary"][2:34]
#             string = memory_value_b[adress//4]
#             print(string)
#             value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+8+2]
#             value_required = twos_comp(int(value_required_bin_string,2), len(value_required_bin_string))
#             Register_value_d[int(RD,2)] = value_required
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '010011'): #LBU
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             adress = Register_value_d[int(RS1,2)]+IMM_value
#             mem_line = (adress//4)*4
#             within_adress = adress-mem_line
#             #string = Memory.iloc[mem_line/4]["Binary"][2:34]
#             string = memory_value_b[adress//4]
#             value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+8+2]
#             value_required = int(value_required_bin_string,2)
#             Register_value_d[int(RD,2)] = value_required
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '010100'): #LH
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             adress = Register_value_d[int(RS1,2)]+IMM_value
#             mem_line = (adress//4)*4
#             within_adress = adress-mem_line
#             #string = Memory.iloc[mem_line/4]["Binary"][2:34]
#             string = memory_value_b[adress//4]
#             if (within_adress == 1 | within_adress == 3):
#                 print("Memory not accessable")
#             value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+16+2]
#             value_required = twos_comp(int(value_required_bin_string,2), len(value_required_bin_string))
#             Register_value_d[int(RD,2)] = value_required
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '010101'): #LHU
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             adress = Register_value_d[int(RS1,2)]+IMM_value
#             mem_line = (adress//4)*4
#             within_adress = adress-mem_line
#             #string = Memory.iloc[mem_line/4]["Binary"][2:34]
#             string = memory_value_b[adress//4]
#             if (within_adress == 1 | within_adress == 3):
#                 print("Memory not accessable")
#             value_required_bin_string = string[2+8*(within_adress):8*(within_adress)+16+2]
#             value_required = int(value_required_bin_string,2)
#             Register_value_d[int(RD,2)] = value_required
#             Register_value_b[int(RD,2)] = '0b{:032b}'.format((value_required)%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '010110'): #LW (Loads the whole 4 bytes; Load byte and Load byte unsigned is litte more complicated)
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             adress = Register_value_d[int(RS1,2)]+IMM_value
#             #value_required_bin_string = Memory.iloc[adress/4]["Binary"][2:34]
#             value_required_bin_string = memory_value_b[adress//4]
#             value_required = int(value_required_bin_string,2)
#             Register_value_d[int(RD,2)] = value_required
#             Register_value_b[int(RD,2)] = value_required_bin_string

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0
#             #mem_adress = '0x{:08x}'.format(adress)
#             #value = Memory[Memory["Memory Adress"] == mem_adress]["Decimal"].iloc[0]
#             #Register_value_d[int(RD,2)] = value
#             #Register_value_b[int(RD,2)] = '0b{:032b}'.format(value%(1<<32))

#         if (instruction[:6] == '010111'): #SB
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             adress = Register_value_d[int(RS1,2)]+IMM_value
#             mem_line = (adress//4)*4
#             within_adress = adress-mem_line
#             #string = Reg_file.iloc[int(RD,2)]["Binary"][2:34]
#             string = Register_value_b[int(RD,2)]
#             value_required_bin_string = string[-8:]

#             if (within_adress == 0):
#                 req_string = value_required_bin_string+'{:024}'.format(0)
#             if (within_adress == 1):
#                 req_string = '{:008}'.format(0)+value_required_bin_string+'{:016}'.format(0)
#             if (within_adress == 2):
#                 req_string = '{:016}'.format(0)+value_required_bin_string+'{:008}'.format(0)
#             if (within_adress == 3):
#                 req_string = '{:024}'.format(0)+value_required_bin_string

#             req_value = twos_comp(int(req_string,2), len(req_string))

#             memory_value_d[(adress//4)] = req_value
#             memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '011000'): #SH
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             adress = Register_value_d[int(RS1,2)]+IMM_value
#             mem_line = (adress//4)*4
#             within_adress = adress-mem_line
#             #string = Reg_file.iloc[int(RD,2)]["Binary"][2:34]
#             string = Register_value_b[int(RD,2)]
#             value_required_bin_string = string[-16:]

#             if (within_adress == 1 | within_adress == 3):
#                 print("Memory not accessable")

#             if (within_adress == 0):
#                 req_string = value_required_bin_string+'{:024}'.format(0)

#             if (within_adress == 2):
#                 req_string = '{:016}'.format(0)+value_required_bin_string+'{:008}'.format(0)


#             req_value = twos_comp(int(req_string,2), len(req_string))

#             memory_value_d[(adress//4)] = req_value
#             memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0

#         if (instruction[:6] == '011001'): #SW
#             RS1 = instruction[6:11]
#             RD = instruction[11:16]
#             IMM = instruction[16:32]
#             IMM_value = twos_comp(int(IMM,2), len(IMM))
#             adress = Register_value_d[int(RS1,2)]+IMM_value
#             mem_line = (adress//4)*4
#             within_adress = adress-mem_line
#             string = Register_value_b[int(RD,2)]


#             if (within_adress == 1 | within_adress == 3 | within_adress ==2):
#                 print("Memory not accessable")

#             if (within_adress == 0):
#                 req_string = string


#             req_value = twos_comp(int(req_string,2), len(req_string))


#             memory_value_d[adress//4] = req_value
#             memory_value_b[(adress//4)] = '0b{:032b}'.format((req_value)%(1<<32))

#             if (flag == 0):
#                 PC +=1
#             else:
#                 PC = new_PC
#                 flag = 0


#         if (instruction[:6] == '011010'): #BEQZ
#             RS1 = instruction[6:11]
#             SO_string = instruction[16:32]
#             SO_value = twos_comp(int(SO_string,2), len(SO_string))

#             if (Register_value_d[int(RS1,2)] == 0):
#                 new_PC = PC+SO_value
#                 flag = 1
#                 PC += 1
#             else:
#                 PC += 1

#         if (instruction[:6] == '011011'): #BNEZ
#             RS1 = instruction[6:11]
#             SO_string = instruction[16:32]
#             SO_value = twos_comp(int(SO_string,2), len(SO_string))

#             if (Register_value_d[int(RS1,2)] != 0):
#                 new_PC = PC+SO_value
#                 flag = 1
#                 PC += 1
#             else:
#                 PC += 1

#         if (instruction[:6] == '011100'): #JR
#             RS1 = instruction[6:11]
#             SO_string = instruction[16:32]
#             SO_value = twos_comp(int(SO_string,2), len(SO_string))
#             new_PC = Register_value_d[int(RS1,2)]/4 + SO_value
#             PC += 1
#             flag = 1

#         if (instruction[:6] == '011101'): #JALR
#             RS1 = instruction[6:11]
#             SO_string = instruction[16:32]
#             SO_value = twos_comp(int(SO_string,2), len(SO_string))
#             Register_value_d[31] = PC+2
#             Register_value_b[31] = '0b{:032b}'.format((PC+2)%(1<<32))
#             new_PC = Register_value_d[int(RS1,2)]/4 + SO_value
#             PC += 1
#             flag = 1

#         if (instruction[:6] == '011110'): #J
#             SO_string = instruction[6:32]
#             SO_value = twos_comp(int(SO_string,2), len(SO_string))
#             new_PC = PC + SO_value
#             PC += 1
#             flag = 1

#         if (instruction[:6] == '011111'): #JAL
#             SO_string = instruction[6:32]
#             SO_value = twos_comp(int(SO_string,2), len(SO_string))
#             Register_value_d[31] = PC+2
#             Register_value_b[31] = '0b{:032b}'.format((PC+2)%(1<<32))
#             new_PC = PC + SO_value
#             PC += 1
#             flag = 1
