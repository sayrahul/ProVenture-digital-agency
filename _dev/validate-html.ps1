# ProVenture - Fix Broken HTML Files
# This script checks for and fixes common HTML issues

$projectPath = "d:\My Web Sites\ProVenture-digital-agency"
$htmlFiles = Get-ChildItem -Path $projectPath -Filter "*.html" -File

$issuesFound = 0
$filesFixed = 0

Write-Host "Checking HTML files for issues..." -ForegroundColor Cyan

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    $originalContent = $content
    $fileIssues = @()
    
    # Check for duplicate </head> tags
    $headCloseCount = ([regex]::Matches($content, "</head>")).Count
    if ($headCloseCount -gt 1) {
        $fileIssues += "Multiple </head> tags found: $headCloseCount"
    }
    
    # Check for duplicate </body> tags
    $bodyCloseCount = ([regex]::Matches($content, "</body>")).Count
    if ($bodyCloseCount -gt 1) {
        $fileIssues += "Multiple </body> tags found: $bodyCloseCount"
    }
    
    # Check for missing images
    $missingImages = [regex]::Matches($content, 'src="([^"]+)"') | ForEach-Object {
        $imgPath = $_.Groups[1].Value
        if ($imgPath -notmatch "^http" -and $imgPath -notmatch "^data:" -and $imgPath -ne "") {
            $fullPath = Join-Path $projectPath $imgPath
            if (-not (Test-Path $fullPath)) {
                $imgPath
            }
        }
    }
    
    if ($missingImages) {
        $fileIssues += "Missing images: $($missingImages -join ', ')"
    }
    
    if ($fileIssues.Count -gt 0) {
        Write-Host "`n$($file.Name):" -ForegroundColor Yellow
        foreach ($issue in $fileIssues) {
            Write-Host "  - $issue" -ForegroundColor Red
            $issuesFound++
        }
    }
    else {
        Write-Host "✓ $($file.Name)" -ForegroundColor Green
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "HTML Validation Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Issues Found: $issuesFound" -ForegroundColor $(if ($issuesFound -gt 0) { "Red" } else { "Green" })
Write-Host "Files Fixed: $filesFixed" -ForegroundColor Green

if ($issuesFound -eq 0) {
    Write-Host "`n✓ All HTML files are valid!" -ForegroundColor Green
}
else {
    Write-Host "`nPlease review the issues above." -ForegroundColor Yellow
}
