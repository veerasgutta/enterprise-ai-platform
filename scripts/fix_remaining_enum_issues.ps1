#!/usr/bin/env pwsh
# PowerShell Script to Fix Remaining Issues After AgeGroup Conversion

Write-Host "Fixing remaining compilation errors..." -ForegroundColor Green

# Fix remaining old enum value references
$enumFixes = @{
    'ExperienceLevel.Elementary' = 'ExperienceLevel.Entry'
    'ExperienceLevel.MiddleSchool' = 'ExperienceLevel.Junior'
    'ExperienceLevel.HighSchool' = 'ExperienceLevel.Mid'
    'ExperienceLevel.Transition' = 'ExperienceLevel.Senior'
    'ExperienceLevel.Adult' = 'ExperienceLevel.Principal'
    'CommunicationLevel.Moderate' = 'CommunicationLevel.Standard'
    'CommunicationLevel.Complex' = 'CommunicationLevel.Advanced'
    'CommunicationLevel.Professional' = 'CommunicationLevel.Expert'
    'NotificationType.Push' = 'NotificationType.Alert'
    'NotificationType.InApp' = 'NotificationType.Information'
    'NotificationType.Email' = 'NotificationType.Message'
}

# Apply enum fixes to all CS files
$csFiles = Get-ChildItem -Path "backend\**\*.cs" -Recurse

foreach ($file in $csFiles) {
    $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    
    $originalContent = $content
    $hasChanges = $false
    
    foreach ($find in $enumFixes.Keys) {
        $replace = $enumFixes[$find]
        if ($content.Contains($find)) {
            $content = $content.Replace($find, $replace)
            $hasChanges = $true
            Write-Host "  Fixed $find -> $replace in $($file.Name)" -ForegroundColor Cyan
        }
    }
    
    if ($hasChanges) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
    }
}

Write-Host "Enum fixes completed!" -ForegroundColor Green
