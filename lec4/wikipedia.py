import sys
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def get_id_from_title(self, title):
        for id in self.titles.keys():
            if self.titles[id] == title:
                return id
        return None
    
    def calc_pagerank_diff(self, old_pagerank, new_pagerank):
        diff_sum = 0
        for i in old_pagerank:
            diff = new_pagerank[i] - old_pagerank[i]
            diff_sum += diff ** 2

        return diff_sum
    
    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        queue = deque()
        # タイトルからそれぞれのIDを取得
        startId = wikipedia.get_id_from_title(start)
        goalId = wikipedia.get_id_from_title(goal)
        # 親ノードとスタートからの距離を保存
        visited = {}
        visited[startId] = {"parent": None, "count": 0}
        queue.append(startId)
        while len(queue) > 0:
            node = queue.popleft()
            if node == goalId:
                # ゴールのタイトルを追加
                titles = [self.titles[goalId]]
                # 親ノードを遡り、titlesにタイトルを追加
                before = visited[node]["parent"]
                while before:
                    titles.insert(0, self.titles[before])
                    before = visited[before]["parent"]
                return titles
            for child in self.links[node]:
                if not child in visited:
                    # 自分の親とそこまでの移動回数を保存
                    visited[child] = {"parent": node, "count": visited[node]["count"]+1}
                    queue.append(child)
        return "Not Found"

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        new_pagerank = {}
        old_pagerank = {}
        for id in self.titles.keys():
            new_pagerank[id] = 0.0
            old_pagerank[id] = 1.0
        
        while True:
            handout_pagerank = 0.0
            for page_id in self.titles.keys():
                children = len(self.links[page_id])
                # 子ノードがいる場合、0.85を子ノードに、0.15を全ノードに分配
                if children:
                    for child in self.links[page_id]:
                        new_pagerank[child] += old_pagerank[page_id] * 0.85 / children
                    handout_pagerank += old_pagerank[page_id] * 0.15
                # 子ノードがいない場合は全ノードに分配
                else:
                    handout_pagerank += old_pagerank[page_id]
            
            # 全ノードに分配するページランク
            for id in self.titles.keys():
                new_pagerank[id] += handout_pagerank / len(self.titles.keys())

            # 距離計算で0.01を下回ったら終了
            if wikipedia.calc_pagerank_diff(old_pagerank, new_pagerank) < 0.01:
                break
            for id in self.titles.keys():
                old_pagerank[id] = new_pagerank[id]
                new_pagerank[id] = 0.0
        
        # ページランク順にソート
        sorted_dic = sorted(new_pagerank.items(), key=lambda x:x[1], reverse=True)
        # 存在する限り上位10件を表示
        for i in range(10):
            if i < len(sorted_dic):
                print(self.titles[sorted_dic[i][0]])
            
        

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia = Wikipedia("lec4/wikipedia_dataset/pages_medium.txt", "lec4/wikipedia_dataset/links_medium.txt")
    # Example
    # wikipedia.find_longest_titles()
    # Example
    # wikipedia.find_most_linked_pages()
    # Homework #1
    print(wikipedia.find_shortest_path("渋谷", "小野妹子"))
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    # wikipedia.find_longest_path("渋谷", "池袋")