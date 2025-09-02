#!/usr/bin/env pwsh
# PowerShell Script to Convert AgeGroup to ExperienceLevel systematically

Write-Host "Starting conversion of AgeGroup to ExperienceLevel..." -ForegroundColor Green

# Define replacement mappings
$replacements = @{
    'AgeGroup.Elementary' = 'ExperienceLevel.Entry'
    'AgeGroup.MiddleSchool' = 'ExperienceLevel.Junior'
    'AgeGroup.HighSchool' = 'ExperienceLevel.Mid'
    'AgeGroup.Transition' = 'ExperienceLevel.Senior'
    'AgeGroup.Adult' = 'ExperienceLevel.Principal'
    'AgeGroup' = 'ExperienceLevel'
    'Ages 5-11' = 'Entry Level (0-2 years)'
    'Ages 11-14' = 'Junior Level (2-4 years)'
    'Ages 14-18' = 'Mid Level (4-7 years)'
    'Ages 18-25' = 'Senior Level (7-10 years)'
    'Ages 25+' = 'Principal+ Level (10+ years)'
    'Elementary School' = 'Entry Level'
    'Middle School' = 'Junior Level'
    'High School' = 'Mid Level'
    'Transition Years' = 'Senior Level'
    'Adult Life' = 'Principal Level'
    'Early Intervention' = 'Onboarding Support'
    'Educational Support' = 'Training Resources'
    'Social Skills' = 'Team Collaboration'
    'Academic Planning' = 'Career Planning'
    'Independence Skills' = 'Leadership Skills'
    'College Preparation' = 'Career Advancement'
    'Employment' = 'Job Performance'
    'Independent Living' = 'Work-Life Balance'
    'Career Development' = 'Professional Development'
    'Relationships' = 'Professional Networks'
    'early childhood support' = 'new employee onboarding'
    'School and learning resources' = 'Training and development resources'
    'Building social connections' = 'Building professional networks'
    'Educational planning and accommodations' = 'Career planning and development'
    'Preparing for independence' = 'Developing leadership skills'
    'Planning for higher education' = 'Planning for career advancement'
    'Job search and workplace skills' = 'Performance optimization and workplace skills'
    'Living independently' = 'Work-life balance and autonomy'
    'Advancing in your career' = 'Professional development and growth'
    'Building and maintaining relationships' = 'Building and maintaining professional networks'
    'Find early intervention resources' = 'Find onboarding and training resources'
    'Explore family support options' = 'Explore team support and mentoring'
    'Learn about transition planning' = 'Learn about career transition planning'
    'Find peer support groups' = 'Find professional networking groups'
    'Explore college preparation' = 'Explore career advancement opportunities'
    'Learn about independence skills' = 'Learn about leadership and autonomy skills'
    'Find employment support' = 'Find performance optimization support'
    'Explore housing options' = 'Explore work-life balance strategies'
    'Find career development resources' = 'Find professional development resources'
    'Explore relationship resources' = 'Explore professional networking resources'
}

# Define variable name replacements (separate to avoid conflicts)
$variableReplacements = @{
    'ageGroup' = 'experienceLevel'
}

# Get all files to process
$filesToProcess = @(
    "backend\Controllers\*.cs"
    "backend\Services\*.cs"
    "backend\Models\*.cs"
    "backend\Data\*.cs"
    "web\src\**\*.ts"
    "web\src\**\*.tsx"
    "web\src\**\*.js"
    "web\src\**\*.jsx"
)

$totalFilesProcessed = 0
$totalReplacements = 0

foreach ($pattern in $filesToProcess) {
    $files = Get-ChildItem -Path $pattern -Recurse -ErrorAction SilentlyContinue
    
    foreach ($file in $files) {
        Write-Host "Processing: $($file.FullName)" -ForegroundColor Yellow
        
        $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
        if (-not $content) { continue }
        
        $originalContent = $content
        $fileReplacements = 0
        
        # Apply all replacements
        foreach ($find in $replacements.Keys) {
            $replace = $replacements[$find]
            $beforeCount = ($content -split [regex]::Escape($find)).Count - 1
            $content = $content -replace [regex]::Escape($find), $replace
            $replacementsMade = $beforeCount
            $fileReplacements += $replacementsMade
            
            if ($replacementsMade -gt 0) {
                Write-Host "  Replaced '$find' with '$replace' ($replacementsMade times)" -ForegroundColor Cyan
            }
        }
        
        # Apply variable name replacements
        foreach ($find in $variableReplacements.Keys) {
            $replace = $variableReplacements[$find]
            $beforeCount = ($content -split [regex]::Escape($find)).Count - 1
            $content = $content -replace [regex]::Escape($find), $replace
            $replacementsMade = $beforeCount
            $fileReplacements += $replacementsMade
            
            if ($replacementsMade -gt 0) {
                Write-Host "  Replaced variable '$find' with '$replace' ($replacementsMade times)" -ForegroundColor Cyan
            }
        }
        
        # Write back if changes were made
        if ($content -ne $originalContent) {
            Set-Content -Path $file.FullName -Value $content -NoNewline
            $totalFilesProcessed++
            $totalReplacements += $fileReplacements
            Write-Host "  Updated file with $fileReplacements replacements" -ForegroundColor Green
        }
    }
}

Write-Host "`nConversion completed!" -ForegroundColor Green
Write-Host "Files processed: $totalFilesProcessed" -ForegroundColor White
Write-Host "Total replacements: $totalReplacements" -ForegroundColor White

# Verify no AgeGroup references remain
Write-Host "`nChecking for remaining AgeGroup references..." -ForegroundColor Yellow
$remainingRefs = Select-String -Path "backend\**\*.cs", "web\src\**\*.*" -Pattern "AgeGroup" -ErrorAction SilentlyContinue

if ($remainingRefs) {
    Write-Host "Warning: Found remaining AgeGroup references:" -ForegroundColor Red
    $remainingRefs | ForEach-Object { Write-Host "  $($_.Filename):$($_.LineNumber) - $($_.Line.Trim())" -ForegroundColor Red }
} else {
    Write-Host "✅ No remaining AgeGroup references found!" -ForegroundColor Green
}

Write-Host "`nRecommended next steps:" -ForegroundColor Yellow
Write-Host "1. Build the project to check for compilation errors" -ForegroundColor White
Write-Host "2. Run tests to ensure functionality works correctly" -ForegroundColor White
Write-Host "3. Review and commit changes" -ForegroundColor White
