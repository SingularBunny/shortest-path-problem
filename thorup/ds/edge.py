class Edge:

    def __init__(self, source: int, target: int, weight=0) -> None:
        super().__init__()
        self.source = source
        self.target = target
        self.weight = weight

    def __eq__(self, o: object) -> bool:
        return (self.source == o.source) and (self.target == o.target) and (self.weight == o.weight)
