# -*- coding: utf-8 -*-
"""
GitHub API Integration
Handles GitHub API interactions for fetching release information
"""

import requests
import re
import fnmatch
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging


@dataclass
class GitHubRelease:
    """GitHub release information"""
    tag_name: str
    name: str
    published_at: str
    prerelease: bool
    assets: List[Dict]
    
    @property
    def version(self) -> str:
        """Extract version from tag name"""
        # Remove common prefixes like 'v', 'release-', etc.
        version = self.tag_name
        for prefix in ['v', 'release-', 'version-']:
            if version.lower().startswith(prefix):
                version = version[len(prefix):]
                break
        return version


class GitHubAPI:
    """GitHub API client for fetching release information"""
    
    def __init__(self, token: Optional[str] = None):
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        
        # Set up authentication if token is provided
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})
        
        # Set user agent
        self.session.headers.update({
            "User-Agent": "UbuntuAutoConfigure-PackageManager/1.0",
            "Accept": "application/vnd.github.v3+json"
        })
        
        self.logger = logging.getLogger(__name__)
    
    def get_latest_release(self, repo: str, include_prerelease: bool = False) -> Optional[GitHubRelease]:
        """
        Get the latest release for a repository
        
        Args:
            repo: Repository in format "owner/repo"
            include_prerelease: Whether to include pre-release versions
            
        Returns:
            GitHubRelease object or None if not found
        """
        try:
            if include_prerelease:
                # Get all releases and find the latest
                releases = self.get_releases(repo, limit=10)
                if releases:
                    return releases[0]
                return None
            else:
                # Get latest stable release
                url = f"{self.base_url}/repos/{repo}/releases/latest"
                response = self.session.get(url)
                response.raise_for_status()
                
                data = response.json()
                return GitHubRelease(
                    tag_name=data["tag_name"],
                    name=data["name"],
                    published_at=data["published_at"],
                    prerelease=data["prerelease"],
                    assets=data["assets"]
                )
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching latest release for {repo}: {e}")
            return None
        except KeyError as e:
            self.logger.error(f"Unexpected response format for {repo}: {e}")
            return None
    
    def get_releases(self, repo: str, limit: int = 30) -> List[GitHubRelease]:
        """
        Get releases for a repository
        
        Args:
            repo: Repository in format "owner/repo"
            limit: Maximum number of releases to fetch
            
        Returns:
            List of GitHubRelease objects
        """
        try:
            url = f"{self.base_url}/repos/{repo}/releases"
            params = {"per_page": min(limit, 100)}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            releases = []
            for data in response.json():
                release = GitHubRelease(
                    tag_name=data["tag_name"],
                    name=data["name"],
                    published_at=data["published_at"],
                    prerelease=data["prerelease"],
                    assets=data["assets"]
                )
                releases.append(release)
            
            return releases
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching releases for {repo}: {e}")
            return []
    
    def find_asset_by_pattern(self, release: GitHubRelease, pattern: str) -> Optional[Dict]:
        """
        Find asset in release that matches the given pattern
        
        Args:
            release: GitHubRelease object
            pattern: Glob pattern to match asset names (e.g., "*amd64.deb")
            
        Returns:
            Asset dictionary or None if not found
        """
        for asset in release.assets:
            if fnmatch.fnmatch(asset["name"], pattern):
                return asset
        return None
    
    def get_download_url(self, repo: str, asset_pattern: str, 
                        include_prerelease: bool = False) -> Optional[Tuple[str, str]]:
        """
        Get download URL for the latest release asset matching pattern
        
        Args:
            repo: Repository in format "owner/repo"
            asset_pattern: Glob pattern to match asset names
            include_prerelease: Whether to include pre-release versions
            
        Returns:
            Tuple of (download_url, version) or None if not found
        """
        release = self.get_latest_release(repo, include_prerelease)
        if not release:
            return None
        
        asset = self.find_asset_by_pattern(release, asset_pattern)
        if not asset:
            self.logger.warning(f"No asset matching pattern '{asset_pattern}' found in {repo}")
            return None
        
        return asset["browser_download_url"], release.version
    
    def get_repository_info(self, repo: str) -> Optional[Dict]:
        """
        Get basic repository information
        
        Args:
            repo: Repository in format "owner/repo"
            
        Returns:
            Repository information dictionary or None
        """
        try:
            url = f"{self.base_url}/repos/{repo}"
            response = self.session.get(url)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching repository info for {repo}: {e}")
            return None
    
    def check_rate_limit(self) -> Dict:
        """
        Check current rate limit status
        
        Returns:
            Rate limit information
        """
        try:
            url = f"{self.base_url}/rate_limit"
            response = self.session.get(url)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error checking rate limit: {e}")
            return {}
    
    def search_repositories(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for repositories
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of repository information
        """
        try:
            url = f"{self.base_url}/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": min(limit, 100)
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get("items", [])
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error searching repositories: {e}")
            return []


class GitHubReleaseCache:
    """Simple cache for GitHub release information"""
    
    def __init__(self, cache_duration: int = 3600):  # 1 hour default
        self.cache: Dict[str, Tuple[GitHubRelease, float]] = {}
        self.cache_duration = cache_duration
    
    def get(self, repo: str) -> Optional[GitHubRelease]:
        """Get cached release information"""
        import time
        
        if repo in self.cache:
            release, timestamp = self.cache[repo]
            if time.time() - timestamp < self.cache_duration:
                return release
            else:
                # Cache expired, remove entry
                del self.cache[repo]
        
        return None
    
    def set(self, repo: str, release: GitHubRelease):
        """Cache release information"""
        import time
        self.cache[repo] = (release, time.time())
    
    def clear(self):
        """Clear all cached data"""
        self.cache.clear()


# Global cache instance
_github_cache = GitHubReleaseCache()


def get_cached_github_api() -> GitHubAPI:
    """Get a GitHub API instance with caching support"""
    api = GitHubAPI()
    
    # Monkey patch to add caching
    original_get_latest_release = api.get_latest_release
    
    def cached_get_latest_release(repo: str, include_prerelease: bool = False) -> Optional[GitHubRelease]:
        cache_key = f"{repo}:{include_prerelease}"
        cached = _github_cache.get(cache_key)
        if cached:
            return cached
        
        release = original_get_latest_release(repo, include_prerelease)
        if release:
            _github_cache.set(cache_key, release)
        
        return release
    
    api.get_latest_release = cached_get_latest_release
    return api
