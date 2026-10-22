# devops-exercises<h2>Description</h2>

<p>devops-exercises is a collection of questions, exercises, and answers covering a wide range of DevOps and systems topics, such as:</p>

<ul>
<li><a href="https://github.com/bregman-arie/devops-exercises">Linux</a></li>
<li><a href="https://github.com/bregman-arie/devops-exercises">Networking</a></li>
<li><a href="https://github.com/bregman-arie/devops-exercises">Kubernetes</a></li>
<li><a href="https://github.com/bregman-arie/devops-exercises">Terraform</a></li>
<li><a href="https://github.com/bregman-arie/devops-exercises">CI/CD</a></li>
<li><a href="https://github.com/bregman-arie/devops-exercises">Cloud (AWS, GCP, Azure)</a></li>
<li><a href="https://github.com/bregman-arie/devops-exercises">Databases, coding and scripting, monitoring, and more</a></li>
</ul>

<p>The project is designed to help engineers prepare for interviews, practice for certifications, and generally improve their knowledge of DevOps-related technologies. Topics are organized in the repository as directories containing question files, and exercises often include hands-on labs (for example, Kubernetes deployment manifests or Terraform configuration snippets) along with their solutions.</p>

<p>Only use the links that actually appear in the repository's own README; the repository is located at file:///home/ilya/README<em>benchmark/benchmark</em>README/results/readme<em>2026</em>three_models/workspaces/devops-exercises-bb4n38je.</p>
<h2>Requirements</h2>

<p>To run the Terraform-based exercises in this project, you will need:</p>

<ul>
<li><strong>Terraform</strong> version <strong>1.3.0 or later</strong> (<code>required_version = "&gt;=1.3.0"</code>)</li>
<li><strong>Google Cloud Provider</strong> (<code>hashicorp/google</code>) version <strong>&gt;= 4.10.0, &lt; 5.0</strong></li>
</ul>

<p>Example provider configuration used in the project:</p>

<p>```hcl
terraform {
    required_version = ">=1.3.0"</p>

<pre><code>required_providers {
    google = {
        source  = "hashicorp/google"
        version = "&gt;= 4.10.0, &lt; 5.0"
    }
}
</code></pre>

<p>}
```</p>
<h2>Installation</h2>
<h2>Usage</h2>
<h2>Contributing</h2>

<p>Thank you for your interest in contributing to devops-exercises!</p>

<p>Unfortunately, the repository contents provided do not include explicit contribution guidelines (such as a CONTRIBUTING.md file or a "Contributing" section in the original README). As a result, specific instructions about how to submit pull requests, report issues, or follow coding standards for this project are not available in the provided context.</p>

<p>If you would like to contribute, a good starting point would be to review the existing exercise content in the repository to understand its structure and format, and then follow general open-source best practices:</p>

<ol>
<li>Fork the repository.</li>
<li>Create a new branch for your changes.</li>
<li>Make your changes or additions.</li>
<li>Submit a pull request describing your changes.</li>
</ol>

<p>Note: Please keep in mind that this project is licensed under the Creative Commons license terms referenced in this repository, and any contributions will be subject to those license terms.</p>
<h2>License</h2>

<p>This project is licensed under the terms of the license included in the <a href="LICENSE">LICENSE</a> file in the repository root.</p>

<p>In summary, the license grants You a worldwide, royalty-free, non-exclusive, perpetual license to exercise the rights in the Work, subject to the terms and conditions of the License. Key points include:</p>

<ul>
<li>You may Distribute or Publicly Perform the Work only under the terms of this License, and you must include a copy of (or the URI for) the License with every copy you distribute.</li>
<li>You may not offer or impose any terms that restrict the terms of this License or the recipient's ability to exercise the rights granted under it, and you may not sublicense the Work.</li>
<li>All notices referring to the License and the disclaimer of warranties must be kept intact with every copy distributed.</li>
<li>Nothing in the License reduces, limits, or restricts any uses free from copyright or rights arising from limitations or exceptions under copyright law or other applicable laws.</li>
<li>No term or provision of the License is deemed waived, and no breach consented to, unless such waiver or consent is in writing and signed by the party to be charged.</li>
</ul>

<p>For the complete terms and conditions, please refer to the full license text in the repository.</p>
<h2>Description</h2>

<p>This repository contains a large collection of questions and exercises on various technical topics related to DevOps and SRE.</p>

<p>The purpose of the project is to help developers and engineers learn, practice, and test their knowledge across a wide range of DevOps-related subjects, such as:</p>

<ul>
<li>Linux</li>
<li>Networking</li>
<li>Kubernetes</li>
<li>Terraform</li>
<li>CI/CD</li>
<li>Cloud platforms</li>
<li>Security</li>
<li>Programming (Python)</li>
<li>Software Design</li>
</ul>

