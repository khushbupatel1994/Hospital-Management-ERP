import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ai.ai_queries import AIQueryService
from ai.ai_insights import AIInsights


def test_summary_has_core_metrics():
    q = AIQueryService()
    try:
        data = q.summary()
        for key in ("doctors", "patients", "appointments", "pending_appointments", "revenue"):
            assert key in data
    finally:
        q.close()


def test_insights_builds():
    x = AIInsights()
    try:
        data, insights = x.build()
        assert isinstance(data, dict)
        assert isinstance(insights, list)
        assert insights
    finally:
        x.close()
