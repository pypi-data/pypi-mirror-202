# Keypoint MoSeq 

![logo](docs/source/logo.jpg)

Motion Sequencing (MoSeq) is an unsupervised machine learning method for animal behavior analysis [(Wiltschko et al., 2015)](http://datta.hms.harvard.edu/wp-content/uploads/2018/01/pub_23.pdf). Given behavioral recordings, MoSeq learns a set of stereotyped movement patterns and when they occur over time. This package provides tools for fitting a MoSeq model to keypoint tracking data [(Weinreb et al., 2023)](https://www.biorxiv.org/content/10.1101/2023.03.16.532307v1). 

## [Documentation](https://keypoint-moseq.readthedocs.io/en/latest/)

- [Installation](https://keypoint-moseq.readthedocs.io/en/latest/install.html)

- [Tutorial](https://keypoint-moseq.readthedocs.io/en/latest/tutorial.html)

- [Keypoint-MoSeq paper](https://www.biorxiv.org/content/10.1101/2023.03.16.532307v1)

- [Slack workspace](https://join.slack.com/t/moseqworkspace/shared_invite/zt-151x0shoi-z4J0_g_5rwJDlO1IfCU34A)

- [MoSeq homepage](https://dattalab.github.io/moseq2-website/index.html)

## Installation

- The first import of `keypoint_moseq` after installation can take a few minutes. 
- To install on a Mac with an M1 chip, we recommend option 2 (conda environment installation).

### Option 1: Install using pip

1. If you plan to use a GPU (recommended), install the appropriate driver and CUDA version. CUDA ≥11.1 and cuDNN ≥8.2 are required. [This section of the DeepLabCut docs](https://deeplabcut.github.io/DeepLabCut/docs/installation.html#gpu-support) may be helpful.


2. Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html). Create and activate an environment called `keypoint_moseq` with python 3.9:
```
conda create -n keypoint_moseq python=3.9
conda activate keypoint_moseq

# Include the following line if installing on Windows
# conda install -c conda-forge pytables
```

3. Install jax
```
# MacOS and Linux (CPU-only)
pip install "jax[cpu]"

# MacOS and Linux (GPU)
pip install "jax[cuda11_cudnn82]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

# Windows (CPU-only)
pip install jax==0.3.22 https://whls.blob.core.windows.net/unstable/cpu/jaxlib-0.3.22-cp39-cp39-win_amd64.whl

# Windows (GPU)
pip install jax==0.3.22 https://whls.blob.core.windows.net/unstable/cuda111/jaxlib-0.3.22+cuda11.cudnn82-cp39-cp39-win_amd64.whl
```

4. Install keypoint-moseq
```
pip install keypoint-moseq
```

5. Make the new environment accessible in jupyter 
```
python -m ipykernel install --user --name=keypoint_moseq
```

## Option 2: Conda environment installation
As an alternative, you can install directly from conda environment files. This will automatically install the appropriate GPU drivers and other dependencies.

1. Clone the repository:
```
git clone https://github.com/dattalab/keypoint-moseq && cd keypoint-moseq
```

2. Install the appropriate conda environment for your platform:

```
# Windows (CPU-only)
conda env create -f conda_envs/environment.win64_cpu.yml

# Windows (GPU)
conda env create -f conda_envs/environment.win64_gpu.yml

# Linux (CPU-only)
conda env create -f conda_envs/environment.linux_cpu.yml

# Linux (GPU)
conda env create -f conda_envs/environment.linux_gpu.yml

# Mac (CPU-only)
conda env create -f conda_envs/environment.mac_cpu.yml
```

See [this issue](https://github.com/dattalab/keypoint-moseq/issues/5) for updates regarding Apple Silicon (M1/M2) support. For now, you can use the Mac (CPU) version on newer Macs.

3. Activate the new environment:
```
conda activate keypoint_moseq
```


### Troubleshooting
#### `UNKNOWN: no kernel image is available for execution on the device`
If you're running into issues when trying to use the GPU-accelerated version, you might see this error message:
```
jaxlib.xla_extension.XlaRuntimeError: UNKNOWN: no kernel image is available for execution on the device
```
First, check if Jax can detect your GPU:
```
(keypoint_moseq) λ python -c "import jax; print(jax.default_backend())"
gpu
```
If it can't, then you might not be using the right version of `cudatoolkit` or `cudnn`. If you installed these via `conda`, you can check by doing a `conda list | grep cud`.

If you are on the right versions, try [updating your GPU driver to the latest version](https://nvidia.com/drivers).

# License
MoSeq is freely available for academic use under a license provided by Harvard University. Please refer to the license file for details. If you are interested in using MoSeq for commercial purposes please contact Bob Datta directly at srdatta@hms.harvard.edu, who will put you in touch with the appropriate people in the Harvard Technology Transfer office.

