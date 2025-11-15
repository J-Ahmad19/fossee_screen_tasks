# FOSSEE Screening Tasks – Structural Analysis & Visualization

This repository contains my submission for the **FOSSEE Winter Internship Screening Task (OSDAG)**.  
It includes Python scripts for extracting, processing, and visualizing **Shear Force Diagrams (SFD)** and **Bending Moment Diagrams (BMD)** based on a structural analysis model.

---

## 🚀 Features

### **Task 1 — 2D SFD/BMD for Central Longitudinal Girder**
- Reads force data from `screening_task1.nc`
- Extracts bending moment (Mz) and shear force (Vy) for each element
- Automatically handles i-end and j-end orientations
- Generates:
  - `BMD_central_girder.png`
  - `SFD_central_girder.png`
- Outputs node-wise force table:
  - `central_girder_Mz_Vy.csv`

---

### **Task 2 — 3D Extruded BMD/SFD for All Longitudinal Girders**
- Uses `element.py` and `node.py` for mesh connectivity and node coordinates  
- Builds continuous node chains for each girder  
- Produces 3D extruded structural diagrams with color mapping  
- Optional ribbon-surface rendering for smoother visuals  
- Generates:
  - `Task2_BMD_3D.png`
  - `Task2_SFD_3D.png`
- Exports a girder-wise max/min summary:
  - `task2_summary.csv`

---

### **📂 Files in Repository**

- task1.py # Task 1 script (2D BMD/SFD)
- task2.py # Task 2 script (3D extruded diagrams)
- screening_task1.nc # Input dataset
- element.py # Element -> [node_i, node_j]
- node.py # Node -> [x, y, z]

- BMD_central_girder.png # Output from Task 1
- SFD_central_girder.png
- central_girder_Mz_Vy.csv

- Task2_BMD_3D.png # Output from Task 2
- Task2_SFD_3D.png
- task2_summary.csv

- requirements.txt # Python dependencies
- README.md # Project documentation


---

## ⚙️ How to Run

### **1. Install requirements**
```bash
pip install -r requirements.txt
```
### Run task 1
python task1.py

### Run task 2
python task2.py

### **🖼 Output Examples**
##Task 1 – Central Girder

BMD_central_girder.png

SFD_central_girder.png

##Task 2 – Longitudinal Girders (3D Extrusions)

Task2_BMD_3D.png

Task2_SFD_3D.png

(Refer to images included in the repository.)

### **📘 Summary of Approach**

Extracts internal force components (Mz_i, Mz_j, Vy_i, Vy_j)

Reconstructs node sequencing along each girder using connectivity

Computes chainage along the X–Z plan

Produces engineering-style 2D and 3D visualization outputs

Saves complete numerical force data in CSV format

Designed to be solver-agnostic as long as force components are provided


### **📄 License**

This project was created for the FOSSEE Internship Screening Task.
You may use or modify the scripts for academic learning or structural analysis studies.
