import os
import csv
from github import Github
from dotenv import load_dotenv

load_dotenv()


class GithubRepoDelete:
    def __init__(self):
        self.forkedRepo = []
        self.githubRepos = []

        self.getRepos()
        self.extractForkedRepo()

    def getRepos(self):
        g = Github(os.getenv("ACCESS_TOKEN"))
        self.githubRepos = g.get_user().get_repos()

    def extractForkedRepo(self):
        protectedRepo = self.getProtectedForkedRepo()
        for repo in self.githubRepos:
            if(repo.private is False and repo.fork is True and repo.name not in protectedRepo):
                self.forkedRepo.append(repo)

    def printForkedRepo(self):
        for repo in self.forkedRepo:
            print(repo.name)
            print("Parent: ", repo.parent)
            # print("Private: ", repo.private)
            # print("Fork: ", repo.fork)
            print("url: ", repo.parent.html_url)
            print("==============")

    def getCountOfFokedRepo(self):
        # print(len(self.githubRepos))
        print(len(self.forkedRepo))

    def exportForkedRepoToCsv(self):
        try:
            with open('forkedRepo.csv', 'w') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(["name", "url", "language", "description"])
                for repo in self.forkedRepo:
                    rowData = [repo.parent.name, repo.parent.html_url, repo.parent.language, repo.parent.description]
                    print(rowData)
                    writer.writerow(rowData)
            csvFile.close()
            print("All Done")
        except Exception as ex:
            print(ex)

    def getProtectedForkedRepo(self):
        return [
            "go-to-do-app",
            "gitignore",
            "30-seconds-of-code",
            "30-seconds-of-css",
            "30-seconds-of-interviews",
            "30-seconds-of-react",
            "33-js-concepts"
        ]

    def deleteForkedRepo(self):
        # counter = 0
        protectedRepo = self.getProtectedForkedRepo()
        for repo in self.forkedRepo:
            if(repo.private is False and repo.fork is True and repo.name not in protectedRepo):
                print("Deleting ",repo.name)
                repo.delete()
                print("Deleted ",repo.name)
            # if counter == 2:
            #     break
            # else:
            #     counter += 1
        


if __name__ == "__main__":
    forkedRepo = GithubRepoDelete()
    # forkedRepo.printForkedRepo()
    # forkedRepo.getCountOfFokedRepo()
    # forkedRepo.exportForkedRepoToCsv()
    forkedRepo.deleteForkedRepo()
