# Update All Pages Script
# This script applies the new ProVenture design to all HTML files

$files = Get-ChildItem -Path "." -Filter "*.html" -Recurse

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $modified = $false
    
    # 1. Add Custom CSS if not present
    if ($content -notmatch "proventure-custom.css") {
        $cssLink = '<link href="custom/css/default-20252e34.css?v=112" rel="prefetch" type="style"/>' + "`n" + '<link href="custom/css/proventure-custom.css" rel="stylesheet" type="text/css"/>'
        $content = $content -replace [regex]::Escape('<link href="custom/css/default-20252e34.css?v=112" rel="prefetch" type="style"/>'), $cssLink
        $modified = $true
    }
    
    # 2. Add Custom JS if not present
    if ($content -notmatch "proventure-custom.js") {
        $jsScript = '</script>' + "`n" + '<!-- ProVenture Custom JavaScript -->' + "`n" + '<script src="custom/js/proventure-custom.js"></script>'
        # Find the last closing script tag before body end
        $content = $content -replace '(?s)</script>(?!.*</script>)', $jsScript
        $modified = $true
    }
    
    # 3. Update Buttons (Add pv-btn-primary and magnetic effect)
    if ($content -match 'class="btn btn-outline"') {
        $content = $content -replace 'class="btn btn-outline"', 'class="btn btn-outline pv-btn-primary pv-magnetic"'
        $modified = $true
    }
    
    # 4. Update Service Cards (Add glassmorphism)
    if ($content -match 'class="servicecards-item servicecard"') {
        $content = $content -replace 'class="servicecards-item servicecard"', 'class="servicecards-item servicecard pv-glass-card"'
        $modified = $true
    }
    
    # 5. Update Hero/Header Sections (Add gradient background if it's a hero section)
    # This is a bit safer to do generally on the 'header' or specific sections if identifiable
    # For now, we'll stick to safe component updates to avoid breaking layout
    
    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        Write-Host "Updated: $($file.Name)" -ForegroundColor Green
    }
    else {
        Write-Host "Skipped: $($file.Name) (Already updated)" -ForegroundColor Yellow
    }
}

Write-Host "`nGlobal design update complete!" -ForegroundColor Cyan
