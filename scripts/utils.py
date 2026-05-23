'''
Code contributed by Anh Tung Ho
'''

import numpy as np
import os
from dataclasses import dataclass
from pathlib import Path
import sys
import subprocess

# Input and output file
abs_path = os.path.realpath(os.path.join(Path(__file__).resolve(),"..",".."))
nTOP_path = os.path.join(abs_path, "nTOP_file") 
dyna_path = os.path.join(abs_path, "DYNA_file")
input_origin_dir = os.path.join(dyna_path, "system_dyna.k")
output_modify_dir = os.path.join(dyna_path, "system_dyna_setup.k")
output_modify_dir = os.path.join(dyna_path, "system_dyna_final.k")

BIT_ORDER = [0, 8, 8+16, 8+16*2, 8+16*3]

@dataclass
class Node:
    id: int
    x: float
    y: float
    z: float

def make_node_from_line(line:str) -> Node:
    '''
    Take the index of element in line 
    '''
    # line = line.strip()
    # line = line.split()
    # return int(line[2])
    id = int(line[BIT_ORDER[0]:BIT_ORDER[1]])
    x = float(line[BIT_ORDER[1]:BIT_ORDER[2]])
    y = float(line[BIT_ORDER[2]:BIT_ORDER[3]])
    z = float(line[BIT_ORDER[3]:BIT_ORDER[4]])

    node = Node(id,x,y,z)
    return node

def make_node_info(line:str):
    """
    Create info from line
    """
    line = line.strip()
    line = line.split()
    node_info = {"id":int(line[0]), "position":[float(ele) for ele in line[1:]]}
    return node_info

def cut_redundant(input_dir: str, output_dir: str):
    """
    Read input file and return all lines as well as the 
    """
    isWrite = True
    
    # Open read input file
    with open(input_dir, "r") as input_file, open(output_dir, "w") as output_file:
        lines = input_file.readlines()
        for line in lines:
            # put all input lines into output file
            if line.strip() == "*END": 
                output_file.write(line)
                break

            if line.strip() == "$***       Element properties": 
                isWrite = False

            if isWrite:
                output_file.write(line)
            else:
                continue

def add_part_id(input_dir: str, output_dir: str, part_name: str, part_id: int):
    """
    Add part id for objects
    """
    # Open read input file
    with open(input_dir, "r") as input_file:
        lines = input_file.readlines()

    # Find the index of the *END line
    end_index = lines.index("$***       Nodes\n")

    # Create the new *PART section
    new_part = (
        f"*PART\n"
        f"$# title\n"
        f"{part_name:<80}\n"
        f"$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid\n"
        f"         {part_id:<9} 0         0 \n"
    )

    # Insert the new *PART section before the *END line
    lines.insert(end_index, new_part)

    # Write the updated content back to the file
    with open(output_dir, "w") as output_file:
        output_file.writelines(lines)

def get_nodes(input_dir: str):
    """
    
    """
    startNode = False
    nodes = []
    
    # Get nodes from file 
    with open(input_dir, "r") as input_file:
        lines = input_file.readlines()
        for (i,line) in enumerate(lines):
            if line.strip() == "*NODE":
                startNode = True
                continue
            if len(line.strip().split()) == 0:
                continue
            if line.strip().split()[0] == "$#":
                continue
            if line.strip() == "$***       Elements":
                break
            if startNode:
                node = make_node_from_line(line) # get (id,[x,y,z]) of node
                nodes.append(node) # save node to list 

    # Build KD tree
    # kd_tree = KDTree(nodes)

    # Define range 
    x_range = (-100, 100)
    y_range = (-1, 0.05)
    z_range = (-100, 100)

    # selected id
    sid = {"fixed_constraint": [],
           "initial_velocity": [],
           "head_model": []}

    for node in nodes:
        if (x_range[0] <= node.x <= x_range[1]) and \
            (y_range[0] <= node.y <= y_range[1]) and \
            (z_range[0] <= node.z <= z_range[1]):
                sid["fixed_constraint"].append(node.id)
        if (node.y <= 50):
            sid["initial_velocity"].append(node.id)
        if (node.y >= 51):
            sid["head_model"].append(node.id)

    return sid 

def get_nodesets_lattice(input_dir: str):
    """
    Create node sets for given lattice
    """
    startNode = False
    nodes = []
    
    # Get nodes from file 
    with open(input_dir, "r") as input_file:
        lines = input_file.readlines()
        for (i,line) in enumerate(lines):
            if line.strip() == "*NODE":
                startNode = True
                continue
            if len(line.strip().split()) == 0:
                continue
            if line.strip().split()[0] == "$#":
                continue
            if line.strip() == "$***       Elements":
                startNode = False
            if line.strip() == "*PART":
                startNode = False
            if line.strip() == "*END":
                break
            if startNode:
                node = make_node_from_line(line) # get (id,[x,y,z]) of node
                nodes.append(node) # save node to list 

    # Build KD tree
    # print(len(nodes))

    # Define range 
    x_range = (-100, 100)
    y_range = (-5, 0.5)
    z_range = (-100, 100)

    # selected id
    sid = {
        "fixed_constraint": [],
        "initial_velocity": [],
    }

    for node in nodes:
        if (x_range[0] <= node.x <= x_range[1]) and \
            (y_range[0] <= node.y <= y_range[1]) and \
            (z_range[0] <= node.z <= z_range[1]):
                sid["fixed_constraint"].append(node.id)
        if (node.y >= 0):
            sid["initial_velocity"].append(node.id)

    return sid 


