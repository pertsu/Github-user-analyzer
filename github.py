import requests

user = input("Github Username: ")

url = f"https://api.github.com/users/{user}"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    params = {
        "per_page": 10,
        "sort": "updated",
        "direction": "desc"
    }

    repo_response = requests.get(data["repos_url"], params=params)

    if repo_response.status_code == 200:

        repo_data = repo_response.json()

        print("\nGithub User Report\n")

        print("Username:", data["login"])
        print("Name:", data["name"])
        print("Location:", data["location"])
        print("Followers:", data["followers"])
        print("Following:", data["following"])
        print("Public Repositories:", data["public_repos"])

        print("\nREPOSITORY ANALYSIS")

        print("Total Repositories Analyzed:", len(repo_data))

        if repo_data:

            # Most starred repository
            highest_star = 0
            most_starred = ""

            for i in repo_data:
                if i["stargazers_count"] > highest_star:
                    highest_star = i["stargazers_count"]
                    most_starred = i["name"]

            print("\nMost Starred Repo:", most_starred)
            print("Stars:", highest_star)

            # Most recently updated repository
            most_recent = repo_data[0]

            for i in repo_data:
                if i["updated_at"] > most_recent["updated_at"]:
                    most_recent = i

            print("Most Recently Updated Repository:", most_recent["name"])
            print("Updated:", most_recent["updated_at"])

            # Languages
            languages = {}

            for i in repo_data:
                language = i["language"]

                if language is not None:
                    if language in languages:
                        languages[language] += 1
                    else:
                        languages[language] = 1

            print("\nLanguages Found")

            for language, count in languages.items():
                print(f"{language}: {count}")

            # Repositories with more than 100 stars
            print("\nRepositories with More Than 100 Stars")

            found = False

            for i in repo_data:
                if i["stargazers_count"] > 100:
                    print(f'{i["name"]} - {i["stargazers_count"]} stars')
                    found = True

            if not found:
                print("No repositories found.")

        else:
            print("\nNo repositories found.")

    else:
        print("Could not retrieve repositories.")

else:
    print("User not found.")
