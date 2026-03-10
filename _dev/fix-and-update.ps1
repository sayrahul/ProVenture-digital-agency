# Fix Paths and Apply Design Script

$rootPath = "c:\My Web Sites\ProVenture-digital-agency"
$files = Get-ChildItem -Path $rootPath -Filter "*.html"

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $modified = $false
    
    # 1. Fix broken paths (../custom -> custom)
    if ($content -match '\.\./custom/') {
        $content = $content -replace '\.\./custom/', 'custom/'
        $modified = $true
    }
    if ($content -match '\.\./util/') {
        $content = $content -replace '\.\./util/', 'util/'
        $modified = $true
    }
    
    # 2. Add Custom CSS
    # Regex to match the default CSS link, handling variations
    $cssRegex = '<link href=".*?default-20252e34\.css\?v=112".*?>'
    if ($content -match $cssRegex -and $content -notmatch "proventure-custom.css") {
        $content = $content -replace ($cssRegex), '$0' + "`n" + '<link href="custom/css/proventure-custom.css" rel="stylesheet" type="text/css"/>'
        $modified = $true
    }
    
    # 3. Add Custom JS
    if ($content -notmatch "proventure-custom.js") {
        # Try to insert before closing body
        if ($content -match "</body>") {
            $content = $content -replace "</body>", '<!-- ProVenture Custom JavaScript -->' + "`n" + '<script src="custom/js/proventure-custom.js"></script>' + "`n" + '</body>'
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
