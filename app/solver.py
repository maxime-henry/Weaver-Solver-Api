import json
import heapq
from collections import namedtuple
from dataclasses import dataclass

@dataclass
class QueueItem:
    node: str
    path: list[str]
    cost: int = 1

    def __lt__(self, other):
        return self.cost < other.cost

class WeaverSolver:
    def __init__(self, weaver_graph_path: str):
        self.weaver_graph = json.loads(open(weaver_graph_path,"r").read())

    def solve(self, start_word: str, end_word: str, avoid_words: list[str] = None) -> list[str]:
        assert start_word in self.weaver_graph, f"Start word {start_word} not in graph"
        assert end_word in self.weaver_graph, f"End word {end_word} not in graph"

        if not avoid_words:
            avoid_words = []

        init_queue_item = QueueItem(node=start_word, path=[], cost=0)
        queue = [init_queue_item]
        seen = set()

        while True:
            qi = heapq.heappop(queue)
            if qi.node not in seen:

                qi.path = qi.path + [qi.node]
                seen.add(qi.node)

                # if we are at the end, return the path
                if qi.node == end_word:
                    return qi.path

                # search edges avoiding nodes and increasing cost
                for search_node in self.weaver_graph[qi.node]:
                    cost = float("inf") if search_node in avoid_words else qi.cost + 1
                    heapq.heappush(
                        queue,
                        QueueItem(
                            node=search_node,
                            path=qi.path,
                            cost=cost,
                        )
                    )


# solver = WeaverSolver("tmp/weaver_graph.json")
# print(solver.solve("bone", "cast"))