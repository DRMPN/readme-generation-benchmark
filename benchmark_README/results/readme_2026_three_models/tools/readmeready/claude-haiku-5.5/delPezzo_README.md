# delPezzo<h2>Description</h2>

<p>delPezzo is a SageMath module for studying the flexibility of affine cones over del Pezzo surfaces.</p>

<p>The package includes modules for:</p>

<ul>
<li><strong>Surfaces</strong>: representing del Pezzo surfaces, along with their curves, points, and contractions (<code>Surface</code>, <code>Curve</code>, <code>Point</code>, <code>Contraction</code>).</li>
<li><strong>Cylinders</strong>: collections of cylinders on a surface (<code>Cylinder</code>, <code>CylinderList</code>, <code>CylinderGenerator</code>).</li>
<li><strong>Cones</strong>: subdivisions of the cone of effective curves (<code>NE_SubdivisionCone</code>).</li>
<li><strong>Finding and covering</strong>: searching for structures and covering cones (<code>Finder</code>, <code>ConeCovering</code>).</li>
<li><strong>Lubbes parsing</strong>: generating surfaces from Lubbes data (<code>generate_surfaces</code>, <code>generate_surface</code>, <code>Lubbes_lines</code>).</li>
</ul>

<p>The package requires Python 3.9 or newer.</p>
<h2>Requirements</h2>

<ul>
<li><strong>Python 3.9 or newer</strong> (the project declares <code>requires-python = "&gt;=3.9"</code>).</li>
<li><strong>SageMath</strong>, since delPezzo is a SageMath module for studying flexibility of affine cones over del Pezzo surfaces.</li>
</ul>
<h2>Installation</h2>

<!-- Left blank: the provided context does not include installation instructions. -->
<h2>Usage</h2>

<p>The package is imported as <code>delPezzo</code>. The main classes are available directly from the top-level package:</p>

<p><code>python
from delPezzo import Surface, WeakDependencies
</code></p>

<p>The source also provides the following, which can be imported from their submodules:</p>

<ul>
<li><code>Cylinder</code>, <code>CylinderList</code>, <code>CylinderGenerator</code> (from <code>.cylinder</code>)</li>
<li><code>Finder</code>, <code>ConeCovering</code> (from <code>.finder</code>)</li>
<li><code>NE_SubdivisionCone</code>, <code>relint_contains_relint</code>, <code>relints_intersect</code> (from <code>.cone</code>)</li>
<li><code>generate_surfaces</code>, <code>generate_surface</code>, <code>Lubbes_lines</code> (from <code>.Lubbes_parse</code>)</li>
</ul>

<p>The available code does not include example calls or function signatures, so this section does not describe how to run the library.</p>
<h2>Contributing</h2>

<!-- No contribution guidelines were found in the provided context, so this section is left blank. -->
<h2>License</h2>
