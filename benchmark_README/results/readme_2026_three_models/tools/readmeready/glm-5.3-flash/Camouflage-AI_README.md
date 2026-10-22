# Camouflage-AI<h2>Description</h2>

<p><strong>Camouflage-AI</strong> is an AI-powered desktop tool for removing backgrounds from videos using YOLOv8 segmentation. It provides a graphical desktop interface in which users can process their videos to separate subjects of interest from the background.</p>

<p>The application is written in Python and is designed to run on Microsoft Windows. Under the hood, it builds on a set of established libraries for computer vision, image processing, and video handling, including:</p>

<ul>
<li><strong>CustomTkinter</strong> – the desktop GUI framework used for the application interface</li>
<li><strong>OpenCV</strong> – frame-level video processing</li>
<li><strong>Rembg</strong> – AI-based background removal support</li>
<li><strong>Pillow</strong> – image handling</li>
<li><strong>MoviePy</strong> – video editing and processing</li>
</ul>

<p>Key characteristics of the project:</p>

<ul>
<li><strong>AI segmentation:</strong> Background removal is driven by YOLOv8 segmentation.</li>
<li><strong>Desktop application:</strong> A user-friendly GUI rather than a command-line-only workflow.</li>
<li><strong>Platform:</strong> Targets Microsoft Windows and requires Python 3.8 or later.</li>
<li><strong>License:</strong> Released under the MIT License.</li>
</ul>

<p>The project is developed by Vishnu and is available at <a href="https://github.com/Vishnu-tppr/Camouflage-AI">https://github.com/Vishnu-tppr/Camouflage-AI</a>.</p>
<h2>Requirements</h2>

<ul>
<li><strong>Python</strong>: 3.8 or higher (<code>python_requires='&gt;=3.8'</code>)</li>
<li><strong>Operating System</strong>: Windows (Win32 / MS Windows environment)</li>
</ul>

<p>No additional third-party dependencies are explicitly listed in the project's setup configuration.</p>
<h2>Installation</h2>

<p>To install Camouflage-AI, follow these steps:</p>

<ol>
<li>Clone the repository from <a href="https://github.com/VishnuBhaarath/Camouflage-AI">GitHub</a>:</li>
</ol>

<p><code>bash
git clone https://github.com/VishnuBhaarath/Camouflage-AI.git
cd Camouflage-AI
</code></p>

<ol start="2">
<li><p>Ensure you have <strong>Python 3.8 or higher</strong> installed.</p></li>
<li><p>Install the required dependencies:</p></li>
</ol>

<p><code>bash
pip install customtkinter
pip install opencv-python
pip install numpy
pip install rembg
pip install pillow
pip install moviepy
pip install matplotlib
pip install scikit-image
pip install tqdm
pip install pyperclip
</code></p>

<p>Once all dependencies are installed, you are ready to use Camouflage-AI.</p>
<h2>Usage</h2>

<p>Camouflage-AI is a Windows desktop application (Python 3.8+) that is operated through a graphical user interface. The typical workflow is:</p>

<h3>1. Launch the application</h3>

<p>Run the application from the repository root. Once started, the main window presents the video-processing controls.</p>

<h3>2. Select a video</h3>

<p>Click the <strong>Select Video</strong> button and choose the video file you want to process.</p>

<h3>3. Choose a camouflage mode</h3>

<p>Select one of the available processing modes using the radio buttons:</p>

<ul>
<li><strong>Color</strong> – apply a solid color to the video. After choosing this mode, use the <strong>Select Color</strong> button to pick the color.</li>
<li><strong>Image</strong> – apply an image to the video. After choosing this mode, use the <strong>Select Image</strong> button to pick the image file.</li>
<li><strong>Blur</strong> – apply a blur effect (no additional selection is required).</li>
</ul>

<h3>4. Process the video</h3>

<p>Click the <strong>Process</strong> button to start processing the selected video with the chosen mode.</p>

<blockquote>
  <p><strong>Note:</strong> All input controls (video selection, mode radio buttons, color/image selection, and the Process button) are enabled and disabled together as a group, so they become unavailable while the application is busy and are re-enabled once it is ready to accept input again.</p>
</blockquote>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the MIT License.</p>

<p>```
MIT License</p>

<p>Copyright (c) 2025 Vishnu</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```</p>
<h2>Description</h2>

<p><strong>Camouflage-AI</strong> is an AI-powered desktop tool for removing video backgrounds using YOLOv8 segmentation. It provides a graphical desktop application (built with CustomTkinter) that runs on Windows and allows users to process video files and strip away their backgrounds automatically.</p>

<p>Key characteristics of the project:</p>

<ul>
<li><strong>AI-based segmentation</strong>: Uses YOLOv8 segmentation to identify and separate subjects from the video background.</li>
<li><strong>Desktop application</strong>: Ships with a graphical user interface built on the <a href="https://github.com/Vishnu-tppr/Camouflage-AI">customtkinter</a> toolkit.</li>
<li><strong>Video processing</strong>: Leverages libraries such as OpenCV, MoviePy, Pillow, NumPy, and scikit-image to handle frame extraction, processing, and video reconstruction.</li>
<li><strong>Windows-focused</strong>: Developed and distributed for the Microsoft Windows environment.</li>
<li><strong>Python 3.8+</strong>: Requires Python 3.8 or newer.</li>
</ul>

