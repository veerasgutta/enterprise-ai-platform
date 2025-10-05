# 🧹 Repository Cleanup Script
# Removes sensitive/proprietary content while keeping impressive learning examples

Write-Host "=== CLEANING ENTERPRISE-AI-PLATFORM FOR PUBLIC LEARNING SHOWCASE ===" -ForegroundColor Cyan
Write-Host ""

$repoPath = "C:\Veera\avinshi-platform-learning"
Set-Location $repoPath

# Files to remove (sensitive/production)
$filesToRemove = @(
    "config/environment.json",           # May contain environment-specific settings
    "ai-data-intelligence/config/config.json",  # May contain API keys
    "ai-data-intelligence/data/*.csv",   # Sample data that might be based on real data
    "backend/*.http",                    # May contain API endpoints/tokens
    "quick-demo.ps1"                     # May contain production paths
)

Write-Host "Step 1: Removing potentially sensitive files..." -ForegroundColor Yellow

foreach ($file in $filesToRemove) {
    $fullPath = Join-Path $repoPath $file
    if (Test-Path $fullPath) {
        Write-Host "  Removing: $file" -ForegroundColor Red
        Remove-Item $fullPath -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "Step 2: Adding learning disclaimers to Python files..." -ForegroundColor Yellow

$disclaimer = @"
"""
🎓 LEARNING PROJECT - Educational Example

This code is part of a personal learning project exploring enterprise AI patterns.
Created for educational purposes and portfolio demonstration.

⚠️ NOT PRODUCTION CODE - For learning and demonstration only.

Technologies: Multi-agent systems, AI orchestration, enterprise architecture
Author: Personal learning project
License: Educational use only
"""

"@

# Add disclaimer to main Python files
$pythonFiles = @(
    "agent-ecosystem/orchestration_hub.py",
    "ai-data-intelligence/data_intelligence_orchestrator.py",
    "ai-native-framework/ai_native_orchestrator.py",
    "multi-agent-orchestration/workflow_engine.py"
)

foreach ($file in $pythonFiles) {
    $fullPath = Join-Path $repoPath $file
    if (Test-Path $fullPath) {
        $content = Get-Content $fullPath -Raw
        if ($content -notlike "*LEARNING PROJECT*") {
            Write-Host "  Adding disclaimer to: $file" -ForegroundColor Green
            $newContent = $disclaimer + $content
            Set-Content $fullPath $newContent -NoNewline
        }
    }
}

Write-Host ""
Write-Host "Step 3: Creating LEARNING_NOTES.md..." -ForegroundColor Yellow

# Already exists or will be created separately

Write-Host ""
Write-Host "Step 4: Sanitizing configuration files..." -ForegroundColor Yellow

# Check for any remaining config files and sanitize
$configFiles = Get-ChildItem -Recurse -Include "*.json","*.yml","*.yaml" | Where-Object { $_.FullName -notlike '*\.git\*' -and $_.FullName -notlike '*node_modules\*' }

foreach ($config in $configFiles) {
    Write-Host "  Checking: $($config.Name)" -ForegroundColor Gray
    $content = Get-Content $config.FullName -Raw -ErrorAction SilentlyContinue
    
    # Check for potential secrets (basic check)
    if ($content -match 'api[_-]?key|password|secret|token|credential') {
        Write-Host "    ⚠️ WARNING: Potential secret found in $($config.Name)" -ForegroundColor Red
        Write-Host "    Please manually review this file!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Step 5: Creating .gitignore enhancements..." -ForegroundColor Yellow

$gitignoreAdditions = @"

# Personal/Sensitive (added during cleanup)
*.env
*.env.local
**/config/environment.json
**/config/production.json
**/*secret*
**/*password*
**/*key*.json
.vscode/settings.json

# Local development
local/
temp/
scratch/
"@

Add-Content -Path ".gitignore" -Value $gitignoreAdditions

Write-Host ""
Write-Host "✅ CLEANUP COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review the changes with: git status" -ForegroundColor White
Write-Host "2. Manually check any files flagged above" -ForegroundColor White
Write-Host "3. Test the code still works" -ForegroundColor White
Write-Host "4. Commit changes: git add -A && git commit -m 'Clean for public learning showcase'" -ForegroundColor White
Write-Host "5. Push to GitHub: git push origin master" -ForegroundColor White
Write-Host ""
Write-Host "⚠️ Remember to manually review:" -ForegroundColor Yellow
Write-Host "  - Any config files flagged above" -ForegroundColor White
Write-Host "  - README.md (already has disclaimers)" -ForegroundColor White
Write-Host "  - Any customer-specific references" -ForegroundColor White