<p>The repository includes both conceptual questions and hands-on exercises — for example, writing Terraform configurations or working with Kubernetes manifests. The questions vary in difficulty, from beginner-friendly to advanced, and can be used for self-study, preparing for technical interviews, or assessing one's own DevOps knowledge.</p>
<h2>Requirements</h2>

<p>The Terraform code included in this repository declares the following requirements in its <code>terraform</code> configuration blocks:</p>

<ul>
<li><strong>Terraform</strong>: version <code>&gt;= 1.3.0</code></li>
<li><strong>Google Cloud provider</strong> (<code>hashicorp/google</code>): version <code>&gt;= 4.10.0, &lt; 5.0</code></li>
</ul>

<p>These constraints are defined via the <code>required_version</code> and <code>required_providers</code> settings, so when you initialize the Terraform configurations in this repository, Terraform will automatically verify the CLI version and download a compatible version of the Google provider.</p>
<h2>Installation</h2>
<h2>Usage</h2>

<p><code>devops-exercises</code> is a collection of questions and exercises on various technical topics, sometimes related to DevOps and SRE. There is nothing to install, build, or run — the repository is simply a set of question/answer exercises written in Markdown.</p>

<p>The recommended way to work through the content:</p>

<ol>
<li><strong>Pick a topic you want to practice or learn.</strong> The exercises are grouped by subject, such as Linux, Kubernetes, Terraform, Networking, CI/CD, and more. Each exercise focuses on a single question.</li>
<li><strong>Try to answer the question on your own first.</strong> Some exercises include code or configuration snippets (for example, Kubernetes manifests or Terraform configuration) as part of the question or its solution.</li>
<li><strong>Check the solution.</strong> Each exercise includes an answer/solution so you can compare it with your own answer and dig deeper into any part you weren't sure about.</li>
</ol>

<p>The exercises can be used for self-learning, refreshing knowledge on specific topics, or preparing for DevOps/SRE interviews.</p>
<h2>Contributing</h2>

<p>Thank you for considering to contribute to devops-exercises.</p>

<p>You are welcome to contribute to the project in the following ways:</p>

<ul>
<li>Adding new questions and exercises</li>
<li>Improving existing questions and exercises (for example, by adding explanations or fixing errors)</li>
<li>Fixing typos and other mistakes</li>
</ul>

<p>If you are adding a new question, please follow the format used by the existing questions in this repository. Each question is wrapped in a collapsible block using the HTML <code>&lt;details&gt;</code> and <code>&lt;summary&gt;</code> tags, with the answer placed inside the block, for example:</p>

<p><details>
<summary>Question text goes here</summary><br><b></p>

<p>Answer text goes here.
</b></details></p>

<p>New questions and exercises should be added to the relevant topic section of the README. When your changes are ready, open a pull request with them.</p>
<h2>License</h2>

<p>This project is distributed under the terms of a Creative Commons license, the full text of which is included in this repository. The key terms of the license are summarized below:</p>

<ul>
<li><p><strong>License Grant</strong> – Subject to the terms and conditions of the license, the Licensor grants a worldwide, royalty-free, non-exclusive, perpetual (for the duration of the applicable copyright) license to exercise the rights in the Work as stated in the license.</p></li>
<li><p><strong>Distribution and Public Performance</strong> – You may Distribute or Publicly Perform the Work only under the terms of this license. You must include a copy of, or the Uniform Resource Identifier (URI) for, this license with every copy of the Work you Distribute or Publicly Perform. You may not offer or impose any terms on the Work that restrict the terms of the license or the ability of recipients to exercise the rights granted to them, and you may not sublicense the Work. You must keep intact all notices that refer to the license and to the disclaimer of warranties, and you may not impose any effective technological measures on the Work that restrict recipients from exercising the rights granted to them under the license.</p></li>
<li><p><strong>Fair Dealing Rights</strong> – Nothing in this license is intended to reduce, limit, or restrict any uses free from copyright or rights arising from limitations or exceptions that are provided for in connection with the copyright protection under copyright law or other applicable laws.</p></li>
<li><p><strong>Entire Agreement</strong> – This license constitutes the entire agreement between the parties with respect to the Work licensed under it. There are no understandings, agreements, or representations with respect to the Work not specified in the license. The Licensor shall not be bound by any additional provisions that may appear in any communication from you, and the license may not be modified without the mutual written agreement of the Licensor and you.</p></li>
<li><p><strong>Miscellaneous</strong> – Each time you Distribute or Publicly Perform the Work or a Collection, the Licensor offers to the recipient a license to the Work on the same terms and conditions as the license granted to you. If any provision of the license is invalid or unenforceable under applicable law, it shall not affect the validity or enforceability of the remainder of the license, and such provision shall be reformed to the minimum extent necessary to make it valid and enforceable. No term or provision of the license shall be deemed waived, and no breach consented to, unless such waiver or consent is in writing and signed by the party to be charged with such waiver or consent.</p></li>
</ul>