<p>The project is licensed under the MIT License and is authored by Vishnu.</p>
<h2>Requirements</h2>

<p>To run Camouflage-AI, you will need the following:</p>

<ul>
<li><strong>Python 3.8 or higher</strong> – the project requires <code>python &gt;= 3.8</code> as specified in its <code>setup.py</code>.</li>
<li><strong>Windows OS</strong> – the project is currently targeted at the Windows environment (<code>Environment :: Win32 (MS Windows)</code> classifier).</li>
</ul>

<p>Additional dependency information (e.g., required packages and their versions) can be found in the project's <code>setup.py</code> / packaging configuration within the <a href="https://github.com/">repository</a>.</p>
<h2>Installation</h2>

<p>To get started with <strong>Camouflage-AI</strong>, follow the steps below.</p>

<h3>Prerequisites</h3>

<ul>
<li>Python <strong>3.8</strong> or higher is required.</li>
</ul>

<h3>Install Dependencies</h3>

<p>Install the required Python packages using <code>pip</code>:</p>

<p><code>bash
pip install customtkinter
pip install opencv-python
pip install numpy
pip install rembg
pip install pillow
pip install moviepy
pip install matplotlib
pip install scikit-image
pip install tqdm
pip install pyperclip
</code></p>

<p>Alternatively, you can install them in a single command:</p>

<p><code>bash
pip install customtkinter opencv-python numpy rembg pillow moviepy matplotlib scikit-image tqdm pyperclip
</code></p>

<p>Once the dependencies are installed, you are ready to run the project.</p>
<h2>Usage</h2>

<p>Camouflage-AI provides a desktop graphical interface built with Tkinter for applying camouflage effects to videos.</p>

<blockquote>
  <p><strong>Note:</strong> This project is designed to run on Windows (<code>Environment :: Win32 (MS Windows)</code>) and requires <strong>Python 3.8 or later</strong> (<code>python_requires='&gt;=3.8'</code>).</p>
</blockquote>

<h3>Basic Workflow</h3>

<ol>
<li><p><strong>Launch the application</strong> — start the program from your local clone of the repository.</p></li>
<li><p><strong>Select a video</strong> — click the <strong>Select Video</strong> button to choose the video file you want to process.</p></li>
<li><p><strong>Choose a camouflage mode</strong> — once a video is loaded, the controls become enabled and you can pick one of three processing modes using the radio buttons:</p>

<ul>
<li><strong>Color</strong> — use a solid color as the camouflage source.</li>
<li><strong>Image</strong> — use an image file as the camouflage source.</li>
<li><strong>Blur</strong> — apply a blur-based camouflage effect.</li>
</ul></li>
<li><p><strong>Select a source (if applicable)</strong> — if you chose the <strong>Color</strong> or <strong>Image</strong> mode, use the corresponding <strong>Select Color</strong> / <strong>Select Image</strong> button to pick your camouflage source.</p></li>
<li><p><strong>Process the video</strong> — click the <strong>Process</strong> button to start applying the selected camouflage effect to your video.</p></li>
</ol>

<p>While the application is working, the selection and processing controls are disabled to prevent conflicting inputs, and they are re-enabled once the operation completes.</p>
<h2>Contributing</h2>

<p>Contributions are welcome! If you'd like to help improve Camouflage-AI, please follow these steps:</p>

<ol>
<li><strong>Fork the repository</strong> on GitHub: <a href="https://github.com/Vishnu-tppr/Camouflage-AI">https://github.com/Vishnu-tppr/Camouflage-AI</a></li>
<li><strong>Clone your fork</strong> locally:
<code>bash
git clone https://github.com/&lt;your-username&gt;/Camouflage-AI.git
</code></li>
<li><strong>Create a new branch</strong> for your changes:
<code>bash
git checkout -b feature/your-feature-name
</code></li>
<li><strong>Install the project dependencies</strong> (Python 3.8+ required):
<code>bash
pip install customtkinter opencv-python numpy rembg pillow moviepy matplotlib scikit-image tqdm pyperclip
</code></li>
<li><strong>Make your changes</strong> and commit them with clear, descriptive messages.</li>
<li><strong>Push your branch</strong> and open a <strong>Pull Request</strong> against the main repository, describing what your change does and why it's needed.</li>
</ol>

<p>Please note that this project is licensed under the <a href="https://github.com/Vishnu-tppr/Camouflage-AI">MIT License</a>, so any contributions you submit will be governed by the same license.</p>
<h2>License</h2>

<p>This project is licensed under the <strong>MIT License</strong>.</p>

<p>Copyright (c) 2025 Vishnu</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>

<p><strong>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</strong></p>
