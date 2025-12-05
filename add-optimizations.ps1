# ProVenture - Add Optimization Files to All HTML Pages
# This script adds mobile optimizations and performance scripts to all HTML files

$projectPath = "c:\My Web Sites\ProVenture-digital-agency"
$htmlFiles = Get-ChildItem -Path $projectPath -Filter "*.html" -File

$mobileCSS = '<link rel="stylesheet" href="custom/css/mobile-optimizations.css">'
$performanceJS = '<script src="custom/js/performance-optimizations.js"></script>'

$filesUpdated = 0
$filesSkipped = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    $updated = $false
    
    # Check if mobile CSS is already added
    if ($content -notmatch "mobile-optimizations\.css") {
        # Add mobile CSS before </head>
        $content = $content -replace '</head>', "$mobileCSS`n</head>"
        $updated = $true
        Write-Host "Added mobile CSS to: $($file.Name)" -ForegroundColor Green
    }
    
    # Check if performance JS is already added
    if ($content -notmatch "performance-optimizations\.js") {
        # Add performance JS before </body>
        $content = $content -replace '</body>', "$performanceJS`n</body>"
        $updated = $true
        Write-Host "Added performance JS to: $($file.Name)" -ForegroundColor Green
    }
    
    if ($updated) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        $filesUpdated++
    } else {
        Write-Host "Skipped (already optimized): $($file.Name)" -ForegroundColor Yellow
        $filesSkipped++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Optimization Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Files Updated: $filesUpdated" -ForegroundColor Green
Write-Host "Files Skipped: $filesSkipped" -ForegroundColor Yellow
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Test on mobile devices" -ForegroundColor White
Write-Host "2. Run Google PageSpeed Insights" -ForegroundColor White
Write-Host "3. Deploy to Vercel" -ForegroundColor White
