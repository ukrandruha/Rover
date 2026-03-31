# core/health_manager.py

class HealthManager:
    def __init__(self, checks):
        self.checks = checks
        self.state = {}

    def update(self):
        for c in self.checks:
            self.state[c.name] = c.check()

    def is_ready(self):
        return all(
            not v["critical"] or v["status"] == "ok"
            for v in self.state.values()
        )