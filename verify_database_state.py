#!/usr/bin/env python3
"""
Database state verification script for SAFS project
This script helps verify the current state of the database and migrations
"""
import os
import sys
from pathlib import Path
import traceback

# Add the backend directory to the path
backend_dir = Path(__file__).parent / "backend" / "backend"
sys.path.insert(0, str(backend_dir))

def check_database_connection():
    """Check if we can connect to the database"""
    try:
        # Change to backend directory for imports
        original_cwd = os.getcwd()
        os.chdir(backend_dir)
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv('.env')
        
        # Import database modules
        from sqlalchemy import create_engine, text
        from urllib.parse import quote_plus
        import socket
        
        # Get database configuration
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        
        print("Database Configuration:")
        print(f"  DB_USER: {db_user}")
        print(f"  DB_PASSWORD: {'*' * len(db_password) if db_password else 'None'}")
        print(f"  DB_HOST: {db_host}")
        print(f"  DB_PORT: {db_port}")
        print(f"  DB_NAME: {db_name}")
        
        # Resolve hostname to IP
        try:
            resolved_ip = socket.gethostbyname(db_host)
            print(f"  Resolved IP: {resolved_ip}")
            db_host = resolved_ip
        except socket.gaierror as e:
            print(f"  Hostname resolution failed: {e}")
        
        # Encode password
        encoded_password = quote_plus(db_password)
        
        # Create database URL
        database_url = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
        print(f"  Database URL: postgresql://{db_user}:****@{db_host}:{db_port}/{db_name}")
        
        # Test connection
        print("\nTesting database connection...")
        engine = create_engine(database_url, echo=False)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"SUCCESS: Connected to PostgreSQL")
            print(f"Version: {version}")
            
            # Check if alembic_version table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'alembic_version'
                )
            """))
            alembic_table_exists = result.scalar()
            print(f"Alembic version table exists: {alembic_table_exists}")
            
            if alembic_table_exists:
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                current_version = result.scalar()
                print(f"Current migration version: {current_version}")
            else:
                print("No migration version found - database not initialized")
            
            # List existing tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            print(f"\nExisting tables ({len(tables)}):")
            for table in tables:
                print(f"  - {table}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Database connection failed: {e}")
        traceback.print_exc()
        return False
        
    finally:
        os.chdir(original_cwd)

def analyze_migration_files():
    """Analyze the migration files"""
    print("\n" + "="*50)
    print("MIGRATION FILES ANALYSIS")
    print("="*50)
    
    versions_dir = backend_dir / "alembic" / "versions"
    
    if not versions_dir.exists():
        print("No versions directory found")
        return
    
    migration_files = sorted(versions_dir.glob("*.py"))
    print(f"Found {len(migration_files)} migration files:")
    
    migrations = []
    for file in migration_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract revision info
            revision = None
            down_revision = None
            doc = None
            
            lines = content.split('\n')
            for line in lines:
                if line.startswith('revision:'):
                    revision = line.split("'")[1] if "'" in line else line.split('"')[1]
                elif line.startswith('down_revision:'):
                    if 'None' not in line:
                        down_revision = line.split("'")[1] if "'" in line else line.split('"')[1]
                elif '"""' in line and not doc:
                    # Extract the docstring (migration description)
                    doc = line.replace('"""', '').strip()
                    if not doc:  # If empty, try next line
                        continue
            
            migrations.append({
                'file': file.name,
                'revision': revision,
                'down_revision': down_revision,
                'description': doc
            })
            
        except Exception as e:
            print(f"Error reading {file.name}: {e}")
    
    # Sort by dependency chain
    print("\nMigration chain:")
    current = None
    processed = set()
    
    # Find the root migration (no down_revision)
    root_migrations = [m for m in migrations if m['down_revision'] is None]
    
    if root_migrations:
        current = root_migrations[0]['revision']
        
        while current and current not in processed:
            # Find migration with this revision
            migration = next((m for m in migrations if m['revision'] == current), None)
            if migration:
                print(f"  {migration['revision']}: {migration['description']}")
                processed.add(current)
                
                # Find next migration
                next_migration = next((m for m in migrations if m['down_revision'] == current), None)
                current = next_migration['revision'] if next_migration else None
            else:
                break
    
    # Show any orphaned migrations
    orphaned = [m for m in migrations if m['revision'] not in processed]
    if orphaned:
        print("\nOrphaned migrations:")
        for m in orphaned:
            print(f"  {m['revision']}: {m['description']}")

def main():
    """Main execution function"""
    print("SAFS Database State Verification")
    print("=" * 50)
    
    print(f"Backend directory: {backend_dir}")
    print(f"Backend directory exists: {backend_dir.exists()}")
    
    # Check .env file
    env_file = backend_dir / ".env"
    print(f".env file exists: {env_file.exists()}")
    
    if not env_file.exists():
        print("ERROR: .env file not found. Database connection will fail.")
        return 1
    
    # Analyze migration files
    analyze_migration_files()
    
    # Test database connection
    print("\n" + "="*50)
    print("DATABASE CONNECTION TEST")
    print("="*50)
    
    connection_success = check_database_connection()
    
    if connection_success:
        print("\n" + "="*50)
        print("RECOMMENDATIONS")
        print("="*50)
        print("1. Database connection is working")
        print("2. You can now run Alembic migrations manually:")
        print("   - Open Command Prompt or PowerShell")
        print("   - Navigate to: backend\\backend")
        print("   - Activate virtual environment: venv\\Scripts\\activate")
        print("   - Run: alembic current")
        print("   - Run: alembic upgrade head")
        print("   - Run: alembic current (to verify)")
    else:
        print("\n" + "="*50)
        print("TROUBLESHOOTING")
        print("="*50)
        print("1. Check if PostgreSQL server is running")
        print("2. Verify database credentials in .env file")
        print("3. Ensure database 'postgres' exists")
        print("4. Check network connectivity to database host")
    
    return 0 if connection_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)