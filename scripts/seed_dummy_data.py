#!/usr/bin/env python3

"""
Seed Dummy Data
================
Populates the DuckDB database with ~30 realistic IEEE-style papers spread
across three categories (machine learning, power electronics, robotics) so
the dashboard has meaningful content to display.

Usage:
    cd <project-root>
    .venv/bin/python scripts/seed_dummy_data.py
"""

import random
from datetime import date, timedelta

from ieee_papers_mapper.config import config as cfg
from ieee_papers_mapper.data.database import Database

# ---------------------------------------------------------------------------
# Dummy data definitions
# ---------------------------------------------------------------------------

ML_PAPERS = [
    {
        "title": "A Scalable Transformer Architecture for Low-Resource Language Modelling",
        "abstract": (
            "We propose a lightweight transformer variant that achieves competitive "
            "perplexity on low-resource languages while reducing parameter count by 60%. "
            "Experiments on six African language benchmarks demonstrate consistent "
            "improvements over baseline models."
        ),
        "ieee_terms": ["natural language processing", "transformer networks", "language models"],
        "dynamic_terms": ["low-resource NLP", "parameter efficiency", "African languages"],
    },
    {
        "title": "Federated Learning With Differential Privacy for Medical Image Classification",
        "abstract": (
            "This paper introduces a federated learning framework that incorporates "
            "differential privacy guarantees while maintaining high classification accuracy "
            "on chest X-ray datasets. Our approach reduces communication overhead by 45% "
            "compared to FedAvg."
        ),
        "ieee_terms": ["federated learning", "privacy", "medical imaging"],
        "dynamic_terms": ["differential privacy", "chest X-ray classification", "communication efficiency"],
    },
    {
        "title": "Self-Supervised Contrastive Learning for Time-Series Anomaly Detection",
        "abstract": (
            "We present a contrastive pretraining strategy for multivariate time-series "
            "data that significantly improves downstream anomaly detection without labelled "
            "examples. Evaluation on three industrial benchmarks shows F1 gains of 8-12%."
        ),
        "ieee_terms": ["anomaly detection", "unsupervised learning", "time series analysis"],
        "dynamic_terms": ["contrastive learning", "self-supervised pretraining", "industrial IoT"],
    },
    {
        "title": "Graph Neural Networks for Combinatorial Optimisation on Large-Scale Instances",
        "abstract": (
            "This work applies graph neural networks to NP-hard combinatorial problems, "
            "demonstrating near-optimal solutions on instances with up to 10,000 nodes. "
            "Our GNN-guided search achieves a 3x speed-up over state-of-the-art solvers."
        ),
        "ieee_terms": ["graph neural networks", "combinatorial optimization", "heuristic algorithms"],
        "dynamic_terms": ["NP-hard problems", "scalable inference", "vehicle routing"],
    },
    {
        "title": "Efficient Fine-Tuning of Vision-Language Models via Adapter Layers",
        "abstract": (
            "We investigate adapter-based fine-tuning for CLIP-style vision-language models "
            "on domain-specific tasks. Results on satellite imagery and medical scans show "
            "that adapters match full fine-tuning performance at 5% of the compute cost."
        ),
        "ieee_terms": ["transfer learning", "computer vision", "multimodal learning"],
        "dynamic_terms": ["adapter layers", "vision-language models", "domain adaptation"],
    },
    {
        "title": "Bayesian Hyperparameter Optimisation for Deep Reinforcement Learning",
        "abstract": (
            "Tuning hyperparameters in deep RL is notoriously expensive. We propose a "
            "Bayesian optimisation scheme that exploits task similarity to warm-start the "
            "search, reducing wall-clock time by 70% on Atari and MuJoCo benchmarks."
        ),
        "ieee_terms": ["reinforcement learning", "Bayesian optimization", "hyperparameter tuning"],
        "dynamic_terms": ["deep RL", "warm-start transfer", "sample efficiency"],
    },
    {
        "title": "Attention-Based Multi-Task Learning for Autonomous Driving Perception",
        "abstract": (
            "A shared attention backbone is proposed for joint object detection, lane "
            "segmentation, and depth estimation in autonomous driving. The multi-task model "
            "outperforms separate networks while using 40% fewer parameters."
        ),
        "ieee_terms": ["object detection", "attention mechanisms", "autonomous vehicles"],
        "dynamic_terms": ["multi-task learning", "lane segmentation", "depth estimation"],
    },
    {
        "title": "Continual Learning Without Catastrophic Forgetting: A Regularisation Perspective",
        "abstract": (
            "We unify existing regularisation-based continual-learning methods under a "
            "single theoretical framework and derive a new penalty term that outperforms "
            "EWC and SI on Split-CIFAR and Permuted-MNIST benchmarks."
        ),
        "ieee_terms": ["neural networks", "learning systems", "regularization"],
        "dynamic_terms": ["continual learning", "catastrophic forgetting", "elastic weight consolidation"],
    },
    {
        "title": "Sparse Mixture-of-Experts for Energy-Efficient Edge Inference",
        "abstract": (
            "We design a sparse mixture-of-experts layer optimised for mobile hardware, "
            "achieving 2.5x throughput improvement on edge TPUs. Accuracy on ImageNet "
            "remains within 0.3% of the dense baseline."
        ),
        "ieee_terms": ["neural network architecture", "edge computing", "energy efficiency"],
        "dynamic_terms": ["mixture of experts", "model sparsity", "edge inference"],
    },
    {
        "title": "Generative Adversarial Networks for Synthetic Tabular Data Augmentation",
        "abstract": (
            "Generating realistic synthetic tabular data is challenging due to mixed column "
            "types. Our conditional GAN preserves inter-column correlations and passes "
            "statistical fidelity tests on five real-world financial datasets."
        ),
        "ieee_terms": ["generative adversarial networks", "data augmentation", "data privacy"],
        "dynamic_terms": ["tabular data synthesis", "conditional generation", "financial data"],
    },
    {
        "title": "Knowledge Distillation From Large Language Models to Compact Classifiers",
        "abstract": (
            "We distill the reasoning capabilities of a 70B-parameter language model into "
            "a 125M classifier for sentiment analysis and intent detection. The student "
            "model retains 95% of the teacher's accuracy at 500x lower latency."
        ),
        "ieee_terms": ["knowledge distillation", "natural language processing", "model compression"],
        "dynamic_terms": ["large language models", "compact classifiers", "inference latency"],
    },
    {
        "title": "Physics-Informed Neural Networks for Partial Differential Equation Solvers",
        "abstract": (
            "Physics-informed neural networks embed PDE constraints directly into the loss "
            "function, enabling mesh-free solutions. We extend this approach to turbulent "
            "fluid dynamics and demonstrate convergence guarantees on Navier-Stokes problems."
        ),
        "ieee_terms": ["neural networks", "differential equations", "scientific computing"],
        "dynamic_terms": ["physics-informed learning", "fluid dynamics", "mesh-free solvers"],
    },
]