def add_failure_strain(input_dir: str, output_dir: str, strain_failure:float = 0.0):
    """
    change failure
    """
    with open(input_dir, "r") as input_file:
        lines = input_file.readlines()
    
    # Find the all linear plastic material 
    line_id = []
    for (id,line) in enumerate(lines):
        if "*MAT_PIECEWISE_LINEAR_PLASTICITY" in line:
            line_id.append(id)
    
    # Modify
    edit_line_id = line_id[0]+2
    edit_line = list(lines[edit_line_id])
    modify_content = (10-len(str(strain_failure)))*' ' + str(strain_failure)
    for i in range(10):
        edit_line[60+i] = modify_content[i]

    lines[edit_line_id] = ''.join(edit_line)

    # Save file
    with open(output_dir, "w") as output_file:
        output_file.writelines(lines)

def run_ls_prepost(cfile="merge_nodes.cfile"):
    """
    Runs LS-PrePost in batch mode to process a command file (cfile) to merge nodes within a threshold.
    
    Parameters:
    ===
        cfile: Name (or path) of the command file.
    """
    # Construct the command
    exe = r"C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64\lsprepost411\lsprepost4.11.exe"
    cfile = os.path.join(dyna_path, cfile)
    
    cmd = [exe]
    cmd.append(f"c={cfile}")
    cmd.append("-nographics")
    
    # Execute the command
    try:
        subprocess.run(cmd, 
                       timeout=10, 
                       stderr=subprocess.DEVNULL, 
                       stdout=subprocess.DEVNULL,
                       text=False)
        print(f"Command executed successfully: {' '.join(cmd)}")
    except subprocess.CalledProcessError as e:
        print(f"Error running LS-PrePost: {e}")
    except FileNotFoundError:
        print(f"Executable not found: {exe}. Make sure the path is correct or in your system PATH.")

# def run_dyna(k_file: str, ncpu: int=16, memory: int=200, shell=False, text=False):
#     """
#     Call LS-Run for given k_file with number of cpu and memmory
#     """
#     run_file_path = os.path.abspath(k_file)
#     run_file_folder = os.path.abspath(os.path.join(run_file_path,".."))

#     ls_env_setup = r'C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64\lsprepost411\LS-Run\lsdynamsvar.bat'
#     ls_solver = r'C:\Program Files\ANSYS Inc\v242\ansys\bin\winx64\lsdyna_dp.exe'
    
#     # Command for LS Dyna
#     ls_dyna_command = [ls_env_setup, '&&', ls_solver]
#     ls_dyna_command.append('i=' + run_file_path)
#     ls_dyna_command.append('ncpu=' + str(ncpu))
#     ls_dyna_command.append('memory=' + str(memory) + 'm')

#     try:
#         subprocess.run(ls_dyna_command, 
#                        shell=shell, 
#                        text=text,
#                        # stdout=subprocess.DEVNULL, 
#                        # stderr=subprocess.DEVNULL,
#                        cwd=run_file_folder)
#         print(f"LS-Dyna executed successfully with command: {' '.join(ls_dyna_command)}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error running LS-Dyna: {e}")
#     except FileNotFoundError:
#         print(f"Executable not found: {ls_solver}. Make sure the path is correct or in your system PATH.")

def run_dyna(ls_solver: str, k_file: str, run_folder: str, ncpu: int=16, memory: int=200, text=True):
    """
    Call LS-Run for given k_file with number of cpu and memmory
    """
    run_folder = os.path.abspath(run_folder)
    
    # Command for LS Dyna
    cmd = [
        ls_solver,
        f"i={k_file}",
        f"ncpu={ncpu}",
        f"memory={memory}m",
    ]

    print(f"Running LS-Dyna with command: {' '.join(cmd)} in folder: {run_folder}")

    try:
        process = subprocess.Popen(
            cmd,
            cwd=run_folder,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            print(line, end="")
            sys.stdout.flush()

        return_code = process.wait()

        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, cmd)

        print("LS-DYNA completed successfully.")

    except FileNotFoundError:
        print(f"Executable not found: {cmd[0]}")

