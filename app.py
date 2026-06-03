from flask import Flask, render_template, request

from middleware.detector import analyze_sql
from middleware.parser import extract_id
from middleware.router import get_site
from middleware.permission import allowed
from middleware.executor import execute_query
from middleware.logger import write_log


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():

    user = request.form.get("user", "").strip().lower()
    sql = request.form.get("sql", "").strip()

    # 1. SQL Injection / Forbidden Pattern Detection
    analysis = analyze_sql(sql)

    if not analysis["allowed"]:

        write_log(
            user=user,
            sql=sql,
            result="BLOCKED",
            reason=analysis["reason"]
        )

        return render_template(
            "result.html",
            status="BLOCKED",
            color="danger",
            message="SQL Injection or Forbidden Query Detected",
            reason=analysis["reason"],
            user=user,
            sql=sql,
            site=None,
            employee=None
        )

    # 2. Parse Employee ID
    emp_id = extract_id(sql)

    if emp_id is None:

        write_log(
            user=user,
            sql=sql,
            result="BLOCKED",
            reason="CANNOT_EXTRACT_EMPLOYEE_ID"
        )

        return render_template(
            "result.html",
            status="BLOCKED",
            color="warning",
            message="Cannot extract Employee ID from SQL query",
            reason="Query must contain condition like WHERE ID=100",
            user=user,
            sql=sql,
            site=None,
            employee=None
        )

    # 3. Route to distributed fragment
    site = get_site(emp_id)

    if site is None:

        write_log(
            user=user,
            sql=sql,
            result="BLOCKED",
            reason="NO_FRAGMENT_FOUND"
        )

        return render_template(
            "result.html",
            status="BLOCKED",
            color="warning",
            message="No distributed fragment found for this Employee ID",
            reason="Employee ID must be in range 1-2000",
            user=user,
            sql=sql,
            site=None,
            employee=None
        )

    # 4. Fragment Access Control
    if not allowed(user, site):

        write_log(
            user=user,
            sql=sql,
            result="ACCESS_DENIED",
            reason="UNAUTHORIZED_FRAGMENT_ACCESS",
            site=site
        )

        return render_template(
            "result.html",
            status="ACCESS DENIED",
            color="danger",
            message="Unauthorized Fragment Access",
            reason=f"User '{user}' is not allowed to access Site {site}",
            user=user,
            sql=sql,
            site=site,
            employee=None
        )

    # 5. Execute query
    employee = execute_query(site, emp_id)

    if employee is None:

        write_log(
            user=user,
            sql=sql,
            result="NOT_FOUND",
            reason="EMPLOYEE_NOT_FOUND",
            site=site
        )

        return render_template(
            "result.html",
            status="NOT FOUND",
            color="secondary",
            message="Employee Not Found",
            reason="No record found in selected fragment",
            user=user,
            sql=sql,
            site=site,
            employee=None
        )

    # 6. Success
    write_log(
        user=user,
        sql=sql,
        result="ALLOWED",
        reason="QUERY_EXECUTED_SUCCESSFULLY",
        site=site
    )

    return render_template(
        "result.html",
        status="ALLOWED",
        color="success",
        message="Employee Found",
        reason="Query passed all Query Guard checks",
        user=user,
        sql=sql,
        site=site,
        employee=employee
    )


if __name__ == "__main__":
    app.run(debug=True)