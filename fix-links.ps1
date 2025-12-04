# Fix Broken Links Script
# This script fixes broken footer and navigation links across all HTML files

$files = Get-ChildItem -Path "." -Filter "*.html" -Recurse

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $modified = $false
    
    # 1. Fix Legal/Privacy/Terms links (often found as folder/index.html)
    if ($content -match 'href="legal/index.html"') {
        $content = $content -replace 'href="legal/index.html"', 'href="legal.html"'
        $modified = $true
    }
    if ($content -match 'href="privacy/index.html"') {
        $content = $content -replace 'href="privacy/index.html"', 'href="privacy.html"'
        $modified = $true
    }
    if ($content -match 'href="terms/index.html"') {
        $content = $content -replace 'href="terms/index.html"', 'href="terms.html"'
        $modified = $true
    }
    
    # 2. Fix Projects Link (Standardize to projects.html)
    if ($content -match 'href="projects/index.html"') {
        $content = $content -replace 'href="projects/index.html"', 'href="projects.html"'
        $modified = $true
    }
    if ($content -match 'href="projects/"') {
        $content = $content -replace 'href="projects/"', 'href="projects.html"'
        $modified = $true
    }
    
    # 3. Fix any remaining relative path issues for root files
    # (e.g. if a file has href="../legal.html" but is in root)
    # This is safer to do if we know the file is in root.
    # We'll skip complex relative path logic for now to avoid breaking subfolder files if any exist.

    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        Write-Host "Fixed Links: $($file.Name)" -ForegroundColor Green
    }
}
