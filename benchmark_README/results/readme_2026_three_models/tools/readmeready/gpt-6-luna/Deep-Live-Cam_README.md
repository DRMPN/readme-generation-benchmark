# Deep-Live-Cam<p>I’ll inspect the project’s README and core entry points to summarize what Deep-Live-Cam does without relying on assumptions.</p>

<h2>Description</h2>

<p>Deep-Live-Cam is an application for swapping a face from a source image onto a target image or video, and for using a live camera preview. It supports both a graphical interface and command-line operation, with options for processing frames and controlling the generated video output.</p>
<h2>Requirements</h2>

<ul>
<li>Python 3.10</li>
<li><code>pip</code></li>
<li>Git</li>
<li>FFmpeg</li>
</ul>

<p>A compatible GPU is optional; the application can also run without GPU acceleration.</p>
<p>I’ll inspect the repository’s setup instructions and dependency files to summarize the actual installation steps.</p>

<h2>Installation</h2>
<h2>Usage</h2>

<p>From the repository root, start the application with:</p>

<p><code>bash
python run.py
</code></p>

<p>To process a source image against a target, provide the source, target, and output paths:</p>

<p><code>bash
python run.py --source &lt;source-image&gt; --target &lt;target-video&gt; --output &lt;output-file&gt;
</code></p>

<p>You can select an execution provider and set the number of execution threads. For example:</p>

<p><code>bash
python run.py --execution-provider cpu --execution-threads 4
</code></p>

<p>Other available options include <code>--keep-fps</code>, <code>--keep-audio</code>, <code>--keep-frames</code>, <code>--many-faces</code>, <code>--mouth-mask</code>, <code>--nsfw-filter</code>, <code>--map-faces</code>, <code>--video-encoder</code>, and <code>--video-quality</code>. For live camera display, use <code>--live-mirror</code> or <code>--live-resizable</code>. The application also accepts <code>--max-memory</code> to set the RAM limit in GB and <code>--lang</code> to choose the UI language (default: <code>en</code>).</p>

<p>Use <code>python run.py --help</code> to see the command-line options, or <code>python run.py --version</code> to print the application version.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>Deep-Live-Cam is licensed under the GNU Affero General Public License, version 3 (AGPL-3.0). See the <code>LICENSE</code> file for the full terms.</p>
