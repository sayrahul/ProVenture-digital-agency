const fs = require('fs');
let html = fs.readFileSync('blog.html', 'utf8');

// Fix main tag
html = html.replace('<main id="C_T_DefaultRegion">', '<main class="main" id="C_T_DefaultRegion">');

// Update Hero to match Clients exactly
html = html.replace(/<div class="hero bg-white hero-small">[\s\S]*?<!-- Blog Section -->/, `<div class="hero bg-dark bg-gradient hero-small">
<div class="container-big scroll-parallax">
<h1 class="nospan">
Blog
</h1>
<div class="grid-row twocol">
<div class="hero-topt">
<span class="toptitle">Insights &amp; News</span>
</div>
<div class="hero-lead">
<p>
<span>Trends, strategies, and updates from the world of digital marketing.</span>
</p>
</div>
</div>
</div>
</div>
<!-- Blog Section -->`);

// Fix backgrounds and positioning
html = html.replace('<section class="section bg-light" style="padding: 80px 0; background-color: #f8f9fa;">', '<section class="section bg-light" style="padding: 80px 0; background-color: #f8f9fa; position: relative; z-index: 1;">');
html = html.replace('<section class="section bg-white" style="padding: 80px 0;">', '<section class="section bg-white" style="padding: 80px 0; background-color: #ffffff; position: relative; z-index: 1;">');

fs.writeFileSync('blog.html', html);
