# DDoS Detection in Software-Defined Networking using Machine Learning

An experimental SDN security project that collects OpenFlow traffic statistics in a **Mininet** network, builds a labeled flow dataset, and trains a **Random Forest** classifier to distinguish normal and high-rate traffic in a simulated environment.

> **Scope:** This repository demonstrates a research/prototype workflow. The current labels are generated using a packet-rate threshold, so evaluation scores should not be interpreted as validated performance on independent, real-world DDoS attacks.

## Overview

- **Network emulation:** Mininet, Open vSwitch, OpenFlow 1.3
- **SDN control and monitoring:** Ryu Controller
- **Traffic features:** packet/byte counts, flow durations, rates, protocol fields
- **Classification:** scikit-learn Random Forest
- **Dataset:** Flow statistics collected at runtime rather than a bundled benchmark dataset
- **Additional experiments:** ML scripts for Decision Tree, KNN, Logistic Regression, Naive Bayes, Random Forest and SVM
- **Experimental mitigation:** separate code exists, but end-to-end blocking effectiveness has not been established

## Architecture

```text
             Mininet network (18 hosts, 6 OVS switches)
                              |
                        OpenFlow 1.3
                              |
                       Ryu Controller
                              |
                Flow stats polling (~5 seconds)
                              |
                 FlowStatsfile.csv (labeled)
                              |
                  Feature preprocessing
                              |
                Random Forest training
                       (75/25 split)
                              |
                Evaluation / prediction
```

The topology connects six switches in a chain, with three hosts attached to each switch. The remote controller is configured at `127.0.0.1:6653` in `Codes/mininet/topology.py`.

## How the pipeline works

1. Start the Ryu flow-statistics collector.
2. Start the Mininet topology and generate benign and simulated attack traffic in the isolated lab.
3. The collector requests flow statistics approximately every **5 seconds**.
4. Flow records are written to `FlowStatsfile.csv`, including packet/byte counts, duration, protocol details, and derived rate features.
5. The collector assigns a training label: `1` when **packets per second (pps) > 20**, otherwise `0`.
6. `Codes/controller/controller.py` drops selected nonnumeric columns, performs a **75% training / 25% testing** split, and trains a Random Forest with **10 trees** and entropy criterion.
7. The controller logs a confusion matrix and accuracy. The code also includes a prediction routine that reads `PredictFlowStatsfile.csv`.

**Implementation note:** The simple `controller.py` monitor loop shown in this repository sleeps but does not itself call `flow_predict()`. The separate experimental `mitigation_module.py` includes periodic prediction logic. These paths should not be described as a verified fully automated detection-and-mitigation service without further integration testing.

## Repository structure

```text
DDoS-Detection-SDN-ML/
├── Codes/
│   ├── controller/
│   │   ├── controller.py                # Random Forest training/prediction logic
│   │   ├── start_traffic_collection.py # OpenFlow stats collection + labels
│   │   ├── collect_ddos_trafic.py
│   │   ├── mitigation_module.py        # Experimental mitigation-related logic
│   │   ├── ML.py
│   │   ├── switch.py
│   │   └── switchm.py
│   ├── mininet/
│   │   ├── topology.py                 # 18-host / 6-switch topology
│   │   ├── generate_benign_trafic.py
│   │   ├── generate_ddos_trafic.py
│   │   └── generate_ddos_trafic1.py
│   ├── ml/
│   │   ├── DT.py
│   │   ├── KNN.py
│   │   ├── LR.py
│   │   ├── NB.py
│   │   ├── RF.py
│   │   ├── SVM.py
│   │   └── ML.py
│   └── Mitigation/                    # Additional experimental module
├── Installation_setup/
│   └── Readme.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Technology stack

| Layer | Tools |
|---|---|
| Network emulation | Mininet, Open vSwitch |
| Controller | Ryu, OpenFlow 1.3 |
| Language | Python |
| Data handling | Pandas, NumPy |
| Machine learning | scikit-learn |
| Environment | Linux / Ubuntu VM recommended |

## Setup and demonstration

The project uses Mininet and Ryu and is intended for a **Linux-based lab or VM**, not a native Windows CMD execution. See [`Installation_setup/Readme.md`](Installation_setup/Readme.md) for the repository's environment instructions.

Clone the repository:

```bash
git clone https://github.com/himnad/DDoS-Detection-SDN-ML.git
cd DDoS-Detection-SDN-ML
```

In a Linux terminal, with Mininet, Open vSwitch, Ryu, Python, Pandas and scikit-learn already installed, start the statistics collector from the controller directory:

```bash
cd Codes/controller
ryu-manager start_traffic_collection.py
```

In another terminal, from the repository root, start the Mininet topology:

```bash
sudo mn -c
sudo python3 Codes/mininet/topology.py
```

Within the Mininet CLI, check connectivity:

```text
pingall
```

The repository includes traffic-generation scripts in `Codes/mininet/`. Run them **only inside an authorized, isolated lab** after reviewing their parameters. The existing README also documents sample Mininet ping commands.

After collecting sufficient labeled data, stop the collector and start the training controller from `Codes/controller/`:

```bash
ryu-manager controller.py
```

This expects `FlowStatsfile.csv` in the current working directory. The model reports training/test metrics in the Ryu logs. Depending on the environment and controller versions, further setup or debugging may be required; the commands above have not been independently executed in this review.

## Evaluation and limitations

The earlier project README reports a confusion matrix of `[[105971, 0], [0, 240]]` and **100% accuracy** in one run. Treat these as **reported results from that experiment**, not independently reproduced benchmarks.

Important limitations:

- **Threshold-derived labels:** `pps > 20` determines the target label, while packet-rate-related features are included in the model input. This makes the task much easier than recognizing independently labeled attacks and can inflate reported accuracy.
- **Class imbalance:** The reported confusion matrix has substantially more normal samples than attack samples.
- **Random row split:** A 75/25 random split may place related flows from the same simulation in both sets, overstating generalization.
- **Simulation-only evaluation:** Results do not establish performance against diverse real-world traffic or attacks.
- **Mitigation not validated:** Experimental mitigation code exists, but robust automated blocking, recovery and false-positive handling need verification.
- **Runtime-generated CSV:** Training depends on collecting the required flow data first.

### Recommended next experiments

1. Label traffic using **independent attack/benign generation ground truth**, not the same feature threshold used for prediction.
2. Evaluate on separate traffic-generation sessions and topology configurations.
3. Report precision, recall, F1, false-positive rate, confusion matrix and detection latency alongside accuracy.
4. Compare Random Forest with the additional ML scripts using the same reproducible splits.
5. Test mitigation only in a controlled lab and document the exact switch rules and recovery behavior.

## Project documentation

- [Environment setup](Installation_setup/Readme.md)
- [Contribution guidelines](CONTRIBUTING.md)
- [License](LICENSE)

## Author

**Akhil Himnad** — [GitHub](https://github.com/himnad)

## License

Released under the [MIT License](LICENSE).
