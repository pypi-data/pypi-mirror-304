# ML-Agents SPS Plugin

A plugin for Unity ML-Agents to log Steps Per Second (SPS) to TensorBoard and the console, providing insights into training speed and performance. This tool allows users to monitor the number of steps completed per second, helping to optimize training configuration, including the number of parallel executables (`--num-envs`) and parallel agents/areas.

## Example Output

Here’s an example of the output you’ll see in the console with this plugin:

```plaintext
[INFO] Brain. Steps Per Second: 5275.42.
[INFO] Brain. Step: 44020000. Time Elapsed: 235.580 s. Mean Reward: 1379.877. Std of Reward: 184.503. Training.
[INFO] Brain. Step: 44030000. Time Elapsed: 250.285 s. No episode was completed since last summary. Training.
[INFO] Brain. Steps Per Second: 898.65.
[INFO] Brain. Step: 44040000. Time Elapsed: 250.563 s. No episode was completed since last summary. Training.
```

## Features

- **Steps Per Second Logging**: Logs the SPS (Steps Per Second) to TensorBoard, making it easy to track training speed over time.
- **Performance Monitoring**: Enables users to fine-tune the number of parallel executables and agents to maximize hardware utilization and minimize idle time.
- **TensorBoard Integration**: Integrates seamlessly with TensorBoard to visualize SPS, enabling easier comparison and analysis of training performance.

## Installation

Install via [PyPI](https://pypi.org/) in the same python virtual environment that you have mlagents installed:

```bash
pip install mlagents_sps_plugin
```

Run ML-Agents Training as Usual: Just run your `mlagents-learn` commands as you normally would. The plugin will automatically log the Steps Per Second (SPS) to TensorBoard and the console so you can monitor the performance in real-time.

## Contributing

We welcome contributions! If you have ideas for improvements, feel free to submit a pull request or open an issue.

## Support

If you appreciate this work or are looking for software and AI development, visit [Digiwave](https://dgwave.net) for more details on our tech services.