PE_PAPERS = [
    {
        "title": "A High-Efficiency GaN-Based Totem-Pole Bridgeless PFC Converter",
        "abstract": (
            "This paper presents a totem-pole bridgeless power factor correction converter "
            "using GaN HEMTs that achieves 99.1% peak efficiency at 3.3 kW. EMI "
            "performance complies with CISPR 11 Class B limits."
        ),
        "ieee_terms": ["power factor correction", "gallium nitride", "AC-DC power converters"],
        "dynamic_terms": ["totem-pole PFC", "GaN HEMT", "EMI compliance"],
    },
    {
        "title": "Model Predictive Control of Modular Multilevel Converters for HVDC Applications",
        "abstract": (
            "A finite-control-set model predictive control strategy is developed for "
            "modular multilevel converters in HVDC transmission. Simulation and hardware "
            "results confirm reduced circulating currents and improved THD."
        ),
        "ieee_terms": ["HVDC power transmission", "multilevel converters", "predictive control"],
        "dynamic_terms": ["modular multilevel converter", "circulating current suppression", "finite control set MPC"],
    },
    {
        "title": "SiC MOSFET Gate Driver Design for Fast Switching in EV Traction Inverters",
        "abstract": (
            "We propose an adaptive gate driver for SiC MOSFETs that balances switching "
            "speed and voltage overshoot in electric-vehicle traction inverters. Switching "
            "losses are reduced by 30% compared to a fixed-resistance design."
        ),
        "ieee_terms": ["silicon carbide", "MOSFET circuits", "electric vehicles"],
        "dynamic_terms": ["SiC gate driver", "traction inverter", "switching loss reduction"],
    },
    {
        "title": "Wireless Power Transfer for Implantable Medical Devices at 6.78 MHz",
        "abstract": (
            "A resonant inductive wireless power transfer link operating at 6.78 MHz is "
            "designed for cardiac pacemakers. The system delivers 150 mW through 15 mm of "
            "tissue with 62% end-to-end efficiency."
        ),
        "ieee_terms": ["wireless power transmission", "biomedical electronics", "resonant coupling"],
        "dynamic_terms": ["implantable devices", "inductive power transfer", "pacemaker charging"],
    },
    {
        "title": "Digital Twin-Based Condition Monitoring of Medium-Voltage Transformers",
        "abstract": (
            "This paper develops a digital-twin framework for real-time thermal and "
            "electrical monitoring of oil-immersed transformers. Field data from a 33 kV "
            "substation validate the model with less than 2% temperature prediction error."
        ),
        "ieee_terms": ["power transformers", "condition monitoring", "digital twins"],
        "dynamic_terms": ["medium-voltage transformer", "thermal modelling", "predictive maintenance"],
    },
    {
        "title": "Bidirectional DC-DC Converter Topologies for Battery Energy Storage Systems",
        "abstract": (
            "A comparative study of isolated bidirectional DC-DC converter topologies for "
            "grid-scale battery storage is presented. The dual-active-bridge topology with "
            "triple-phase-shift modulation achieves the best efficiency across the load range."
        ),
        "ieee_terms": ["DC-DC power converters", "energy storage", "battery management systems"],
        "dynamic_terms": ["dual active bridge", "phase-shift modulation", "grid-scale BESS"],
    },
    {
        "title": "Reliability Analysis of IGBT Modules Under Thermal Cycling Stress",
        "abstract": (
            "Accelerated thermal cycling tests on 1700 V IGBT modules reveal wire-bond "
            "lift-off as the dominant failure mode. A physics-of-failure model predicts "
            "remaining useful life within 10% accuracy."
        ),
        "ieee_terms": ["insulated gate bipolar transistors", "reliability", "thermal stress"],
        "dynamic_terms": ["IGBT module", "wire-bond degradation", "remaining useful life"],
    },
    {
        "title": "Harmonic Mitigation in Grid-Connected PV Inverters Using Active Damping",
        "abstract": (
            "An active-damping control scheme for LCL-filtered grid-connected photovoltaic "
            "inverters is proposed that eliminates the need for physical damping resistors. "
            "THD of injected current is maintained below 3% across all operating conditions."
        ),
        "ieee_terms": ["photovoltaic systems", "power harmonic filters", "inverters"],
        "dynamic_terms": ["LCL filter", "active damping", "grid-connected PV"],
    },
]

