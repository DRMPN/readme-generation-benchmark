# Deep-Live-Cam<h2>Description</h2>

<p>Deep-Live-Cam is a tool for real-time and offline face swapping. It can swap faces in a live webcam feed or in a target image or video, using a source face image. The project provides both an interactive graphical mode and a headless command-line mode.</p>

<p>The application's behavior is controlled through command-line arguments and a set of global settings. These settings include:</p>

<ul>
<li><strong>Inputs and outputs:</strong> a source image, a target image or video, and an output path. If a source or target is given on the command line, the tool runs in headless mode.</li>
<li><strong>Frame processors:</strong> the processing steps applied to each frame.</li>
<li><strong>Face handling:</strong> options to swap multiple faces (<code>many_faces</code>), map specific faces (<code>map_faces</code>), and apply a mouth mask (<code>mouth_mask</code>).</li>
<li><strong>Content filtering:</strong> an NSFW filter (<code>nsfw_filter</code>).</li>
<li><strong>Video output:</strong> options to keep the original frame rate (<code>keep_fps</code>), keep the original audio (<code>keep_audio</code>), and keep intermediate frames (<code>keep_frames</code>), as well as the video encoder and quality.</li>
<li><strong>Live display:</strong> options to mirror the live camera view (<code>live_mirror</code>) and make the camera window resizable (<code>live_resizable</code>).</li>
<li><strong>Performance:</strong> a memory limit (<code>max_memory</code>, in GB), execution providers (such as <code>cpu</code>), and the number of execution threads.</li>
</ul>
<h2>Requirements</h2>

<p><em>(Left blank: the provided context does not include information about this project's requirements, such as supported Python versions, dependencies, or hardware needs. The supplied text is GPL license terms and a code snippet that sets runtime options.)</em></p>
<h2>Installation</h2>

<!-- No installation instructions were available in the provided context, so this section is intentionally left blank. -->
<h2>Usage</h2>

<p>Deep-Live-Cam runs in two modes. It runs with a graphical UI by default. If you pass a source path, a target path, or an output path, it runs headless, without the UI.</p>

<h3>Command-line options</h3>

<p>| Option | Description | Default |
|---|---|---|
| <code>-l</code>, <code>--lang</code> | UI language | <code>en</code> |
| <code>--live-mirror</code> | Displays the live camera feed as you see it in a front-facing camera (mirrored) | Off |
| <code>--live-resizable</code> | Makes the live camera frame resizable | Off |
| <code>--max-memory</code> | Maximum amount of RAM to use, in GB | Suggested automatically based on your system |
| <code>--execution-provider</code> | Execution provider(s) to use. Accepts one or more values from the choices suggested for your system | <code>cpu</code> |
| <code>--execution-threads</code> | Number of execution threads | Suggested automatically based on your system |
| <code>-v</code>, <code>--version</code> | Prints the program name and version, then exits | |</p>

<h3>Processing options</h3>

<p>These settings are read from the command line and applied to the program's global configuration:</p>

<ul>
<li><strong>Source, target, and output paths:</strong> Set the source, target, and output locations. If the output path is not given, it is determined from the source and target paths.</li>
<li><strong>Frame and audio handling:</strong> <code>keep_fps</code>, <code>keep_audio</code>, and <code>keep_frames</code> control whether the frame rate, audio, and intermediate frames are kept.</li>
<li><strong>Face handling:</strong> <code>many_faces</code> and <code>map_faces</code> control how multiple faces are processed and mapped. <code>mouth_mask</code> applies a mouth mask.</li>
<li><strong>Content filtering:</strong> <code>nsfw_filter</code> enables the NSFW filter.</li>
<li><strong>Video output:</strong> <code>video_encoder</code> and <code>video_quality</code> set the encoder and output quality.</li>
<li><strong>Frame processors:</strong> <code>frame_processor</code> selects which frame processors to apply.</li>
</ul>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the GNU Affero General Public License v3 (AGPL-3.0).</p>

<p>Under this license, you may run the unmodified program without restriction. If you modify the program or distribute a work based on it, the license terms apply to the whole work, including its source code. Users who interact with a modified version over a network must be able to receive its Corresponding Source.</p>
