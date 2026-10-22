# python-fire<h2>Description</h2>

<p>When Fire generates help text for a component (a function, class, or object), the <strong>Description</strong> section gives a longer explanation of what that component does.</p>

<p>The text comes from the component's docstring:</p>

<ul>
<li>If a description is available, it is used.</li>
<li>If there is no description, Fire falls back to the summary (the first line of the docstring).</li>
<li>If neither is available, the section is omitted.</li>
</ul>

<p>For builtin objects whose docstrings are messy or unhelpful, Fire uses custom descriptions instead. These are generated for the component, and the description and summary are trimmed to fit the help screen's line length and indentation.</p>

<p>Fire parses docstrings with a few known limitations:</p>

<ul>
<li>A description must be separated from the summary by a blank line. Otherwise, the description is merged into the summary.</li>
<li>Some reStructuredText (RST) field styles are not fully supported. For example, <code>:rtype:</code> and other return-type directives are ignored, and <code>:raises ExceptionType:</code> ignores the exception type.</li>
<li>Sections such as "Examples" and "Notes" are recognized as their own section types, but "Returns" sections written as <code># Returns</code> are not.</li>
</ul>
<h2>Requirements</h2>
<h2>Installation</h2>

<p>Python Fire is published as the <code>fire</code> package and can be installed with pip:</p>

<p><code>bash
pip install fire
</code></p>

<p><strong>Requirements:</strong></p>

<ul>
<li>Python 3.7 or later (<code>requires_python='&gt;=3.7'</code>). Classifiers list support for Python 3.7 through 3.13.</li>
<li>The <code>termcolor</code> package, which is installed automatically as a dependency.</li>
</ul>

<p>The project is licensed under the Apache Software License and works on Windows, macOS, and POSIX/Unix systems.</p>

<p>For the source code, see the <a href="https://github.com/google/python-fire">python-fire GitHub repository</a>.</p>
<h2>Usage</h2>

<p>Fire generates a help screen for a component, such as a function, class, or object. The help screen is built from the component's docstring and its arguments.</p>

<p>The usage details part of the help screen is divided into up to four sections, depending on what the component contains:</p>

<ul>
<li><strong>GROUPS</strong>: Groups of members that the component exposes.</li>
<li><strong>COMMANDS</strong>: Callable members that can be run as commands.</li>
<li><strong>VALUES</strong>: Non-callable members, shown with their values.</li>
<li><strong>INDEXES</strong>: Index choices for the component.</li>
</ul>

<p>A section appears only when the component has members of that kind. The <code>verbose</code> option controls whether private members are included in the help screen.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>Python Fire is licensed under the Apache License, Version 2.0. You may use this project in compliance with that license. A copy of the license is available at http://www.apache.org/licenses/LICENSE-2.0.</p>

<p>Copyright 2017 Google Inc. All rights reserved.</p>