ROBOTICS_PAPERS = [
    {
        "title": "Sim-to-Real Transfer for Dexterous Manipulation Using Domain Randomisation",
        "abstract": (
            "We train a dexterous hand policy entirely in simulation with domain "
            "randomisation and transfer it to a real Shadow Hand. The policy solves "
            "in-hand cube reorientation with a 92% success rate."
        ),
        "ieee_terms": ["robot hands", "simulation", "transfer learning"],
        "dynamic_terms": ["sim-to-real", "domain randomisation", "dexterous manipulation"],
    },
    {
        "title": "LiDAR-Inertial SLAM for Underground Mine Exploration",
        "abstract": (
            "A tightly-coupled LiDAR-inertial SLAM system is presented for GPS-denied "
            "underground environments. Loop-closure detection via scan context descriptors "
            "keeps drift below 0.5% over 2 km traversals in an active mine."
        ),
        "ieee_terms": ["SLAM (robots)", "laser radar", "inertial navigation"],
        "dynamic_terms": ["LiDAR-inertial fusion", "underground mapping", "loop closure"],
    },
    {
        "title": "Safe Reinforcement Learning for Bipedal Locomotion With Lyapunov Constraints",
        "abstract": (
            "We incorporate Lyapunov-based safety constraints into a model-free RL "
            "algorithm for bipedal walking. The resulting policy avoids falls during "
            "training and achieves stable locomotion on uneven terrain."
        ),
        "ieee_terms": ["legged locomotion", "reinforcement learning", "Lyapunov methods"],
        "dynamic_terms": ["safe RL", "bipedal robot", "stability constraints"],
    },
    {
        "title": "Vision-Based Reactive Navigation for UAVs in Cluttered Indoor Environments",
        "abstract": (
            "A monocular-vision reactive navigation pipeline enables a quadrotor to fly "
            "at 3 m/s through cluttered indoor spaces without a pre-built map. Depth is "
            "estimated via a lightweight MiDaS model running on-board at 30 Hz."
        ),
        "ieee_terms": ["unmanned aerial vehicles", "collision avoidance", "computer vision"],
        "dynamic_terms": ["reactive navigation", "monocular depth estimation", "indoor UAV"],
    },
    {
        "title": "Collaborative Multi-Robot Task Allocation Using Auction-Based Methods",
        "abstract": (
            "An auction-based framework for heterogeneous multi-robot task allocation is "
            "proposed that accounts for robot capability and travel cost. Experiments with "
            "12 robots in a warehouse setting show 25% throughput improvement over greedy baselines."
        ),
        "ieee_terms": ["multi-robot systems", "task analysis", "resource management"],
        "dynamic_terms": ["auction algorithms", "heterogeneous robots", "warehouse automation"],
    },
    {
        "title": "Compliant Control of Robotic Arms for Human-Robot Collaborative Assembly",
        "abstract": (
            "A variable-impedance controller allows a 7-DOF robotic arm to safely share "
            "a workspace with human operators during PCB assembly. Contact forces are kept "
            "below ISO/TS 15066 thresholds at all times."
        ),
        "ieee_terms": ["robot control", "impedance control", "human-robot interaction"],
        "dynamic_terms": ["compliant manipulation", "collaborative assembly", "force limiting"],
    },
    {
        "title": "Terrain-Adaptive Gait Planning for Quadruped Robots Using Elevation Maps",
        "abstract": (
            "We propose a gait planner that adapts foothold selection and body trajectory "
            "based on real-time elevation maps built from stereo cameras. Field tests on "
            "rocky hillsides show a 40% reduction in slippage events."
        ),
        "ieee_terms": ["mobile robots", "terrain mapping", "gait analysis"],
        "dynamic_terms": ["quadruped robot", "elevation mapping", "foothold planning"],
    },
    {
        "title": "Semantic SLAM for Service Robots in Dynamic Hospital Environments",
        "abstract": (
            "A semantic SLAM system fuses object-level detections with geometric features "
            "to handle dynamic obstacles such as people and trolleys in hospital corridors. "
            "Localisation accuracy improves by 35% over ORB-SLAM3 in high-traffic scenarios."
        ),
        "ieee_terms": ["SLAM (robots)", "service robots", "object detection"],
        "dynamic_terms": ["semantic mapping", "dynamic environments", "hospital robotics"],
    },
    {
        "title": "End-to-End Learned Motion Planning for Autonomous Mobile Robots",
        "abstract": (
            "We train a neural motion planner end-to-end from raw sensor observations to "
            "velocity commands using imitation learning. The planner generalises to unseen "
            "office layouts and handles narrow doorways reliably."
        ),
        "ieee_terms": ["path planning", "mobile robots", "machine learning"],
        "dynamic_terms": ["end-to-end learning", "imitation learning", "motion planning"],
    },
    {
        "title": "Soft Pneumatic Grippers With Embedded Tactile Sensing for Fruit Harvesting",
        "abstract": (
            "A soft pneumatic gripper with piezoresistive tactile sensors is designed for "
            "delicate fruit harvesting. The gripper successfully picks strawberries with "
            "zero bruising across 500 grasp trials."
        ),
        "ieee_terms": ["soft robotics", "tactile sensors", "agricultural robots"],
        "dynamic_terms": ["pneumatic gripper", "fruit harvesting", "tactile feedback"],
    },
]

