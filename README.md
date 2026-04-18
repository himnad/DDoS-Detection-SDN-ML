

---

```markdown
# DDoS Detection using SDN and Machine Learning

## Overview
This project implements a real-time DDoS detection system using Software Defined Networking (SDN) and Machine Learning.

The system uses:
- Mininet to simulate network topology and traffic  
- Ryu Controller to monitor network flows and collect statistics  
- Machine Learning (Random Forest) to classify traffic as normal or attack  

Unlike static datasets, this project generates real-time network data, making it more practical and dynamic.

---

## What is a DDoS Attack?

A Distributed Denial of Service (DDoS) attack occurs when multiple compromised systems flood a target with excessive traffic, making it unavailable to legitimate users.

### Key Characteristics:
- High traffic volume  
- Multiple distributed sources  
- Resource exhaustion  
- Service disruption  

---

## DDoS Attack Visualization

![DDoS Attack](https://i.postimg.cc/sfYf2DGQ/Chat-GPT-Image-Apr-18-2026-01-49-04-PM.png)

---

## System Architecture & Working

![System Workflow](https://i.postimg.cc/rwhvp79J/Screenshot-2026-04-18-134009.png)

### Workflow

```

Mininet → Traffic Generation → Ryu Controller → Flow Statistics → CSV Dataset → ML Model → Detection

```

---

## Implementation Details

### 1. Network Simulation (Mininet)
- Custom topology created using `topology.py`
- Multiple hosts and switches simulated
- Connected to Ryu controller using OpenFlow

---

### 2. Traffic Generation
Traffic is generated inside Mininet:

- Normal Traffic
```

h1 ping h2

```

- DDoS-like Traffic
```

h1 ping -f h2

````

---

### 3. Flow Statistics Collection (Ryu)

- Implemented in: `start_traffic_collection.py`
- Uses OpenFlow messages to collect flow stats every 5 seconds
- Extracts:
- packet_count  
- byte_count  
- flow duration  
- protocol details  

---

### 4. Feature Engineering

Calculated features include:

- Packets per second (pps)
- Bytes per second (bps)
- Flow duration
- Source/Destination details

---

### 5. Real-Time Dataset Creation

- Dataset file: `FlowStatsfile.csv`
- Generated dynamically during runtime
- Each flow is labeled using logic:

```python
if pps > 20:
  label = 1  # DDoS
else:
  label = 0  # Normal
````

No external dataset is used. Data is fully generated in real time.

---

### 6. Machine Learning Model

Implemented in: `controller.py`

* Algorithm: Random Forest Classifier
* Library: scikit-learn
* Train-test split: 75% / 25%

#### Preprocessing:

* Dropped non-numeric fields:

  * flow_id
  * ip_src
  * ip_dst

---

### 7. Model Training & Evaluation

* Model trained on generated dataset
* Evaluation metrics:

  * Confusion Matrix
  * Accuracy

Example output:

```
Confusion Matrix:
[[105971      0]
 [     0    240]]

