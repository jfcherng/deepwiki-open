import RepoInfo from "@/types/repoinfo";

export default function getRepoUrl(repoInfo: RepoInfo): string {
  console.log('getRepoUrl', repoInfo);
  if (repoInfo.type === 'local' && repoInfo.localPath) {
    return repoInfo.localPath;
  } else {
    if(repoInfo.repoUrl) {
      return repoInfo.repoUrl;
    } else {
      if(repoInfo.owner && repoInfo.repo) {
        return "http://example/" + repoInfo.owner + "/" + repoInfo.repo;
      }
      return '';
    }
  }
};

export function isRtkGerritUrl(input: string): boolean {
  return extractRtkGerritUrlInfo(input) !== null;
}

export function extractRtkGerritUrlInfo(input: string): {
  baseUrl: string;
  repo: string;
} | null {
  // Some URL formats...
  // - https://release-git.rtkbf.com/gerrit/sdlc/admin/repos/sdlc/realtek_release,general
  // - git clone "https://release-git.rtkbf.com/gerrit/sdlc/realtek_release"
  const rtkGerritRegex = /^(https?:\/\/(?:.+)\.(?:rtkbf|realtek)\.com\/gerrit)\/(?:admin\/repos\/)?([^,?]+)/;

  const match = input.match(rtkGerritRegex);
  if (match) {
    const baseUrl = match[0] || "";
    const repo = match[1] || "";
    return { baseUrl, repo };
  }

  return null;
}
