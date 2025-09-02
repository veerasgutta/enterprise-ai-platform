#!/bin/bash
# Quick Demo Setup Script for Professional Showcase
# Perfect for LinkedIn portfolio demonstration

echo "🚀 Enterprise AI Platform - Professional Demo Setup"
echo "=================================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if command -v python &> /dev/null; then
    echo "✅ Python found: $(python --version)"
else
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

# Check .NET
if command -v dotnet &> /dev/null; then
    echo "✅ .NET found: $(dotnet --version)"
else
    echo "❌ .NET not found. Please install .NET 8+"
    exit 1
fi

echo ""
echo "🎯 Starting Professional Demo..."
echo ""

# Demo 1: AI Intelligence Platform
echo "1️⃣ AI Intelligence Platform Demo"
echo "   Generating autonomous business insights..."
cd ai-data-intelligence
python demo_enterprise_platform.py &
AI_PID=$!
cd ..

# Wait for AI platform to generate some insights
sleep 5

# Demo 2: Enterprise API
echo ""
echo "2️⃣ Enterprise API Demo"
echo "   Starting .NET 8 backend services..."
cd backend
dotnet run &
API_PID=$!
cd ..

# Wait for API to start
sleep 10

echo ""
echo "🎉 Professional Demo Ready!"
echo "=========================="
echo ""
echo "📊 AI Intelligence:"
echo "   • Check: ./ai-data-intelligence/generated_reports/"
echo "   • Live insights generation in progress..."
echo ""
echo "🔧 Enterprise API:"
echo "   • Health Check: http://localhost:5294/health"
echo "   • Swagger Docs: http://localhost:5294/swagger"
echo ""
echo "📈 Executive Dashboard:"
echo "   • Open: enterprise-dashboard.html in browser"
echo ""
echo "⏱️  Perfect for 5-minute professional demonstrations!"
echo ""
echo "🛑 To stop demo: Press Ctrl+C"

# Keep script running
wait $AI_PID $API_PID
