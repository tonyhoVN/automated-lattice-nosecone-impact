'''
Code contributed by Anh Tung Ho
'''

import os
import subprocess
import json

def login(email,password):
    """ Log in to nTop Platform using command line interface """
    exePath = r"C:/Program Files/nTopology/nTop Platform/nTopCL.exe"
    arguments = [exePath]
    arguments.append("-u ")
    arguments.append(email)
    arguments.append("-w ")
    arguments.append(password)
    print(arguments)
    subprocess.call(arguments)
    #subprocess.call("C:/Program Files/nTopology/nTop Platform/ntopcl.exe -u",email," -w",password)
    
def json_template(ntopfile):
    """ Generate json input template from nTop file """
    exePath = r'ntopcl.exe'
    run_file_path = os.path.abspath(ntopfile)
    run_file_folder = os.path.dirname(run_file_path)

    ## Put together string that calls nTop with input and output JSON databases
    arguments = [exePath]
    arguments.append("-t")
    arguments.append(ntopfile)
    subprocess.call(arguments, cwd=run_file_folder)
    
    
def run_json(GUI:bool,save:bool, jsonin, jsonout, ntopfile, verbose=2):
    """
    Run nTop with JSON input and output files
    """
    run_file_path = os.path.abspath(ntopfile)
    run_file_folder = os.path.abspath(os.path.join(run_file_path,".."))
    

    if GUI:
        exePath = r'ntop.exe'
    else:
        exePath = r'ntopcl.exe'
        


    ## Put together string that calls nTop with input and output JSON databases
    arguments = [exePath]
        
    if save:
        arguments.append("-s -j")
    else:
        arguments.append("-j")
        
    arguments.append(jsonin)
    
    arguments.append("-o")
    arguments.append(jsonout)

    arguments.append("-v")
    arguments.append(str(verbose))

    arguments.append(ntopfile)
    #arguments.        
    arguments = " ".join(arguments)

    print('Starting...')
    print('')
    # run nTop
    print(arguments)
    subprocess.call(arguments, cwd=run_file_folder)
    
def numtext(GUI,save,Inputs,nTopFile):

    Current_Directory = os.path.dirname(os.path.abspath('__file__'))

    if GUI:
        exePath = r'ntop.exe'
    else:
        exePath = r'ntopcl.exe'
    
    Argument_Values = [exePath]
    
    Argument_String = [r"%s"]

    # The formmating below automatically adds the unit 'mm' to the numeric inputs
    Real_Input   = r"-i %0.6f"
    String_Input = r"-i %s"

    for key in Inputs:
        if type(Inputs[key]) is float:
            Argument_String.append(Real_Input)
            Argument_Values.append(Inputs[key])
        if type(Inputs[key]) is str:
            Argument_String.append(String_Input)
            Argument_Values.append(Inputs[key])
        else:
            pass
        
    if save:
        Argument_String.append("-s")  
        
    Argument_String.append(r"%s")
    Argument_Values.append(nTopFile)
    
    AS = " ".join(Argument_String)

    arguments = (AS % (*Argument_Values,))
    print(arguments)
    subprocess.call(arguments)

def edit_json_input(input_template_path: str, input_json_path: str, Inputs:dict):
    """
    Generate input json file from given user inputs
    """
    # Read template json file
    with open(input_template_path, "r") as inputfile:
        data_input = json.load(inputfile)

    # Change input parameters
    for keyname in Inputs.keys():      
        for (i,input) in enumerate(data_input["inputs"]):
            if input["name"] == keyname:
                data_input["inputs"][i]["value"] = Inputs[keyname]

    # make json input file 
    with open(input_json_path, 'w') as outfile:
        json.dump(data_input, outfile, indent=4)

def get_json_output(output_json_path: str):
    from json import load
    with open(output_json_path, 'r') as output_file:
        output_file = load(output_file)

    return output_file[0]["value"]["val"]