# Nillion AIVM

AIVM is a cutting-edge framework designed for privacy-preserving inference using advanced cryptographic protocols. With AIVM, you can deploy a local development network (devnet) to explore private inference using provided examples or custom models.

## Table of Contents

- [Installing AIVM](#installing-aivm)
- [Running AIVM](#running-aivm)
- [Usage](#usage)
   - [Private Inference](#performing-secure-inference)
   - [Custom Model Upload](#custom-model-upload)
- [License](#license)

## Installing AIVM

### Recommended Instalation
1. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

2. Activate the virtual environment:

   On Linux/macOS:

   ```bash
   source .venv/bin/activate
   ```

   On Windows:

   ```bash
   .\venv\Scripts\activate
   ```

3. Install the package:

   If you are going to execute the examples execute:
   ```bash
   pip install "nillion-aivm[examples]"
   ```
   Otherwise, if you are going to produce your own code, you can just:
   ```bash
   pip install nillion-aivm
   ```
### Install using Poetry from source

1. Install Poetry (if not already installed):

   ```bash
   pip install poetry
   ```

2. Install dependencies:

   ```bash
   cd aivm
   poetry install -E examples
   ```

3. Activate the virtual environment:

   ```bash
   poetry shell
   ```

### Install using Pip from source

1. Install dependencies:

   ```bash
   cd aivm
   pip install ".[examples]"
   ```
   If it is used as a development environment it is recommended to install using:

   ```bash
   cd aivm
   pip install -e ".[examples]"
   ```



## Running AIVM

1. Start the AIVM devnet:

   ```bash
   aivm-devnet
   ```

2. Open the provided Jupyter notebook [examples/getting-started.ipynb](./examples/1-getting-started.ipynb) to run private inference examples on AIVM.

3. After completing your tasks, terminate the devnet process by pressing `CTRL+C`.

## Usage

**For additional usage, refer to the [examples](./examples/README.md) folder, which demonstrates how to set up private inference workflows using AIVM.**

## Performing Secure Inference

### Basic Usage

1. First, import the AIVM client and check available models:

```python
import aivm_client as aic

# List all supported models
available_models = aic.get_supported_models()
print(available_models)
```

2. Prepare your input data. Here's an example using PyTorch to generate a random input:

```python
import torch

# Create a sample input (e.g., for LeNet5 MNIST)
random_input = torch.randn((1, 1, 28, 28))  # Batch size 1, 1 channel, 28x28 pixels
```

3. Encrypt your input using the appropriate Cryptensor:

```python
# Encrypt the input
encrypted_input = aic.LeNet5Cryptensor(random_input)
```

4. Perform secure inference:

```python
# Get prediction while maintaining privacy
result = aic.get_prediction(encrypted_input, "LeNet5MNIST")
```

The `get_prediction` function automatically handles the secure computation protocol with the `aivm-devnet` nodes, ensuring that your input data remains private throughout the inference process.

## Custom Model Upload

You can deploy your own trained models to AIVM, provided they follow the supported architectures (BertTiny or LeNet5).

### Uploading Custom Models

1. Import the AIVM client:

```python
import aivm_client as aic
```

2. Upload your custom model:

```python
# For BertTiny models
aic.upload_bert_tiny_model(model_path, "MyCustomBertTiny")

# For LeNet5 models
aic.upload_lenet5_model(model_path, "MyCustomLeNet5")
```

3. Perform inference with your custom model:

```python
# For BertTiny models
result = aic.get_prediction(private_berttiny_input, "MyCustomBertTiny")

# For LeNet5 models
result = aic.get_prediction(private_lenet5_input, "MyCustomLeNet5")
```

## License

This project is licensed under the MIT License.