# ESAME: Evolutionary Search for Agent Misalignment Events

## Overview

ESAME is an open-source framework that uses evolutionary algorithms to discover unintentional misalignment in AI agents.
The framework leverages LLM-guided evolution to systematically find inputs that cause AI agents to competently pursue 
undesirable goals without explicit instructions to do so.

Unlike traditional red-teaming approaches that rely on adversarial prompting, ESAME focuses on discovering 
natural-seeming inputs that trigger misalignment without malicious intent, addressing crucial safety concerns in
deployed AI systems.

## Project Description
ESAME uses evolutionary algorithms to systematically discover patterns of unintentional misalignment in AI agents. 
Unlike traditional red-teaming or jailbreaking approaches that rely on explicit adversarial inputs, ESAME focuses on 
finding natural-seeming inputs that trigger competent, goal-directed violations of developer specifications without 
explicitly instructing the agent to misbehave. The framework leverages LLM-guided mutation and crossover operations to 
evolve prompts that induce misalignment while maintaining naturalness.

## Key Features

- **Evolutionary Algorithm Framework**: Uses DEAP with LLM-guided mutation and crossover operations
- **Comprehensive Fitness Evaluation**: Evaluates misalignment detection, naturalness, and persistence
- **Multi-Agent Support**: Tests evolved prompts across different agent implementations
- **Analysis Toolkit**: Clustering, ablation studies, and visualization tools for misalignment patterns

## Research Background
This project builds on recent work in AI safety focusing on unintentional misalignment:

Järviniemi & Hubinger (2024): Uncovering deceptive tendencies in language models
Meinke et al. (2025): Frontier models are capable of in-context scheming
Yuan et al. (2024): R-Judge benchmarking safety risk awareness for LLM agents

ESAME extends these findings by applying evolutionary algorithms to systematically discover misalignment patterns
across multiple agents and contexts.

@software{esame2025,
  author = {Your Name},
  title = {ESAME: Evolutionary Search for Agent Misalignment Events},
  year = {2025},
  url = {https://github.com/yourusername/esame}
}

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/esame.git
cd esame

# Install dependencies
pip install -e .# ESAME-Evolutionary-Search-for-Agent-Misalignment-Events-
