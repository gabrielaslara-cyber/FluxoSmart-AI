"""Entrypoint premium; mantém o app original sem alterações."""
import runpy
from pathlib import Path
import fluxosmart.reports as reports
from fluxosmart.premium_report_v3 import build_sales_report
reports.build_sales_report = build_sales_report
runpy.run_path(str(Path(__file__).with_name("app.py")), run_name="__main__")
