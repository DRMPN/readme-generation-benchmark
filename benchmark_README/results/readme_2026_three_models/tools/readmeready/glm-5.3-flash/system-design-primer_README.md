# system-design-primer<h2>Description</h2>

<p><strong>system-design-primer</strong> is a collection of resources for learning how to design large-scale systems and for preparing for system design and object-oriented design interviews. It was created by <a href="https://github.com/donnemartin">Donne Martin</a>, and the source and license info is on <a href="https://github.com/donnemartin/system-design-primer">GitHub</a>.</p>

<p>The repository contains worked design problems presented as interactive Python 3 notebooks. Each notebook follows a consistent structure:</p>

<ul>
<li><strong>Constraints and assumptions</strong> — the problem is scoped up front, clarifying what is being designed and what can be assumed. For example:
<ul>
<li><em>Design an LRU cache</em> — we are caching the results of web queries, inputs are assumed to be valid, and the cache is assumed to fit in memory</li>
<li><em>Design an online chat</em> — the focus is on text conversations, user management (adding, removing, and updating users), friend request workflows (approve/reject), and group chats</li>
<li><em>Design a deck of cards</em> — a generic 52-card, four-suit deck for games like poker, which is then extended to black jack</li>
</ul></li>
<li><strong>Solution</strong> — the design is implemented in Python, with code cells and their outputs so the reader can run and experiment with the solution directly</li>
</ul>

<p>The notebooks are maintained alongside the rest of the project's system design material, and each one notes that it was prepared by <a href="https://github.com/donnemartin">Donne Martin</a>, with source and license info available on <a href="https://github.com/donnemartin/system-design-primer">GitHub</a>.</p>
<h2>Requirements</h2>

<p>There is very little you need to install or configure to use this project — it is primarily a reading and study resource:</p>

<ul>
<li><p><strong>Reading the guide</strong> — nothing to install. The study guide and all of the system design topics are plain Markdown documents that render directly on GitHub, so the material can be read entirely in a browser.</p></li>
<li><p><strong>Running the solution notebooks</strong> — the sample solutions for the object-oriented design exercises (such as <em>Design an LRU cache</em>, <em>Design a deck of cards</em>, and <em>Design an online chat</em>) are provided as Jupyter notebooks written in Python 3. To open and execute them interactively you need:</p>

<ul>
<li>Python 3</li>
<li>Jupyter Notebook</li>
</ul>

<p>You can also simply read the solutions in the browser, since GitHub renders notebooks directly.</p></li>
<li><p><strong>Dependencies</strong> — the notebook code relies only on the Python standard library (for example, the <code>enum</code> module), so no third-party packages need to be installed.</p></li>
<li><p><strong>Flash cards (optional)</strong> — the project provides Anki flash cards for spaced-repetition study; to use them you need the Anki application.</p></li>
</ul>

<p>All of the tools listed above are free to download and use. Source and license information for the project is available on <a href="https://github.com/donnemartin/system-design-primer">GitHub</a>.</p>
<h2>Installation</h2>

<p>This project is a collection of study materials for system design interviews. It consists primarily of Markdown documents and interactive Jupyter notebooks, so there is nothing to compile or install — no external dependencies or build steps are required.</p>

<p>To get started, simply clone the repository to your local machine:</p>

<p><code>bash
git clone &lt;repository-url&gt;
</code></p>

<p>Once cloned, you can read the study guide and related documents directly, or open the interactive notebooks (such as the notebook implementing an LRU cache) to explore the accompanying Python code examples. The notebooks use Python 3 and can be run with any standard Python 3 environment (for example, using Jupyter Notebook or JupyterLab).</p>
<h2>Usage</h2>

<p>This repo is designed as a study resource to help you prepare for the <strong>System Design Interview</strong>. You can work through it end to end, or jump straight to the topics and exercises you want to review. Source and license info is on <a href="https://github.com/donnemartin/system-design-primer">GitHub</a>.</p>

<h3>Study guide</h3>

<h4>Suggested study plan</h4>

<ul>
<li><strong>Review</strong> the system design topics to build a foundation in scalability and distributed system fundamentals.</li>
<li><strong>Work through</strong> the system design interview questions with solutions — for example, designing an online chat. Each exercise first lays out the constraints and assumptions, then presents the solution.</li>
<li><strong>Work through</strong> the object-oriented design interview questions with solutions — for example, designing an LRU cache.</li>
<li><strong>Reinforce</strong> what you've learned with the flashcards.</li>
</ul>

<h3>Flashcards</h3>

<p>Flashcards are included to help you study and retain the key concepts covered throughout the repo.</p>

<h3>Interactive coding challenges</h3>

<p>Looking for resources to help you practice for the <strong>Coding</strong> Interview? Check out the sister repo <strong>Interactive Coding Challenges</strong>, which contains a growing set of interactive coding challenges with solutions.</p>

<p>This material was prepared by <a href="https://github.com/donnemartin">Donne Martin</a>.</p>
<h2>Contributing</h2>

<p>Contributions are welcome!</p>
<h2>License</h2>

<p>```
Copyright 2017 Donne Martin</p>

<p>Creative Commons Attribution 4.0 International License (CC-BY 4.0)</p>

<p>http://creativecommons.org/licenses/by/4.0/
```</p>
