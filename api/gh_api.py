from flask import Flask, request, Response
import requests as rq
import os
import json

app = Flask(__name__)

api_token = os.environ.get('GH_API_TOKEN')


@app.route('/api/gh_api')
def gh_api():
    dest_ = request.args.get("url")
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + api_token,
        "X-GitHub-Api-Version": "2022-11-28"
    }

    api_req = rq.get(dest_.encode(), headers=headers)
    
    if not api_req.status_code == 200:
        return Response(f"An unexpected error occurred: {api_req.reason}", 500)
    
    data = api_req.json()

    commit_url = data[0].get("html_url")
    commit_hash = data[0].get("url")[7:].split('/')[6][0:6]
    commit_message = data[0].get("commit").get("message")

    request_response = {
        "commit_url": commit_url,
        "commit_hash": commit_hash,
        "commit_message": commit_message
    }

    print("request complete")

    return Response(json.dumps(request_response), 200)