def HIC_calculation(time: np.ndarray, acc: np.ndarray, duration: int = 15):
    def hic_cal(start_ind, end_ind):
        if end_ind <= start_ind:
            return 0.0
        delta_T = time[end_ind] - time[start_ind]
        if delta_T <= 0:
            return 0.0
        area = np.trapz(acc[start_ind:end_ind + 1], time[start_ind:end_ind + 1])
        return (area ** 2.5) / (delta_T ** 1.5)  # clearer form of the same formula

    n = len(time)
    if n < 2:
        return 0.0, time[0] if n == 1 else 0.0

    max_duration = (time[-1] - time[0]) if duration == -1 else duration / 1000.0

    max_HIC = 0.0
    time_at_max_HIC = time[0]
    index_at_max_HIC = 0
    end_ind_at_max_HIC = 0
    end_ind = 0

    for start_ind in range(n):
        # Slide end_ind forward while within allowed duration
        while end_ind < n and (time[end_ind] - time[start_ind]) <= max_duration:
            end_ind += 1

        # end_ind reached array end — no more valid windows
        if end_ind == n:
            break

        # end_ind is now 1 past the last valid point, so pass end_ind - 1
        if end_ind - 1 > start_ind:
            hic = hic_cal(start_ind, end_ind - 1)
            if hic >= max_HIC:
                max_HIC = hic
                time_at_max_HIC = time[start_ind]
                index_at_max_HIC = start_ind
                end_ind_at_max_HIC = end_ind - 1

        if end_ind < start_ind + 1:
            end_ind = start_ind + 1

    return max_HIC, time_at_max_HIC, index_at_max_HIC, end_ind_at_max_HIC
 
# def HIC_calculation(time:np.array, acc: np.array, duration: int=15):
#     """
#     calculate HIC with duration of collision (15mm,36ms or infinite -1)
#     """
#     # Function to Find first element in array larger than target value 
#     def find_first_larger(arr, target, start):
#         left, right = start, len(arr) - 1
#         result = -1  # Default value if no element is found

#         while left <= right:
#             mid = (left + right) // 2
#             if arr[mid] >= target:
#                 result = mid # Save the best value
#                 right = mid - 1  # Move left to find the first occurrence
#             else:
#                 left = mid + 1  # Move right to continue searching

#         return result

#     # Function to calculate HIC over given period 
#     def hic_cal(start_ind, end_ind):
#         area = np.trapz(acc[start_ind:end_ind], time[start_ind:end_ind])
#         delta_T = time[end_ind] - time[start_ind]
#         return delta_T*pow((area/delta_T),2.5)

#     # Main loop to calculate max HIC over period
#     end_period = time[-1]
#     max_HIC = 0
#     time_at_max_HIC = time[0]
#     start_search_ind = 0

#     if duration == -1:
#         duration = end_period - time[0]
#     else:
#         duration /= 1000 # second

#     for current_ind in range(len(time)):
#         # Check termination condition 
#         current_time = time[current_ind]
#         target_time = current_time + duration
        
#         if target_time > end_period:
#             break 
        
#         # Find index of element larger than duration
#         end_period_ind = find_first_larger(time, target_time, start_search_ind)
#         start_search_ind = end_period_ind

#         # calculate HIC from start_ind to end_ind
#         hic = hic_cal(start_ind=current_ind,end_ind=end_period_ind)

#         if hic >= max_HIC:
#             max_HIC = hic 
#             time_at_max_HIC = current_time

#     return max_HIC, time_at_max_HIC

def peak_acc_calculate(acc: np.array):
    """
    Calculate peak acceleration
    """
    return np.max(acc)

def extract_data(dyna_path, nodes_id):
    """
    Extract time(second) and acceleration(g) of result
    """
    from ansys.dpf import core as dpf
    # Create model and load data
    d3plot = os.path.join(dyna_path, "d3plot")
    ds = dpf.DataSources()
    ds.set_result_file_path(d3plot, "d3plot")
    model = dpf.Model(ds)

    # Extract time and all acceleration
    time = np.array(model.metadata.time_freq_support.time_frequencies.data)/1000 # second unit
    acceleration_field_container:dpf.FieldsContainer = model.results.acceleration.on_all_time_freqs.eval()

    # Get acceleration of head nodes over_time
    acceleration = []
    for time_ind in range(len(time)):
        # average (ax,ay,az) of nodes in head (ax,ay,az)
        acc_head_nodes = np.zeros([len(nodes_id), 3])
        for (id_ind, node_id) in enumerate(nodes_id):
            acc_head_nodes[id_ind] = acceleration_field_container[time_ind].get_entity_data_by_id(node_id).squeeze()
        acc_head_nodes_avg = np.average(acc_head_nodes, axis=0)
        
        # average acc over components
        acc_avg = np.sqrt(np.sum(np.square(acc_head_nodes_avg),axis=0)) # mm/ms^2 unit
        acc_avg = acc_avg/(9.8E-3) # gravity unit
        acceleration.append(acc_avg) 

    acceleration = np.array(acceleration) # convert to np

    return time, acceleration