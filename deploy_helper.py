#!/usr/bin/env python3
"""
Django Blog App - Automated Render Deployment Helper
This script prepares and validates everything for deployment
"""

import os
import json
import subprocess
import sys
from pathlib import Path

class DeploymentHelper:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.blog_app_dir = self.base_dir / "projects_code" / "blog_app"
        self.checks_passed = []
        self.checks_failed = []
        
    def print_header(self, text):
        print("\n" + "="*60)
        print(f"  {text}")
        print("="*60 + "\n")
    
    def check_files(self):
        """Verify all deployment files exist"""
        self.print_header("📋 Checking Deployment Files")
        
        required_files = {
            "requirements.txt": self.blog_app_dir / "requirements.txt",
            "Procfile": self.blog_app_dir / "Procfile",
            ".env.example": self.blog_app_dir / ".env.example",
            "render.yaml": self.base_dir / "render.yaml",
            "settings.py": self.blog_app_dir / "blog_project" / "settings.py",
        }
        
        for name, path in required_files.items():
            if path.exists():
                size = path.stat().st_size
                print(f"✅ {name:<25} ({size:,} bytes)")
                self.checks_passed.append(name)
            else:
                print(f"❌ {name:<25} MISSING")
                self.checks_failed.append(name)
        
        return len(self.checks_failed) == 0
    
    def check_dependencies(self):
        """Verify all Python dependencies"""
        self.print_header("📦 Checking Python Dependencies")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            required = [
                "Django",
                "gunicorn",
                "pillow",
                "django-crispy-forms",
                "python-decouple",
                "whitenoise"
            ]
            
            installed = result.stdout.lower()
            
            for pkg in required:
                if pkg.lower() in installed:
                    print(f"✅ {pkg:<30} installed")
                    self.checks_passed.append(f"pkg:{pkg}")
                else:
                    print(f"⚠️  {pkg:<30} not in current environment*")
                    # This is ok, Render will install from requirements.txt
            
            print("\n*Note: Dependencies will be installed on Render during build")
            return True
            
        except Exception as e:
            print(f"⚠️  Could not verify packages: {e}")
            return True
    
    def validate_git(self):
        """Verify git is configured and files are committed"""
        self.print_header("🔐 Checking Git Status")
        
        try:
            # Check git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print("✅ Git repository initialized")
                self.checks_passed.append("git-repo")
                
                # Check for uncommitted changes
                if result.stdout.strip():
                    print(f"⚠️  Uncommitted changes detected:")
                    print(result.stdout)
                    return False
                else:
                    print("✅ All changes committed")
                    self.checks_passed.append("git-clean")
                    return True
            else:
                print(f"❌ Git error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Git check failed: {e}")
            return False
    
    def generate_deployment_report(self):
        """Generate a deployment readiness report"""
        self.print_header("📊 Deployment Readiness Report")
        
        passed = len(self.checks_passed)
        failed = len(self.checks_failed)
        total = passed + failed
        
        print(f"✅ Checks Passed: {passed}")
        print(f"❌ Checks Failed: {failed}")
        print(f"📈 Success Rate: {(passed/total*100):.1f}%" if total > 0 else "")
        
        if self.checks_failed:
            print(f"\n⚠️  Issues to resolve:")
            for issue in self.checks_failed:
                print(f"   - {issue}")
        
        return failed == 0
    
    def show_next_steps(self):
        """Display deployment instructions"""
        self.print_header("🚀 Next Steps: Deploy on Render")
        
        print("""
1. Go to: https://render.com
2. Click "Sign up with GitHub"
3. Authorize and login
4. Click "New +" → "Web Service"
5. Select "My_portfolio" repository
6. Configure:
   - Name: blog-app
   - Environment: Python 3
   - Build Command: cd projects_code/blog_app && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   - Start Command: cd projects_code/blog_app && gunicorn blog_project.wsgi:application
7. Add Environment Variables (click "Add Environment Variable"):
   - SECRET_KEY = (auto-generated)
   - DEBUG = false
   - ALLOWED_HOSTS = *.onrender.com
   - SECURE_SSL_REDIRECT = true
   - SESSION_COOKIE_SECURE = true
   - CSRF_COOKIE_SECURE = true
8. Click "Create Web Service"
9. Wait 5-10 minutes for deployment
10. Share the deployed URL with me to update your portfolio!

""")
    
    def run(self):
        """Run all checks"""
        print("\n")
        print("🎯 DJANGO BLOG APP - DEPLOYMENT VALIDATOR")
        print("Checking everything before Render deployment...\n")
        
        # Run checks
        files_ok = self.check_files()
        deps_ok = self.check_dependencies()
        git_ok = self.validate_git()
        
        # Generate report
        ready = self.generate_deployment_report()
        
        # Show summary
        if ready:
            print("\n✨ READY FOR DEPLOYMENT! ✨\n")
            self.show_next_steps()
            print("Open Render now: https://render.com\n")
        else:
            print("\n⚠️  Please resolve the issues above before deploying.\n")
        
        return 0 if ready else 1

if __name__ == "__main__":
    helper = DeploymentHelper()
    sys.exit(helper.run())
