# devops-exercises<h2>Description</h2>

<p><code>devops-exercises</code> contains DevOps exercises and configuration examples. The provided examples include a Kubernetes Deployment that runs three replicas of NGINX and Terraform configuration requiring Terraform 1.3 or later and the Google provider version 4.x.</p>
<h2>Requirements</h2>

<ul>
<li>Terraform version <strong>1.3.0 or later</strong>.</li>
<li>The Terraform Google provider, version <strong>4.10.0 or later and earlier than 5.0.0</strong>.</li>
</ul>
<h2>Installation</h2>

<p>Install the Python dependency with:</p>

<p><code>bash
pip install boto3==1.17.95
</code></p>

<p>For the Terraform configuration, use Terraform 1.3.0 or later. It declares the Google provider with a version constraint of <code>&gt;= 4.10.0, &lt; 5.0</code>.</p>
<h2>Usage</h2>

<p>Apply the Kubernetes manifest or manifests with <code>kubectl</code>:</p>

<p><code>sh
kubectl apply -f &lt;path-to-manifest-or-directory&gt;
</code></p>

<p>The Deployment requests three <code>nginx:1.14.2</code> replicas. The Service selects pods labeled <code>app: nginx</code> and exposes TCP port 80, forwarding to target port 9376. The Deployment declares container port 80, so check that the Service’s <code>targetPort</code> matches the port the container actually listens on.</p>

<p>For a Terraform configuration, run <code>terraform init</code> from its directory. The configuration requires Terraform 1.3 or later and the Google provider version 4.10 or later, but below 5.0.</p>
<h2>Contributing</h2>

<p>Contributions are welcome. You can help by adding exercises, improving answers, or correcting errors. Please follow the existing organization and formatting when making changes.</p>
<h2>License</h2>

<p>You may distribute or publicly perform the Work only under the terms of this License. Include a copy of, or the URI for, the License with each copy you distribute or publicly perform, and keep intact notices referring to the License and its warranty disclaimer. The License grants worldwide, royalty-free, non-exclusive rights for the duration of the applicable copyright, subject to its terms.</p>
