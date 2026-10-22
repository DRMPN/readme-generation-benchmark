# delPezzo<h2>Description</h2>

<p><strong>delPezzo</strong> is a SageMath module for studying the flexibility of affine cones over del Pezzo surfaces.</p>

<p>In this context, <em>flexibility</em> refers to the existence of uniruled cylinders on the cone — that is, whether the cone admits families of algebraic cylinders covering it. The module works with smooth del Pezzo surfaces (including weak del Pezzo surfaces) and analyzes when the corresponding affine cone can be covered by cylinders coming from anticanonical pencils on the surface.</p>

<p>The main capabilities of the module include:</p>

<ul>
<li><strong>Surface and geometry machinery</strong> — construction of (weak) del Pezzo surfaces, working with their curves, points, and blowdown contractions (<code>Surface</code>, <code>Curve</code>, <code>Contraction</code>, <code>Point</code>).</li>
<li><strong>Cylinder detection</strong> — computation of cylinders on the surface and collections of cylinders whose union covers the complement of their anticanonical degree; a <code>CylinderList</code> also tracks auxiliary information such as the (-1)-curves left in the complement and the generic fiber class, and reports whether the cylinder collection is <em>transversal</em>.</li>
<li><strong>Cone-based search</strong> — a <code>Finder</code> component that searches for cylinder coverings by analyzing the effective cone and its subdivisions (<code>NE_SubdivisionCone</code>), including checks on relative interior intersections of cones.</li>
<li><strong>Dependencies handling</strong> — tracking of "weak dependencies" (<code>WeakDependencies</code>) that record which (-1)-curves are used in a given construction.</li>
<li><strong>Data import</strong> — parsing of a precomputed database of weak del Pezzo surfaces (the Lubbes database) to generate the surfaces that the analysis is applied to.</li>
</ul>

<p>Typical use cases: checking whether a given affine cone over a del Pezzo surface is flexible, finding all anticanonical pencils whose generic fiber is trivial, and enumerating transversal cylinder collections with their corresponding polarity cones and forbidden curves.</p>
<h2>Requirements</h2>

<p>This project is a <a href="https://www.sagemath.org/">SageMath</a> module, so a working SageMath installation is required before you can use it.</p>

<ul>
<li><strong>Python</strong>: version 3.9 or higher (<code>requires-python = "&gt;=3.9"</code>)</li>
<li><strong>SageMath</strong>: the module relies on SageMath, which provides its own bundled Python environment</li>
</ul>

<h3>Testing</h3>

<p>The test suite uses <a href="https://docs.pytest.org/">pytest</a>, with the following configuration specified in <code>pyproject.toml</code>:</p>

<p><code>toml
[tool.pytest.ini_options]
addopts = "--import-mode importlib -p no:warnings"
</code></p>

<p>Note that tests should be run using the Python interpreter bundled with SageMath, since the module imports SageMath functionality (e.g. in <code>surface.py</code>).</p>
<h2>Installation</h2>

<p><code>delPezzo</code> is a <a href="https://www.sagemath.org/">SageMath</a> module, so a working SageMath installation is required before installing the package. Python 3.9 or newer is supported.</p>

<p>To install the module, clone the repository and install it with <code>pip</code>:</p>

<p><code>bash
git clone &lt;repository-url&gt;
cd delPezzo
sage -pip install .
</code></p>

<p>If you prefer to work inside a virtual environment, you can create one and install the package as follows:</p>

<p><code>bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
</code></p>

<p>Once installed, the module can be imported (both in Python and in Sage):</p>

<p><code>python
from delPezzo import Surface, WeakDependencies
</code></p>

<p>This gives you access to the core classes of the library, such as <code>Surface</code>, <code>Curve</code>, <code>Contraction</code>, <code>Cylinder</code>, and <code>Finder</code>.</p>
<h2>Usage</h2>

<h3>Getting started</h3>

<p>The main entry point of the package is the <code>delPezzo</code> module, which exposes the core classes for working with del Pezzo surfaces and cylinders on them:</p>

<p><code>python
from delPezzo import Surface, WeakDependencies
</code></p>

<ul>
<li><code>Surface</code> — represents a del Pezzo surface, together with its curves (<code>Curve</code>), points (<code>Point</code>), and blow-down structure (<code>Contraction</code>, <code>WeakDependencies</code>).</li>
<li><code>WeakDependencies</code> — describes the weak dependency (blowing-down) structure of a surface.</li>
</ul>

<h3>Working with cylinders</h3>

<p>To search for cylinders on a del Pezzo surface, use the <code>Finder</code> class, which returns results as a <code>ConeCovering</code>. Individual cylinders are represented by the <code>Cylinder</code> class, and collections of cylinders by <code>CylinderList</code> / <code>CylinderGenerator</code>:</p>

<p><code>python
from delPezzo.cylinder import Cylinder, CylinderList
from delPezzo.finder import Finder, ConeCovering
</code></p>

<p>A <code>CylinderList</code> is a list of cylinders with extra information attached:</p>

<ul>
<li><code>complement</code> — the list of (-1)-curves lying in the complement of the cylinders' union;</li>
<li><code>fiber</code> — the generic fiber class of the collection (empty if the collection is transversal).</li>
</ul>

<h3>Cones and subdivisions</h3>

<p>Cones associated to surfaces (e.g. subdivisions of the nef cone and tests for intersection/relative interior containment) are provided in the <code>cone</code> module:</p>

<p><code>python
from delPezzo.cone import NE_SubdivisionCone, relint_contains_relint, relints_intersect
</code></p>

<h3>Loading surfaces from the families database</h3>

<p>The <code>Lubbes_parse</code> module provides helpers to generate surfaces from the families data (following Lubbes' minimal families of curves):</p>

<p><code>python
from delPezzo.Lubbes_parse import generate_surfaces, generate_surface, Lubbes_lines
</code></p>

<ul>
<li><code>generate_surfaces</code> / <code>generate_surface</code> — build <code>Surface</code> objects from the families data;</li>
<li><code>Lubbes_lines</code> — raw lines of the families data used by the generators.</li>
</ul>

<h3>References</h3>

<p>The cylinder-finding machinery implemented here is based on the following works:</p>

<ul>
<li>[CPW13] Ivan Cheltsov, Jihun Park, and Joonyeong Won. <em>Affine cones over smooth cubic surfaces</em>. Journal of the European Mathematical Society, 18(7):1537–1564, 2016. doi:10.4171/jems/622.</li>
<li>[CPW15] Ivan Cheltsov, Jihun Park, and Joonyeong Won. <em>Cylinders in del Pezzo surfaces</em>. International Mathematics Research Notices, 2017(4):1179–1230, 2017. doi:10.1093/imrn/rnw063.</li>
<li>[KimPark21] Jaehyun Kim and Jihun Park. <em>Generic flexibility of affine cones over del Pezzo surfaces of degree 2</em>. International Journal of Mathematics, 32(14):2150104, 2021. doi:10.1142/S0129167X21501044.</li>
<li>[Lub-min] Niels Lubbes. <em>Minimal families of curves on surfaces</em>. Journal of Symbolic Computation, 65:29–48, 2014. URL: https://www.sciencedirect.com/science/article/pii/S0747717114000133, doi:10.1016/j.jsc.2014.01.003.</li>
</ul>
<h2>Contributing</h2>
<h2>License</h2>