AUTHOR_NAMES = [
    "Wei Zhang", "Maria Garcia", "James O'Brien", "Priya Sharma", "Yuki Tanaka",
    "Ahmed Hassan", "Laura Fernandez", "Chen Liu", "Olga Petrov", "Samuel Osei",
    "Raj Patel", "Anna Kowalski", "David Kim", "Fatima Al-Rashid", "Thomas Mueller",
    "Ines Morales", "Hiroshi Nakamura", "Elena Volkov", "Carlos Rodriguez", "Aisha Bello",
    "Liam O'Connor", "Sofia Rossi", "Jun Li", "Nadia Benali", "Patrick Dubois",
    "Kenji Watanabe", "Lucia Santos", "Viktor Novak", "Amara Diallo", "Mikael Johansson",
]

AFFILIATIONS = [
    "MIT, Cambridge, MA, USA",
    "Stanford University, Stanford, CA, USA",
    "ETH Zurich, Zurich, Switzerland",
    "Tsinghua University, Beijing, China",
    "University of Oxford, Oxford, UK",
    "Technical University of Munich, Munich, Germany",
    "University of Tokyo, Tokyo, Japan",
    "EPFL, Lausanne, Switzerland",
    "Georgia Institute of Technology, Atlanta, GA, USA",
    "University of Toronto, Toronto, Canada",
    "National University of Singapore, Singapore",
    "KAIST, Daejeon, South Korea",
    "Imperial College London, London, UK",
    "University of Sao Paulo, Sao Paulo, Brazil",
    "Indian Institute of Technology Bombay, Mumbai, India",
    "KTH Royal Institute of Technology, Stockholm, Sweden",
    "University of Melbourne, Melbourne, Australia",
    "Politecnico di Milano, Milan, Italy",
    "Delft University of Technology, Delft, Netherlands",
    "University of Cape Town, Cape Town, South Africa",
]


