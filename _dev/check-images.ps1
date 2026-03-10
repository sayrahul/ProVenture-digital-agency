# ProVenture - Check for Missing Images
# This script checks if image files referenced in HTML exist

$projectPath = "c:\My Web Sites\ProVenture-digital-agency"
$htmlFiles = Get-ChildItem -Path $projectPath -Filter "*.html" -File

$totalMissing = 0
$checkedFiles = 0

Write-Host "Checking for missing images..." -ForegroundColor Cyan
Write-Host ""

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    $missingInFile = 0
    
    # Find all image sources
    $matches = [regex]::Matches($content, 'src="([^"]+)"')
    
    foreach ($match in $matches) {
        $imgPath = $match.Groups[1].Value
        
        # Skip external URLs and data URIs
        if ($imgPath -match "^http" -or $imgPath -match "^data:" -or $imgPath -eq "") {
            continue
        }
        
        # Check if file exists
        $fullPath = Join-Path $projectPath $imgPath
        if (-not (Test-Path $fullPath)) {
            if ($missingInFile -eq 0) {
                Write-Host "$($file.Name):" -ForegroundColor Yellow
            }
            Write-Host "  Missing: $imgPath" -ForegroundColor Red
            $missingInFile++
            $totalMissing++
        }
    }
    
    if ($missingInFile -eq 0) {
        Write-Host "✓ $($file.Name) - All images found" -ForegroundColor Green
    }
    
    $checkedFiles++
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Image Check Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Files Checked: $checkedFiles" -ForegroundColor White
Write-Host "Missing Images: $totalMissing" -ForegroundColor $(if ($totalMissing -gt 0) { "Red" } else { "Green" })

if ($totalMissing -eq 0) {
    Write-Host ""
    Write-Host "✓ All images found!" -ForegroundColor Green
}