Accuracy: 100%
```

---

### 8. Detection Phase

* New flow data is processed

* Model predicts:

  * 0 → Normal
  * 1 → DDoS

* System can identify:

  * Presence of attack
  * Potential victim host

---

## Development Environment

* Host System: Windows
* Virtualization: Oracle VirtualBox
* Guest OS: Ubuntu 20.04.6 LTS (Focal Fossa)
* Ubuntu downloaded using IDM for faster transfer

---

## Tools and Technologies

* Mininet
* Ryu Controller
* Python 3
* Scikit-learn
* Pandas, NumPy
* Git and GitHub

---

## Installation and Setup

### Clone Repository

```
git clone https://github.com/himnad/DDoS-Detection-SDN-ML.git
cd DDoS-Detection-SDN-ML
```

---

## Execution Steps

### Terminal 1 — Ryu (Data Collection)

```
cd Codes/controller
rm -f FlowStatsfile.csv
ryu-manager start_traffic_collection.py
```

---

### Terminal 2 — Mininet

```
sudo mn -c
cd Codes/mininet
sudo -E python3 topology.py
```

Inside Mininet:

```
pingall
```

Expected output: 0% dropped

---

### Traffic Generation

```
h1 ping h2
h1 ping -f h2
```

---

### Terminal 3 — Dataset Check

```
cd Codes/controller
grep ",1" FlowStatsfile.csv
```

---

### Terminal 4 — Machine Learning Execution

```
ryu-manager controller.py
```

---

## Results

* Successfully detects DDoS traffic
* Real-time dataset generation
* High classification accuracy

---

## Limitations

* Simulated environment (Mininet)
* Threshold-based labeling
* Limited real-world variability

---

## Future Enhancements

* Real-time mitigation (blocking attackers)
* Deep Learning models (LSTM, CNN)
* Integration with real networks
* Adaptive thresholding

---
<h2> References</h2>

Here are some related papers

[[1] Dong Li,Chang Yu, Qizhao Zhou and Junqing Yu .”Using SVM to Detect DDoS Attacks in SDN Network.” 2018 IOP Conf. Ser.: Mater. Sci. Eng. 466 012003,2018 .](https://iopscience.iop.org/article/10.1088/1757-899X/466/1/012003/meta)

[[2] Yijie Li, Boyi Liu, Shang Zhai and Mingrui Chen ,”DDoS attack detection method based on feature extraction of deep belief networks.”,IOP Conference Series: Earth and Environmental Science, Volume 252, Issue 3,2019.](https://iopscience.iop.org/article/10.1088/1755-1315/252/3/032013/met)

[[3] Peng Xiao,Wenyu Qu,Heng Qi ,Zhiyang Li.”Detecting DDoS attacks against data centers with correlation analysis.”,Computer Communications 67,2015.](https://www.sciencedirect.com/science/article/abs/pii/S0140366415002285)

[[4] Fatima Khashab, Joanna Moubarak, Antoine Feghali , and Carole Bassil.”DDoS Attack Detection and Mitigation in SDN using Machine Learning”,IEEE 7th International Conference on Network Softwarization (NetSoft),2021.](https://ieeexplore.ieee.org/abstract/document/9492558/)

[[5] Bawany NZ, Shamsi JA, Salah K. DDoS attack detection and mitigation  using
 SDN:     methods, practices, and solutions. Arabian Journal for Science and 
 Engineering. 2017 Feb;42(2):425-41.](https://link.springer.com/article/10.1007/s13369-017-2414-5)


[[6] Dharma, N.G., Muthohar, M.F., Prayuda, J.A., Priagung, K. and Choi, D., 2015,
August. Time-based DDoS detection and mitigation for SDN controller. In 
2015 17th Asia-Pacific Network Operations and Management Symposium (APNOMS) (pp. 550-553). IEEE.](https://ieeexplore.ieee.org/abstract/document/7275389/)
            
[[7]  da Silveira Ilha, A., Lapolli, A.C., Marques, J.A. and Gaspary, L.P., 2020. Euclid: A fully in-network, P4-based approach for real-time DDoS attack detection and mitigation. IEEE Transactions on Network and Service Management, 18(3), pp.3121-3139.](https://ieeexplore.ieee.org/abstract/document/9311137/)

    
[[8] Singh, J. and Behal, S., 2020. Detection and mitigation of DDoS attacks in SDN: A comprehensive review, research challenges and future directions. Computer Science Review, 37, p.100279.](https://www.sciencedirect.com/science/article/abs/pii/S1574013720301647)


[[9] Mihoub A, Fredj OB, Cheikhrouhou O, Derhab A, Krichen M. Denial of service attack detection and mitigation for internet of things using looking-back-enabled machine learning techniques. Computers & Electrical Engineering. 2022 Mar 1;98:107716.](https://www.sciencedirect.com/science/article/abs/pii/S0045790622000337)


[[10] Miao, R., Yu, M. and Jain, N., 2014. Nimbus: cloud-scale attack detection and mitigation. Acm sigcomm computer communication review, 44(4), pp.121-122.](https://www.researchgate.net/publication/286424649_NIMBUS)


[[11] Srinivasan, Karthik, Azath Mubarakali, Abdulrahman Saad Alqahtani, and A. Dinesh Kumar. "A survey on the impact of DDoS attacks in cloud computing: prevention, detection and mitigation techniques." In Intelligent Communication Technologies and Virtual Mobile Networks, pp. 252-270. Springer, Cham, 2019.](https://www.springerprofessional.de/en/a-survey-on-the-impact-of-ddos-attacks-in-cloud-computing-preven/17060314)


[[12] Kautish, Sandeep, A. Reyana, and Ankit Vidyarthi. "SDMTA: Attack Detection and Mitigation Mechanism for DDoS Vulnerabilities in Hybrid Cloud Environment." IEEE Transactions on Industrial Informatics (2022).](https://ieeexplore.ieee.org/document/9695185)


[[13] Gadze, James Dzisi, Akua Acheampomaa Bamfo-Asante, Justice Owusu Agyemang, Henry Nunoo-Mensah, and Kwasi Adu-Boahen Opare. "An investigation into the application of deep learning in the detection and mitigation of DDOS attack on SDN controllers." Technologies 9, no. 1 (2021): ](https://www.mdpi.com/2227-7080/9/1/14)


[[14] Jaramillo, L.E.S., 2018. Malware detection and mitigation techniques: lessons learned from Mirai DDOS attack. Journal of Information Systems Engineering & Management, 3(3), p.19.](https://www.researchgate.net/publication/326425061_Malware_Detection_and_Mitigation_Techniques_Lessons_Learned_from_Mirai_DDOS_Attack)


[[15] Al-Duwairi, B., Al-Kahla, W., AlRefai, M.A., Abedalqader, Y., Rawash, A. and Fahmawi, R., 2020. SIEM-based detection and mitigation of IoT-botnet DDoS attacks. International Journal of Electrical and Computer Engineering, 10(2), p.2182.](https://ijece.iaescore.com/index.php/IJECE/article/view/20812)

## Author

Akhil Himnad
GitHub: [https://github.com/himnad](https://github.com/himnad)

```


