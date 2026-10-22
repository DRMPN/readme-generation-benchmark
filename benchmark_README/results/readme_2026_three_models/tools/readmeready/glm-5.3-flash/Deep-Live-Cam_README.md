# Deep-Live-Cam<h2>Description</h2>

<p><strong>Deep-Live-Cam</strong> is a real-time AI-based face swap tool. It takes a single image of a face as the source and lets you swap that face onto a target — either a video/image file or a live webcam stream — all running locally on your own machine.</p>

<p>The project consists of a small set of modules:</p>

<ul>
<li><strong>Core swap logic</strong> — handles face detection, recognition, and swapping for both image/video files and live camera feeds.</li>
<li><strong>Frame processors</strong> — optional processing passes that can be chained together, such as the face enhancer and the mouth mask features.</li>
<li><strong>Command-line interface (<code>run.py</code>)</strong> — parses options like the source path, target path, output path, execution provider, execution threads, and max memory, then stores them in shared globals.</li>
<li><strong>Graphical user interface</strong> — a desktop UI for selecting a source face and a target webcam or file, previewing the live result, and starting the swap.</li>
</ul>

<h3>Key features</h3>

<ul>
<li><strong>Real-time webcam preview</strong> — swap a face live from your camera, with options to mirror the display (<code>--live-mirror</code>) and resize the preview window (<code>--live-resizable</code>).</li>
<li><strong>Image and video processing</strong> — swap faces in pictures or videos, with options to keep the original FPS (<code>--keep-fps</code>), keep the original audio (<code>--keep-audio</code>), and keep temporary frames (<code>--keep-frames</code>).</li>
<li><strong>Multiple faces</strong> — with <code>--many-faces</code>, every face in the target is swapped, and with <code>--map-faces</code> you can map different source faces to different target faces.</li>
<li><strong>Mouth masking</strong> — an optional frame processor that preserves the target's original mouth region, with configurable mask size and feathering.</li>
<li><strong>Face enhancement</strong> — an optional face enhancer frame processor to improve the quality of swapped faces.</li>
<li><strong>NSFW filter</strong> — an optional check (<code>--nsfw-filter</code>) that can block inappropriate content.</li>
<li><strong>Flexible execution</strong> — choose your execution provider (e.g. <code>cpu</code>, CoreML, CUDA) via <code>--execution-provider</code>, control the number of threads with <code>--execution-threads</code>, and cap RAM usage with <code>--max-memory</code>.</li>
<li><strong>Headless mode</strong> — when only the source, target, and/or output paths are supplied, the tool runs without opening the GUI, which makes it suitable for automation and scripting.</li>
<li><strong>Output control</strong> — choose the video encoder and quality for processed videos, and control logging verbosity via <code>--log-level</code>.</li>
</ul>

<h3>How it works (typical usage)</h3>

<ol>
<li>Launch the app (GUI mode, or headless mode by passing <code>--source</code>, <code>--target</code>, and <code>-o</code>).</li>
<li>Pick an image containing a face as the <strong>source</strong>.</li>
<li>Pick a webcam or a video/image file as the <strong>target</strong>.</li>
<li>Start the live preview or the processing job; the selected face is swapped onto the target.</li>
<li>The result is written to the chosen output path (for videos, with the original FPS and audio preserved if those options are enabled).</li>
</ol>

<blockquote>
  <p><strong>Note:</strong> This tool is intended for responsible use. Always obtain consent from the people whose likeness you use and comply with applicable laws when creating face-swapped media.</p>
</blockquote>
<h2>Requirements</h2>

<p>Before installing and running <strong>Deep-Live-Cam</strong>, make sure your system meets the following prerequisites:</p>

<ul>
<li><strong>Python 3.10 or higher</strong> — the project is developed and tested against Python 3.10+.</li>
<li><strong>pip</strong> — Python's package manager, used to install the dependencies listed in <code>requirements.txt</code>.</li>
<li><strong>Git</strong> — needed to clone the repository and pull the model assets.</li>
<li><strong>FFmpeg</strong> — required for video processing tasks such as preserving frame rate and handling audio in output files.</li>
<li><strong>A webcam</strong> (optional) — required only if you intend to use the real-time live preview feature.</li>
</ul>

<h3>GPU Support (Optional)</h3>

<p>Deep-Live-Cam can run on CPU, but performance is significantly better with a supported GPU:</p>

<ul>
<li><strong>NVIDIA GPU</strong> with CUDA support for accelerated processing on Windows/Linux.</li>
<li><strong>Apple Silicon</strong> (M1/M2/M3) with CoreML support on macOS.</li>
</ul>

<p>If no compatible GPU is available, the application will fall back to CPU execution, which works but is slower.</p>

<p>All Python package dependencies are pinned in the project's <code>requirements.txt</code> file, so once Python and pip are set up, installing everything else is handled by the installation steps described in the next section.</p>
<h2>Installation</h2>

