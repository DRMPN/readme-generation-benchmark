# face_recognition<h2>Description</h2>

<p><code>face_recognition</code> is a Python library and command-line tool for finding and recognizing faces in images. It provides functions for locating faces, identifying facial features, generating face encodings, and comparing faces. The library is built on dlib’s face-recognition models.</p>
<p>I’ll inspect the project’s installation and packaging files to identify the requirements documented or enforced by the repository.</p>

<h2>Requirements</h2>

<ul>
<li>Python 3.3+ or Python 2.7</li>
<li>macOS or Linux. Windows is not officially supported, though it may work.</li>
</ul>
<h2>Installation</h2>

<p>From the repository root, install the package into the active Python 3 environment:</p>

<p><code>bash
python3 setup.py install
</code></p>
<h2>Usage</h2>

<h3>Command-line interface</h3>

<p>The <code>face_recognition</code> command compares faces in a directory of known people with faces in another directory:</p>

<p><code>bash
face_recognition ./known_people/ ./unknown_pictures/
</code></p>

<p>The filenames in <code>known_people</code> are used as the people’s names. The command prints each image filename and the name matched to a face it finds. Use <code>--tolerance</code> to adjust how closely faces must match; a lower value is stricter. The default tolerance is <code>0.6</code>. Add <code>--show-distance</code> to include the face distance in the output.</p>

<h3>Python</h3>

<p>Load an image and find its face locations, landmarks, or encodings:</p>

<p>```python
import face_recognition</p>

<p>image = face<em>recognition.load</em>image_file("photo.jpg")</p>

<p>face<em>locations = face</em>recognition.face<em>locations(image)
face</em>landmarks = face<em>recognition.face</em>landmarks(image)
face<em>encodings = face</em>recognition.face_encodings(image)
```</p>

<p>To compare a face in an unknown image with a known face:</p>

<p>```python
import face_recognition</p>

<p>known<em>image = face</em>recognition.load<em>image</em>file("known.jpg")
known<em>encoding = face</em>recognition.face<em>encodings(known</em>image)[0]</p>

<p>unknown<em>image = face</em>recognition.load<em>image</em>file("unknown.jpg")
unknown<em>encoding = face</em>recognition.face<em>encodings(unknown</em>image)[0]</p>

<p>matches = face<em>recognition.compare</em>faces([known<em>encoding], unknown</em>encoding)
print(matches[0])
```</p>

<p><code>compare_faces</code> returns a boolean for each known encoding, indicating whether it matches the unknown encoding.</p>
<p>I’ll inspect the repository’s contribution guide and use its contents to draft the README section.</p>

<h2>Contributing</h2>
<h2>License</h2>

<p>MIT License</p>

<p>Copyright (c) 2021, Adam Geitgey</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>