def _random_date(start: date, end: date) -> date:
    """Return a random date between start and end (inclusive)."""
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def _build_prompt(title: str, abstract: str, ieee_terms: list[str], dynamic_terms: list[str]) -> str:
    return (
        f"Title: {title}\n"
        f"Abstract: {abstract}\n"
        f"IEEE Terms: {', '.join(ieee_terms)}\n"
        f"Dynamic Terms: {', '.join(dynamic_terms)}"
    )


def seed(db: Database) -> dict[str, int]:
    """Insert all dummy data and return per-table row counts."""
    conn = db.connection
    counts = {"papers": 0, "authors": 0, "index_terms": 0, "prompts": 0, "classification": 0}

    datasets = [
        ("machine learning", ML_PAPERS),
        ("power electronics", PE_PAPERS),
        ("robotics", ROBOTICS_PAPERS),
    ]

    is_number_counter = 10001000  # starting fake IS number

    for category, papers in datasets:
        for paper in papers:
            is_number = str(is_number_counter)
            is_number_counter += 1

            insert_date = _random_date(date(2024, 1, 15), date(2025, 6, 30))
            pub_year = random.choice([2024, 2025])
            download_count = random.randint(50, 5000)
            citing_patent_count = random.randint(0, 20)

            # --- Paper ---------------------------------------------------------
            row = conn.execute(
                """
                INSERT INTO papers (is_number, insert_date, publication_year,
                                    download_count, citing_patent_count, title, abstract)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                RETURNING paper_id
                """,
                [
                    is_number,
                    insert_date,
                    pub_year,
                    download_count,
                    citing_patent_count,
                    paper["title"],
                    paper["abstract"],
                ],
            ).fetchone()
            paper_id = row[0]
            counts["papers"] += 1

            # --- Authors -------------------------------------------------------
            num_authors = random.randint(1, 3)
            chosen_authors = random.sample(AUTHOR_NAMES, num_authors)
            for author_name in chosen_authors:
                affiliation = random.choice(AFFILIATIONS)
                conn.execute(
                    """
                    INSERT INTO authors (paper_id, name, affiliation)
                    VALUES (?, ?, ?)
                    """,
                    [paper_id, author_name, affiliation],
                )
                counts["authors"] += 1

            # --- Index terms ---------------------------------------------------
            ieee_terms = paper["ieee_terms"]
            dynamic_terms = paper["dynamic_terms"]

            for term in ieee_terms[:random.randint(2, len(ieee_terms))]:
                conn.execute(
                    "INSERT INTO index_terms (paper_id, term_type, term) VALUES (?, ?, ?)",
                    [paper_id, "IEEE", term],
                )
                counts["index_terms"] += 1

            for term in dynamic_terms[:random.randint(2, len(dynamic_terms))]:
                conn.execute(
                    "INSERT INTO index_terms (paper_id, term_type, term) VALUES (?, ?, ?)",
                    [paper_id, "Dynamic", term],
                )
                counts["index_terms"] += 1

            # --- Prompt --------------------------------------------------------
            prompt_text = _build_prompt(
                paper["title"], paper["abstract"], ieee_terms, dynamic_terms
            )
            conn.execute(
                "INSERT INTO prompts (paper_id, prompt_text) VALUES (?, ?)",
                [paper_id, prompt_text],
            )
            counts["prompts"] += 1

            # --- Classification ------------------------------------------------
            confidence = round(random.uniform(0.6, 0.98), 4)
            conn.execute(
                "INSERT INTO classification (paper_id, category, confidence) VALUES (?, ?, ?)",
                [paper_id, category, confidence],
            )
            counts["classification"] += 1

    return counts


def main() -> None:
    print("Resetting and initialising database...")
    db = Database(name="ieee_papers", filepath=cfg.SRC_DIR)
    db.initialise()

    # Wipe existing data so the script is idempotent
    for table in reversed(cfg.DB_TABLES):
        db.connection.execute(f"DELETE FROM {table}")
    # Reset sequences so IDs start from 1
    for seq in [
        "papers_id_seq",
        "authors_id_seq",
        "index_terms_id_seq",
        "prompts_id_seq",
        "classification_id_seq",
    ]:
        db.connection.execute(f"DROP SEQUENCE IF EXISTS {seq}")
        db.connection.execute(f"CREATE SEQUENCE {seq} START 1")

    print("Inserting dummy data...")
    counts = seed(db)

    print("\n=== Seed Summary ===")
    for table, count in counts.items():
        print(f"  {table:20s} {count:>4} rows")
    print(f"\n  Total rows inserted: {sum(counts.values())}")

    db.close()
    print("\nDone. Database seeded successfully.")


if __name__ == "__main__":
    main()
