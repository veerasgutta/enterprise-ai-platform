#!/bin/bash
# Enterprise AI Platform Deployment Script

echo "🚀 Starting Enterprise AI Platform Deployment"
echo "============================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "ai-data-intelligence" ] || [ ! -d "backend" ]; then
    print_error "Please run this script from the Enterprise-AI-Platform root directory"
    exit 1
fi

print_status "Checking dependencies..."

# Check Python
if ! command -v python &> /dev/null; then
    print_error "Python is not installed"
    exit 1
fi

# Check .NET
if ! command -v dotnet &> /dev/null; then
    print_error ".NET is not installed"
    exit 1
fi

print_success "Dependencies verified"

# Start AI Data Intelligence Platform
print_status "Starting AI Data Intelligence Platform..."
cd ai-data-intelligence
python demo_enterprise_platform.py &
AI_PID=$!
cd ..
print_success "AI Data Intelligence Platform started (PID: $AI_PID)"

# Start Backend API
print_status "Starting Backend API..."
cd backend
dotnet run &
API_PID=$!
cd ..
print_success "Backend API starting (PID: $API_PID)"

# Wait a moment for services to start
sleep 5

print_success "🎉 Enterprise AI Platform Deployment Complete!"
echo ""
echo "📊 PLATFORM STATUS:"
echo "=================="
echo "✅ AI Data Intelligence: Running (PID: $AI_PID)"
echo "✅ Backend API: Starting (PID: $API_PID)"
echo "✅ Enterprise Dashboard: Available"
echo ""
echo "🔗 ACCESS POINTS:"
echo "================"
echo "📊 Executive Dashboard: file://$(pwd)/ai-data-intelligence/generated_reports/dashboard_executive.html"
echo "🌐 Enterprise Dashboard: file://$(pwd)/enterprise-dashboard.html"
echo "🛠️  API Documentation: http://localhost:5294/swagger"
echo "⚡ API Health Check: http://localhost:5294/api/health"
echo ""
echo "📁 GENERATED REPORTS:"
echo "===================="
echo "📋 Reports Directory: ./ai-data-intelligence/generated_reports/"
echo ""
echo "🛑 TO STOP SERVICES:"
echo "===================="
echo "kill $AI_PID $API_PID"
echo ""
echo "🚀 Platform ready for enterprise use!"

# Keep script running
wait
