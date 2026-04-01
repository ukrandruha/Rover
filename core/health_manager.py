class HealthManager:
    def __init__(self, checks):
        self.checks = checks

    def run_checks(self):
        results = {}

        for check in self.checks:
            result = check.check()
            results[check.name] = result

        return results

    def is_system_ready(self, results):
        for r in results.values():
            if r["critical"] and r["status"] != "ok":
                return False
        return True