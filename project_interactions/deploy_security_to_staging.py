#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Deploy security updates to staging environment
This script packages and deploys all security fixes
"""

import os
import sys
import json
import shutil
import subprocess
import tarfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SecurityDeployment:
    """Deploy security updates to staging"""
    
    def __init__(self):
        self.staging_config = self.load_staging_config()
        self.deployment_id = f"security_deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.package_dir = Path(f"deployment_package_{self.deployment_id}")
        
    def load_staging_config(self) -> Dict:
        """Load staging environment configuration"""
        # Check for staging config in environment or config file
        config_path = Path("staging_config.json")
        
        if config_path.exists():
            return json.loads(config_path.read_text())
        
        # Default configuration
        return {
            "staging_host": os.getenv("STAGING_HOST", "localhost"),
            "staging_port": os.getenv("STAGING_PORT", "8080"),
            "staging_path": os.getenv("STAGING_PATH", "/tmp/granger_staging"),
            "modules": [
                "arangodb", "marker", "sparta", "arxiv",
                "llm_call", "youtube_transcripts", "gitget",
                "granger_hub", "rl_commons", "world_model"
            ]
        }
    
    def create_deployment_package(self) -> Path:
        """Create deployment package with all security updates"""
        logger.info(f"Creating deployment package: {self.deployment_id}")
        
        # Create package directory
        self.package_dir.mkdir(exist_ok=True)
        
        # Copy security middleware
        security_file = Path("granger_security_middleware_simple.py")
        shutil.copy2(security_file, self.package_dir)
        
        # Copy all patched interaction files
        interaction_files = list(Path(".").glob("*_interaction.py"))
        (self.package_dir / "interactions").mkdir(exist_ok=True)
        
        for interaction_file in interaction_files:
            # Only copy files with security import
            content = interaction_file.read_text()
            if "GrangerSecurity" in content:
                shutil.copy2(interaction_file, self.package_dir / "interactions")
        
        # Copy security tests
        test_files = [
            "test_security_patches.py",
            "automated_bug_hunter_simple.py",
            "comprehensive_bug_hunt_final.py"
        ]
        
        (self.package_dir / "tests").mkdir(exist_ok=True)
        for test_file in test_files:
            test_path = Path(test_file)
            if test_path.exists():
                shutil.copy2(test_path, self.package_dir / "tests")
        
        # Copy CI/CD configuration
        ci_dir = Path(".github/workflows")
        if ci_dir.exists():
            shutil.copytree(ci_dir, self.package_dir / ".github" / "workflows", dirs_exist_ok=True)
        
        # Create deployment manifest
        manifest = {
            "deployment_id": self.deployment_id,
            "timestamp": datetime.now().isoformat(),
            "security_version": "1.0.0",
            "files": {
                "middleware": ["granger_security_middleware_simple.py"],
                "interactions": [f.name for f in (self.package_dir / "interactions").glob("*.py")],
                "tests": [f.name for f in (self.package_dir / "tests").glob("*.py")]
            },
            "modules_updated": self.staging_config["modules"]
        }
        
        manifest_path = self.package_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))
        
        # Create tarball
        tarball_path = Path(f"{self.deployment_id}.tar.gz")
        with tarfile.open(tarball_path, "w:gz") as tar:
            tar.add(self.package_dir, arcname=self.deployment_id)
        
        logger.info(f"Deployment package created: {tarball_path}")
        return tarball_path
    
    def verify_package(self, package_path: Path) -> Tuple[bool, List[str]]:
        """Verify deployment package integrity"""
        logger.info("Verifying deployment package...")
        
        issues = []
        
        # Check package exists and size
        if not package_path.exists():
            issues.append("Package file not found")
            return False, issues
        
        if package_path.stat().st_size < 1000:  # Too small
            issues.append("Package suspiciously small")
        
        # Extract and verify contents
        with tarfile.open(package_path, "r:gz") as tar:
            members = tar.getnames()
            
            # Check for required files
            required = [
                "granger_security_middleware_simple.py",
                "manifest.json"
            ]
            
            for req in required:
                if not any(req in member for member in members):
                    issues.append(f"Missing required file: {req}")
        
        return len(issues) == 0, issues
    
    def deploy_to_staging(self, package_path: Path) -> Dict:
        """Deploy package to staging environment"""
        logger.info("Deploying to staging environment...")
        
        deployment_result = {
            "status": "unknown",
            "deployment_id": self.deployment_id,
            "timestamp": datetime.now().isoformat(),
            "errors": [],
            "warnings": []
        }
        
        staging_path = Path(self.staging_config["staging_path"])
        
        try:
            # Create staging directory if needed
            staging_path.mkdir(parents=True, exist_ok=True)
            
            # Copy package to staging
            staging_package = staging_path / package_path.name
            shutil.copy2(package_path, staging_package)
            
            # Extract in staging
            deployment_dir = staging_path / self.deployment_id
            deployment_dir.mkdir(exist_ok=True)
            
            with tarfile.open(staging_package, "r:gz") as tar:
                tar.extractall(staging_path)
            
            # Apply security patches to staging modules
            deployed_count = 0
            for module in self.staging_config["modules"]:
                module_staging_path = staging_path / module
                
                if not module_staging_path.exists():
                    deployment_result["warnings"].append(f"Module {module} not found in staging")
                    continue
                
                # Copy security middleware
                security_src = deployment_dir / self.deployment_id / "granger_security_middleware_simple.py"
                security_dst = module_staging_path / "granger_security_middleware_simple.py"
                
                if security_src.exists():
                    shutil.copy2(security_src, security_dst)
                    deployed_count += 1
                    logger.info(f"Deployed security to {module}")
            
            deployment_result["status"] = "success"
            deployment_result["modules_updated"] = deployed_count
            
        except Exception as e:
            deployment_result["status"] = "failed"
            deployment_result["errors"].append(str(e))
            logger.error(f"Deployment failed: {e}")
        
        return deployment_result
    
    def run_staging_tests(self) -> Dict:
        """Run security tests in staging environment"""
        logger.info("Running security tests in staging...")
        
        test_results = {
            "tests_run": 0,
            "passed": 0,
            "failed": 0,
            "errors": []
        }
        
        staging_path = Path(self.staging_config["staging_path"])
        test_script = staging_path / self.deployment_id / self.deployment_id / "tests" / "automated_bug_hunter_simple.py"
        
        if test_script.exists():
            try:
                # Run automated security tests
                result = subprocess.run(
                    [sys.executable, str(test_script)],
                    capture_output=True,
                    text=True,
                    cwd=staging_path / self.deployment_id / self.deployment_id
                )
                
                test_results["tests_run"] = 1
                
                if result.returncode == 0:
                    test_results["passed"] = 1
                    logger.info("Staging security tests PASSED")
                else:
                    test_results["failed"] = 1
                    test_results["errors"].append(result.stderr)
                    logger.error("Staging security tests FAILED")
                    
            except Exception as e:
                test_results["errors"].append(str(e))
                logger.error(f"Error running staging tests: {e}")
        else:
            test_results["errors"].append("Test script not found in staging")
        
        return test_results
    
    def generate_deployment_report(self, package_verified: bool, deployment_result: Dict, test_results: Dict) -> Path:
        """Generate deployment report"""
        report_path = Path(f"deployment_report_{self.deployment_id}.md")
        
        content = f"""# Security Deployment Report

