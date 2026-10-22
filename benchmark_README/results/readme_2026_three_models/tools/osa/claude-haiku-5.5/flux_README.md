# flux-uvedareu

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

flux-uvedareu is an inference codebase for FLUX models, supporting text-to-image generation and several image-editing and conditioning workflows. It is intended for developers and ML researchers who want to run or integrate FLUX inference. The project provides a command-line interface with separate task modes, an interactive mode for repeated sampling, and optional browser-based demos. The source is laid out as a Python package (`src/flux`); direct import of this package for custom integration is not documented here. For runnable steps, see Getting Started and Examples.

---

## Core Features

- **Multiple generation workflows in one CLI:** Run text-to-image, structural conditioning, fill, image editing, and image variation from a single command-line entry point with separate subcommands for each workflow.
- **Interactive loop mode:** Generate several images in one session and adjust prompt, resolution, seed, guidance, and step count between samples without restarting the process.
- **CPU offload option:** Keep the flow model and autoencoder on the CPU instead of the selected device, which lets you run inference on hardware with limited GPU memory.
- **Optional TensorRT backend:** Enable an optimized inference path with the `tensorrt` extra and the `trt` option.
- **Gradio and Streamlit demos:** Try the models through browser-based interfaces, installed with the `gradio` or `streamlit` extras.

---

## Installation

**Prerequisites:** Python >=3.10

Install flux-uvedareu from a local copy of the repository. From the repository root