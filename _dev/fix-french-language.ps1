# Fix French Language Script
# This PowerShell script removes French language remnants from HTML files

$files = Get-ChildItem -Path "." -Filter "*.html" -Recurse

$replacements = @{
    'Passer au contenu' = 'Skip to content'
    'A la page d''accueil' = 'Go to homepage'
    'lang_fr' = 'lang_en'
    'lang="fr"' = 'lang="en"'
}

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $modified = $false
    
    foreach ($key in $replacements.Keys) {
        if ($content -match [regex]::Escape($key)) {
            $content = $content -replace [regex]::Escape($key), $replacements[$key]
            $modified = $true
        }
    }
    
    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        Write-Host "Updated: $($file.Name)" -ForegroundColor Green
    }
}

Write-Host "`nFrench language cleanup complete!" -ForegroundColor Cyan