<blockquote>
  <p><strong>Note:</strong> In order to achieve better output quality, the processing time will be increased. Please be patient during face swapping and face enhancement.</p>
</blockquote>

<h3>Pre-requisites</h3>

<p>Before installing Deep-Live-Cam, make sure you have the following:</p>

<ul>
<li><strong>Python 3.10</strong> (recommended, works on Windows, macOS and Linux)</li>
<li><strong>pip</strong> (Python package manager)</li>
<li><strong>git</strong></li>
<li><strong>ffmpeg</strong></li>
<li>A code editor such as Visual Studio Code (optional, but useful)</li>
</ul>

<h3>Setup</h3>

<h4>1. Clone the Repository</h4>

<p><code>bash
git clone https://github.com/hacksider/Deep-Live-Cam.git
cd Deep-Live-Cam
</code></p>

<h4>2. Download the Models</h4>

<p>The project relies on two ONNX models for face swapping and face enhancement. Download both models and place them inside the <code>assets</code> folder of the repository:</p>

<ul>
<li><code>inswapper_128.onnx</code> — used for face swapping</li>
<li><code>GFPGANv1.4.onnx</code> — used for face enhancement</li>
</ul>

<h4>3. Install Dependencies (Windows / Linux)</h4>

<p>It is recommended to set up a virtual environment first:</p>

<p>```bash</p>

<h1>Windows</h1>

<p>python -m venv venv
venv\Scripts\activate</p>

<h1>Linux</h1>

<p>python3 -m venv venv
source venv/bin/activate
```</p>

<p>Then install the required Python packages:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>

<h4>4. Install Dependencies (macOS — Apple Silicon)</h4>

<p>For macOS with Apple Silicon (M1/M2/M3), use the following steps:</p>

<p>```bash</p>

<h1>Install Python 3.10 and ffmpeg via Homebrew</h1>

<p>brew install python@3.10
brew install ffmpeg</p>

<h1>Create and activate a virtual environment</h1>

<p>python3 -m venv venv
source venv/bin/activate</p>

<h1>Install the required Python packages</h1>

<p>pip install -r requirements.txt
```</p>

<h3>FFmpeg Installation</h3>

<p>FFmpeg is required for processing video streams. Install it based on your operating system:</p>

<p><strong>Windows:</strong>
<code>bash
winget install ffmpeg
</code>
Alternatively, download a build from the FFmpeg website and add it to your <code>PATH</code>.</p>

<p><strong>macOS:</strong>
<code>bash
brew install ffmpeg
</code></p>

<p><strong>Linux:</strong>
<code>bash
sudo apt install ffmpeg
</code></p>

<h3>GPU Acceleration (Optional)</h3>

<p>Deep-Live-Cam can run on the CPU out of the box, but for significantly better performance you can enable GPU execution. Make sure the appropriate CUDA execution provider is installed (for NVIDIA GPUs), and run the application with the corresponding <code>--execution-provider</code> flag as described in the usage section.</p>

<h3>Running the Application</h3>

<p>Once installation is complete, you can start the application:</p>

<p><code>bash
python run.py
</code></p>

<p>A GUI window will open, allowing you to select source and target media and start the live camera or face swap processing.</p>
<h2>Usage</h2>

<h3>Running the Program</h3>

<p>To start the application, run the following command from the root of the <a href="https://github.com">repository</a>:</p>

<p><code>bash
python run.py
</code></p>

<p>This opens the graphical user interface (GUI), where you can:</p>

