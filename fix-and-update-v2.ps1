# Fix Paths and Apply Design Script (Fixed)

$rootPath = "c:\My Web Sites\ProVenture-digital-agency"
$files = Get-ChildItem -Path $rootPath -Filter "*.html"

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $modified = $false
    
    # 1. Fix broken paths
    if ($content -match '\.\./custom/') {
        $content = $content -replace '\.\./custom/', 'custom/'
        $modified = $true
    }
    if ($content -match '\.\./util/') {
        $content = $content -replace '\.\./util/', 'util/'
        $modified = $true
    }
    
    # 2. Add Custom CSS
    $cssRegex = '<link href=".*?default-20252e34\.css\?v=112".*?>'
    if ($content -match $cssRegex -and $content -notmatch "proventure-custom.css") {
        # Use a simpler replacement approach
        $match = [regex]::match($content, $cssRegex).Value
        $replacement = $match + "`n" + '<link href="custom/css/proventure-custom.css" rel="stylesheet" type="text/css"/>'
        $content = $content.Replace($match, $replacement)
        $modified = $true
    }
    
    # 3. Add Custom JS
    if ($content -notmatch "proventure-custom.js") {
        if ($content -match "</body>") {
            $jsReplacement = '<!-- ProVenture Custom JavaScript -->' + "`n" + '<script src="custom/js/proventure-custom.js"></script>' + "`n" + '</body>'
            $content = $content -replace "</body>", $jsReplacement
            $modified = $true
        }
    }
    
    # 4. Update Buttons
    if ($content -match 'class="btn btn-outline"') {
        $content = $content -replace 'class="btn btn-outline"', 'class="btn btn-outline pv-btn-primary pv-magnetic"'
        $modified = $true
    }
    
    # 5. Update Service Cards
    if ($content -match 'class="servicecards-item servicecard"') {
        $content = $content -replace 'class="servicecards-item servicecard"', 'class="servicecards-item servicecard pv-glass-card"'
        $modified = $true
    }

    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        Write-Host "Fixed & Updated: $($file.Name)" -ForegroundColor Green
    }
}
