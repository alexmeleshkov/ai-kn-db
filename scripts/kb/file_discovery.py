#!/usr/bin/env python3
"""
Minimal file discovery script for KB extraction.
Outputs file_manifest.json with classified files and framework hints.

Usage:
    python file_discovery.py <repo_path> --output <output_path>
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple


# File classification rules
TIER1_PATTERNS = {
    'backend': [
        'services/**/*.py',
        'api/**/*.py',
        'routes/**/*.py',
        'handlers/**/*.py',
        'controllers/**/*.py',
        'models/**/*.py',
        'schemas/**/*.py',
    ],
    'frontend': [
        'components/**/*.tsx',
        'components/**/*.jsx',
        'pages/**/*.tsx',
        'pages/**/*.jsx',
        'views/**/*.tsx',
        'views/**/*.jsx',
        'hooks/**/*.ts',
        'hooks/**/*.js',
        'contexts/**/*.tsx',
        'contexts/**/*.ts',
        'stores/**/*.ts',
        'stores/**/*.js',
    ]
}

TIER2_PATTERNS = [
    'utils/**/*.py',
    'utils/**/*.ts',
    'utils/**/*.js',
    'helpers/**/*.py',
    'helpers/**/*.ts',
    'lib/**/*.py',
    'lib/**/*.ts',
    'middleware/**/*.py',
    'middleware/**/*.ts',
]

TIER3_PATTERNS = [
    'package.json',
    'requirements.txt',
    'pyproject.toml',
    'Cargo.toml',
    'go.mod',
    'docker-compose.yml',
    'Dockerfile',
    '.env.example',
    'tsconfig.json',
    'vite.config.*',
    'webpack.config.*',
]

# Framework detection patterns
FRAMEWORK_INDICATORS = {
    'react': ['react', 'react-dom', '@types/react'],
    'vue': ['vue', '@vue/'],
    'angular': ['@angular/core'],
    'svelte': ['svelte'],
    'fastapi': ['fastapi', 'from fastapi import'],
    'express': ['express', 'require("express")'],
    'django': ['django', 'from django.'],
    'flask': ['flask', 'from flask import'],
    'spring': ['spring-boot', '@SpringBootApplication'],
    'postgresql': ['psycopg2', 'pg', 'postgresql://'],
    'mysql': ['mysql', 'pymysql'],
    'mongodb': ['mongodb', 'pymongo', 'mongoose'],
    'sqlite': ['sqlite3', 'sqlite://'],
}

IGNORE_DIRS = {
    'node_modules', '__pycache__', '.git', '.venv', 'venv',
    'dist', 'build', '.next', '.nuxt', 'target', 'vendor',
    '.pytest_cache', 'coverage', '.coverage', 'htmlcov'
}


def should_ignore(path: Path) -> bool:
    """Check if path should be ignored."""
    parts = path.parts
    return any(ignored in parts for ignored in IGNORE_DIRS)


def classify_file(file_path: Path, repo_root: Path) -> str:
    """Classify file into tier1/tier2/tier3."""
    rel_path = file_path.relative_to(repo_root)
    rel_str = str(rel_path).replace('\\', '/')

    # Check tier3 (exact matches)
    if rel_path.name in [p for p in TIER3_PATTERNS if '/' not in p and '*' not in p]:
        return 'tier3'

    # Check tier1 patterns
    for category, patterns in TIER1_PATTERNS.items():
        for pattern in patterns:
            if matches_pattern(rel_str, pattern):
                return 'tier1'

    # Check tier2 patterns
    for pattern in TIER2_PATTERNS:
        if matches_pattern(rel_str, pattern):
            return 'tier2'

    # Default to tier3 for config/docs
    if file_path.suffix in ['.json', '.yaml', '.yml', '.toml', '.md', '.txt', '.env']:
        return 'tier3'

    return 'tier3'


def matches_pattern(path: str, pattern: str) -> bool:
    """Simple pattern matching for globs."""
    pattern = pattern.replace('\\', '/')
    path = path.replace('\\', '/')

    if '**' in pattern:
        # Pattern like "services/**/*.py"
        parts = pattern.split('**')
        prefix = parts[0].strip('/')  # "services"
        suffix = parts[1].strip('/')  # "*.py"

        # Check if path contains the directory name and ends with the file pattern
        if prefix:
            # Must have directory name somewhere in path
            if f'/{prefix}/' not in f'/{path}/':
                return False

        # Check file extension
        if suffix.startswith('*.'):
            ext = suffix[1:]  # ".py"
            return path.endswith(ext)

        return True

    # Simple suffix match
    if pattern.startswith('*.'):
        return path.endswith(pattern[1:])

    # Exact match
    return path == pattern


def scan_repository(repo_path: Path) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
    """Scan repository and classify all files."""
    files_by_tier = {
        'tier1': [],
        'tier2': [],
        'tier3': []
    }

    stats = {
        'total_files': 0,
        'tier1_count': 0,
        'tier2_count': 0,
        'tier3_count': 0
    }

    for root, dirs, files in os.walk(repo_path):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        root_path = Path(root)
        if should_ignore(root_path):
            continue

        for file in files:
            file_path = root_path / file

            if should_ignore(file_path):
                continue

            # Classify file
            tier = classify_file(file_path, repo_path)
            rel_path = str(file_path.relative_to(repo_path)).replace('\\', '/')

            files_by_tier[tier].append(rel_path)
            stats['total_files'] += 1
            stats[f'{tier}_count'] += 1

    return files_by_tier, stats


def detect_frameworks(repo_path: Path, files_by_tier: Dict[str, List[str]]) -> Dict[str, str]:
    """Detect frameworks from package files and source code."""
    frameworks = {
        'frontend': 'none',
        'backend': 'none',
        'database': 'none'
    }

    # Check package.json
    package_json = repo_path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                content = f.read()
                for fw, indicators in FRAMEWORK_INDICATORS.items():
                    if fw in ['react', 'vue', 'angular', 'svelte']:
                        if any(ind in content for ind in indicators):
                            frameworks['frontend'] = fw
                            break
        except Exception:
            pass

    # Check requirements.txt
    req_txt = repo_path / 'requirements.txt'
    if req_txt.exists():
        try:
            with open(req_txt, 'r', encoding='utf-8') as f:
                content = f.read()
                for fw, indicators in FRAMEWORK_INDICATORS.items():
                    if fw in ['fastapi', 'django', 'flask']:
                        if any(ind in content for ind in indicators):
                            frameworks['backend'] = fw
                            break

                # Check database
                for db, indicators in FRAMEWORK_INDICATORS.items():
                    if db in ['postgresql', 'mysql', 'mongodb', 'sqlite']:
                        if any(ind in content for ind in indicators):
                            frameworks['database'] = db
                            break
        except Exception:
            pass

    return frameworks


def generate_manifest(repo_path: Path, output_path: Path) -> None:
    """Generate file manifest JSON."""
    print(f"Scanning repository: {repo_path}")

    if not repo_path.exists():
        print(f"ERROR: Repository path not found: {repo_path}")
        sys.exit(1)

    # Scan repository
    files_by_tier, stats = scan_repository(repo_path)

    # Detect frameworks
    frameworks = detect_frameworks(repo_path, files_by_tier)

    # Build manifest
    manifest = {
        'project_root': str(repo_path.absolute()).replace('\\', '/'),
        'framework_hints': frameworks,
        'files_by_tier': files_by_tier,
        'statistics': stats
    }

    # Write manifest
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    # Print summary
    print(f"\nFile Discovery Complete:")
    print(f"  Total files: {stats['total_files']}")
    print(f"  Tier 1 (services/components): {stats['tier1_count']}")
    print(f"  Tier 2 (utils/helpers): {stats['tier2_count']}")
    print(f"  Tier 3 (config/docs): {stats['tier3_count']}")
    print(f"\nFramework Detection:")
    print(f"  Frontend: {frameworks['frontend']}")
    print(f"  Backend: {frameworks['backend']}")
    print(f"  Database: {frameworks['database']}")
    print(f"\nManifest written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Discover and classify files in a repository for KB extraction'
    )
    parser.add_argument('repo_path', help='Path to repository to scan')
    parser.add_argument(
        '--output',
        default='.claude/tmp/file_manifest.json',
        help='Output path for manifest JSON (default: .claude/tmp/file_manifest.json)'
    )

    args = parser.parse_args()

    repo_path = Path(args.repo_path).resolve()
    output_path = Path(args.output)

    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path

    generate_manifest(repo_path, output_path)


if __name__ == '__main__':
    main()
