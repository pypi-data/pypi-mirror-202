# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['papdl',
 'papdl.backend',
 'papdl.backend.containers.Benchmarker.app',
 'papdl.backend.containers.Orchestrator.app',
 'papdl.backend.containers.Orchestrator.app.proto',
 'papdl.backend.containers.Slice.app',
 'papdl.backend.containers.Slice.app.proto',
 'papdl.benchmark',
 'papdl.clean',
 'papdl.configure',
 'papdl.deploy',
 'papdl.slice']

package_data = \
{'': ['*'],
 'papdl.backend': ['certificates/.stub',
                   'containers/Benchmarker/*',
                   'containers/Orchestrator/*',
                   'containers/Slice/*',
                   'registry_volume/*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'asynchttp>=0.0.4,<0.0.5',
 'asyncio>=3.4.3,<4.0.0',
 'asyncstdlib>=3.10.5,<4.0.0',
 'autopep8>=2.0.1,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'crossplane>=0.5.8,<0.6.0',
 'dill>=0.3.6,<0.4.0',
 'docker>=6.0.1,<7.0.0',
 'filprofiler>=2023.3.0,<2024.0.0',
 'iperf3>=0.1.11,<0.2.0',
 'ipykernel>=6.21.3,<7.0.0',
 'jsonpickle>=3.0.1,<4.0.0',
 'keras>=2.11.0,<3.0.0',
 'lz4>=4.3.2,<5.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'memory-profiler>=0.61.0,<0.62.0',
 'notebook>=6.5.3,<7.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pympler>=1.0.1,<2.0.0',
 'pyopenssl>=23.0.0,<24.0.0',
 'pythonping>=1.1.4,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'random-word>=1.0.11,<2.0.0',
 'sanic>=22.12.0,<23.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tensorflow>=2.11.0,<3.0.0',
 'termcolor>=2.1.1,<3.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'uproot>=5.0.4,<6.0.0',
 'websockets>=10.4,<11.0']

entry_points = \
{'console_scripts': ['papdl = papdl.cli:main']}

setup_kwargs = {
    'name': 'papdl',
    'version': '0.1.2',
    'description': '',
    'long_description': '\n# PAPDL - Making Distributed Model Deployment Easier\n\nDistributed systems and edge computing have become increasingly important due to the rapid growth of data generated and the demand for scalable computer systems. In parallel to this growth, Deep Neural Networks have shown exceptional results in a variety of tasks to be performed on the data from image recognition to video processing. PAPDL is a command line program that addresses the challenges of Deep Neural Network (DNN) predictions on real-time streaming data. The proposed program aims to decouple DNN layers from the original model, encapsulate them using containerized services, and deploy them across of set of distributed systems. The decoupling operation takes resource utilization metrics for executing a DNN layer into account in order to prevent certain devices from being overloaded and also aims to minimize the latency for getting a prediction for a given input. PAPDL can orchestrate services running across the distributed system to perform prediction that is semantically equivalent to running the entire model as a monolithic architecture on a single device.\n\n## Requirements and Installation\n\n1. Install Docker https://docs.docker.com/get-docker/\n2. Install PAPDL `pip3 install papdl`\n\n\n## Usage\n\n### 1. Prepare a set of devices which can communicate with each other within a local network or over the internet.\n\nThis example will show a practical use case of optimally deploying a VGG16 Image classification model across a Docker Swarm. We will be using the following devices to run the model:\n\n| Device Name | CPU Cores | Arch    | Memory | Swap |\n|-------------|-----------|---------|--------|------|\n| vm4         | 1         | x86\\_64 | 2GB    | 2GB  |\n| vm5         | 2         | x86\\_64 | 4GB    | 4GB  |\n| pc5         | 4         | x86\\_64 | 32GB   | 8GB  |\n\n\n\n### 2. Setup Docker Swarm configuration.\n\n\n```bash\n$ ssh pc5\n$ docker swarm init\ndocker swarm join --token {JOIN_TOKEN} {IP ADDRESS}\n```\n\nOn one of the devices, run the following command to initialize a Docker Swarm and the manager node. For the purposes of the example, pc5 is used.\n\n\n### 3. Save any arbitrary deep neural network model on the manager node device.\n\n```python\n\nimport keras.applications as apps\nfrom keras.models import save_model\n\nsave_model(apps.VGG16(), filepath=f"vgg16_model")\n```\n\n### 4. Slice the models into layers with the papdl slice command.\n\n```bash\npapdl slice vgg16_model -o sliced_vgg16_model\n```\n\n### 5. Compile layer performance statistics and inter-device network communications statistics with the papdl benchmark command.\n\n```bash\npapdl benchmark sliced_vgg16_model -o benchmarked_vgg16_model\n```\n\n### 6. Determine the node ID of the source device from which input data will be provided from\n\n\n```bash\n$ docker node ls\n \nVM4 {VM4_NODE_ID}\nVM5 {VM5_NODE_ID}\nPC5 {PC5_NODE_ID}\n\n```\n\nFor this guide, all inputs will be provided from vm4 which has the strongest memory and compute constraints.\n\n### 7. Generate optimal deployment configuration based on aggregated data.\n\n```bash\npapdl configure benchmarked_vgg16_model {VM4_NODE_ID} 150528 -o configured_vgg16_model\n```\n\nThe configure step takes two additional arguments {SOURCE_DEVICE} and {INPUT_SIZE}. {SOURCE_DEVICE} indicates where the source of inputs to perform predictions are coming from.  The {INPUT_SIZE} can be calculated multiplying the input shape of VGG16 which is `224 * 224 * 3 * {batch_size}`. The batch size for this guide will be `1` resulting in an input shape of `224 * 224 * 3 * 1 = 150528`.\n\n\n### 8. Deploy the model.\n\n```bash\npapdl deploy configured_vgg16_model\n```\n\nBased on the optimal deployment configuration, we can now containerize sets of layers and distribute them across the configured Docker swarm as micro services. We can verify the instantiation of the services from the following command:\n\n```bash\n$ docker service ls\n```\n\n### 9. Activate a chain of connections between all the containerized micro services:\n\n```bash\n$ ssh vm4\n$ curl localhost:8765/connect\n$ curl localhost:8765/activate\n```\n\n### 10. Perform prediction!\n\nNow we are ready to perform prediction! The `get_papdl_prediction` method shows how we make predictions with PAPDL and `get_local_prediction` method shows how we traditionally make predictions on input using a monolithic DNN architecture running on a single device.\n\n```python\n"""\nLOCAL MONOLITHIC PREDICTION\n"""\ndef get_local_prediction(image):\n    output = model.predict(input)\n    prede = vgg16.decode_predictions(output, top=1)\n    return pred\n\n"""\nDISTRIBUTED PREDICTION WITH PAPDL\n"""\n\ndef get_papdl_prediction(input):\n    buff = io.BytesIO()\n    np.save(buff,input)\n    buff.seek(0)\n\n    response = requests.post("http://localhost:8765/input",data=buff.read(), verify=False, stream=True)\n\n    result_buff = io.BytesIO()\n    result_buff.write(response.content)\n    result_buff.seek(0)\n    result_np = np.load(result_buff)\n\n    pred = vgg16.decode_predictions(result_np,top=1)\n    return pred\n\n\n\ndef predict(dataset):\n    fix,ax = plt.subplots(nrows=1,ncols=len(dataset),figsize=(20,20))\n    for i,(image,sample) in enumerate(dataset):\n        # display(image)\n        input = sample.reshape((-1,224,224,3))\n        pred = get_papdl_prediction(input)\n\n        ax[i].imshow(sample.astype("uint8"),interpolation="nearest")\n        ax[i].get_xaxis().set_visible(False)\n        ax[i].get_yaxis().set_visible(False)\n        ax[i].set_title(f"{pred[0][0][2]} {pred[0][0][1]}")\n\ndef load_data(images):\n    result = []\n    for filename in images:\n        image = load_img(filename,target_size=(224,224))\n        result.append((image, img_to_array(image)))\n    return result\n\npredic(dataset)\n```\n\nIf all goes well, we can verify the output below:\n\n![PAPDL prediction](./scripts/predictions/outputs/papdl.png)\n\n\n## That easy?\n\nYes!\n\n',
    'author': 'Tamim Azmain',
    'author_email': 'maat1@st-andrews.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
