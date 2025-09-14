#!/usr/bin/env python3
"""
Debug script to check file and directory permissions
Useful for diagnosing "readonly database" errors
"""

import os
import stat
import sys


def check_path_permissions(path, description=""):
    """Check permissions for a given path."""
    print(f"\n🔍 Checking: {path} {description}")
    
    if not os.path.exists(path):
        print(f"❌ Path does not exist: {path}")
        return False
    
    try:
        file_stat = os.stat(path)
        file_mode = stat.filemode(file_stat.st_mode)
        
        print(f"  📁 Type: {'Directory' if os.path.isdir(path) else 'File'}")
        print(f"  📋 Permissions: {file_mode} (octal: {oct(file_stat.st_mode)[-3:]})")
        print(f"  👤 Owner UID: {file_stat.st_uid}")
        print(f"  👥 Group GID: {file_stat.st_gid}")
        print(f"  📖 Readable: {os.access(path, os.R_OK)}")
        print(f"  ✏️  Writable: {os.access(path, os.W_OK)}")
        
        if os.path.isdir(path):
            print(f"  🚀 Executable: {os.access(path, os.X_OK)}")
            print(f"  📝 Can create files: {os.access(path, os.W_OK | os.X_OK)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking {path}: {e}")
        return False


def test_file_creation(directory):
    """Test if we can create and write files in a directory."""
    print(f"\n🧪 Testing file creation in: {directory}")
    
    if not os.path.exists(directory):
        print(f"❌ Directory does not exist: {directory}")
        return False
    
    test_file = os.path.join(directory, "test_write_permissions.tmp")
    
    try:
        # Test file creation
        with open(test_file, 'w') as f:
            f.write("test data for permission check")
        print(f"✅ Can create files in {directory}")
        
        # Test file reading
        with open(test_file, 'r') as f:
            content = f.read()
        print(f"✅ Can read files from {directory}")
        
        # Test file modification
        with open(test_file, 'a') as f:
            f.write("\nappended data")
        print(f"✅ Can modify files in {directory}")
        
        # Cleanup
        os.remove(test_file)
        print(f"✅ Can delete files from {directory}")
        
        return True
        
    except Exception as e:
        print(f"❌ File operation failed in {directory}: {e}")
        
        # Try to cleanup if file was created
        try:
            if os.path.exists(test_file):
                os.remove(test_file)
        except:
            pass
        
        return False


def get_user_info():
    """Get current user information."""
    print(f"\n👤 Current Process Information:")
    
    try:
        current_uid = os.getuid()
        current_gid = os.getgid()
        print(f"  UID: {current_uid}")
        print(f"  GID: {current_gid}")
        
        try:
            import pwd
            user_info = pwd.getpwuid(current_uid)
            print(f"  Username: {user_info.pw_name}")
            print(f"  Home: {user_info.pw_dir}")
        except ImportError:
            print(f"  Username: N/A (pwd module not available)")
            
    except AttributeError:
        print(f"  UID/GID: N/A (not available on this system)")
    
    print(f"  Working Directory: {os.getcwd()}")


def main():
    """Main debugging function."""
    print("🔧 Permission Debug Tool for Telegram Keyword Monitor")
    print("=" * 60)
    
    # Get user info
    get_user_info()
    
    # Check current directory
    check_path_permissions(".", "(current directory)")
    
    # Check data directory
    check_path_permissions("data", "(data directory)")
    
    # Check logs directory
    check_path_permissions("logs", "(logs directory)")
    
    # Check config file
    check_path_permissions("config.json", "(config file)")
    
    # Check session files
    session_files = [
        "telegram_monitor.session",
        "data/telegram_monitor.session"
    ]
    
    for session_file in session_files:
        if os.path.exists(session_file):
            check_path_permissions(session_file, "(session file)")
    
    # Test file creation in data directory
    if os.path.exists("data"):
        test_file_creation("data")
    
    # Test file creation in logs directory
    if os.path.exists("logs"):
        test_file_creation("logs")
    
    # Docker-specific checks
    print(f"\n🐳 Docker Environment Checks:")
    
    # Check if we're in Docker
    if os.path.exists("/.dockerenv"):
        print(f"✅ Running inside Docker container")
    else:
        print(f"❌ Not running in Docker container")
    
    # Check for common Docker volume mount points
    docker_paths = ["/app/data", "/app/logs", "/app/config.json"]
    for path in docker_paths:
        if os.path.exists(path):
            check_path_permissions(path, "(Docker mount point)")
    
    print(f"\n" + "=" * 60)
    print(f"🎯 Debugging Complete!")
    print(f"\n💡 Common Solutions for 'readonly database' errors:")
    print(f"  1. Fix directory ownership: sudo chown -R $(id -u):$(id -g) data/ logs/")
    print(f"  2. Fix permissions: chmod -R 755 data/ logs/")
    print(f"  3. Restart Docker container: docker-compose restart")
    print(f"  4. Check Docker user mapping in docker-compose.yml")


if __name__ == "__main__":
    main()