#!/usr/bin/env python3
"""
Direct Alembic migration runner using Python API
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent / "backend" / "backend"
sys.path.insert(0, str(backend_dir))

def run_alembic_migrations():
    """Run Alembic migrations using Python API"""
    try:
        # Change to the backend directory
        original_cwd = os.getcwd()
        os.chdir(backend_dir)
        
        # Import alembic modules
        from alembic.config import Config
        from alembic import command
        from alembic.script import ScriptDirectory
        from alembic.runtime.environment import EnvironmentContext
        
        print(f"Working directory: {os.getcwd()}")
        print(f"Backend directory: {backend_dir}")
        print(f"Backend directory exists: {backend_dir.exists()}")
        
        # Create Alembic configuration
        alembic_cfg = Config("alembic.ini")
        
        print("\n=== Alembic Configuration ===")
        print(f"Config file: {alembic_cfg.config_file_name}")
        print(f"Script location: {alembic_cfg.get_main_option('script_location')}")
        
        # Check current revision
        print("\n=== Current Revision ===")
        try:
            script_dir = ScriptDirectory.from_config(alembic_cfg)
            
            def get_current_revision():
                """Get current database revision"""
                from alembic.runtime.environment import EnvironmentContext
                from alembic.script import ScriptDirectory
                
                # Import the env module to get database connection
                sys.path.append(os.path.join(os.path.dirname(__file__), 'alembic'))
                import env
                
                # This is a bit tricky - we need to get the current revision from the database
                # For now, let's just show what we can
                return "Unknown - need database connection"
            
            current_rev = get_current_revision()
            print(f"Current revision: {current_rev}")
            
        except Exception as e:
            print(f"Could not determine current revision: {e}")
        
        # Show migration history
        print("\n=== Migration History ===")
        try:
            script_dir = ScriptDirectory.from_config(alembic_cfg)
            revisions = list(script_dir.walk_revisions())
            
            print(f"Total migrations found: {len(revisions)}")
            for rev in revisions:
                print(f"  {rev.revision}: {rev.doc}")
                
        except Exception as e:
            print(f"Could not show migration history: {e}")
        
        # Show head revision
        print("\n=== Head Revision ===")
        try:
            script_dir = ScriptDirectory.from_config(alembic_cfg)
            head_rev = script_dir.get_current_head()
            print(f"Head revision: {head_rev}")
            
        except Exception as e:
            print(f"Could not determine head revision: {e}")
        
        # Apply migrations
        print("\n=== Applying Migrations ===")
        try:
            print("Running: alembic upgrade head")
            command.upgrade(alembic_cfg, "head")
            print("SUCCESS: Migrations applied successfully!")
            
        except Exception as e:
            print(f"ERROR: Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Check final status
        print("\n=== Final Status ===")
        try:
            current_rev = get_current_revision()
            print(f"Final revision: {current_rev}")
            
        except Exception as e:
            print(f"Could not check final status: {e}")
        
        return True
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

def main():
    """Main execution function"""
    print("SAFS Alembic Migration Runner")
    print("=" * 50)
    
    # Check environment
    env_file = backend_dir / ".env"
    print(f".env file exists: {env_file.exists()}")
    
    if env_file.exists():
        print("\nEnvironment configuration:")
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if 'PASSWORD' in line:
                        key = line.split('=')[0]
                        print(f"  {key}=****")
                    else:
                        print(f"  {line}")
    
    # Run migrations
    success = run_alembic_migrations()
    
    if success:
        print("\n" + "=" * 50)
        print("MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 50)
        return 0
    else:
        print("\n" + "=" * 50)
        print("MIGRATION FAILED")
        print("=" * 50)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)