<ol>
<li><strong>Select a source</strong> – Choose the face image you want to swap from (an image of a person's face).</li>
<li><strong>Select a target</strong> – Choose the target media. This can be an image, a video, or the live webcam.</li>
<li><strong>Start the process</strong> – Click <code>START</code> to begin the face swap on the selected target. For the webcam, click <code>LIVE</code> to run in real time.</li>
</ol>

<h3>Webcam / Live Mode</h3>

<p>After selecting a source image, click the <code>LIVE</code> button to start face swapping on your live camera feed. Use the options below to control the live preview:</p>

<ul>
<li><code>--live-mirror</code> – Display the live camera as you would see it in a front-facing (mirrored) camera frame.</li>
<li><code>--live-resizable</code> – Make the live camera frame resizable.</li>
</ul>

<h3>Command Line (Headless) Mode</h3>

<p>The program can also be run without the GUI by providing a source and/or target path directly. When <code>--source</code>, <code>--target</code>, or <code>--output</code> paths are supplied, the application runs in headless mode.</p>

<p><strong>Face swap on a video:</strong></p>

<p><code>bash
python run.py --source &lt;source_image_path&gt; --target &lt;target_video_path&gt; --output &lt;output_video_path&gt;
</code></p>

<h3>Command Line Options</h3>

<p>The following options are available when running <code>python run.py</code>:</p>

<p>| Option | Description |
|---|---|
| <code>-s</code>, <code>--source</code> | Path to the source image (the face to swap from) |
| <code>-t</code>, <code>--target</code> | Path to the target image/video, or <code>0</code> for the webcam |
| <code>-o</code>, <code>--output</code> | Path where the output file will be saved |
| <code>--frame-processor</code> | Frame processor to use (e.g. face swapper, face enhancer) |
| <code>--keep-fps</code> | Keep the frames per second of the original target video |
| <code>--keep-audio</code> | Keep the audio of the original target video |
| <code>--keep-frames</code> | Keep the temporary frames in the output directory |
| <code>--many-faces</code> | Apply the face swap to all faces detected in the target, not just the best match |
| <code>--mouth-mask</code> | Apply a mouth mask to improve the realism of the swap |
| <code>--map-faces</code> | Map faces from the target so multiple source faces are swapped onto matching target faces |
| <code>--nsfw-filter</code> | Filter out NSFW content |
| <code>--video-encoder</code> | Video encoder to use for output videos |
| <code>--video-quality</code> | Video quality for the output video |
| <code>--live-mirror</code> | Mirror the live camera preview like a front-facing camera |
| <code>--live-resizable</code> | Make the live camera frame resizable |
| <code>--max-memory</code> | Maximum amount of RAM to use, in GB |
| <code>--execution-provider</code> | Execution provider(s) to use (e.g. <code>cpu</code>, <code>cuda</code>, <code>coreml</code>). Defaults to <code>cpu</code> |
| <code>--execution-threads</code> | Number of execution threads to use |
| <code>-l</code>, <code>--lang</code> | UI language (defaults to <code>en</code>) |
| <code>-v</code>, <code>--version</code> | Show the program name and version, then exit |</p>

<h3>Example</h3>

<p>Swap a face from <code>source.jpg</code> onto <code>target.mp4</code> and save the result as <code>output.mp4</code>:</p>

<p><code>bash
python run.py --source source.jpg --target target.mp4 --output output.mp4
</code></p>

<p>To run on a GPU, specify an execution provider, for example:</p>

<p><code>bash
python run.py --execution-provider cuda
</code></p>
<h2>Contributing</h2>

<p>We welcome contributions to improve this project! Please follow these guidelines to help us review and merge your work smoothly:</p>

<ol>
<li><strong>Fork the repository</strong> and create a new branch for your feature or bug fix.</li>
<li><strong>Create a pull request</strong> for your contribution with a clear description.</li>
<li><strong>Explain the changes</strong> you've made in your pull request, including the motivation behind them and any issues they address.</li>
<li><strong>Ensure your code adheres</strong> to the project's existing style and standards, and test your changes before submitting.</li>
</ol>

<p>If you find a bug or have an idea for an improvement but are not ready to write the code yourself, please open an issue describing the problem or feature so the maintainers and community can discuss it.</p>

<blockquote>
  <p><strong>Note:</strong> By contributing to this project, you agree that your contributions will be licensed under the project's license.</p>
</blockquote>
<h2>License</h2>

<p>This project is licensed under the <strong>GNU Affero General Public License v3.0 (AGPL-3.0)</strong>. The full text of the license can be found in the <a href="LICENSE">LICENSE</a> file in the root of this repository.</p>

<h3>Key Terms of the License</h3>

<ul>
<li><strong>Copyleft Requirement</strong>: Any modified version of this software must also be licensed under the AGPL-3.0, and the complete corresponding source code must be made available to anyone who comes into possession of a copy of the work.</li>
<li><strong>Network Use</strong>: If you run a modified version of this software as a network service, you must make the source code of the modified version available to users interacting with it remotely.</li>
<li><strong>Attribution</strong>: The work must carry prominent notices stating that it is released under this License.</li>
<li><strong>Warranty Disclaimer</strong>: The software is provided "as is", without warranty of any kind, as detailed in sections 15 and 16 of the license.</li>
</ul>

<h3>Important Usage Notice</h3>

<p>This software is intended to be used in an ethical and legally responsible manner. By using this project, you agree to the terms of the AGPL-3.0 license and acknowledge that:</p>

<ul>
<li>You will not use this software for any illegal or unethical purposes, including but not limited to creating misleading content, impersonating individuals without consent, or violating the privacy and rights of others.</li>
<li>The creators and contributors of this software are not responsible for any misuse of the software.</li>
</ul>

<p>If you add your own material to a covered work, you may (if authorized by the copyright holders of that material) supplement the terms of this License with additional terms, such as disclaiming warranty or limiting liability differently, requiring preservation of legal notices or author attributions, prohibiting misrepresentation of origin, limiting publicity uses of licensors' names, or declining trademark rights — as permitted under section 7 of the AGPL-3.0 license.</p>
