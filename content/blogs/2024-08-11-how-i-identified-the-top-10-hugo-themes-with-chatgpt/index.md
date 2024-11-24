+++
title = 'Harnessing AI for Blog Customization: How I Identified the Top 10 Hugo Themes with ChatGPT'
description = 'Harnessing AI for Blog Customization: How I Identified the Top 10 Hugo Themes with ChatGPT'
date = 2024-08-11T22:50:16-04:00
draft = false
author = 'uright'
tags = ['python','openai','gpt4o', 'gohugo']
image = '/posts/2024-08-11-how-i-identified-the-top-10-hugo-themes-with-chatgpt/blog-post-image.jpeg'
toc = true

+++

## Introduction
Blogging is an essential outlet for sharing knowledge, especially in the tech community. As a part-time AI researcher and tech enthusiast, I often rely on my blog to share insights and discoveries. However, as my content evolved, I realized my blog’s look and feel needed an upgrade. I wanted a modern, professional design that matched the quality of my posts. That’s when I turned to Hugo, a popular static site generator, known for its speed and flexibility. But choosing the right Hugo theme proved to be more challenging than I anticipated. This blog post chronicles how I leveraged ChatGPT to identify the top 10 most popular Hugo themes, making my selection process both efficient and insightful.

## Problem Statement
The Hugo Themes page boasts an extensive collection of themes, each promising a unique look and feel. However, this variety comes with a downside—there's no built-in sorting mechanism to easily identify the most popular or widely used themes. With hundreds of options available, I found myself lost, unable to decide which theme would best suit my blog.

My goal was to find the most popular themes based on objective criteria like GitHub stars and forks, indicators of how widely a theme is adopted and contributed to by the community. I wondered if AI could assist me in this task by automating the process of identifying these popular themes.

## Discovering the Data Source
After some initial struggles, I found the GitHub repository that powers the [Hugo Themes website](https://themes.gohugo.io/). This repository contains all the themes listed on the site, but more importantly, it includes a file named `themes.txt`. This file is a goldmine—it lists every theme, along with links to their respective GitHub or GitLab repositories.

* https://github.com/gohugoio/hugoThemesSiteBuilder
* https://github.com/gohugoio/hugoThemesSiteBuilder/blob/main/themes.txt

## Understanding the Structure
The `themes.txt` file is relatively straightforward. Each line represents a theme and includes the URL to its repository. This structure meant that all the information I needed to assess the popularity of a theme—namely, the number of stars and forks—was just a few steps away. All I needed was a way to systematically extract this information and rank the themes accordingly.

## Leveraging ChatGPT to Automate the Process
Instead of manually going through each theme's repository, I turned to ChatGPT to streamline the process. My initial prompt to ChatGPT was simple: I asked it to generate a Python script that could scrape the number of stars and forks from each GitHub repository listed in the `themes.txt` file. 

ChatGPT delivered exactly what I needed—a Python script that systematically accessed each repository, retrieved the number of stars and forks, and then ranked the themes based on these metrics. The script was designed to handle errors gracefully, such as skipping over any repositories that were no longer available or had changed their URL structure.

https://chatgpt.com/share/7125faa2-8825-4403-874f-098a3f323eab

```text
# User Prompt
Attached is a list of github links, can you write a python script and create a csv that export it's repo name, forks and stars?
```

```python
import requests
import csv

# Function to extract repo details
def get_repo_details(repo_url):
    # Extracting the owner and repo name from the URL
    parts = repo_url.rstrip('/').split('/')
    if len(parts) >= 2:
        owner = parts[-2]
        repo = parts[-1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        # Making a GET request to the GitHub API
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return {
                'repo_name': data['name'],
                'forks': data['forks_count'],
                'stars': data['stargazers_count']
            }
    return None

# Read GitHub URLs from the file
with open('./hugo-themes-url.txt', 'r') as file:
    repo_urls = file.readlines()

# Prepare CSV file
with open('github_repo_details.csv', 'w', newline='') as csvfile:
    fieldnames = ['repo_name', 'forks', 'stars']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for repo_url in repo_urls:
        repo_details = get_repo_details(repo_url.strip())
        if repo_details:
            writer.writerow(repo_details)

print("CSV file created successfully.")
```

## Executing the Script and Analyzing the Results
Once I ran the script, I quickly had a list of the most popular Hugo themes based on the community’s engagement. The top themes were not only visually appealing but also had a strong community presence, ensuring regular updates and support.

## Conclusion
This experiment was a clear demonstration of how AI can simplify complex tasks, turning what could have been a tedious manual process into an automated and insightful analysis. By using ChatGPT, I was able to efficiently identify the top Hugo themes for my blog, ensuring that I chose a theme that was both popular and well-supported.

At the time of writing this post, the top 10 themes based on the number of Stars is as follow:

| Theme Name                                                                           | Forks ⑂ | Stars 🌟 |
| ------------------------------------------------------------------------------------ | ------- | --------- |
| [hugo-PaperMod](https://github.com/adityatelange/hugo-PaperMod)                      | 2540    | 9362      |
| [hugo-book](https://github.com/alex-shpak/hugo-book)                                 | 1164    | 3304      |
| [archie](https://github.com/athul/archie)                                            | 295     | 960       |
| [hugo-theme-diary](https://github.com/AmazingRise/hugo-theme-diary)                  | 186     | 540       |
| [blist-hugo-theme](https://github.com/apvarun/blist-hugo-theme)                      | 162     | 332       |
| [gokarna](https://github.com/526avijitgupta/gokarna)                                 | 134     | 329       |
| [hugo-orbit-theme](https://github.com/aerohub/hugo-orbit-theme)                      | 120     | 252       |
| [digital-garden-hugo-theme](https://github.com/apvarun/digital-garden-hugo-theme)    | 77      | 236       |
| [hugo-theme-bootstrap4-blog](https://github.com/alanorth/hugo-theme-bootstrap4-blog) | 132     | 203       |
| [hugo-theme-pixyll](https://github.com/azmelanar/hugo-theme-pixyll)                  | 58      | 180       |
