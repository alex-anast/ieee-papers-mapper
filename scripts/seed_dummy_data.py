#!/usr/bin/env python3

"""
Seed Dummy Data
================
Populates the DuckDB database with ~120 realistic IEEE-style papers spread
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
    {
        "title": "Robust Speech Recognition in Noisy Environments via Multi-Channel Beamforming",
        "abstract": (
            "We combine neural beamforming with a conformer-based ASR model to achieve "
            "robust speech recognition in cocktail-party settings. Word error rate drops "
            "by 35% compared to single-channel baselines on the CHiME-6 challenge."
        ),
        "ieee_terms": ["speech recognition", "beamforming", "signal processing"],
        "dynamic_terms": ["multi-channel ASR", "conformer model", "noisy environments"],
    },
    {
        "title": "Differentiable Neural Architecture Search With Hardware-Aware Constraints",
        "abstract": (
            "We extend DARTS with latency and memory constraints measured on real hardware. "
            "The discovered architectures run 2x faster on mobile GPUs while maintaining "
            "top-1 accuracy on CIFAR-100 within 0.5% of unconstrained search."
        ),
        "ieee_terms": ["neural architecture search", "mobile computing", "optimization"],
        "dynamic_terms": ["DARTS", "hardware-aware NAS", "latency-constrained search"],
    },
    {
        "title": "Causal Inference in Observational Health Data Using Double Machine Learning",
        "abstract": (
            "We apply double machine learning to estimate average treatment effects from "
            "electronic health records. Cross-fitting with gradient-boosted trees yields "
            "treatment effect estimates that agree with randomised trial results within 8%."
        ),
        "ieee_terms": ["machine learning", "biomedical informatics", "causal inference"],
        "dynamic_terms": ["double ML", "treatment effect estimation", "observational studies"],
    },
    {
        "title": "Multi-Agent Reinforcement Learning for Dynamic Spectrum Access",
        "abstract": (
            "A decentralised multi-agent RL algorithm enables cognitive radios to share "
            "spectrum without explicit coordination. Throughput in a 20-user simulation "
            "exceeds centralised allocation by 12% under rapidly changing channel conditions."
        ),
        "ieee_terms": ["cognitive radio", "reinforcement learning", "spectrum management"],
        "dynamic_terms": ["multi-agent RL", "dynamic spectrum access", "decentralised coordination"],
    },
    {
        "title": "Explainable AI for Credit Scoring: Balancing Accuracy and Transparency",
        "abstract": (
            "We benchmark SHAP, LIME, and attention-based explanations on three credit "
            "scoring datasets. An ensemble that combines gradient boosting with post-hoc "
            "explanations satisfies regulatory interpretability requirements while matching "
            "black-box AUC."
        ),
        "ieee_terms": ["explainable AI", "decision support systems", "financial computing"],
        "dynamic_terms": ["credit scoring", "SHAP explanations", "model transparency"],
    },
    {
        "title": "Neural Radiance Fields for Indoor Scene Reconstruction From Sparse Views",
        "abstract": (
            "We adapt NeRF to reconstruct photorealistic indoor scenes from as few as five "
            "posed images. Depth priors from a monocular estimator regularise geometry and "
            "reduce floater artefacts by 60% compared to vanilla NeRF."
        ),
        "ieee_terms": ["computer vision", "3D reconstruction", "image synthesis"],
        "dynamic_terms": ["neural radiance fields", "sparse-view reconstruction", "depth priors"],
    },
    {
        "title": "Prompt Tuning for Few-Shot Text Classification With Pre-Trained Language Models",
        "abstract": (
            "We show that continuous prompt tuning on RoBERTa matches full fine-tuning "
            "performance with only 16 labelled examples per class. The method adds fewer "
            "than 0.1% trainable parameters and converges in under 500 gradient steps."
        ),
        "ieee_terms": ["natural language processing", "text classification", "transfer learning"],
        "dynamic_terms": ["prompt tuning", "few-shot learning", "parameter-efficient fine-tuning"],
    },
    {
        "title": "Variational Autoencoders for Molecular Property Prediction and Generation",
        "abstract": (
            "A hierarchical VAE jointly predicts molecular properties and generates novel "
            "molecules satisfying target constraints. On the ZINC-250K benchmark, validity "
            "reaches 98% and the model discovers three new drug-like compounds."
        ),
        "ieee_terms": ["generative models", "molecular computing", "deep learning"],
        "dynamic_terms": ["variational autoencoder", "molecular generation", "drug discovery"],
    },
    {
        "title": "Temporal Graph Networks for Dynamic Link Prediction in Social Media",
        "abstract": (
            "We propose a temporal graph network that captures evolving user interactions "
            "for link prediction on Twitter and Reddit datasets. Our model outperforms "
            "static GNN baselines by 18% mean reciprocal rank."
        ),
        "ieee_terms": ["graph neural networks", "social networks", "temporal reasoning"],
        "dynamic_terms": ["temporal graphs", "dynamic link prediction", "social media analysis"],
    },
    {
        "title": "Active Learning Strategies for Efficient Semantic Segmentation Annotation",
        "abstract": (
            "We compare uncertainty-based and diversity-based active learning strategies "
            "for urban scene segmentation. A hybrid approach achieves 95% of fully-supervised "
            "mIoU using only 10% of the labelling budget on Cityscapes."
        ),
        "ieee_terms": ["image segmentation", "active learning", "annotation"],
        "dynamic_terms": ["semantic segmentation", "labelling efficiency", "urban scenes"],
    },
    {
        "title": "Diffusion Models for High-Fidelity Audio Synthesis and Voice Cloning",
        "abstract": (
            "A denoising diffusion probabilistic model generates speech waveforms that "
            "achieve state-of-the-art MOS scores. Zero-shot voice cloning from a 3-second "
            "reference clip reaches naturalness ratings within 0.1 of ground truth."
        ),
        "ieee_terms": ["speech synthesis", "generative models", "audio processing"],
        "dynamic_terms": ["diffusion models", "voice cloning", "high-fidelity audio"],
    },
    {
        "title": "Reinforcement Learning for Adaptive Video Streaming Over 5G Networks",
        "abstract": (
            "An RL-based adaptive bitrate algorithm learns buffer and bandwidth dynamics "
            "in real time. Deployed on a 5G testbed, it reduces rebuffering by 50% while "
            "increasing average video quality by 0.8 dB PSNR."
        ),
        "ieee_terms": ["video streaming", "reinforcement learning", "5G mobile communication"],
        "dynamic_terms": ["adaptive bitrate", "quality of experience", "network optimisation"],
    },
    {
        "title": "Equivariant Neural Networks for Protein Structure Prediction",
        "abstract": (
            "We build SE(3)-equivariant message-passing networks for protein backbone "
            "prediction. On CASP14 targets our model improves GDT-TS by 4 points over "
            "non-equivariant architectures while training 3x faster."
        ),
        "ieee_terms": ["neural networks", "bioinformatics", "structural biology"],
        "dynamic_terms": ["equivariant networks", "protein folding", "SE(3) symmetry"],
    },
    {
        "title": "Federated Continual Learning Across Heterogeneous Edge Devices",
        "abstract": (
            "We tackle the intersection of federated learning and continual learning on "
            "edge devices with heterogeneous compute budgets. Knowledge distillation at "
            "aggregation time mitigates forgetting and achieves 92% accuracy retention "
            "after five sequential tasks."
        ),
        "ieee_terms": ["federated learning", "edge computing", "continual learning"],
        "dynamic_terms": ["heterogeneous devices", "knowledge distillation", "task-incremental learning"],
    },
    {
        "title": "Scaling Laws for Data-Efficient Pretraining of Large Language Models",
        "abstract": (
            "We empirically derive scaling laws relating model size, dataset tokens, and "
            "compute budget for data-constrained regimes. Our formulas predict optimal "
            "allocation within 5% of brute-force search on models up to 13B parameters."
        ),
        "ieee_terms": ["language models", "scaling analysis", "computational efficiency"],
        "dynamic_terms": ["scaling laws", "LLM pretraining", "Chinchilla-optimal training"],
    },
    {
        "title": "Anomaly Detection in Satellite Imagery Using Hyperspectral Autoencoders",
        "abstract": (
            "A convolutional autoencoder trained on hyperspectral satellite bands detects "
            "anomalous land-cover changes with 94% recall. The method flags illegal mining "
            "sites in the Amazon basin from Sentinel-2 time series."
        ),
        "ieee_terms": ["remote sensing", "anomaly detection", "autoencoders"],
        "dynamic_terms": ["hyperspectral imaging", "land-cover change", "satellite monitoring"],
    },
    {
        "title": "Meta-Learning for Rapid Adaptation in Few-Shot Object Detection",
        "abstract": (
            "A meta-learning framework enables a detector to adapt to new object classes "
            "with only five support images. On COCO novel-class splits, our approach "
            "improves AP50 by 6 points over fine-tuning baselines."
        ),
        "ieee_terms": ["object detection", "meta-learning", "computer vision"],
        "dynamic_terms": ["few-shot detection", "rapid adaptation", "support set learning"],
    },
    {
        "title": "Quantum-Classical Hybrid Optimisation for Combinatorial Scheduling Problems",
        "abstract": (
            "We embed QAOA sub-circuits into a classical branch-and-bound solver for job-shop "
            "scheduling. On instances with up to 50 jobs, the hybrid method finds solutions "
            "within 2% of optimality 4x faster than pure classical approaches."
        ),
        "ieee_terms": ["quantum computing", "scheduling", "optimization"],
        "dynamic_terms": ["QAOA", "hybrid quantum-classical", "job-shop scheduling"],
    },
    {
        "title": "Curriculum Learning for Training Robust Image Classifiers Under Label Noise",
        "abstract": (
            "We design a curriculum that progressively introduces noisier samples during "
            "training. On CIFAR-10 with 40% symmetric label noise, our method recovers "
            "91% test accuracy compared to 82% for standard training."
        ),
        "ieee_terms": ["image classification", "robust learning", "training data"],
        "dynamic_terms": ["curriculum learning", "label noise", "noise-robust training"],
    },
    {
        "title": "Spiking Neural Networks for Ultra-Low-Power Keyword Spotting on Neuromorphic Chips",
        "abstract": (
            "A recurrent spiking neural network achieves 96% accuracy on the Google Speech "
            "Commands dataset while consuming only 85 microjoules per inference on Intel "
            "Loihi 2. This is 20x more energy-efficient than equivalent ANNs."
        ),
        "ieee_terms": ["spiking neural networks", "speech recognition", "neuromorphic computing"],
        "dynamic_terms": ["keyword spotting", "Loihi chip", "ultra-low-power inference"],
    },
    {
        "title": "Privacy-Preserving Machine Learning via Secure Multi-Party Computation",
        "abstract": (
            "We implement logistic regression and gradient-boosted trees under a three-party "
            "secret-sharing protocol. End-to-end training on a million-row dataset completes "
            "in under 10 minutes with accuracy within 0.2% of plaintext baselines."
        ),
        "ieee_terms": ["privacy", "machine learning", "cryptography"],
        "dynamic_terms": ["secure MPC", "secret sharing", "privacy-preserving training"],
    },
    {
        "title": "Transformer-Based Weather Forecasting at Global Scale",
        "abstract": (
            "A vision transformer trained on ERA5 reanalysis data produces 10-day global "
            "weather forecasts in under one second on a single GPU. RMSE on 500 hPa "
            "geopotential height beats the operational ECMWF model beyond day 5."
        ),
        "ieee_terms": ["weather forecasting", "transformer networks", "geoscience"],
        "dynamic_terms": ["global weather prediction", "vision transformer", "ERA5 data"],
    },
    {
        "title": "Data-Centric AI: Automated Data Quality Scoring for Tabular Datasets",
        "abstract": (
            "We propose a data quality scoring framework that flags duplicates, outliers, "
            "and label errors in tabular datasets. Applied to 12 Kaggle competitions, fixing "
            "flagged issues improves winning model scores by 1-3% on average."
        ),
        "ieee_terms": ["data quality", "machine learning", "data management"],
        "dynamic_terms": ["data-centric AI", "quality scoring", "automated data cleaning"],
    },
    {
        "title": "Long-Context Attention Mechanisms for Document-Level Machine Translation",
        "abstract": (
            "We extend standard attention to a 16K-token context window for document-level "
            "translation. A sliding-window approach with global sentinel tokens preserves "
            "discourse coherence and improves d-BLEU by 2.1 points on WMT document sets."
        ),
        "ieee_terms": ["machine translation", "attention mechanisms", "natural language processing"],
        "dynamic_terms": ["long-context attention", "document translation", "discourse coherence"],
    },
    {
        "title": "Multimodal Emotion Recognition From Speech and Facial Expressions",
        "abstract": (
            "A cross-attention fusion module combines wav2vec 2.0 speech features with "
            "facial action units for emotion recognition. The multimodal model achieves "
            "78% weighted accuracy on IEMOCAP, a 6% improvement over unimodal baselines."
        ),
        "ieee_terms": ["emotion recognition", "multimodal fusion", "affective computing"],
        "dynamic_terms": ["speech emotion", "facial action units", "cross-attention fusion"],
    },
    {
        "title": "Federated Graph Learning for Privacy-Preserving Recommendation Systems",
        "abstract": (
            "We design a federated graph neural network for collaborative filtering that "
            "keeps user interaction graphs on-device. On MovieLens-1M, hit rate at 10 "
            "matches centralised training while guaranteeing user-level differential privacy."
        ),
        "ieee_terms": ["recommender systems", "graph neural networks", "privacy"],
        "dynamic_terms": ["federated graph learning", "collaborative filtering", "on-device training"],
    },
    {
        "title": "Energy-Based Models for Out-of-Distribution Detection in Safety-Critical Systems",
        "abstract": (
            "We train an energy-based model as a companion to a primary classifier for "
            "out-of-distribution detection in autonomous systems. AUROC exceeds 99% on "
            "near-OOD benchmarks while adding less than 5 ms inference overhead."
        ),
        "ieee_terms": ["anomaly detection", "safety-critical systems", "neural networks"],
        "dynamic_terms": ["energy-based models", "OOD detection", "autonomous systems safety"],
    },
    {
        "title": "Neural Combinatorial Optimisation for Chip Placement via Graph Transformers",
        "abstract": (
            "A graph transformer learns to place macro blocks on ASIC floorplans, reducing "
            "total wirelength by 8% compared to simulated annealing. Training on synthetic "
            "layouts generalises to unseen commercial chip designs."
        ),
        "ieee_terms": ["VLSI design", "optimization", "graph neural networks"],
        "dynamic_terms": ["chip placement", "graph transformer", "electronic design automation"],
    },
    {
        "title": "Self-Supervised Depth Estimation From Monocular Video for Autonomous Navigation",
        "abstract": (
            "A self-supervised monocular depth network trained on ego-motion consistency "
            "achieves state-of-the-art absolute relative error on KITTI. Real-time inference "
            "at 45 FPS on an embedded Jetson Orin enables deployment on small UGVs."
        ),
        "ieee_terms": ["depth estimation", "computer vision", "autonomous navigation"],
        "dynamic_terms": ["self-supervised depth", "monocular video", "embedded inference"],
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
    {
        "title": "Solid-State Transformer Design for Medium-Voltage Distribution Grids",
        "abstract": (
            "A 10 kV / 400 V solid-state transformer based on cascaded H-bridge modules "
            "and dual-active-bridge DC-DC stages is designed and prototyped. The system "
            "achieves 96.5% efficiency and provides reactive power compensation."
        ),
        "ieee_terms": ["power transformers", "power electronics", "smart grids"],
        "dynamic_terms": ["solid-state transformer", "cascaded H-bridge", "medium-voltage distribution"],
    },
    {
        "title": "Maximum Power Point Tracking for Partially Shaded PV Arrays via Particle Swarm Optimisation",
        "abstract": (
            "A modified particle swarm optimisation algorithm is applied to global MPPT "
            "under partial shading conditions. Hardware tests on a 5 kW array show 99.2% "
            "tracking efficiency and convergence in under 1.5 seconds."
        ),
        "ieee_terms": ["photovoltaic systems", "maximum power point trackers", "optimization"],
        "dynamic_terms": ["partial shading MPPT", "particle swarm", "global tracking"],
    },
    {
        "title": "EMI Modelling and Filter Design for High-Frequency SiC-Based Motor Drives",
        "abstract": (
            "Conducted EMI in a 400 V SiC inverter-fed motor drive is modelled using a "
            "mixed-mode noise separation technique. A compact common-mode filter reduces "
            "emissions by 30 dB while adding less than 1% volume overhead."
        ),
        "ieee_terms": ["electromagnetic interference", "silicon carbide", "motor drives"],
        "dynamic_terms": ["EMI filter design", "common-mode noise", "high-frequency switching"],
    },
    {
        "title": "Hybrid Energy Storage Sizing for Fast-Charging EV Stations",
        "abstract": (
            "An optimal sizing methodology for hybrid battery-supercapacitor storage at "
            "350 kW EV fast-charging stations is presented. The hybrid approach reduces "
            "peak grid demand by 60% and battery degradation by 25% over five years."
        ),
        "ieee_terms": ["energy storage", "electric vehicle charging", "power demand"],
        "dynamic_terms": ["hybrid storage sizing", "supercapacitor buffer", "fast-charging station"],
    },
    {
        "title": "Gallium Oxide Power Devices: A Review of Recent Advances and Challenges",
        "abstract": (
            "This review surveys progress in beta-Ga2O3 power MOSFETs and Schottky diodes. "
            "Breakdown voltages exceeding 8 kV and Baliga figures of merit surpassing SiC "
            "are discussed alongside thermal management and p-type doping challenges."
        ),
        "ieee_terms": ["wide bandgap semiconductors", "power semiconductor devices", "gallium oxide"],
        "dynamic_terms": ["Ga2O3 MOSFET", "ultra-wide bandgap", "Baliga FOM"],
    },
    {
        "title": "Resonant Gate Drive Circuits for High-Frequency GaN Half-Bridge Converters",
        "abstract": (
            "A resonant gate driver recovers gate-charge energy in GaN half-bridge converters "
            "switching at 5 MHz. Gate-drive losses drop by 70% compared to conventional "
            "totem-pole drivers, enabling fanless 48 V to 12 V point-of-load converters."
        ),
        "ieee_terms": ["gate drives", "gallium nitride", "DC-DC power converters"],
        "dynamic_terms": ["resonant gate drive", "high-frequency converter", "gate-charge recovery"],
    },
    {
        "title": "Virtual Synchronous Generator Control for Grid-Forming Inverters in Microgrids",
        "abstract": (
            "A virtual synchronous generator algorithm enables battery inverters to provide "
            "inertia and frequency regulation in islanded microgrids. Experimental results "
            "show frequency nadir improvement of 40% during load transients."
        ),
        "ieee_terms": ["microgrids", "inverters", "frequency regulation"],
        "dynamic_terms": ["virtual synchronous generator", "grid-forming control", "synthetic inertia"],
    },
    {
        "title": "Thermal Management of SiC Power Modules Using Embedded Micro-Channel Cooling",
        "abstract": (
            "Micro-channel coolers fabricated directly into the DBC substrate of SiC modules "
            "achieve junction-to-coolant thermal resistance of 0.08 K/W. The integrated "
            "design enables continuous operation at 200 degrees Celsius junction temperature."
        ),
        "ieee_terms": ["silicon carbide", "thermal management", "power modules"],
        "dynamic_terms": ["micro-channel cooling", "DBC substrate", "high-temperature operation"],
    },
    {
        "title": "Lifetime Extension of DC-Link Capacitors Through Active Voltage Balancing",
        "abstract": (
            "An active balancing circuit equalises voltage across series-connected film "
            "capacitors in a 1500 V DC link. Simulations and accelerated aging tests show "
            "a 30% increase in capacitor bank lifetime."
        ),
        "ieee_terms": ["capacitors", "voltage control", "power converter reliability"],
        "dynamic_terms": ["DC-link capacitor", "active balancing", "lifetime prediction"],
    },
    {
        "title": "Multi-Port Power Electronic Interface for Hybrid Renewable Energy Systems",
        "abstract": (
            "A three-port converter interfaces a PV array, wind turbine, and battery pack "
            "through a single magnetic structure. Decoupled power flow control is validated "
            "on a 3 kW prototype with peak efficiency of 97.2%."
        ),
        "ieee_terms": ["renewable energy", "DC-DC power converters", "hybrid power systems"],
        "dynamic_terms": ["multi-port converter", "integrated magnetics", "hybrid renewable interface"],
    },
    {
        "title": "Online Impedance Estimation for Lithium-Ion Battery Health Monitoring",
        "abstract": (
            "An EIS-inspired online impedance estimation method uses pseudo-random current "
            "injection during normal battery operation. State of health is predicted within "
            "2% accuracy across temperatures from -10 to 45 degrees Celsius."
        ),
        "ieee_terms": ["lithium-ion batteries", "impedance measurement", "battery health"],
        "dynamic_terms": ["online EIS", "state of health", "impedance spectroscopy"],
    },
    {
        "title": "Interleaved Boost Converter With Coupled Inductors for Fuel Cell Applications",
        "abstract": (
            "An interleaved boost converter with inversely coupled inductors achieves high "
            "voltage gain for PEMFC stacks. Current ripple is reduced by 80% and efficiency "
            "exceeds 97% at 2 kW rated power."
        ),
        "ieee_terms": ["fuel cells", "DC-DC power converters", "coupled inductors"],
        "dynamic_terms": ["interleaved boost", "PEMFC converter", "ripple cancellation"],
    },
    {
        "title": "Wide-Bandgap Device Characterisation Under Cryogenic Conditions for Space Applications",
        "abstract": (
            "GaN and SiC transistors are characterised at temperatures down to 77 K for "
            "space power systems. On-resistance drops by 40% at cryogenic temperatures, "
            "suggesting significant efficiency gains for deep-space mission converters."
        ),
        "ieee_terms": ["wide bandgap semiconductors", "space power", "cryogenic electronics"],
        "dynamic_terms": ["cryogenic characterisation", "space converters", "GaN at low temperature"],
    },
    {
        "title": "Modular Battery Charger Architecture With Fault-Tolerant Reconfiguration",
        "abstract": (
            "A modular charger with N+1 redundancy and hot-swap capability is designed for "
            "data centre UPS systems. Automatic fault isolation and redistribution maintain "
            "full charging power within 50 ms of a module failure."
        ),
        "ieee_terms": ["battery chargers", "fault tolerance", "uninterruptible power systems"],
        "dynamic_terms": ["modular charger", "hot-swap modules", "data centre UPS"],
    },
    {
        "title": "Current Sensing Techniques for GaN Power Stages: A Comparative Study",
        "abstract": (
            "Five current sensing methods — shunt resistor, PCB Rogowski coil, Hall sensor, "
            "desaturation monitor, and on-resistance estimation — are compared on a 2 MHz "
            "GaN half-bridge. PCB Rogowski coils offer the best bandwidth-to-insertion-loss "
            "trade-off."
        ),
        "ieee_terms": ["current measurement", "gallium nitride", "power converters"],
        "dynamic_terms": ["current sensing", "Rogowski coil", "high-bandwidth measurement"],
    },
    {
        "title": "Predictive Maintenance of Wind Turbine Power Converters Using Vibration Analysis",
        "abstract": (
            "Accelerometer data from IGBT heat sinks is processed with a 1D-CNN to detect "
            "incipient solder fatigue. The classifier achieves 97% detection accuracy with "
            "a false-positive rate below 1% on field data from 50 turbines."
        ),
        "ieee_terms": ["wind turbines", "predictive maintenance", "power converters"],
        "dynamic_terms": ["vibration-based monitoring", "solder fatigue detection", "1D-CNN classifier"],
    },
    {
        "title": "Adaptive Dead-Time Optimisation for ZVS in Half-Bridge GaN Converters",
        "abstract": (
            "An adaptive dead-time controller monitors drain-source voltage transitions and "
            "adjusts dead time cycle-by-cycle to guarantee zero-voltage switching across the "
            "full load range. Efficiency improves by 0.5% at light load."
        ),
        "ieee_terms": ["zero-voltage switching", "gallium nitride", "DC-DC converters"],
        "dynamic_terms": ["adaptive dead-time", "ZVS optimisation", "light-load efficiency"],
    },
    {
        "title": "Arc Fault Detection in DC Microgrids Using Wavelet Packet Decomposition",
        "abstract": (
            "A wavelet-packet-based arc fault detection scheme for 380 V DC microgrids "
            "distinguishes series and parallel arcs from normal switching transients. "
            "Detection latency is below 5 ms with zero false trips over 1000 test events."
        ),
        "ieee_terms": ["fault detection", "DC microgrids", "wavelet transforms"],
        "dynamic_terms": ["arc fault detection", "wavelet packet", "DC safety"],
    },
    {
        "title": "Three-Level T-Type Inverter for Photovoltaic Applications With Reduced Common-Mode Voltage",
        "abstract": (
            "A modulation strategy for three-level T-type inverters limits common-mode "
            "voltage steps to one-sixth of the DC-link voltage. Leakage current in "
            "transformer-less PV systems drops below 10 mA, meeting VDE 0126-1-1."
        ),
        "ieee_terms": ["multilevel inverters", "photovoltaic systems", "pulse width modulation"],
        "dynamic_terms": ["T-type inverter", "common-mode voltage reduction", "transformer-less PV"],
    },
    {
        "title": "High Step-Up DC-DC Converter for Fuel Cell Electric Vehicles Using Voltage Multiplier Cells",
        "abstract": (
            "A non-isolated DC-DC converter achieves a voltage gain of 10 using switched-capacitor "
            "multiplier cells. The 5 kW prototype for FCEV applications reaches 96.8% peak "
            "efficiency and eliminates the need for a high-frequency transformer."
        ),
        "ieee_terms": ["fuel cells", "DC-DC power converters", "electric vehicles"],
        "dynamic_terms": ["high step-up converter", "voltage multiplier", "non-isolated topology"],
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
    {
        "title": "Multi-Sensor Fusion for Robust Localisation of Autonomous Underwater Vehicles",
        "abstract": (
            "A factor-graph fusion framework combines DVL, IMU, pressure sensor, and "
            "acoustic range measurements for AUV navigation. Position error stays below "
            "0.3% of distance travelled over 5 km transects in open ocean."
        ),
        "ieee_terms": ["underwater vehicles", "sensor fusion", "navigation"],
        "dynamic_terms": ["AUV localisation", "factor-graph SLAM", "acoustic ranging"],
    },
    {
        "title": "Reinforcement Learning for Agile Quadrotor Flight Through Narrow Gaps",
        "abstract": (
            "An RL policy trained in a high-fidelity simulator enables a quadrotor to fly "
            "through gaps smaller than its wingspan at 5 m/s. The policy learns to tilt the "
            "body mid-flight and achieves a 95% success rate in real-world trials."
        ),
        "ieee_terms": ["unmanned aerial vehicles", "reinforcement learning", "agile flight"],
        "dynamic_terms": ["gap traversal", "acrobatic flight", "sim-to-real UAV"],
    },
    {
        "title": "Whole-Body Control of Humanoid Robots Using Centroidal Momentum Dynamics",
        "abstract": (
            "A centroidal momentum-based whole-body controller enables a humanoid to walk "
            "on stepping stones and recover from pushes. Task-space QP optimisation runs "
            "at 1 kHz on embedded hardware."
        ),
        "ieee_terms": ["humanoid robots", "motion control", "dynamics"],
        "dynamic_terms": ["centroidal momentum", "whole-body control", "push recovery"],
    },
    {
        "title": "Deep Imitation Learning for Robotic Suturing in Minimally Invasive Surgery",
        "abstract": (
            "We collect expert demonstrations on a da Vinci Research Kit and train a "
            "diffusion policy for autonomous suturing. The learned policy achieves "
            "80% task completion with suture spacing within 1 mm of expert performance."
        ),
        "ieee_terms": ["surgical robots", "imitation learning", "minimally invasive surgery"],
        "dynamic_terms": ["diffusion policy", "robotic suturing", "dVRK demonstrations"],
    },
    {
        "title": "Swarm Robotics for Environmental Monitoring Using Bio-Inspired Algorithms",
        "abstract": (
            "A swarm of 30 ground robots uses a stigmergy-based exploration algorithm "
            "inspired by ant foraging to map soil contamination. Coverage reaches 95% of "
            "a 1-hectare field in under 40 minutes."
        ),
        "ieee_terms": ["swarm robotics", "environmental monitoring", "bio-inspired algorithms"],
        "dynamic_terms": ["stigmergy exploration", "soil contamination mapping", "ant-colony robots"],
    },
    {
        "title": "Robust Visual-Inertial Odometry for Legged Robots on Rough Terrain",
        "abstract": (
            "A visual-inertial odometry system is hardened against motion blur and dynamic "
            "occlusion caused by leg swing. On ANYmal traversing rubble, drift is reduced "
            "by 55% compared to standard VIO pipelines."
        ),
        "ieee_terms": ["visual odometry", "legged locomotion", "inertial navigation"],
        "dynamic_terms": ["robust VIO", "rough terrain", "legged-robot egomotion"],
    },
    {
        "title": "Grasp Quality Prediction From Point Clouds Using PointNet++",
        "abstract": (
            "PointNet++ processes partial point clouds from a single depth camera to predict "
            "6-DOF grasp quality. Grasping novel household objects succeeds at 88% on first "
            "attempt, outperforming analytical baselines by 15%."
        ),
        "ieee_terms": ["robot grasping", "point cloud processing", "deep learning"],
        "dynamic_terms": ["PointNet++", "6-DOF grasp", "novel object grasping"],
    },
    {
        "title": "Formation Control of Multi-UAV Systems Under Communication Constraints",
        "abstract": (
            "A consensus-based formation controller maintains geometric shapes among "
            "quadrotors under intermittent and delayed communication links. Real-world "
            "flights with 8 UAVs show formation errors below 15 cm at 2 m/s cruise speed."
        ),
        "ieee_terms": ["unmanned aerial vehicles", "multi-robot systems", "formation control"],
        "dynamic_terms": ["UAV formation", "consensus control", "communication-constrained swarm"],
    },
    {
        "title": "Learned Dynamics Models for Model-Predictive Control of Soft Robots",
        "abstract": (
            "A neural-network dynamics model trained on 10 hours of random actuation data "
            "enables MPC of a pneumatic soft arm. Trajectory tracking error drops to 3 mm, "
            "a 60% improvement over Jacobian-based control."
        ),
        "ieee_terms": ["soft robotics", "model predictive control", "neural networks"],
        "dynamic_terms": ["learned dynamics", "soft-arm MPC", "pneumatic actuation"],
    },
    {
        "title": "Lifelong Mapping With Sparse Semantic Landmarks for Long-Term Robot Navigation",
        "abstract": (
            "A compact semantic landmark graph enables long-term navigation across seasons "
            "and lighting changes. Over a 6-month deployment in a university campus, the "
            "robot maintains 98% goal-reach success using less than 50 MB of map storage."
        ),
        "ieee_terms": ["robot navigation", "mapping", "semantic understanding"],
        "dynamic_terms": ["lifelong mapping", "semantic landmarks", "long-term autonomy"],
    },
    {
        "title": "Cable-Driven Parallel Robots for Large-Scale 3D Printing of Concrete Structures",
        "abstract": (
            "A cable-driven parallel robot with a 10 m x 10 m x 5 m workspace is designed "
            "for additive manufacturing of concrete walls. Positional accuracy of the "
            "print head is maintained within 2 mm under 50 kg payload."
        ),
        "ieee_terms": ["parallel robots", "3D printing", "construction robotics"],
        "dynamic_terms": ["cable-driven robot", "concrete printing", "large-scale additive manufacturing"],
    },
    {
        "title": "Tactile-Guided In-Hand Manipulation With Multi-Fingered Robotic Hands",
        "abstract": (
            "Dense tactile sensing on each fingertip enables a four-fingered hand to "
            "reorient objects purely from touch. The policy, trained via reinforcement "
            "learning in simulation, transfers to hardware with 85% success."
        ),
        "ieee_terms": ["robot hands", "tactile sensors", "manipulation"],
        "dynamic_terms": ["tactile manipulation", "in-hand reorientation", "multi-finger control"],
    },
    {
        "title": "Autonomous Inspection of Wind Turbine Blades Using Coordinated UAV-Crawler Systems",
        "abstract": (
            "A UAV and a magnetic crawler coordinate to inspect offshore wind turbine blades. "
            "The UAV provides global localisation while the crawler performs close-range "
            "ultrasonic thickness measurements. Inspection time is halved compared to "
            "rope-access teams."
        ),
        "ieee_terms": ["inspection robots", "unmanned aerial vehicles", "wind turbines"],
        "dynamic_terms": ["blade inspection", "UAV-crawler coordination", "offshore wind"],
    },
    {
        "title": "Robust Bipedal Walking on Deformable Sand Using Proprioceptive Feedback",
        "abstract": (
            "A proprioception-only controller enables a bipedal robot to walk on loose "
            "sand by adapting foot-ground contact timing. Metabolic cost of transport "
            "is 15% lower than a vision-augmented baseline on beach terrain."
        ),
        "ieee_terms": ["legged locomotion", "proprioception", "walking robots"],
        "dynamic_terms": ["sand walking", "deformable terrain", "proprioceptive control"],
    },
    {
        "title": "Learning Task-Parameterised Movement Primitives for Pick-and-Place in Clutter",
        "abstract": (
            "Task-parameterised Gaussian mixture models learn pick-and-place trajectories "
            "that adapt to varying object poses and bin configurations. On a Franka Panda, "
            "the method generalises to 90% of unseen arrangements with zero collisions."
        ),
        "ieee_terms": ["robot programming", "motion planning", "pick-and-place"],
        "dynamic_terms": ["movement primitives", "task parameterisation", "cluttered bin picking"],
    },
    {
        "title": "Event-Camera-Based Obstacle Avoidance for High-Speed Drones",
        "abstract": (
            "An event camera provides microsecond-level temporal resolution for obstacle "
            "detection at 15 m/s flight speed. The asynchronous processing pipeline runs "
            "on an FPGA and reacts to obstacles within 3 ms latency."
        ),
        "ieee_terms": ["unmanned aerial vehicles", "collision avoidance", "event cameras"],
        "dynamic_terms": ["event-driven vision", "FPGA processing", "high-speed obstacle avoidance"],
    },
]

AUTHOR_NAMES = [
    "Wei Zhang", "Maria Garcia", "James O'Brien", "Priya Sharma", "Yuki Tanaka",
    "Ahmed Hassan", "Laura Fernandez", "Chen Liu", "Olga Petrov", "Samuel Osei",
    "Raj Patel", "Anna Kowalski", "David Kim", "Fatima Al-Rashid", "Thomas Mueller",
    "Ines Morales", "Hiroshi Nakamura", "Elena Volkov", "Carlos Rodriguez", "Aisha Bello",
    "Liam O'Connor", "Sofia Rossi", "Jun Li", "Nadia Benali", "Patrick Dubois",
    "Kenji Watanabe", "Lucia Santos", "Viktor Novak", "Amara Diallo", "Mikael Johansson",
    "Sven Lindqvist", "Mei Wong", "Ravi Krishnan", "Chiara Bianchi", "Tariq Mansour",
    "Ingrid Haugen", "Kwame Asante", "Isabel Herrera", "Andrei Popescu", "Yuna Park",
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
    "Carnegie Mellon University, Pittsburgh, PA, USA",
    "Peking University, Beijing, China",
    "University of Cambridge, Cambridge, UK",
    "TU Berlin, Berlin, Germany",
    "Seoul National University, Seoul, South Korea",
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

    is_number_counter = 10001000

    for category, papers in datasets:
        for paper in papers:
            is_number = str(is_number_counter)
            is_number_counter += 1

            insert_date = _random_date(date(2023, 1, 15), date(2025, 6, 30))
            pub_year = random.choice([2023, 2024, 2024, 2025, 2025])
            download_count = random.choice(
                [random.randint(0, 50)] * 2
                + [random.randint(50, 500)] * 4
                + [random.randint(500, 3000)] * 3
                + [random.randint(3000, 15000)]
            )
            citing_patent_count = random.randint(0, 30)

            confidence = round(random.choice(
                [random.uniform(0.25, 0.50)] * 2
                + [random.uniform(0.50, 0.75)] * 3
                + [random.uniform(0.75, 0.98)] * 5
            ), 4)

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
            num_authors = random.randint(1, 4)
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
