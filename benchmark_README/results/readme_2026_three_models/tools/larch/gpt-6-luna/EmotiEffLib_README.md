# EmotiEffLib

EmotiEffLib is a facial-analysis project for estimating emotions and related affective attributes from images and video. The repository includes pretrained models, Python code, training and evaluation notebooks, and example integrations for Android and C++.

The project contains models and examples for:

- Facial emotion recognition
- Valence–arousal prediction
- Engagement classification
- Age, gender, and ethnicity estimation
- Face detection and facial-analysis workflows

> **Note:** Results depend on the selected model, its training data, preprocessing, and the quality of the input image. Model outputs are estimates, not definitive judgments about a person.

## Contents

- [Getting started](#getting-started)
- [Installation](#installation)
- [Using the Python code](#using-the-python-code)
- [Models](#models)
- [Notebooks and training](#notebooks-and-training)
- [Other integrations](#other-integrations)
- [Tests and troubleshooting](#tests-and-troubleshooting)
- [Privacy and responsible use](#privacy-and-responsible-use)
- [License](#license)

## Getting started

Clone the repository and install the dependencies for the workflow you intend to use:

```bash
git clone <repository-url>
cd EmotiEffLib-tjurlz1k
python -m venv .venv
```

Activate the virtual environment:

```bash
# Linux or macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

The repository provides several requirement files because different workflows use different dependencies. Install the base requirements for Python use:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For a PyTorch-based workflow, use the PyTorch requirements file as appropriate:

```bash
pip install -r requirements-torch.txt
```

Other requirement files support CI, Binder, and engagement-related workflows. Review the selected file before installing it, especially if you already have a configured PyTorch or GPU environment.

If the project’s package metadata supports editable installation in your environment, install it from the repository root:

```bash
pip install -e .
```

## Installation

### Python dependencies

The project includes `setup.py`, `setup.cfg`, and `pyproject.toml` for Python packaging and development configuration. Dependency files include:

- `requirements.txt` — general Python dependencies
- `requirements-torch.txt` — PyTorch-related dependencies
- `requirements-engagement.txt` — engagement workflow dependencies
- `requirements-ci.txt` — continuous-integration dependencies
- `requirements-binder.txt` and `requirements-binder-torch.txt` — Binder-oriented environments

Use the dependency set appropriate to your workflow. GPU-enabled PyTorch installations may require a separate installation command selected for your CUDA version; consult the official PyTorch installation instructions.

### Model files

Pretrained model weights are included in the repository. Keep the models in the locations expected by the Python code, notebooks, or example applications. If you move a model, update the corresponding path in the application configuration.

## Using the Python code

The Python implementation is centered around `facial_analysis.py`. The repository also contains utilities, model-loading tests, and test scripts that can help identify the available interfaces in the checked-out version:

- `facial_analysis.py`
- `utils.py`
- `test_facial_analysis.py`
- `test_module_loading.py`

Start by inspecting the public classes and functions in the module:

```bash
python -c "import facial_analysis; help(facial_analysis)"
```

You can also use Python’s interactive help:

```python
import facial_analysis

print(dir(facial_analysis))
help(facial_analysis)
```

The precise constructor arguments, preprocessing requirements, and prediction return values depend on the selected implementation and model. Use the module documentation and tests as the source of truth when writing an application. In general, a facial-analysis workflow consists of:

1. Load an image or video frame.
2. Detect or provide a face region, if required by the selected API.
3. Apply the preprocessing expected by the model.
4. Run the selected prediction task.
5. Interpret the returned values using the matching model labels or output definition.

For emotion classes, consult the model’s label configuration—for example, `affectnet_labels.txt` in the Android sample. Do not assume that all models use the same classes or output ordering.

### Running a test or example

The repository includes a face-analysis test script and a module-loading test. Run them from the repository root:

```bash
python test_module_loading.py
python test_facial_analysis.py
```

These scripts may expect optional dependencies, model files, or test data to be available. See [Tests and troubleshooting](#tests-and-troubleshooting) if a test cannot run in your environment.

## Models

The repository contains model weights in several formats, including PyTorch (`.pt`), ONNX (`.onnx`), TensorFlow/Keras (`.h5`), TensorFlow Lite (`.tflite`), and Android PyTorch Lite (`.ptl`). Use a model with the runtime and preprocessing expected by its implementation.

| Files or filename patterns | Indicated purpose |
|---|---|
| `enet_b0_8_best_vgaf.*`, `enet_b0_8_best_afew.*` | EfficientNet-based emotion models associated with VGAF- and AFEW-named variants |
| `enet_b2_7.*`, `enet_b2_8.*` | EfficientNet-based model variants |
| `enet_b0_8_va_mtl.*`, `mbf_va_mtl.*`, `mobilevit_va_mtl.*` | Models identified as multitask valence–arousal variants |
| `mobilenet_7.h5` | MobileNet model weights |
| `state_vggface2_enet0_new.pt`, `state_vggface2_enet2.pt`, `state_vggface2_rexnet_150.pt` | Model or backbone weights associated with VGGFace2 |
| `engagement_single_attention.h5` | Engagement-classification model |
| `age_gender_tf2_224_deep-03-0.13-0.97.h5` and similarly named `.pb` file | Age/gender-related model artifacts |
| `mtcnn.pb`, `mtcnn_model.pb`, `pnet.tflite`, `rnet.tflite`, `onet.tflite` | Face-detection model artifacts |
| `enet_b0_8_va_mtl.ptl` | Android PyTorch Lite model artifact |

The filenames indicate intended tasks or variants, but they do not fully specify input shape, normalization, output meaning, or class ordering. Check the loading code and accompanying configuration before substituting one model for another.

### Converting models

The repository includes conversion utilities such as:

- `convert_pt_to_onnx.py`
- `prepare_models_for_emotieffcpplib.py`
- `to_pytorchlite.py`
- `to_tflite.py`

Conversion can change supported operators, precision, or runtime behavior. Validate converted models against the original implementation using representative inputs.

## Notebooks and training

The notebooks provide examples and experiments for inference, feature extraction, model training, evaluation, and engagement modeling. Examples include:

- **Emotion recognition:** `One image emotion recognition.ipynb`, `Predict emotions on video.ipynb`
- **Video engagement and emotion:** `Predict engagement and emotions on video.ipynb`
- **Engagement modeling:** `01 - Features-extractor.ipynb`, `02 - Engagement user-independent model training.ipynb`, `03 - Custom dataset features extractor.ipynb`, and `04 - Engagement user-adaptation.ipynb`
- **Model training and evaluation:** notebooks covering AffectNet, AFEW, VGAF, and other experiments

Notebook filenames and their containing directories may vary in this repository. Open the relevant notebook from its directory and follow its setup and data-path instructions.

Training notebooks may require datasets that are not included here. Obtain and prepare those datasets according to their respective terms and the instructions in the notebooks. Do not assume that pretrained weights grant permission to use the underlying training data.

## Other integrations

### Android

The repository contains Android example projects with Gradle build files, manifests, Java source, and mobile model artifacts. The examples include emotion classifiers using TensorFlow Lite and PyTorch, as well as face detection and alignment utilities.

Open the relevant Android project in Android Studio, allow Gradle to sync, and follow the project’s instructions for building and running it. Device compatibility, camera permissions, and supported model operators depend on the project configuration and the Android runtime.

### C++

C++ headers, implementation files, tests, and CMake configuration are included. The C++ code is intended for a native facial-analysis workflow and may use prepared model artifacts.

Build instructions depend on the available toolchain and native dependencies. Begin by reviewing the CMake files and the C++ documentation:

```bash
cmake -S <cpp-project-directory> -B build
cmake --build build
```

The source tree includes `facial_analysis.h`, `facial_analysis.cpp`, test files, and CMake configuration. Check the relevant directory’s `README.md` for project-specific dependencies and options.

### Documentation

Doxygen configuration files are provided for Python and C++ documentation. If Doxygen is installed, consult `Doxyfile`, `Doxyfile-python`, and `Doxyfile-cpp` for the configured documentation targets.

## Tests and troubleshooting

- **Import errors:** Confirm that you installed dependencies into the active virtual environment and are running Python from the intended environment.
- **Missing model errors:** Run the application from the expected directory or update its model paths. The repository contains models in multiple formats; verify that the selected runtime can load the chosen format.
- **Different predictions between runtimes:** Check image color order, face cropping, resizing, normalization, output decoding, and model precision.
- **Missing notebook data:** Some training and evaluation notebooks rely on external datasets or files that are not included in the repository.
- **Test failures:** Review the test’s expected inputs and optional dependencies. Some scripts may need sample images or runtime-specific packages.
- **Android or C++ build failures:** Check the project-specific Gradle or CMake configuration and make sure the required SDKs, compilers, and native libraries are installed.

## Privacy and responsible use

Facial analysis processes sensitive biometric information. Before using this software:

- Obtain appropriate consent and follow applicable privacy and data-protection laws.
- Avoid collecting or retaining face images and predictions unless necessary and authorized.
- Do not use model outputs as the sole basis for consequential decisions.
- Evaluate performance on the intended population and setting; results may vary across demographics, lighting, pose, image quality, and recording conditions.
- Treat emotion, engagement, age, gender, and ethnicity predictions as uncertain model estimates rather than ground truth.

## License

See the repository’s `LICENSE` file for the applicable license and terms. Review it before distributing the software, pretrained weights, or modified versions.
