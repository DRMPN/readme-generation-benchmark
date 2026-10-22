# SMSBoom<h2>Description</h2>

<p>SMSBoom is a SMS bombing tool (短信轰炸) written in Python. It is designed to send a large volume of SMS messages to a target phone number by exploiting publicly available web interfaces that trigger SMS verification codes.</p>

<p>Key features of the project include:</p>

<ul>
<li><strong>Large collection of built-in SMS interfaces</strong>: The tool ships with a set of pre-configured API endpoints (interfaces) from various websites that can be abused to trigger SMS messages to a given phone number.</li>
<li><strong>Custom interface support</strong>: Users can add their own interfaces by contributing additional API definitions, allowing the tool to be extended with new SMS-triggering endpoints.</li>
<li><strong>Proxy support</strong>: Requests can be routed through HTTP proxies (or proxy pools) to avoid rate-limiting and IP bans from the target services.</li>
<li><strong>Configurable concurrency</strong>: The number of threads/concurrent requests can be tuned to control the speed of the bombing.</li>
<li><strong>Docker deployment</strong>: The project can be deployed easily via Docker, making it simple to run without manually setting up the Python environment.</li>
</ul>

<p>The project is licensed under the Apache License 2.0, with copyright held by WhaleFall (2022).</p>

<blockquote>
  <p><strong>Note</strong>: This tool is intended for educational and security research purposes only. Using it to harass others or for any illegal activity is strictly prohibited, and users bear full responsibility for their own actions.</p>
</blockquote>
<h2>Requirements</h2>

<p>To run SMSBoom, you will need the following:</p>

<ul>
<li><strong>Python 3.9+</strong> — the project requires Python version 3.9 or higher.</li>
</ul>

<p>All other dependencies used by the project are listed in the <code>requirements.txt</code> file and can be installed with:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>
<h2>Installation</h2>

<h3>Requirements</h3>

<p>Before you begin, make sure your environment meets the following requirements:</p>

<ul>
<li><strong>Python 3.7+</strong> (Python 3 is required; the project does not support Python 2)</li>
<li><strong>pip3</strong> (Python's package manager)</li>
</ul>

<h3>Clone the Repository</h3>

<p>First, clone the project from GitHub and change into the project directory:</p>

<p><code>bash
git clone https://github.com/WhaleFell/SMSBoom.git
cd SMSBoom
</code></p>

<h3>Install Dependencies</h3>

<p>The project depends on several third-party Python libraries (such as HTTP clients used to send the requests), which are all listed in the <code>requirements.txt</code> file. Install them with:</p>

<p><code>bash
pip3 install -r requirements.txt
</code></p>

<blockquote>
  <p><strong>Tip:</strong> If you have multiple versions of Python installed on your system, make sure <code>pip3</code> corresponds to your Python 3 installation. On some systems you may need to use <code>python3 -m pip install -r requirements.txt</code> instead.</p>
</blockquote>

<h3>Verify the Installation</h3>

<p>Once the dependencies are installed, you can verify that everything works by viewing the command-line help:</p>

<p><code>bash
python3 smsboom.py --help
</code></p>

<p>If the help output is displayed without errors, the installation was successful and the tool is ready to use.</p>
<h2>Usage</h2>

<h3>获取帮助</h3>

<p>运行以下命令可以查看完整的帮助信息：</p>

<p><code>shell
python3 smsboom.py -h
</code></p>

<p>帮助信息输出示例：</p>

<p>```text
usage: smsboom.py [-h] [-v] [--enable<em>enable</em>static] ...</p>

<p>optional arguments:
  -h, --help            show this help message and exit
```</p>

<h3>Windows 系统使用</h3>

<p>如果你下载了编译好的 Windows 可执行文件，可以在命令行（cmd）中直接运行：</p>

<p>```shell</p>

<h1>获取帮助</h1>

<p>smsboom_win64.exe -h</p>

<h1>命令行单次轰炸</h1>

<p>smsboom_win64.exe oneRun</p>

<h1>命令行循环轰炸</h1>

<p>smsboom_win64.exe loopRun</p>

<h1>加参数运行</h1>

<p>smsboom_win64.exe run --phone xxx --interval 65 --thread 32
```</p>

<h3>Linux / macOS 使用</h3>

<p>如果你是克隆仓库使用源码运行，请先安装依赖：</p>

<p><code>shell
pip3 install -r requirements.txt
</code></p>

<p>然后按以下方式运行：</p>

<p>```shell</p>

<h1>获取帮助</h1>

<p>python3 smsboom.py -h</p>

<h1>命令行单次轰炸</h1>

<p>python3 smsboom.py oneRun</p>

<h1>命令行循环轰炸</h1>

<p>python3 smsboom.py loopRun</p>

<h1>加参数直接运行</h1>

<p>python3 smsboom.py run --phone xxx --interval 65 --thread 32
```</p>

<h3>运行参数说明</h3>

<p>| 参数 | 说明 |
| --- | --- |
| <code>--phone</code> | 目标手机号 |
| <code>--interval</code> | 轰炸间隔（单位：秒） |
| <code>--thread</code> | 开启的线程数 |</p>

<h3>GUI 使用</h3>

<p>如果你更习惯图形界面，可以直接运行 GUI 程序：</p>

<p><code>shell
python3 gui.py
</code></p>
<h2>Contributing</h2>

<p>Contributions to SMSBoom are welcome! If you would like to help improve the project, here are some ways you can contribute:</p>

<ul>
<li><strong>Report bugs</strong> — If you encounter an issue while using SMSBoom, please open an issue describing the problem and how to reproduce it.</li>
<li><strong>Suggest features</strong> — Ideas for new functionality or improvements are always appreciated.</li>
<li><strong>Submit pull requests</strong> — Fork the repository, make your changes, and open a pull request. Please make sure your code follows the existing style of the project.</li>
</ul>

<p>Please note that this project is licensed under the <a href="http://www.apache.org/licenses/LICENSE-2.0">Apache License, Version 2.0</a>. By submitting a contribution, you agree that your work will be licensed under the same terms.</p>

<p>Copyright 2022 WhaleFall.</p>
<h2>License</h2>

<p>This project is licensed under the <a href="http://www.apache.org/licenses/LICENSE-2.0">Apache License 2.0</a>.</p>

<p>Copyright © 2022 WhaleFall</p>

<p>You are free to use, reproduce, and distribute this software in accordance with the terms of the Apache License 2.0. The software is provided on an "AS IS" basis, without warranties or conditions of any kind, either express or implied. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with your exercise of permissions under this License.</p>

<p>For the full license text, see the <a href="http://www.apache.org/licenses/LICENSE-2.0">LICENSE</a> file.</p>
