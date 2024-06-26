

async function updateAll() {
    const response = await githubAPIrequest("/api/gh_api?url=https://api.github.com/repos/SunkenPotato/sunkenpotato.github.io/commits");
    const data = await response.json();
    
    document.getElementById("build-number").innerHTML = data.commit_hash
    document.getElementById("latest-commit").innerHTML = data.commit_message // Assuming the commit message is in the first element of the array and accessible via commit.message
    document.getElementById("commit-link").href = data.commit_url
}

async function githubAPIrequest(url) {
    const response = await fetch(url);
    return response;
}

// Update the HTML element after the build number is retrieved
updateAll()