**Deployment ID**: {self.deployment_id}
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Target**: Staging Environment

## Package Verification

**Status**: {"✅ PASSED" if package_verified else "❌ FAILED"}

## Deployment Status

**Status**: {deployment_result['status'].upper()}
**Modules Updated**: {deployment_result.get('modules_updated', 0)}

### Deployment Details
- Timestamp: {deployment_result['timestamp']}
- Errors: {len(deployment_result['errors'])}
- Warnings: {len(deployment_result['warnings'])}

"""
        
        if deployment_result['errors']:
            content += "### Errors\n"
            for error in deployment_result['errors']:
                content += f"- {error}\n"
            content += "\n"
        
        if deployment_result['warnings']:
            content += "### Warnings\n"
            for warning in deployment_result['warnings']:
                content += f"- {warning}\n"
            content += "\n"
        
        content += f"""## Staging Tests

**Tests Run**: {test_results['tests_run']}
**Passed**: {test_results['passed']}
**Failed**: {test_results['failed']}

"""
        
        if test_results['errors']:
            content += "### Test Errors\n"
            for error in test_results['errors']:
                content += f"- {error[:200]}...\n"
            content += "\n"
        
        # Overall assessment
        if package_verified and deployment_result['status'] == 'success' and test_results['passed'] > 0:
            content += """## Assessment: DEPLOYMENT SUCCESSFUL ✅

Security updates have been successfully deployed to staging and all tests pass.

### Next Steps:
1. Monitor staging for 24 hours
2. Run performance benchmarks
3. Schedule production deployment
"""
        else:
            content += """## Assessment: DEPLOYMENT NEEDS ATTENTION ⚠️

Issues were encountered during deployment. Please review and address before proceeding.

### Required Actions:
1. Review deployment errors
2. Fix identified issues
3. Re-run deployment
"""
        
        report_path.write_text(content)
        logger.info(f"Deployment report saved: {report_path}")
        
        return report_path
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.package_dir.exists():
            shutil.rmtree(self.package_dir)
        
        # Remove tarball after successful deployment
        tarball = Path(f"{self.deployment_id}.tar.gz")
        if tarball.exists():
            tarball.unlink()


def main():
    """Deploy security updates to staging"""
    print("\n🚀 SECURITY DEPLOYMENT TO STAGING\n")
    
    deployer = SecurityDeployment()
    
    try:
        # Step 1: Create deployment package
        print("📦 Creating deployment package...")
        package_path = deployer.create_deployment_package()
        
        # Step 2: Verify package
        print("\n🔍 Verifying package integrity...")
        package_ok, issues = deployer.verify_package(package_path)
        
        if not package_ok:
            print("❌ Package verification failed:")
            for issue in issues:
                print(f"  - {issue}")
            return 1
        
        print("✅ Package verified")
        
        # Step 3: Deploy to staging
        print("\n🚢 Deploying to staging...")
        deployment_result = deployer.deploy_to_staging(package_path)
        
        # Step 4: Run staging tests
        print("\n🧪 Running staging tests...")
        test_results = deployer.run_staging_tests()
        
        # Step 5: Generate report
        print("\n📄 Generating deployment report...")
        report = deployer.generate_deployment_report(package_ok, deployment_result, test_results)
        
        # Display summary
        print("\n" + "="*60)
        print("DEPLOYMENT SUMMARY")
        print("="*60)
        print(f"Deployment ID: {deployer.deployment_id}")
        print(f"Status: {deployment_result['status'].upper()}")
        print(f"Modules Updated: {deployment_result.get('modules_updated', 0)}")
        print(f"Tests Passed: {test_results['passed']}/{test_results['tests_run']}")
        print(f"Report: {report}")
        
        # Cleanup
        deployer.cleanup()
        
        # Return appropriate exit code
        if deployment_result['status'] == 'success' and test_results['passed'] > 0:
            print("\n✅ Deployment successful!")
            return 0
        else:
            print("\n⚠️ Deployment needs attention")
            return 1
            
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        print(f"\n❌ Deployment failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())