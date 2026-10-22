# face_recognition<h2>Description</h2>

<p>I don't have enough specific information about this project's description to generate accurate content for this section. The provided context only contains Sphinx documentation configuration files, which don't describe what the face_recognition project actually does.</p>
<h2>Requirements</h2>

<p>This section requires information about the project's dependencies (e.g., Python version requirements, libraries like dlib, etc.), but the provided context does not contain that information. Therefore, this section is left blank.</p>
<h2>Installation</h2>

<h3>Requirements</h3>

<ul>
<li>Python 3.3+ or Python 2.7</li>
<li>macOS or Linux (Windows is not officially supported, but might work)</li>
</ul>

<h3>Installing with pip</h3>

<p>First, make sure you have <code>dlib</code> and its dependencies installed:</p>

<p>```bash</p>

<h1>macOS</h1>

<p>brew install cmake</p>

<h1>Ubuntu/Debian</h1>

<p>sudo apt-get install cmake build-essential
```</p>

<p>Then install the package:</p>

<p><code>bash
pip install face_recognition
</code></p>

<h3>Installing from source</h3>

<p>Clone the repository and install manually:</p>

<p><code>bash
git clone https://github.com/ageitgey/face_recognition.git
cd face_recognition
python3 setup.py install
</code></p>

<p>You can also use the provided Makefile target:</p>

<p><code>bash
make install
</code></p>

<p>This will clean the workspace and install the package into the active Python's site-packages.</p>
<h2>Usage</h2>

<p>The <code>face_recognition</code> library can be used from the command line or from Python code.</p>

<h3>Command line</h3>

<p>Find and recognize faces in a photo:</p>

<p>```bash</p>

<h1>Find all the faces in a picture and show basic info about each one</h1>

<p>face_recognition /path/to/picture.jpg</p>

<h1>Compare the faces in a picture against faces in a folder of known people</h1>

<p>face<em>recognition ./folder</em>of<em>known</em>people.jpg ./unknown_pictures/
```</p>

<h3>Python</h3>

<p>You can also use the library directly from Python code:</p>

<p>```python
import face_recognition</p>

<h1>Load an image and find all the faces in it</h1>

<p>image = face<em>recognition.load</em>image<em>file("picture.jpg")
face</em>locations = face<em>recognition.face</em>locations(image)</p>

<h1>Get the 128-dimension face encodings for each face</h1>

<p>face<em>encodings = face</em>recognition.face_encodings(image)</p>

<h1>Compare a known face encoding with an unknown one to see if they match</h1>

<p>results = face<em>recognition.compare</em>faces(known<em>encodings, unknown</em>encoding)
```</p>

<p>Example scripts demonstrating common tasks (detecting faces, identifying people in photos, comparing faces, real-time face recognition with a webcam) can be found in the <code>examples</code> folder of the repository.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the MIT License.</p>

<p>Copyright (c) 2021, Adam Geitgey</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>
